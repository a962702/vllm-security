async function loadJson(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`failed to fetch ${path}: ${response.status}`);
  }
  return response.json();
}

async function loadHistory(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`failed to fetch ${path}: ${response.status}`);
  }
  const text = await response.text();
  return text
    .split("\n")
    .filter((line) => line.trim().length > 0)
    .map((line) => JSON.parse(line));
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

// ---------- clipboard ----------

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Clipboard API needs a secure context; fall back to a hidden textarea.
    const area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    const ok = document.execCommand("copy");
    area.remove();
    return ok;
  }
}

// Swaps a button's label to confirm the copy, then restores it.
function flashButton(button, ok) {
  const label = button.dataset.label ?? button.textContent;
  button.dataset.label = label;
  button.textContent = ok ? "Copied" : "Copy failed";
  button.classList.toggle("is-copied", ok);
  clearTimeout(button._flashTimer);
  button._flashTimer = setTimeout(() => {
    button.textContent = label;
    button.classList.remove("is-copied");
  }, 1800);
}

// ---------- latest scan manifest ----------

const VARIANT_LABELS = { gpu: "GPU", cpu: "CPU", rocm: "ROCm" };

function variantLabel(variant) {
  return VARIANT_LABELS[variant] ?? variant;
}

// How far the patch got, as one of the site's status stamps.
function patchState(entry) {
  if (entry.status !== "ok" || !entry.patched_image) {
    return { label: entry.status === "ok" ? "Not published" : "Scan failed", tone: "remaining" };
  }
  if (!entry.python_patch) return { label: "OS only", tone: "new" };
  if (entry.python_upgrade_ok === false) return { label: "Partial", tone: "new" };
  return { label: "Patched", tone: "resolved" };
}

function patchNote(entry) {
  const patch = entry.python_patch;
  if (!patch) {
    return entry.patched_image ? "Python fixes not applied; OS packages upgraded." : "";
  }
  const parts = [`${patch.upgraded} Python fix${patch.upgraded === 1 ? "" : "es"} applied`];
  if (patch.blocked) parts.push(`${patch.blocked} held back by dependencies`);
  if (patch.failed) parts.push(`${patch.failed} failed`);
  if (patch.skipped?.length) parts.push(`skipped: ${patch.skipped.join(", ")}`);
  return parts.join("; ") + ".";
}

function countPair(entry, key) {
  const before = entry.before?.[key];
  const after = entry.after?.[key];
  if (before == null && after == null) return `<dd>-</dd>`;
  return `<dd><span class="count-before">${before ?? "-"}</span> &rarr; <strong>${after ?? "-"}</strong></dd>`;
}

// "vllm-openai-rocm:v0.25.0-20261026" may only break after the colon.
function formatImageRef(ref) {
  const at = ref.lastIndexOf(":");
  if (at < 0) return `<span class="nowrap">${escapeHtml(ref)}</span>`;
  return `<span class="nowrap">${escapeHtml(ref.slice(0, at + 1))}</span><wbr>`
    + `<span class="nowrap">${escapeHtml(ref.slice(at + 1))}</span>`;
}

function renderSlip(entry, registryPrefix) {
  const state = patchState(entry);
  const image = entry.patched_image;
  const shortRef = image && registryPrefix && image.startsWith(registryPrefix)
    ? image.slice(registryPrefix.length)
    : image;
  const pull = image
    ? `<div class="pull">
         <code title="${escapeHtml(image)}">${formatImageRef(shortRef)}</code>
         <button type="button" class="copy-btn" data-copy="docker pull ${escapeHtml(image)}"
                 aria-label="Copy docker pull command for ${escapeHtml(image)}">Copy pull</button>
       </div>`
    : `<p class="pull pull-missing">No patched image for this scan.</p>`;
  const note = patchNote(entry);

  return `
    <section class="slip" data-variant="${escapeHtml(entry.variant)}">
      <header class="slip-head">
        <h4>${escapeHtml(variantLabel(entry.variant))}</h4>
        <span class="stamp stamp-${state.tone}">${state.label}</span>
      </header>
      <dl class="slip-counts">
        <div><dt>Critical</dt>${countPair(entry, "CRITICAL")}</div>
        <div><dt>High</dt>${countPair(entry, "HIGH")}</div>
        <div><dt>All</dt>${countPair(entry, "total")}</div>
      </dl>
      ${pull}
      ${note ? `<p class="slip-note">${escapeHtml(note)}</p>` : ""}
    </section>`;
}

