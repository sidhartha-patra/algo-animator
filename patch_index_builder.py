import os

with open("build_index_html.py", "r", encoding="utf-8") as f:
    code = f.read()

# Add buildTrappingRainWaterSpec
trapping_func = r'''
function buildTrappingRainWaterSpec(nums, sourceCode) {
  const n = nums.length;
  const rawStr = nums.join(",");
  const scenes = [];

  scenes.push({
    id: "trap_init",
    type: "title",
    title: "Trapping Rain Water — Two Pointers",
    narration: `Simulating elevation map [${rawStr}]. Computing trapped water units in O(N) time and O(1) space.`,
    dialogue: [
      { character_id: "algo", text: "Two climbers start from opposite ends and move toward each other. The shorter wall determines water height." },
      { character_id: "bug", text: "Why don't we need to know the entire opposing profile?" }
    ],
    states: [
      { kind: "array", name: "height", value: rawStr },
      { kind: "variable", name: "totalWater", value: "0" }
    ],
    code_line: 1
  });

  if (n < 3) {
    scenes.push({
      id: "trap_edge",
      type: "result",
      title: `Edge Case: Length ${n} < 3`,
      narration: `Array length ${n} < 3 cannot form a basin between walls. Returns 0.`,
      dialogue: [
        { character_id: "algo", text: "Zero water trapped. A container requires at least 2 boundaries and an interior dip." },
        { character_id: "bug", text: "Corner case boundary holds." }
      ],
      states: [{ kind: "variable", name: "totalWater", value: "0" }],
      code_line: 7
    });
    return {
      title: "Trapping Rain Water (Edge Case)",
      algorithm: "Two Pointers",
      problem: `Elevation map: [${rawStr}]`,
      intuition: "Requires at least 3 bars to form a depression.",
      invariant: "Length < 3 yields strictly 0 trapped volume.",
      time_complexity: "O(N)",
      space_complexity: "O(1)",
      source_code: sourceCode,
      scenes: scenes
    };
  }

  let left = 0, right = n - 1;
  let leftMax = 0, rightMax = 0;
  let totalWater = 0;
  const trapped = {};
  let step = 1;

  scenes.push({
    id: "trap_setup",
    type: "setup",
    title: "Initialize Two Pointers",
    narration: `left=0 (height ${nums[0]}), right=${n-1} (height ${nums[n-1]}). leftMax=0, rightMax=0.`,
    dialogue: [
      { character_id: "algo", text: "Left climber at index 0, right climber at index " + (n-1) + "." },
      { character_id: "data", text: `Outer walls established.` }
    ],
    states: [
      { kind: "array", name: "height", value: rawStr },
      { kind: "pointer", name: "left", value: String(left), target_index: left },
      { kind: "pointer", name: "right", value: String(right), target_index: right },
      { kind: "variable", name: "leftMax", value: "0" },
      { kind: "variable", name: "rightMax", value: "0" },
      { kind: "variable", name: "totalWater", value: "0" }
    ],
    code_line: 3
  });

  while (left < right) {
    step++;
    if (nums[left] < nums[right]) {
      const h = nums[left];
      if (h >= leftMax) {
        leftMax = h;
        scenes.push({
          id: `trap_${step}`,
          type: "step",
          title: `Update leftMax to ${leftMax} at Index ${left}`,
          narration: `height[${left}] (${h}) >= leftMax. New leftMax is ${leftMax}.`,
          dialogue: [{ character_id: "algo", text: `New left barrier height: ${leftMax}.` }],
          states: [
            { kind: "array", name: "height", value: rawStr, index: left, highlight: true },
            { kind: "pointer", name: "left", value: String(left), target_index: left },
            { kind: "pointer", name: "right", value: String(right), target_index: right },
            { kind: "variable", name: "leftMax", value: String(leftMax), highlight: true },
            { kind: "variable", name: "rightMax", value: String(rightMax) },
            { kind: "variable", name: "totalWater", value: String(totalWater) }
          ],
          code_line: 11
        });
      } else {
        const w = leftMax - h;
        totalWater += w;
        trapped[left] = w;
        scenes.push({
          id: `trap_${step}`,
          type: "decision",
          title: `Trapped +${w} Water at Index ${left}`,
          narration: `height[${left}] (${h}) < leftMax (${leftMax}). Trapped = ${leftMax} - ${h} = ${w}. totalWater = ${totalWater}.`,
          dialogue: [
            { character_id: "algo", text: `Trapped ${w} water! Bounded by leftMax (${leftMax}).` },
            { character_id: "bug", text: "Why can't water spill to the right?" }
          ],
          states: [
            { kind: "array", name: "height", value: rawStr, index: left, highlight: true },
            { kind: "pointer", name: "left", value: String(left), target_index: left },
            { kind: "pointer", name: "right", value: String(right), target_index: right },
            ...Object.entries(trapped).map(([idx, amt]) => ({ kind: "water", name: `water_${idx}`, value: String(amt), index: +idx })),
            { kind: "variable", name: "leftMax", value: String(leftMax) },
            { kind: "variable", name: "rightMax", value: String(rightMax) },
            { kind: "variable", name: "totalWater", value: String(totalWater), highlight: true }
          ],
          code_line: 14,
          why: {
            decision: `height[${left}] (${h}) < height[${right}] (${nums[right]})`,
            limiting_factor: "Left wall is strictly shorter than right wall",
            invariant_proof: `Since height[${right}] >= leftMax (${leftMax}), water ceiling at index ${left} cannot exceed ${leftMax}.`,
            skeptical_question: "Could a middle peak allow more water here?",
            airtight_answer: `No. Water spills over leftMax (${leftMax}) before any higher level could be reached.`
          }
        });
      }
      left++;
    } else {
      const h = nums[right];
      if (h >= rightMax) {
        rightMax = h;
        scenes.push({
          id: `trap_${step}`,
          type: "step",
          title: `Update rightMax to ${rightMax} at Index ${right}`,
          narration: `height[${right}] (${h}) >= rightMax. New rightMax is ${rightMax}.`,
          dialogue: [{ character_id: "algo", text: `New right barrier height: ${rightMax}.` }],
          states: [
            { kind: "array", name: "height", value: rawStr, index: right, highlight: true },
            { kind: "pointer", name: "left", value: String(left), target_index: left },
            { kind: "pointer", name: "right", value: String(right), target_index: right },
            { kind: "variable", name: "leftMax", value: String(leftMax) },
            { kind: "variable", name: "rightMax", value: String(rightMax), highlight: true },
            { kind: "variable", name: "totalWater", value: String(totalWater) }
          ],
          code_line: 19
        });
      } else {
        const w = rightMax - h;
        totalWater += w;
        trapped[right] = w;
        scenes.push({
          id: `trap_${step}`,
          type: "decision",
          title: `Trapped +${w} Water at Index ${right}`,
          narration: `height[${right}] (${h}) < rightMax (${rightMax}). Trapped = ${rightMax} - ${h} = ${w}. totalWater = ${totalWater}.`,
          dialogue: [
            { character_id: "algo", text: `Trapped ${w} water from right boundary!` },
            { character_id: "bug", text: "Symmetric invariant holds." }
          ],
          states: [
            { kind: "array", name: "height", value: rawStr, index: right, highlight: true },
            { kind: "pointer", name: "left", value: String(left), target_index: left },
            { kind: "pointer", name: "right", value: String(right), target_index: right },
            ...Object.entries(trapped).map(([idx, amt]) => ({ kind: "water", name: `water_${idx}`, value: String(amt), index: +idx })),
            { kind: "variable", name: "leftMax", value: String(leftMax) },
            { kind: "variable", name: "rightMax", value: String(rightMax) },
            { kind: "variable", name: "totalWater", value: String(totalWater), highlight: true }
          ],
          code_line: 22,
          why: {
            decision: `height[${right}] (${h}) <= height[${left}] (${nums[left]})`,
            limiting_factor: "Right wall is limiting boundary",
            invariant_proof: `Since leftMax >= rightMax (${rightMax}), water at index ${right} is strictly bounded by rightMax.`,
            skeptical_question: "Can water leak leftward?",
            airtight_answer: `No. The left side has a wall of at least ${rightMax}, so water cannot escape to the left.`
          }
        });
      }
      right--;
    }
  }

  scenes.push({
    id: "trap_final",
    type: "result",
    title: `Result: ${totalWater} Total Water Trapped`,
    narration: `Pointers met at index ${left}. Total water trapped: ${totalWater} units.`,
    dialogue: [
      { character_id: "algo", text: `Simulation complete. Total trapped water is ${totalWater}.` },
      { character_id: "bug", text: "All invariants held across all steps!" }
    ],
    states: [
      { kind: "array", name: "height", value: rawStr },
      ...Object.entries(trapped).map(([idx, amt]) => ({ kind: "water", name: `water_${idx}`, value: String(amt), index: +idx })),
      { kind: "variable", name: "totalWater", value: String(totalWater), highlight: true }
    ],
    code_line: 26
  });

  return {
    title: "Trapping Rain Water",
    algorithm: "Two Pointers",
    problem: `Elevation map: [${rawStr}]`,
    intuition: "Shorter wall completely bounds the water level, allowing one-pass O(N) evaluation.",
    visual_metaphor: "Climbers measuring elevation ridges and filling basins.",
    invariant: "min(leftMax, rightMax) provides the provable upper water ceiling.",
    time_complexity: "O(N)",
    space_complexity: "O(1)",
    source_code: sourceCode || `public int Trap(int[] height)\n{\n    int left = 0, right = height.Length - 1;\n    int leftMax = 0, rightMax = 0;\n    int totalWater = 0;\n    while (left < right)\n    {\n        if (height[left] < height[right])\n        {\n            if (height[left] >= leftMax) leftMax = height[left];\n            else totalWater += leftMax - height[left];\n            left++;\n        }\n        else\n        {\n            if (height[right] >= rightMax) rightMax = height[right];\n            else totalWater += rightMax - height[right];\n            right--;\n        }\n    }\n    return totalWater;\n}`,
    scenes: scenes
  };
}
'''

