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

function formatBeforeAfter(before, after, severity) {
  if (!before && !after) return "-";
  const beforeVal = before ? before[severity] : "-";
  const afterVal = after ? after[severity] : "-";
  return `${beforeVal} → ${afterVal}`;
}

function renderLatestTable(entries) {
  const tbody = document.querySelector("#latest-table tbody");
  tbody.innerHTML = "";
  for (const entry of entries) {
    const row = document.createElement("tr");
    const cells = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]
      .map((severity) => `<td>${formatBeforeAfter(entry.before, entry.after, severity)}</td>`)
      .join("");
    row.innerHTML = `
      <td>${entry.version}</td>
      <td>${entry.variant}</td>
      ${cells}
    `;
    tbody.appendChild(row);
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
  const partsA = a.split(".").map(Number);
  const partsB = b.split(".").map(Number);
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

  statusEl.textContent = notes.length > 0 ? `Note: ${notes.join("; ")}.` : "";
  outputEl.hidden = false;
}

function wireReportControls(history) {
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
  renderLatestTable(summary);

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
  wireTabs();
}

main().catch((error) => {
  document.getElementById("updated-at").textContent = `Failed to load results: ${error.message}`;
});