function registryPrefixOf(entries) {
  const image = entries.find((entry) => entry.patched_image)?.patched_image;
  return image ? image.slice(0, image.lastIndexOf("/") + 1) : "";
}

function renderManifest(entries) {
  const prefix = registryPrefixOf(entries);
  document.getElementById("registry-prefix").textContent = prefix || "ghcr.io";

  const byVersion = new Map();
  for (const entry of entries) {
    if (!byVersion.has(entry.version)) byVersion.set(entry.version, []);
    byVersion.get(entry.version).push(entry);
  }
  const versions = [...byVersion.keys()].sort(compareVersions).reverse();

  document.getElementById("manifest").innerHTML = versions
    .map((version) => `
      <article class="manifest-row">
        <h3 class="manifest-version">${escapeHtml(version)}</h3>
        <div class="manifest-slips">
          ${byVersion.get(version).map((entry) => renderSlip(entry, prefix)).join("")}
        </div>
      </article>`)
    .join("");
}

function wireManifest() {
  const manifest = document.getElementById("manifest");
  manifest.addEventListener("click", async (event) => {
    const button = event.target.closest(".copy-btn");
    if (!button) return;
    flashButton(button, await copyText(button.dataset.copy));
  });

  const chips = [...document.querySelectorAll(".filter-chip")];
  for (const chip of chips) {
    chip.addEventListener("click", () => {
      for (const c of chips) c.setAttribute("aria-pressed", String(c === chip));
      manifest.dataset.filter = chip.dataset.variant;
    });
  }
}

function tagKey(row) {
  return `${row.version}|${row.variant}`;
}

function compareVersions(a, b) {
  // "nightly" isn't a semver tag -- always sorts newest, ahead of every release.
  if (a === "nightly" || b === "nightly") {
    if (a === b) return 0;
    return a === "nightly" ? 1 : -1;
  }
  // Release tags are "v0.32.0"; compare the numbers, not the prefix.
  const partsA = a.replace(/^v/, "").split(".").map(Number);
  const partsB = b.replace(/^v/, "").split(".").map(Number);
  for (let i = 0; i < Math.max(partsA.length, partsB.length); i++) {
    const diff = (partsA[i] ?? 0) - (partsB[i] ?? 0);
    if (diff !== 0) return diff;
  }
  return 0;
}

// Severity is a status role (good/warning/serious/critical), not a categorical
// identity -- these are the dataviz skill's validated status-palette steps, kept
// distinct from the site's --sev-* badge colors (which pass as text but collapse
// low vs. unknown when used as unlabeled line colors: CVD delta 2.0, below floor).
// dash is a secondary encoding alongside color: the warning/serious hues sit
// below the CVD normal-vision floor (13.6, just under the 15 target) per the
// dataviz skill's validator, so hue alone can't carry the distinction here.
const SEVERITY_STYLES = {
  CRITICAL: { color: "#d03b3b", dash: [] },
  HIGH: { color: "#ec835a", dash: [6, 3] },
  MEDIUM: { color: "#fab219", dash: [2, 2] },
  LOW: { color: "#0ca30c", dash: [10, 3, 2, 3] },
  UNKNOWN: { color: "#898781", dash: [1, 3] },
};

function trendKeyOptions(history, currentKeys) {
  const versions = new Set();
  const variants = new Set();
  for (const row of history) {
    if (!currentKeys.has(tagKey(row))) continue;
    versions.add(row.version);
    variants.add(row.variant);
  }
  return {
    versions: [...versions].sort(compareVersions).reverse(),
    variants: [...variants].sort(),
  };
}