# Insert trapping_func right before "function buildBinarySearchSpec"
if "function buildTrappingRainWaterSpec" not in code:
    code = code.replace("function buildBinarySearchSpec", trapping_func + "\nfunction buildBinarySearchSpec")

# Update runCustomCode detection in build_index_html.py
old_detection = r'''  let spec = null;
  if (codeLower.includes("binary") || codeLower.includes("mid") || codeLower.includes("left <= right")) {
    spec = buildBinarySearchSpec(nums, target, codeText);
  } else if (codeLower.includes("twosum") || codeLower.includes("two_sum") || codeLower.includes("dictionary") || codeLower.includes("complement")) {
    spec = buildTwoSumSpec(nums, target, codeText);
  } else if (codeLower.includes("maxsubarray") || codeLower.includes("kadane") || codeLower.includes("currentsum")) {'''

new_detection = r'''  let spec = null;
  if (codeLower.includes("binary") || codeLower.includes("mid") || codeLower.includes("left <= right")) {
    spec = buildBinarySearchSpec(nums, target, codeText);
  } else if (codeLower.includes("twosum") || codeLower.includes("two_sum") || codeLower.includes("dictionary") || codeLower.includes("complement")) {
    spec = buildTwoSumSpec(nums, target, codeText);
  } else if (codeLower.includes("maxsubarray") || codeLower.includes("kadane") || codeLower.includes("currentsum")) {
    spec = buildKadaneSpec(nums, codeText);
  } else if (codeLower.includes("trap") || codeLower.includes("rain") || codeLower.includes("water") || codeLower.includes("leftmax")) {
    spec = buildTrappingRainWaterSpec(nums, codeText);
  } else {
    // If user provided target or array is sorted, prefer Binary Search; otherwise Two Sum or Trapping
    if (matchTarget || codeLower.includes("target")) {
      spec = buildBinarySearchSpec(nums, target, codeText);
    } else {
      spec = buildTrappingRainWaterSpec(nums, codeText);
    }
  }'''

