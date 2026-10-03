# Algo Animator 🎬

> **Interactive Comic-Style Algorithm Visualizer, Corner-Case Invariant Simulator & Copilot Agent**

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-success?style=for-the-badge&logo=github)](https://sidhartha-patra.github.io/algo-animator/)
[![Dev Tunnel Ready](https://img.shields.io/badge/Dev%20Tunnel-Ready-blue?style=for-the-badge&logo=visualstudiocode)](https://aka.ms/devtunnels)
[![Copilot Skill](https://img.shields.io/badge/Copilot-Skill%20%26%20Agent-purple?style=for-the-badge&logo=githubcopilot)](SKILL.md)

**Algo Animator** transforms any algorithm, interview problem, pseudocode, or production source code (C#, Python, Java, C++, TypeScript) into an interactive, self-contained SVG/HTML comic animation with Staff-level invariant reasoning.

---

## 🌟 Live Interactive Demo

Open the live GitHub Pages app directly in your browser:
👉 **[https://sidhartha-patra.github.io/algo-animator/](https://sidhartha-patra.github.io/algo-animator/)**

- Explore 9 comprehensive corner cases for the two-pointer invariant.
- Interactive timeline scrubber, speed controls (`0.5x`–`2x`), and scene selector.
- Synchronized line-by-line source code inspector.
- **"Why is this safe?" Invariant Inspector** (press `W` or click `💡 Why Mode`).

---

## 🏛️ Architecture

```
                 ┌──────────────────────────────────────┐
                 │ Algorithm / C# / Code / Corner Cases │
                 └──────────────────┬───────────────────┘
                                    ↓
                 ┌──────────────────────────────────────┐
                 │       4-Stage Logical Pipeline       │
                 │                                      │
                 │ 1. Teacher Agent   (Intuition/Meta)  │
                 │ 2. Trace Agent     (Simulate state)  │
                 │ 3. Storyboard Agent(Comic dialogue)  │
                 │ 4. "Why?" Mode     (Invariant proof) │
                 └──────────────────┬───────────────────┘
                                    ↓
                             animation.json
                                    ↓
                 ┌──────────────────────────────────────┐
                 │  Deterministic Local SVG/HTML Engine │
                 └──────────────────┬───────────────────┘
                                    ↓
                             animation.html
                                    ↓
            ┌───────────────────────┴───────────────────────┐
            ↓                                               ↓
 🌐 GitHub Pages Live App                       🔌 Microsoft Dev Tunnel
 (Static / Zero-Dependency)                     (Copilot CLI Backend API)
```

---

## 🧪 Comprehensive Corner-Case Simulator

The engine in `simulator.py` automatically generates and executes a battery of edge and corner cases to verify that algorithmic invariants hold under extreme boundaries:

| Test Case | Array Shape | Trapped Water | Boundary / Invariant Verified |
|---|---|:---:|---|
| **Standard Basin** | `[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]` | **6** | Multi-peak and multi-valley elevation |
| **Empty Elevation Map** | `[]` | **0** | Length 0 boundary check |
| **Single Element** | `[4]` | **0** | Single wall cannot form a container |
| **Two Elements** | `[3, 1]` | **0** | Needs at least 3 elements to trap water |
| **All Equal Heights** | `[2, 2, 2, 2]` | **0** | Flat terrain water runoff |
| **Strictly Decreasing** | `[5, 4, 3, 2, 1]` | **0** | Water spills rightward over lower walls |
| **Strictly Increasing** | `[1, 2, 3, 4, 5]` | **0** | Water spills leftward over lower walls |
| **Deep Single Basin** | `[4, 0, 0, 4]` | **8** | Wide basin between equal height pillars |
| **Asymmetric Peak** | `[10, 1, 2, 1]` | **1** | Bounded strictly by the lower side |

---

## 💡 The Killer Feature: "Why is this safe?" Mode

For every algorithmic decision or pointer movement, the animation provides an explicit mathematical and intuitive proof:
1. **Decision Condition**: The check performed (e.g., `height[left] < height[right]`).
2. **Limiting Bottleneck**: Identifies which side forms the bounding wall.
3. **Invariant Guarantee**: Why future/unseen elements cannot break the current calculation.
4. **Bug's Challenge**: The sharpest counter-question an interviewer or skeptic might ask.
5. **Algo's Airtight Proof**: The mathematical refutation proving the step is sound.

---

## 🔌 Exposing as a Dev Tunnel Backend Service

You can run the backend service on your machine and expose it publicly using Microsoft Dev Tunnels:

```bash
# 1. Start the server and dev tunnel:
python tunnel.py
```

This starts the REST API on port `8000` and creates an authenticated Microsoft Dev Tunnel:
```text
Tunnel ID : algo-animator.inc1
Port      : 8000
Connect   : https://algo-animator-8000.inc1.devtunnels.ms
```

### Endpoints Available via Dev Tunnel:
- `GET /health`: Health check and model readiness
- `GET /api/algorithms`: Supported algorithms and corner-case suites
- `POST /api/animate`: Accepts code/algorithm input, returns `AnimationSpec` JSON and rendered HTML
- `POST /api/simulate-corner-cases`: Executes full battery of corner cases on provided code

---

## 💻 CLI Usage

```bash
# Generate canonical sample:
python algoanimate.py --sample trapping-rain-water --out output

# Animate source code:
python algoanimate.py --file examples/Solution.cs --input "[0,1,0,2,1,0,1,3,2,1,2,1]"

# Render existing specification:
python algoanimate.py --render examples/trapping_rain_water.json --out output
```

---

## 🤖 GitHub Copilot Skill & Agent Integration

Installed locally in:
- **Skill**: `~/.agents/skills/algo-animator` (and `~/.copilot/skills/algo-animator`)
- **Agent**: `~/.copilot/agents/algo-animator.agent.md`

Invoke directly in GitHub Copilot CLI:
```text
/algo-animator Implement trapping rain water using two pointers and verify with corner cases
```
or mention `@algo-animator`.