function populateTrendControls(history, currentKeys) {
  const { versions, variants } = trendKeyOptions(history, currentKeys);
  const versionSelect = document.getElementById("trend-version");
  const variantSelect = document.getElementById("trend-variant");
  versionSelect.innerHTML = versions.map((v) => `<option value="${v}">${v}</option>`).join("");
  variantSelect.innerHTML = variants.map((v) => `<option value="${v}">${v}</option>`).join("");
}

let trendChart = null;

// One version+variant+phase at a time (picked via #trend-controls), plotted as
// severity-count-over-time -- narrower than the old all-tags view but every line
// is now readable, and the dropdown lets you pull up any tag's own history instead
// of hunting for its color in a legend of 20+ overlapping series.
function renderTrendChart(history, version, variant, phase) {
  const rows = history
    .filter((row) => row.version === version && row.variant === variant)
    .sort((a, b) => a.date.localeCompare(b.date));
  const dates = rows.map((row) => row.date);

  const datasets = Object.entries(SEVERITY_STYLES).map(([severity, style]) => ({
    label: severity,
    data: rows.map((row) => row[phase]?.[severity] ?? null),
    borderColor: style.color,
    backgroundColor: style.color,
    borderDash: style.dash,
    borderWidth: 2,
    pointRadius: 0,
    spanGaps: false,
  }));

  if (trendChart) {
    trendChart.destroy();
  }
  trendChart = new Chart(document.getElementById("trend-chart"), {
    type: "line",
    data: { labels: dates, datasets },
    options: {
      responsive: true,
      interaction: { mode: "index", intersect: false },
      scales: { y: { beginAtZero: true } },
      plugins: { legend: { position: "bottom", labels: { boxWidth: 12, font: { size: 10 } } } },
    },
  });
}

function wireTrendControls(history, currentKeys) {
  const versionSelect = document.getElementById("trend-version");
  const variantSelect = document.getElementById("trend-variant");
  const typeSelect = document.getElementById("trend-type");

  const redraw = () => {
    if (!versionSelect.value || !variantSelect.value) return;
    renderTrendChart(history, versionSelect.value, variantSelect.value, typeSelect.value);
  };

  versionSelect.addEventListener("change", redraw);
  variantSelect.addEventListener("change", redraw);
  typeSelect.addEventListener("change", redraw);

  populateTrendControls(history, currentKeys);
  redraw();
}

// Trivy-sourced fields are escaped here, once, since they flow unescaped
// into DataTables' HTML cell rendering (jQuery .html()) after this point.
function extractVulnerabilities(trivyReport) {
  const rows = [];
  for (const result of trivyReport?.Results ?? []) {
    for (const vuln of result.Vulnerabilities ?? []) {
      rows.push({
        severity: escapeHtml(vuln.Severity ?? "UNKNOWN"),
        id: escapeHtml(vuln.VulnerabilityID ?? "-"),
        pkg: escapeHtml(vuln.PkgName ?? "-"),
        installed: escapeHtml(vuln.InstalledVersion ?? "-"),
        fixed: escapeHtml(vuln.FixedVersion ?? "-"),
        title: escapeHtml(vuln.Title ?? "-"),
      });
    }
  }
  return rows;
}

// Merges before/after findings into one row set keyed on (CVE, package),
// tagging each with how it moved across the patch: Resolved (before only),
// New (after only), or Remaining (both). Prefers the after-side snapshot
// of a finding's mutable fields (severity/installed/fixed/title) when both
// sides have it, since that reflects the current image state.
function mergeVulnerabilities(beforeRows, afterRows) {
  const merged = new Map();

  const upsert = (row, phase) => {
    const key = `${row.id}|${row.pkg}`;
    const entry = merged.get(key) ?? { ...row, inBefore: false, inAfter: false };
    entry.inBefore = entry.inBefore || phase === "before";
    entry.inAfter = entry.inAfter || phase === "after";
    if (phase === "after") {
      entry.severity = row.severity;
      entry.installed = row.installed;
      entry.fixed = row.fixed;
      entry.title = row.title;
    }
    merged.set(key, entry);
  };

  for (const row of beforeRows ?? []) upsert(row, "before");
  for (const row of afterRows ?? []) upsert(row, "after");

  return [...merged.values()].map((entry) => ({
    severity: entry.severity,
    id: entry.id,
    pkg: entry.pkg,
    installed: entry.installed,
    fixed: entry.fixed,
    title: entry.title,
    status: entry.inBefore && entry.inAfter ? "Remaining" : entry.inBefore ? "Resolved" : "New",
  }));
}