if old_detection in code:
    code = code.replace(old_detection, new_detection)

# Update manifest loading and case switching in init()
old_init = r'''async function init() {
  updateTunnelUI();
  // Default to Trapping Rain Water pre-generated case
  try {
    const res = await fetch("cases/case_0.json");
    const spec = await res.json();
    setSpec(spec);
  } catch (e) {
    console.warn("Could not load case_0.json, using Binary Search default", e);
    switchParadigm("binary_search");
  }
}'''

new_init = r'''let globalManifest = [];

async function init() {
  updateTunnelUI();
  try {
    const res = await fetch("cases/manifest.json");
    globalManifest = await res.json();
    renderFilteredRibbon("trapping");
    // Load first case
    if (globalManifest.length > 0) {
      loadCaseFile(globalManifest[0].file);
    }
  } catch (e) {
    console.warn("Could not load cases/manifest.json, using local default", e);
    switchParadigm("trapping");
  }
}

function renderFilteredRibbon(paradigm) {
  const ribbon = $("presets-ribbon");
  ribbon.innerHTML = "";

  // Paradigm Buttons
  const paradigms = [
    { id: "trapping", label: "💧 Trapping Rain Water" },
    { id: "binary_search", label: "🔍 Binary Search" },
    { id: "two_sum", label: "⚡ Two Sum" },
    { id: "kadane", label: "📈 Max Subarray" }
  ];

  paradigms.forEach(p => {
    const btn = document.createElement("button");
    btn.className = "preset-chip" + (p.id === paradigm ? " active" : "");
    btn.textContent = p.label;
    btn.onclick = () => switchParadigm(p.id);
    ribbon.appendChild(btn);
  });

  // Filter test cases
  const filtered = globalManifest.filter(m => !paradigm || m.paradigm === paradigm);
  filtered.forEach((c, idx) => {
    const btn = document.createElement("button");
    btn.className = "preset-chip";
    btn.style.borderColor = "rgba(255,255,255,0.15)";
    btn.innerHTML = `<span style="opacity:0.7;">Case:</span> <strong>${c.name.split(':')[1] || c.name}</strong>`;
    btn.onclick = () => loadCaseFile(c.file);
    ribbon.appendChild(btn);
  });
}

async function loadCaseFile(file) {
  try {
    const res = await fetch("cases/" + file);
    const spec = await res.json();
    setSpec(spec);
  } catch (err) {
    console.error("Failed to load case file", err);
  }
}'''

