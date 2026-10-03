---
name: algo-animator
description: >
  Turn any algorithm, pseudocode, or source-code solution (C#, Python, Java, C++, TypeScript) into
  a compact, educational, comic-style interactive SVG/HTML animation. Features a 4-agent logical pipeline
  (Teacher, Trace, Storyboard, and Render Engine) with comic characters Algo (🧑 teacher), Bug (🤔 skeptical
  interviewer), and Data (🧱 structure), synchronized code line highlighting, and a dedicated "Why is this safe?"
  decision invariant inspector for Staff-level interview and system design mastery.
argument-hint: 'algo-animator <algorithm, leetcode problem, or code snippet>'
allowed-tools: powershell, view, create, edit, ask_user
user-invocable: true
metadata:
  emoji: "🎬"
  tags:
    - algorithm
    - animation
    - visualization
    - interview-prep
    - education
    - leetcode
---

# Algo Animator Skill

Convert algorithms, interview problems, pseudocode, or production source code into rich, comic-style, interactive SVG/HTML animations.

## Architecture

```
                 ┌──────────────────────┐
                 │ Algorithm / C# / Code│
                 └──────────┬───────────┘
                            ↓
         ┌──────────────────────────────────────┐
         │     4-Stage Logical Pipeline         │
         │                                      │
         │ 1. Teacher Agent   (Intuition/Meta)  │
         │ 2. Trace Agent     (Simulate state)  │
         │ 3. Storyboard Agent(Comic dialogue)  │
         │ 4. "Why?" Mode     (Invariant proof) │
         └──────────────────┬───────────────────┘
                            ↓
                     animation.json (DSL)
                            ↓
                 ┌──────────────────────┐
                 │ Deterministic Local  │
                 │ SVG/HTML Renderer    │
                 └──────────┬───────────┘
                            ↓
                     animation.html (Self-contained)
```

The model generates a compact, validated semantic storyboard (`animation.json`), and the local deterministic renderer produces a zero-dependency, self-contained `animation.html`.

---

## The Four Logical Agents

### 1. Teacher Agent
- **Brute Force vs Optimal Insight**: Identifies why the naive approach does unnecessary work and reveals the core insight.
- **Visual Metaphor Selection**: Maps the data structure to a clear mental picture (see Visual Metaphors table).
- **Fundamental Invariant**: Establishes the mathematical rule that guarantees correctness at every step.

### 2. Trace Agent
- **Step-by-step Execution**: Simulates the algorithm accurately on an illustrative example (e.g. 6–12 elements).
- **State Tracking**: Maintains arrays, pointers (left, right, mid), and variables (`leftMax`, `rightMax`, `ans`).
- **Code Line Mapping**: Coordinates each state transition to the corresponding 1-based source code line (`code_line`).

### 3. Storyboard Agent
- **Comic Characters**:
  - **Algo (🧑)**: Calm teacher/guide explaining invariants and pointing to state.
  - **Bug (🤔)**: Skeptical technical interviewer asking "Why can we do that?", "What if the right wall is taller?", testing edge cases.
  - **Data (🧱)**: Reactive array/data structure (e.g., "I'm a dip of height 0 between walls!").
- **Dialogue Pacing**: Concise, engaging comic speech bubbles with character mood indicators.

### 4. The Killer Feature: "Why is this safe?" Mode
For every algorithmic decision or pointer advance, the storyboard provides a rigorous invariant breakdown:
- **Decision Condition**: The check performed (e.g., `height[left] < height[right]`).
- **Limiting Factor**: Identifies which side is the bottleneck.
- **Invariant Guarantee**: Why future/unseen elements cannot break the decision.
- **Bug's Challenge**: The sharpest counter-question an interviewer might ask.
- **Algo's Airtight Proof**: The mathematical refutation proving the step is safe.

---

## Visual Metaphor Table

| Algorithm Class | Visual Metaphor |
|---|---|
| **Two Pointers** | Two climbers walking inward from opposite ridges measuring bounding walls |
| **Sliding Window** | A movable spotlight/frame expanding and contracting across the landscape |
| **Binary Search** | A detective systematically eliminating half the suspect rooms at each step |
| **BFS** | A messenger spreading outward to all one-hop neighbors before advancing |
| **DFS** | An explorer traversing deep caverns while spooling out a lifeline rope |
| **Monotonic Stack** | Skyline guards maintaining an unobstructed line-of-sight |
| **Heap / Priority Queue** | A VIP elevator line where priority constantly determines the next passenger |
| **Union-Find** | Isolated islands tying colored bridges together to form nations |
| **Dynamic Programming** | A row of glowing stepping stones where each stone rests on solved sub-stones |
| **Trapping Rain Water** | Wall elevation bars with trapped translucent water pools forming in the basins |

---

## CLI Usage

### 1. Quick Start / Instant Demo
Run the canonical C# Trapping Rain Water sample:
```bash
python algoanimate.py --sample trapping-rain-water --out output
```

### 2. Animate Source Code File
Animate a C#, Python, or Java solution:
```bash
python algoanimate.py --file examples/Solution.cs --input "[0,1,0,2,1,0,1,3,2,1,2,1]" --audience interview
```

### 3. Animate From Description
```bash
python algoanimate.py "Implement trapping rain water using the two pointer approach" \
  --input "[0,1,0,2,1,0,1,3,2,1,2,1]"
```

### 4. Render Pre-Generated JSON
```bash
python algoanimate.py --render examples/trapping_rain_water.json --out output
```

---

## Output Artifacts

- **`animation.html`**: Completely self-contained interactive comic animation. Open directly in any browser (no local web server or npm required).
- **`animation.json`**: Structured JSON spec conforming to `schema.py`.
- **`explanation.md`**: Markdown brief covering intuition, invariant, complexity, and character roster.

---

## Interactive Animation Controls

- **Play / Pause**: Spacebar or `▶ Play` / `⏸ Pause` button.
- **Step Forward / Backward**: Left / Right Arrow keys or `◀` / `▶` buttons.
- **First / Last Scene**: Home / End keys or `⏮` / `⏭` buttons.
- **Timeline Scrubber**: Drag slider to jump to any frame.
- **Scene Dropdown**: Jump directly to key phases (`intuition`, `decision`, `result`).
- **Speed Selector**: `0.5x`, `1x`, `1.5x`, `2x`.
- **"Why is this safe?" Drawer**: Press `W` or click `💡 Why Mode` to inspect the mathematical invariant proof for the current frame.
- **Code Inspector**: Shows side-by-side source code with glowing active-line highlight (`➔`).