let reportTable = null;

function renderMergedReportTable(rows) {
  if (reportTable) {
    reportTable.destroy();
    document.querySelector("#report-table tbody").innerHTML = "";
  }

  reportTable = $("#report-table").DataTable({
    data: rows,
    columns: [
      {
        data: "severity",
        title: "Severity",
        render: (value) => `<span class="sev sev-${value.toLowerCase()}">${value}</span>`,
      },
      { data: "id", title: "CVE" },
      { data: "pkg", title: "Package" },
      { data: "installed", title: "Installed" },
      { data: "fixed", title: "Fixed" },
      { data: "title", title: "Title" },
      {
        data: "status",
        title: "Status",
        render: (value) => `<span class="stamp stamp-${value.toLowerCase()}">${value}</span>`,
      },
    ],
    order: [[0, "asc"]],
    pageLength: 25,
    deferRender: true,
    autoWidth: false,
    // Only the table scrolls sideways on narrow screens; search, length and
    // paging stay in the panel.
    dom: '<"report-toolbar"lf><"table-scroll"t><"report-footer"ip>',
  });
}

// ---------- report prompt ----------

const SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"];

function rawFindings(trivyReport) {
  const rows = [];
  for (const result of trivyReport?.Results ?? []) {
    for (const vuln of result.Vulnerabilities ?? []) {
      rows.push({
        severity: vuln.Severity ?? "UNKNOWN",
        id: vuln.VulnerabilityID ?? "-",
        pkg: vuln.PkgName ?? "-",
        installed: vuln.InstalledVersion ?? "-",
        fixed: vuln.FixedVersion || "",
        title: (vuln.Title ?? "").replace(/\s+/g, " ").trim(),
      });
    }
  }
  return rows;
}

function countBy(rows, key) {
  const counts = new Map();
  for (const row of rows) counts.set(row[key], (counts.get(row[key]) ?? 0) + 1);
  return [...counts.entries()].sort((a, b) => b[1] - a[1]);
}

function formatCounts(counts) {
  if (!counts) return "not available";
  return SEVERITY_ORDER.map((sev) => `${sev} ${counts[sev] ?? 0}`).join(", ");
}

const isMajor = (row) => row.severity === "CRITICAL" || row.severity === "HIGH";