if old_init in code:
    code = code.replace(old_init, new_init)

# Update switchParadigm
old_switch = r'''function switchParadigm(paradigm) {
  document.querySelectorAll(".preset-chip").forEach(c => c.classList.remove("active"));
  if (event && event.target) event.target.classList.add("active");

  if (paradigm === 'binary_search') {
    const spec = buildBinarySearchSpec([-1, 0, 3, 5, 9, 12], 9);
    setSpec(spec);
  } else if (paradigm === 'two_sum') {
    const spec = buildTwoSumSpec([2, 7, 11, 15], 9);
    setSpec(spec);
  } else if (paradigm === 'kadane') {
    const spec = buildKadaneSpec([-2, 1, -3, 4, -1, 2, 1, -5, 4]);
    setSpec(spec);
  } else {
    // Trapping Rain Water
    fetch("cases/case_0.json").then(r => r.json()).then(spec => setSpec(spec)).catch(() => {
      switchParadigm('binary_search');
    });
  }
}'''

new_switch = r'''function switchParadigm(paradigm) {
  renderFilteredRibbon(paradigm);

  if (globalManifest.length > 0) {
    const match = globalManifest.find(m => m.paradigm === paradigm);
    if (match) {
      loadCaseFile(match.file);
      return;
    }
  }

  // Fallback to client-side generated defaults
  if (paradigm === 'binary_search') {
    setSpec(buildBinarySearchSpec([-1, 0, 3, 5, 9, 12], 9));
  } else if (paradigm === 'two_sum') {
    setSpec(buildTwoSumSpec([2, 7, 11, 15], 9));
  } else if (paradigm === 'kadane') {
    setSpec(buildKadaneSpec([-2, 1, -3, 4, -1, 2, 1, -5, 4]));
  } else {
    setSpec(buildTrappingRainWaterSpec([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]));
  }
}'''

if old_switch in code:
    code = code.replace(old_switch, new_switch)

with open("build_index_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("build_index_html.py updated with complete paradigm switching and auto-detection!")
