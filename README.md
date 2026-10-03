# Algo Animator: Comic-Style Algorithm Visualizer & Skill

Turn algorithms, C# interview solutions, and pseudocode into interactive, self-contained SVG/HTML comic animations with Staff-level invariant reasoning.

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

## Features

- **Comic Character System**:
  - **Algo (🧑)**: The guide explaining invariants and state transitions.
  - **Bug (🤔)**: The skeptical interviewer challenging assumptions ("Why can we advance this pointer?").
  - **Data (🧱)**: The reactive data structure representing array elements, walls, or pools.
- **The Killer Feature: "Why is this safe?" Invariant Inspector**:
  - Step-by-step breakdown of every algorithmic decision.
  - Identifies the limiting bottleneck and guarantees why future elements cannot break the current decision.
  - Skeptical Q&A between Bug and Algo.
  - Toggle via keyboard shortcut `W` or the on-screen button.
- **Dual Visual Stage**:
  - Interactive array cells with index tracking and pointer arrows (`left ▲`, `right ▲`).
  - Bar elevation charts and trapped water overlays.
  - Side-by-side synchronized source code inspector with active line indicator (`➔`).
- **Zero Runtime Dependencies**:
  - Output is a single, self-contained HTML file that opens in any browser (`file://` or web).

## Quick Start

```bash
# 1. Generate the canonical Trapping Rain Water sample immediately:
python algoanimate.py --sample trapping-rain-water --out output

# 2. Animate a source code file (e.g. C#):
python algoanimate.py --file examples/Solution.cs --input "[0,1,0,2,1,0,1,3,2,1,2,1]"

# 3. Open the output:
start output/animation.html
```