function uniqueFindings(rows) {
  const seen = new Set();
  return rows.filter((r) => {
    const key = `${r.id}|${r.pkg}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function severityCounts(rows) {
  const counts = Object.fromEntries(SEVERITY_ORDER.map((sev) => [sev, 0]));
  for (const row of rows) counts[SEVERITY_ORDER.includes(row.severity) ? row.severity : "UNKNOWN"] += 1;
  return counts;
}

function severitySplit(rows) {
  const c = rows.filter((r) => r.severity === "CRITICAL").length;
  return `${rows.length} (CRITICAL ${c}, HIGH ${rows.length - c})`;
}

// Asks the assistant for a .pptx deck assessing the image's CRITICAL/HIGH
// findings, modelled on the team's existing assessment deck: one conclusion
// per slide, a verdict per finding (affected / conditional / not affected)
// and W/X/Y columns (impact, reasoning, remediation). Every remaining
// Critical/High finding is listed; Medium and below only as a total.
function buildReportPrompt({ date, version, variant, image, historyRow, summaryEntry, before, after, language, organization }) {
  const beforeAll = uniqueFindings(rawFindings(before));
  const beforeMajor = beforeAll.filter(isMajor);
  const afterAll = uniqueFindings(rawFindings(after));
  const afterMajor = afterAll
    .filter(isMajor)
    .sort((a, b) => SEVERITY_ORDER.indexOf(a.severity) - SEVERITY_ORDER.indexOf(b.severity)
      || a.pkg.localeCompare(b.pkg) || a.id.localeCompare(b.id));
  const afterKeys = new Set(afterMajor.map((r) => `${r.id}|${r.pkg}`));
  const resolvedMajor = beforeMajor.filter((r) => !afterKeys.has(`${r.id}|${r.pkg}`));
  const minorCount = afterAll.length - afterMajor.length;

  const patch = summaryEntry?.python_patch;
  const patchLines = patch
    ? [
        `- Python packages upgraded: ${patch.upgraded}; held back because the fix conflicts with other installed packages: ${patch.blocked ?? 0}; failed: ${patch.failed}.`,
        patch.skipped?.length ? `- Deliberately not upgraded: ${patch.skipped.join(", ")}.` : null,
        `- pip removed from the image: ${patch.pip_removed === true ? "yes" : "no (kept)"}.`,
        patch.pip_removed === true
          ? "- pip ships its own vendored copies of urllib3, msgpack, setuptools, certifi and others. Findings in those copies disappear because pip was removed, so a package can show up as resolved below even when its own installed version was not upgraded (or was deliberately left alone)."
          : null,
      ].filter(Boolean)
    : [];
  const eyebrow = `${organization ? `${organization} ・ ` : ""}vLLM Security Assessment — Critical/High only`;
  const month = date.slice(0, 7).replace("-", ".");

  return [
    "You are a container security analyst who also builds presentation decks. Using only the Trivy scan data below, produce a PowerPoint deck (.pptx) that assesses the CRITICAL and HIGH findings of this vLLM container image for our security team.",
    "",
    "Deliverable: one .pptx file. If you can run code, generate the file (python-pptx or pptxgenjs) and give it to me. If you cannot create files, reply with one complete python-pptx script that writes the deck.",
    "",
    "## Image",
    `- Image: ${image} (variant: ${variant})`,
    `- Patched image: ${historyRow?.patched_image ?? "not published for this scan"}`,
    `- Scan date: ${date} (scanner: Trivy)`,
    "- Workload: vLLM, an OpenAI-compatible LLM inference server, run as a container. The host provides the kernel (and the GPU driver for gpu/rocm variants).",
    "",
    "## How the patched image was produced",
    "- OS packages: apt-get upgrade.",
    "- Python packages with a fixed version were upgraded to the smallest fixed version. vLLM, torch, numpy, transformers and packages built from source were kept at their shipped versions; any upgrade that would downgrade, remove or break another package's requirements was rolled back.",
    ...patchLines,
    "",
    "## Finding counts, all severities, one per (CVE, package) (original image -> patched image)",
    `- Original: ${formatCounts(severityCounts(beforeAll))}`,
    `- Patched: ${formatCounts(severityCounts(afterAll))}`,
    `- CRITICAL/HIGH: ${severitySplit(beforeMajor)} -> ${severitySplit(afterMajor)}. MEDIUM and below remaining: ${minorCount} (out of scope; mention the total only).`,
    "",
    `## CRITICAL/HIGH findings resolved by the patch (${resolvedMajor.length}), by package`,
    ...(resolvedMajor.length
      ? countBy(resolvedMajor, "pkg").map(([pkg, n]) => {
          const ids = resolvedMajor.filter((r) => r.pkg === pkg).map((r) => r.id);
          return `- ${pkg}: ${n} (${ids.slice(0, 8).join(", ")}${ids.length > 8 ? ", ..." : ""})`;
        })
      : ["- none"]),
    "",
    `## Remaining CRITICAL and HIGH findings in the patched image (${afterMajor.length})`,
    "severity | id | package | installed | fixed in | title",
    ...afterMajor.map((r) => [r.severity, r.id, r.pkg, r.installed, r.fixed || "no fix", r.title].join(" | ")),
    "",
    "## Verdicts",
    "Give every remaining CRITICAL/HIGH finding exactly one verdict:",
    "- Affected (構成影響): reachable in a typical vLLM serving deployment.",
    "- Conditional (視設定・條件性): depends on a startup flag, an enabled feature or an exposed endpoint. Name the condition and how to check it.",
    "- Not affected (未見可利用路徑): the vulnerable code is absent or unreachable. Say why.",
    "Reason from what the package contains (linux-libc-dev only ships kernel headers; the kernel comes from the host), whether vLLM's serving path uses the component, and what input an attacker would need. Give one verdict per package when the reasoning is the same; break out single CVEs when it differs. Totals per verdict must add up to the remaining count on every slide.",
    "",
    "## Deck structure",
    "One message per slide; each slide title states the conclusion, not the topic. Group slides into three parts and show the part in each slide's eyebrow as \"Part N ・ topic\", keeping \"Part N\" in English as in our template.",
    `1. Cover. Eyebrow, verbatim and not translated: "${eyebrow}". Title: "vLLM ${variant.toUpperCase()} ${version} 弱點掃描" with the second line "Critical + High 影響評估" (translate both if the deck language is not Traditional Chinese). One line on the goal (how many CRITICAL/HIGH remain in the patched image and what to do about them). One line on the data source (Trivy, scan date, severity ∈ {CRITICAL, HIGH}). Date "${month}" at bottom right.`,
    "2. Part 1, status overview. Title with the headline (how many remain and how many actually matter). A 100% horizontal bar of the three verdicts with a legend under it (count and %). Below, a category × verdict table: rows = categories that have findings (for example Linux kernel headers, other OS packages, Python packages, vLLM itself) plus a total row; columns = category, count, Affected, Conditional, Not affected, page of its detail slide. Zeros in light grey, Not affected in green, Affected in red. One line under the table naming the Affected and Conditional findings.",
    "3. Part 1, what the patch fixed. Big before -> after CRITICAL/HIGH numbers and the resolved findings by package; one line on what was held back or skipped and why.",
    "4. Part 2, one slide per category, biggest first. Left column: the count as a big number with its share of all remaining CRITICAL/HIGH under it (\"條 ・ 佔 C/H x%\" in Traditional Chinese), the severity split, and the verdict. Right side, three columns: Impact (W), Why it is or is not exploitable here (X), Remediation (Y), each as numbered points (01, 02, 03). For a category with several packages, use a table instead: package (count) | verdict | explanation | fixed version | CVE IDs.",
    "5. Part 3, disposition. Three columns side by side, separated by thin vertical rules (no card fill, border or shadow; each rule ends at least 0.15 in above any text below it), each with a big number and a heading: Ignore (record in VEX / .trivyignore with the reason; the real fix is on the host), Fix / upgrade (what to upgrade and to which version), Prioritise (Affected and Conditional findings: what to confirm first, then the fix). A closing line: what is expected to remain after disposition, and that a rescan will change with new base images and advisories.",
    "",
    "## Visual style (match it exactly)",
    "- 16:9, 13.333 × 7.5 in, white background. No gradients, pictures, icons, shadows or decorative bars/stripes.",
    "- Fonts: on every text run set the Latin font to IBM Plex Sans and the East Asian font to Microsoft JhengHei (in OOXML: <a:latin typeface=\"IBM Plex Sans\"/> and <a:ea typeface=\"Microsoft JhengHei\"/> in each a:rPr; python-pptx has no API for ea, so add the element). Also set the theme's major and minor fonts the same way, including the Hant script entry. PowerPoint draws CJK characters with the East Asian font only; a CJK font set as the Latin font is ignored for them.",
    "- Colours: titles 161616; body 393939; eyebrow, captions and footer 6F6F6F; rules E0E0E0; zeros and disabled C6C6C6; light panel F4F4F4; key numbers and the primary accent 0F62FE; Affected / priority DA1E28; Not affected 229338; Conditional 8D8D8D.",
    "- Content slides: eyebrow at (0.6 in, 0.42 in), 11 pt, \"Part N ・ topic\". Title at (0.6 in, 0.74 in), 28 pt bold, one line. Optional lead sentence under it, 11.5 pt. Content from 1.7 in down, left margin 0.6 in. Footer at 7.08 in: \"Source: …\" 8.5 pt at the left, the two-digit page number (\"03\") at the right.",
    "- Cover: eyebrow 12 pt at the top left, title block 42 pt bold from 2.2 in, source line 12 pt under it.",
    "- Big numbers 42-50 pt in 0F62FE (DA1E28 when they count Affected findings or the Ignore card on the disposition slide, as in our template) with a 10 pt label. Make each big-number text box at least 1.3 × its font size tall (48 pt -> 0.87 in) and start its label at least 0.1 in below the box, so the digits never touch the label. No line or rule may cross or touch text: keep 0.1 in clear around every text box. Tables as plain grids: 10.5 pt muted header row, 11 pt body, thin E0E0E0 rules, colour only on verdict numbers. Body text 10-11 pt, dense but aligned on consistent column edges; left-align text, right-align numbers.",
    "",
    "## Rules",
    `- Write all slide text in ${language}. Keep CVE IDs, package names, versions, file names and commands as they are.`,
    "- Use only the data given. Do not invent CVE details, CVSS scores, fixed versions, dates or exploits. If you look anything up, cite it in that slide's footer; otherwise write what has to be verified.",
    "- Every number on a slide must match the counts above.",
  ].join("\n");
}

let promptContext = null;

function renderPrompt() {
  if (!promptContext) return;
  const language = document.getElementById("prompt-lang").value;
  const organization = document.getElementById("prompt-org").value.trim();
  const text = buildReportPrompt({ ...promptContext, language, organization });
  document.getElementById("prompt-text").value = text;
  const kb = (new Blob([text]).size / 1024).toFixed(0);
  document.getElementById("prompt-size").textContent = `${text.split("\n").length} lines, ${kb} KB`;
}

function showPrompt(context) {
  promptContext = context;
  document.getElementById("prompt-target").textContent = `${context.image} (${context.date})`;
  renderPrompt();
  document.getElementById("prompt-block").hidden = false;
}

function wirePrompt() {
  const lang = document.getElementById("prompt-lang");
  const browserLang = (navigator.language || "").toLowerCase();
  if (browserLang.startsWith("zh-cn") || browserLang.startsWith("zh-sg")) lang.value = "Simplified Chinese (zh-CN)";
  else if (browserLang.startsWith("zh")) lang.value = "Traditional Chinese (zh-TW)";
  else if (browserLang.startsWith("ja")) lang.value = "Japanese";
  else lang.value = "English";
  lang.addEventListener("change", renderPrompt);

  // The organization name only goes into the deck's cover; remember it per browser.
  const org = document.getElementById("prompt-org");
  try {
    org.value = localStorage.getItem("prompt-org") ?? "";
  } catch {
    // storage unavailable (private mode); the field just starts empty
  }
  org.addEventListener("input", () => {
    try {
      localStorage.setItem("prompt-org", org.value.trim());
    } catch {
      // ignore
    }
    renderPrompt();
  });

  document.getElementById("prompt-copy").addEventListener("click", async (event) => {
    flashButton(event.currentTarget, await copyText(document.getElementById("prompt-text").value));
  });
}

async function fetchReportFile(date, version, variant, suffix) {
  const path = `results/reports/${date}/${version}-${variant}-${suffix}.json`;
  const response = await fetch(path);
  if (!response.ok) {
    return null;
  }
  return response.json();
}

async function populateReportDateSelect() {
  const dateSelect = document.getElementById("report-date");
  let dates = [];
  try {
    dates = await loadJson("results/reports/index.json");
  } catch (error) {
    document.getElementById("report-status").textContent = "No report history available yet.";
    return [];
  }
  dateSelect.innerHTML = dates.map((d) => `<option value="${d}">${d}</option>`).join("");
  return dates;
}

function populateReportComboSelect(history, date) {
  const comboSelect = document.getElementById("report-combo");
  const combos = history
    .filter((row) => row.date === date && row.status === "ok")
    .map((row) => ({ version: row.version, variant: row.variant }));
  comboSelect.innerHTML = combos
    .map((c) => `<option value="${c.version}|${c.variant}">${c.version} / ${c.variant}</option>`)
    .join("");
}

async function viewSelectedReport() {
  const date = document.getElementById("report-date").value;
  const comboValue = document.getElementById("report-combo").value;
  const statusEl = document.getElementById("report-status");
  const outputEl = document.getElementById("report-output");

  if (!date || !comboValue) {
    statusEl.textContent = "Pick a date and a version/variant first.";
    return;
  }
  const [version, variant] = comboValue.split("|");

  statusEl.textContent = "Loading...";
  let before;
  let after;
  try {
    [before, after] = await Promise.all([
      fetchReportFile(date, version, variant, "before"),
      fetchReportFile(date, version, variant, "after"),
    ]);
  } catch (error) {
    statusEl.textContent = `Failed to load report: ${error.message}`;
    return;
  }

  const notes = [];
  if (!before) notes.push("before-patch report unavailable for this scan");
  if (!after) notes.push("after-patch report unavailable for this scan");

  const merged = mergeVulnerabilities(
    before ? extractVulnerabilities(before) : [],
    after ? extractVulnerabilities(after) : []
  );
  renderMergedReportTable(merged);

  if (after) {
    const historyRow = reportHistory.find(
      (row) => row.date === date && row.version === version && row.variant === variant);
    const summaryEntry = latestSummary.find(
      (entry) => entry.version === version && entry.variant === variant
        && entry.patched_image && entry.patched_image === historyRow?.patched_image);
    const image = summaryEntry?.image ?? `${variant} ${version}`;
    showPrompt({ date, version, variant, image, historyRow, summaryEntry, before, after });
  } else {
    document.getElementById("prompt-block").hidden = true;
  }

  statusEl.textContent = notes.length > 0 ? `Note: ${notes.join("; ")}.` : "";
  outputEl.hidden = false;
}

let reportHistory = [];
let latestSummary = [];

function wireReportControls(history) {
  reportHistory = history;
  document.getElementById("report-date").addEventListener("change", (event) => {
    populateReportComboSelect(history, event.target.value);
  });
  document.getElementById("report-view-btn").addEventListener("click", () => {
    viewSelectedReport();
  });
}

function wireTabs() {
  const tabs = [...document.querySelectorAll(".tab")];
  const panels = {
    overview: document.getElementById("panel-overview"),
    "full-report": document.getElementById("panel-full-report"),
  };

  for (const tab of tabs) {
    tab.addEventListener("click", () => {
      for (const t of tabs) {
        t.setAttribute("aria-selected", String(t === tab));
      }
      for (const [key, panel] of Object.entries(panels)) {
        panel.hidden = key !== tab.dataset.tab;
      }
      if (tab.dataset.tab === "full-report" && reportTable) {
        reportTable.columns.adjust().draw(false);
      }
    });
  }
}

async function main() {
  const summary = await loadJson("results/latest/summary.json");
  latestSummary = summary;
  renderManifest(summary);
  wireManifest();

  document.getElementById("updated-at").textContent =
    `Latest run: ${summary[0]?.scanned_at ?? "unknown"}`;

  const history = await loadHistory("results/history.jsonl");
  const currentKeys = new Set(summary.map(tagKey));
  wireTrendControls(history, currentKeys);

  const dates = await populateReportDateSelect();
  if (dates.length > 0) {
    populateReportComboSelect(history, dates[0]);
  }
  wireReportControls(history);
  wirePrompt();
  wireTabs();
}

main().catch((error) => {
  document.getElementById("updated-at").textContent = `Failed to load results: ${error.message}`;
});
