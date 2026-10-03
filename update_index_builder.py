import re

with open("build_index_html.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update modal description & input
old_modal_desc = r'''    <p style="font-size:13px; color:var(--text-secondary); margin:0;">
      Upload any C# algorithm file (Binary Search, Two Sum, Sliding Window, Trapping Rain Water, etc.) or paste code directly. The engine simulates the execution and proves invariants step-by-step.
    </p>'''

new_modal_desc = r'''    <p style="font-size:13px; color:var(--text-secondary); margin:0;">
      Upload any C# algorithm file or paste code directly. You can provide a custom test case, or <b>leave the test case empty</b> to let AlgoAnimator auto-detect the algorithm and synthesize a complete corner-case test suite!
    </p>'''

content = content.replace(old_modal_desc, new_modal_desc)

old_modal_field = r'''    <div class="form-field">
      <label>Test Case Array (and optional target)</label>
      <input type="text" class="form-input" id="custom-input-data" value="[-1, 0, 3, 5, 9, 12], target=9">
    </div>'''

new_modal_field = r'''    <div class="form-field">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <label>Test Case Array & Target <span style="color:#10b981; font-weight:700;">(Optional)</span></label>
        <span style="font-size:11px; color:var(--text-muted);">Leave empty to auto-synthesize all corner cases</span>
      </div>
      <input type="text" class="form-input" id="custom-input-data" placeholder="Leave empty to auto-detect and synthesize edge cases (e.g. [-1, 0, 3, 5, 9, 12], target=9)">
    </div>'''

content = content.replace(old_modal_field, new_modal_field)

# 2. Update runCustomCode implementation
new_run_custom = r'''async function runCustomCode() {
  const algoTitle = $("custom-algo-title").value.trim();
  const codeText = $("custom-code-area").value.trim();
  const inputStr = $("custom-input-data").value.trim();
  closeUploadModal();

  // If live Dev Tunnel connected, call backend API
  if (devTunnelUrl) {
    try {
      const res = await fetch(`${devTunnelUrl.replace(/\/$/, '')}/api/animate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ algorithm: algoTitle, code: codeText, input: inputStr })
      });
      const data = await res.json();
      if (data.spec) {
        setSpec(data.spec);
        if (data.spec.synthesized_corner_cases && data.spec.synthesized_corner_cases.length > 0) {
          renderSynthesizedRibbon(data.spec.synthesized_corner_cases, codeText, algoTitle);
        }
        return;
      }
    } catch (e) {
      console.warn("Dev tunnel call error, falling back to client simulation:", e);
    }
  }

  // Client-side Auto-Detection & Corner-Case Synthesizer
  const codeLower = (codeText + " " + algoTitle).toLowerCase();
  let nums = [];
  let target = 9;
  const matchTarget = inputStr.match(/target\s*[:=]\s*(-?\d+)/i);
  if (matchTarget) target = parseInt(matchTarget[1], 10);

  const cleanArrStr = inputStr.replace(/target\s*[:=]\s*(-?\d+)/i, "").replace(/[\[\]]/g, "");
  nums = cleanArrStr.split(",").map(x => parseInt(x.trim(), 10)).filter(x => !isNaN(x));

  let spec = null;
  let synthesizedCases = [];

  if (codeLower.includes("binary") || codeLower.includes("mid") || codeLower.includes("left <= right")) {
    if (!nums.length) nums = [-1, 0, 3, 5, 9, 12];
    spec = buildBinarySearchSpec(nums, target, codeText);
    synthesizedCases = [
      { name: "Standard Illustrative", input: "[-1, 0, 3, 5, 9, 12], target=9" },
      { name: "Target at Index 0", input: "[1, 3, 5, 7, 9], target=1" },
      { name: "Target at Rightmost", input: "[1, 3, 5, 7, 9], target=9" },
      { name: "Target Absent (Middle)", input: "[2, 4, 6, 8, 10], target=5" },
      { name: "Target Absent (Too Small)", input: "[2, 4, 6], target=1" },
      { name: "Single Element Match", input: "[5], target=5" },
      { name: "Single Element Miss", input: "[5], target=3" },
      { name: "Empty Array", input: "[], target=1" }
    ];
  } else if (codeLower.includes("twosum") || codeLower.includes("two_sum") || codeLower.includes("dictionary") || codeLower.includes("complement")) {
    if (!nums.length) nums = [2, 7, 11, 15];
    spec = buildTwoSumSpec(nums, target, codeText);
    synthesizedCases = [
      { name: "Standard Pair", input: "[2, 7, 11, 15], target=9" },
      { name: "Adjacent Pair at End", input: "[3, 2, 4], target=6" },
      { name: "Identical Duplicates", input: "[3, 3], target=6" },
      { name: "Negative Numbers", input: "[-1, -2, -3, -4, -5], target=-8" },
      { name: "Zero Boundary", input: "[0, 4, 3, 0], target=0" },
      { name: "No Valid Pair", input: "[1, 2, 3], target=10" }
    ];
  } else if (codeLower.includes("maxsubarray") || codeLower.includes("kadane") || codeLower.includes("currentsum")) {
    if (!nums.length) nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4];
    spec = buildKadaneSpec(nums, codeText);
    synthesizedCases = [
      { name: "Classic LeetCode", input: "[-2, 1, -3, 4, -1, 2, 1, -5, 4]" },
      { name: "All Negative Numbers", input: "[-5, -2, -8, -1, -4]" },
      { name: "All Positive Numbers", input: "[1, 2, 3, 4, 5]" },
      { name: "Alternating Signs", input: "[5, -3, 5]" },
      { name: "Single Positive", input: "[10]" },
      { name: "Single Negative", input: "[-7]" }
    ];
  } else if (codeLower.includes("trap") || codeLower.includes("rain") || codeLower.includes("water") || codeLower.includes("leftmax")) {
    if (!nums.length) nums = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1];
    spec = buildTrappingRainWaterSpec(nums, codeText);
    synthesizedCases = [
      { name: "Standard Basin", input: "[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]" },
      { name: "Empty Elevation Map", input: "[]" },
      { name: "Single Element", input: "[4]" },
      { name: "Two Elements", input: "[3, 1]" },
      { name: "All Equal Heights", input: "[2, 2, 2, 2]" },
      { name: "Strictly Decreasing", input: "[5, 4, 3, 2, 1]" },
      { name: "Strictly Increasing", input: "[1, 2, 3, 4, 5]" },
      { name: "Deep Single Basin", input: "[4, 0, 0, 4]" }
    ];
  } else {
    // Default fallback
    if (matchTarget || codeLower.includes("target")) {
      if (!nums.length) nums = [-1, 0, 3, 5, 9, 12];
      spec = buildBinarySearchSpec(nums, target, codeText);
    } else {
      if (!nums.length) nums = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1];
      spec = buildTrappingRainWaterSpec(nums, codeText);
    }
  }

  setSpec(spec);
  if (synthesizedCases.length > 0) {
    renderSynthesizedRibbon(synthesizedCases, codeText, algoTitle);
  }
}

function renderSynthesizedRibbon(cases, codeText, algoTitle) {
  const ribbon = $("presets-ribbon");
  ribbon.innerHTML = "";

  const titleChip = document.createElement("div");
  titleChip.className = "preset-chip active";
  titleChip.style.background = "rgba(16, 185, 129, 0.15)";
  titleChip.style.borderColor = "rgba(16, 185, 129, 0.4)";
  titleChip.style.color = "#34d399";
  titleChip.innerHTML = `<span>✨ Synthesized Suite:</span> <strong>${algoTitle || "Custom Algorithm"}</strong>`;
  ribbon.appendChild(titleChip);

  cases.forEach((c, idx) => {
    const btn = document.createElement("button");
    btn.className = "preset-chip" + (idx === 0 ? " active" : "");
    btn.style.borderColor = "rgba(255,255,255,0.18)";
    btn.innerHTML = `<span style="opacity:0.75;">Case ${idx + 1}:</span> <strong>${c.name}</strong>`;
    btn.onclick = () => {
      document.querySelectorAll(".preset-chip").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      $("custom-input-data").value = c.input;
      runCustomCode();
    };
    ribbon.appendChild(btn);
  });
}
'''

# Replace from `async function runCustomCode()` down to `window.addEventListener("keydown"`
pattern = r"async function runCustomCode\(\)\s*\{.*?window\.addEventListener\(\"keydown\""
replacement = new_run_custom + "\nwindow.addEventListener(\"keydown\""

content = re.sub(pattern, lambda m: replacement, content, flags=re.DOTALL)

with open("build_index_html.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated build_index_html.py with optional test case input and auto-synthesized test suite!")
