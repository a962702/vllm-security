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

// Critical/High findings are listed one per line; Medium and below are
// summarized per package so the prompt stays within a chat-sized context.
function buildReportPrompt({ date, version, variant, image, historyRow, summaryEntry, before, after, language }) {
  const afterRows = rawFindings(after);
  const beforeKeys = new Set(rawFindings(before).map((r) => `${r.id}|${r.pkg}`));
  const afterKeys = new Set(afterRows.map((r) => `${r.id}|${r.pkg}`));
  const resolved = [...beforeKeys].filter((key) => !afterKeys.has(key)).length;

  const seen = new Set();
  const unique = afterRows.filter((r) => {
    const key = `${r.id}|${r.pkg}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  const major = unique
    .filter((r) => r.severity === "CRITICAL" || r.severity === "HIGH")
    .sort((a, b) => SEVERITY_ORDER.indexOf(a.severity) - SEVERITY_ORDER.indexOf(b.severity)
      || a.pkg.localeCompare(b.pkg) || a.id.localeCompare(b.id));
  const minor = unique.filter((r) => r.severity !== "CRITICAL" && r.severity !== "HIGH");
  const withFix = unique.filter((r) => r.fixed).length;

  const patch = summaryEntry?.python_patch;
  const patchLines = patch
    ? [
        `- Python packages upgraded: ${patch.upgraded}; held back because the fix conflicts with other installed packages: ${patch.blocked ?? 0}; failed: ${patch.failed}.`,
        patch.skipped?.length ? `- Deliberately not upgraded: ${patch.skipped.join(", ")}.` : null,
        `- pip removed from the image: ${patch.pip_removed === true ? "yes" : "no (kept)"}.`,
      ].filter(Boolean)
    : [];

  return [
    "You are a container security analyst. Using only the Trivy scan data below, write a vulnerability impact assessment of this container image for our security team.",
    "",
    "## Image",
    `- Original image: ${image}`,
    `- Patched image: ${historyRow?.patched_image ?? "not published for this scan"}`,
    `- Scan date: ${date} (scanner: Trivy)`,
    "- Workload: vLLM, an LLM inference server, run as a container on a host that provides the kernel (and GPU driver for gpu/rocm variants).",
    "",
    "## How the patched image was produced",
    "- OS packages: apt-get upgrade.",
    "- Python packages with a fixed version were upgraded to the smallest fixed version. vLLM, torch, numpy, transformers and packages built from source were kept at their shipped versions; any upgrade that would downgrade, remove or break another package's requirements was rolled back.",
    ...patchLines,
    "",
    "## Finding counts (before patch -> after patch)",
    `- Before: ${formatCounts(historyRow?.before)}`,
    `- After: ${formatCounts(historyRow?.after)}`,
    `- Findings resolved by the patch: ${resolved}. Remaining findings: ${unique.length}, of which ${withFix} list a fixed version.`,
    "",
    `## Remaining CRITICAL and HIGH findings (${major.length})`,
    "severity | id | package | installed | fixed in | title",
    ...major.map((r) => [r.severity, r.id, r.pkg, r.installed, r.fixed || "no fix", r.title].join(" | ")),
    "",
    `## Remaining MEDIUM / LOW / UNKNOWN findings by package (${minor.length})`,
    ...countBy(minor, "pkg").map(([pkg, n]) => `- ${pkg}: ${n}`),
    "",
    "## What to write",
    `Write the report in ${language}. Sections:`,
    "1. Summary: overall risk of running this image, in a few sentences, with the key numbers.",
    "2. What the patch fixed.",
    "3. Remaining findings grouped by package. For each group decide whether the vulnerable code is present and reachable in this container, with a verdict of Not affected, Affected or Needs investigation, and the reasoning. Consider what the package contains (for example, linux-libc-dev only ships kernel headers; the kernel itself comes from the host), whether the component is used by an inference server, and what an attacker would need.",
    "4. Findings that list a fixed version but remain: why they plausibly could not be applied, and what it would take.",
    "5. Recommended actions and compensating controls, including what must be handled on the host rather than in the image.",
    "6. Appendix: a table of every remaining CRITICAL and HIGH finding with its verdict.",
    "",
    "Rules: do not invent CVE details, versions or exploits that are not in the data; when the data is not enough to decide, say what must be verified and how. Mark assumptions as assumptions.",
  ].join("\n");
}

let promptContext = null;

function renderPrompt() {
  if (!promptContext) return;
  const language = document.getElementById("prompt-lang").value;
  const text = buildReportPrompt({ ...promptContext, language });
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
