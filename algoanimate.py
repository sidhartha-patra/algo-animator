#!/usr/bin/env python3
"""
AlgoAnimator: Algorithm / Code -> Comic Educational Animation Engine.

Four Logical Agents in One Architecture:
1. Teacher Agent: Intuition, Visual Metaphor, Mathematical Invariant
2. Trace Agent: State Transitions, Array/Pointers/Variables, Correctness
3. Storyboard Agent: Comic Characters (Algo 🧑, Bug 🤔, Data 🧱), Dialogue, Code Line Sync
4. Render Engine: Deterministic Local SVG/HTML Animation with "Why is this safe?" Mode.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

# Ensure UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from schema import AnimationSpec, Scene, Character, StateItem, WhyExplanation, DialogueLine

SYSTEM_PROMPT = r"""
You are AlgoAnimator, an expert algorithms teacher, computer science animator, and visual-storyboard designer.

Your mission is to turn an algorithm, pseudocode, or source-code solution into an educational, comic-style interactive storyboard.

You will act as four integrated logical agents in a single generation pass:

1. TEACHER AGENT:
- Contrast the naive/brute force approach with the core insight.
- Formulate the fundamental invariant that guarantees correctness.
- Select an intuitive visual metaphor from the canonical metaphor table (e.g., Two Pointers -> Two climbers walking towards each other measuring wall heights; Sliding Window -> Moving spotlight; Binary Search -> Detective eliminating rooms; BFS -> City messenger; Monotonic Stack -> Skyline guards).

2. TRACE AGENT:
- Faithfully execute the algorithm step-by-step on the provided example input.
- Accurately maintain array states, pointer movements (e.g. left, right, mid), and variable values.
- Map each transition to the corresponding 1-based source code line (`code_line`).

3. STORYBOARD AGENT:
- Character Roles:
  * Algo (🧑): The calm, authoritative guide who explains invariants and points out key states.
  * Bug (🤔): The skeptical student / technical interviewer who asks "Why can we do that?", "What if the other side changes?", and tests edge cases.
  * Data (🧱): The reactive element (e.g. array cells, trapped water pools, visited nodes).
- Dialogue must be natural, educational, concise, and focused on why decisions are sound.

4. THE "WHY IS THIS SAFE?" MODE (MANDATORY FOR DECISIONS):
- For every decision or pointer movement, supply a `WhyExplanation`:
  * `decision`: The condition evaluated (e.g. "height[left] < height[right]").
  * `limiting_factor`: What acts as the bottleneck.
  * `invariant_proof`: Why unseen elements cannot violate the decision.
  * `skeptical_question`: Bug's sharpest challenge.
  * `airtight_answer`: Algo's mathematical refutation of Bug's concern.

OUTPUT REQUIREMENTS:
- Output must strictly match the AnimationSpec JSON schema.
- Do not output Markdown or wrap in code blocks.
- Output semantic storyboard scenes only (8 to 25 scenes).
"""

SAMPLE_CSHARP_CODE = """public int Trap(int[] height)
{
    int left = 0, right = height.Length - 1;
    int leftMax = 0, rightMax = 0;
    int totalWater = 0;

    while (left < right)
    {
        if (height[left] < height[right])
        {
            if (height[left] >= leftMax)
                leftMax = height[left];
            else
                totalWater += leftMax - height[left];
            left++;
        }
        else
        {
            if (height[right] >= rightMax)
                rightMax = height[right];
            else
                totalWater += rightMax - height[right];
            right--;
        }
    }
    return totalWater;
}"""

def get_trapping_rain_water_sample() -> AnimationSpec:
    """Pre-built reference animation specification for Trapping Rain Water (Two Pointers)."""
    raw_array = "0,1,0,2,1,0,1,3,2,1,2,1"
    
    characters = [
        Character(id="algo", name="Algo", role="Guide & Teacher", mood="explaining"),
        Character(id="bug", name="Bug", role="Skeptical Interviewer", mood="skeptical"),
        Character(id="data", name="Data", role="Array Wall", mood="neutral"),
    ]

    scenes = [
        # Scene 1: Title & Metaphor
        Scene(
            id="s1",
            type="title",
            title="Trapping Rain Water — Two Pointer Invariant",
            narration="Given an elevation map where each bar has width 1, compute how much water it can trap after raining. We contrast the O(N) space prefix approach with an O(1) space two-pointer invariant.",
            dialogue=[
                DialogueLine(character_id="algo", text="Welcome! Today we master the two-pointer invariant for Trapping Rain Water.", mood="confident"),
                DialogueLine(character_id="bug", text="I know the O(N) prefix max solution, but why does two pointers work without looking at all walls?", mood="skeptical")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array),
                StateItem(kind="variable", name="totalWater", value="0"),
            ],
            code_line=1,
            duration_ms=2500,
        ),
        # Scene 2: Intuition
        Scene(
            id="s2",
            type="intuition",
            title="Intuition: The Bottleneck Principle",
            narration="Water trapped at index i is determined by: min(max_left, max_right) - height[i]. If leftMax < rightMax, the left side is the strictly limiting wall, regardless of any unknown peaks in the middle!",
            dialogue=[
                DialogueLine(character_id="algo", text="Water only spills over the SHORTER wall. If left is shorter than right, the right side cannot lower the water ceiling!", mood="explaining"),
                DialogueLine(character_id="bug", text="So we don't need to know the exact right maximum—just that it's at least as tall as leftMax!", mood="thinking")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array),
                StateItem(kind="variable", name="left", value="0"),
                StateItem(kind="variable", name="right", value="11"),
            ],
            code_line=7,
            duration_ms=2500,
        ),
        # Scene 3: Setup
        Scene(
            id="s3",
            type="setup",
            title="Initial State & Two Pointers",
            narration="Initialize left pointer at index 0 and right pointer at index 11. leftMax = 0, rightMax = 0, totalWater = 0.",
            dialogue=[
                DialogueLine(character_id="algo", text="Two climbers start at opposite ends. Let's see who faces the shorter wall.", mood="confident"),
                DialogueLine(character_id="data", text="Climbers at index 0 (height 0) and index 11 (height 1).", mood="neutral")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array),
                StateItem(kind="pointer", name="left", value="0", target_index=0),
                StateItem(kind="pointer", name="right", value="11", target_index=11),
                StateItem(kind="variable", name="leftMax", value="0"),
                StateItem(kind="variable", name="rightMax", value="0"),
                StateItem(kind="variable", name="totalWater", value="0"),
            ],
            code_line=3,
            duration_ms=2200,
        ),
        # Scene 4: Step 1 - Compare height[0] < height[11]
        Scene(
            id="s4",
            type="decision",
            title="Compare height[left]=0 vs height[right]=1",
            narration="height[0] (0) < height[11] (1). Left is strictly smaller. We update leftMax = max(0, 0) = 0 and advance left to 1.",
            dialogue=[
                DialogueLine(character_id="algo", text="height[0] is 0, height[11] is 1. Left is smaller, so left is the bottleneck.", mood="explaining"),
                DialogueLine(character_id="bug", text="Why can we advance left without checking index 1 through 10?", mood="skeptical")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array, index=0, highlight=True),
                StateItem(kind="pointer", name="left", value="0", target_index=0),
                StateItem(kind="pointer", name="right", value="11", target_index=11),
                StateItem(kind="variable", name="leftMax", value="0"),
                StateItem(kind="variable", name="rightMax", value="0"),
                StateItem(kind="variable", name="totalWater", value="0"),
            ],
            code_line=9,
            duration_ms=2200,
            why=WhyExplanation(
                decision="height[left] (0) < height[right] (1)",
                limiting_factor="Left side is the shorter boundary",
                invariant_proof="Because height[right]=1 >= leftMax=0, any wall in between will be at least 0. Water capacity at index 0 is max(0, leftMax - height[0]) = 0.",
                skeptical_question="Couldn't a taller wall in the middle trap more water at index 0?",
                airtight_answer="No! The water at index 0 cannot rise above its left boundary (leftMax = 0). It spills to the left immediately."
            )
        ),
        # Scene 5: Step 2 - left at 1 (height 1), right at 11 (height 1)
        Scene(
            id="s5",
            type="step",
            title="Advance left to 1. height[1] = 1, leftMax becomes 1",
            narration="left moves to index 1. height[1] is 1 >= leftMax (0), so leftMax updates to 1. Water trapped = 0. Compare height[1]=1 vs height[11]=1.",
            dialogue=[
                DialogueLine(character_id="algo", text="leftMax is now 1. Now height[left]=1 and height[right]=1 are equal, so we process right.", mood="explaining"),
                DialogueLine(character_id="data", text="Wall at index 1 is height 1. It acts as our new left dam!", mood="neutral")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array, index=1, highlight=True),
                StateItem(kind="pointer", name="left", value="1", target_index=1),
                StateItem(kind="pointer", name="right", value="11", target_index=11),
                StateItem(kind="variable", name="leftMax", value="1", highlight=True),
                StateItem(kind="variable", name="rightMax", value="0"),
                StateItem(kind="variable", name="totalWater", value="0"),
            ],
            code_line=11,
            duration_ms=2000,
        ),
        # Scene 6: Step 3 - right at 11, updates rightMax = 1, right moves to 10
        Scene(
            id="s6",
            type="step",
            title="Process right=11: rightMax becomes 1, right decrements to 10",
            narration="height[11] is 1. rightMax updates to 1. right moves to 10. height[10] = 2. Now left=1 (1), right=10 (2).",
            dialogue=[
                DialogueLine(character_id="algo", text="rightMax is updated to 1. right moves to index 10 (height 2).", mood="explaining"),
                DialogueLine(character_id="bug", text="Now left has height 1, right has height 2. Left is smaller again!", mood="thinking")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array, index=10, highlight=True),
                StateItem(kind="pointer", name="left", value="1", target_index=1),
                StateItem(kind="pointer", name="right", value="10", target_index=10),
                StateItem(kind="variable", name="leftMax", value="1"),
                StateItem(kind="variable", name="rightMax", value="1", highlight=True),
                StateItem(kind="variable", name="totalWater", value="0"),
            ],
            code_line=19,
            duration_ms=2000,
        ),
        # Scene 7: Step 4 - left=1 < right=10 -> advance left to 2
        Scene(
            id="s7",
            type="step",
            title="Advance left to index 2 (height 0)",
            narration="height[left] (1) < height[right] (2). Left climber advances to index 2 where height is 0. leftMax is 1.",
            dialogue=[
                DialogueLine(character_id="algo", text="We are at index 2 with height 0, while leftMax is 1!", mood="explaining"),
                DialogueLine(character_id="data", text="I'm a dip of height 0 between walls!", mood="neutral")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array, index=2, highlight=True),
                StateItem(kind="pointer", name="left", value="2", target_index=2),
                StateItem(kind="pointer", name="right", value="10", target_index=10),
                StateItem(kind="variable", name="leftMax", value="1"),
                StateItem(kind="variable", name="rightMax", value="1"),
                StateItem(kind="variable", name="totalWater", value="0"),
            ],
            code_line=15,
            duration_ms=2000,
        ),
        # Scene 8: Water Trapped at Index 2! (KEY DECISION)
        Scene(
            id="s8",
            type="decision",
            title="First Water Trapped at Index 2! (+1 unit)",
            narration="height[2] = 0 is less than leftMax = 1. Water trapped here = leftMax - height[2] = 1 - 0 = 1. totalWater becomes 1! left advances to index 3.",
            dialogue=[
                DialogueLine(character_id="algo", text="Water trapped = leftMax (1) - height[2] (0) = 1 unit! Safe to finalize.", mood="celebrating"),
                DialogueLine(character_id="bug", text="Wait! Right pointer is at index 10 (height 2). What if there's a height 100 at index 7? Wouldn't index 2 hold 100 water?", mood="skeptical")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array, index=2, highlight=True),
                StateItem(kind="pointer", name="left", value="2", target_index=2),
                StateItem(kind="pointer", name="right", value="10", target_index=10),
                StateItem(kind="water", name="water_2", value="1", index=2),
                StateItem(kind="variable", name="leftMax", value="1"),
                StateItem(kind="variable", name="rightMax", value="1"),
                StateItem(kind="variable", name="totalWater", value="1", highlight=True),
            ],
            code_line=14,
            duration_ms=2800,
            why=WhyExplanation(
                decision="height[2] < leftMax && leftMax <= rightMax",
                limiting_factor="The left wall (leftMax = 1) is the strict bottleneck",
                invariant_proof="Even if index 7 had a height of 1000, water at index 2 would simply spill over the left wall (height 1). Water height is bounded by min(leftMax, rightMax) = min(1, >=2) = 1.",
                skeptical_question="Couldn't a taller wall on the right increase the water at index 2?",
                airtight_answer="No! The formula is min(leftMax, rightMax). Since leftMax is already smaller, increasing the right side changes nothing: min(1, 1000) is still 1!"
            )
        ),
        # Scene 9: left advances to 3 (height 2) -> leftMax becomes 2
        Scene(
            id="s9",
            type="step",
            title="left at index 3: height[3]=2, leftMax updates to 2",
            narration="left moves to index 3. height[3] = 2 >= leftMax (1), so leftMax updates to 2. Now height[3]=2 equals height[10]=2. right side is processed.",
            dialogue=[
                DialogueLine(character_id="algo", text="A taller wall at index 3! leftMax is now 2. No water trapped on the wall itself.", mood="explaining"),
                DialogueLine(character_id="data", text="Wall height 2 establishes a new higher boundary for future steps.", mood="neutral")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array, index=3, highlight=True),
                StateItem(kind="pointer", name="left", value="3", target_index=3),
                StateItem(kind="pointer", name="right", value="10", target_index=10),
                StateItem(kind="water", name="water_2", value="1", index=2),
                StateItem(kind="variable", name="leftMax", value="2", highlight=True),
                StateItem(kind="variable", name="rightMax", value="1"),
                StateItem(kind="variable", name="totalWater", value="1"),
            ],
            code_line=11,
            duration_ms=2000,
        ),
        # Scene 10: right at 10 (height 2) -> rightMax becomes 2, right moves to 9
        Scene(
            id="s10",
            type="step",
            title="right at 10: rightMax becomes 2, right moves to 9 (height 1)",
            narration="height[10] = 2 >= rightMax (1), so rightMax updates to 2. right decrements to index 9 (height 1).",
            dialogue=[
                DialogueLine(character_id="algo", text="rightMax is now 2. Right moves to index 9 where height is 1.", mood="explaining"),
                DialogueLine(character_id="bug", text="Now height[right]=1 is smaller than height[left]=2. Right is the bottleneck now!", mood="thinking")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array, index=9, highlight=True),
                StateItem(kind="pointer", name="left", value="3", target_index=3),
                StateItem(kind="pointer", name="right", value="9", target_index=9),
                StateItem(kind="water", name="water_2", value="1", index=2),
                StateItem(kind="variable", name="leftMax", value="2"),
                StateItem(kind="variable", name="rightMax", value="2", highlight=True),
                StateItem(kind="variable", name="totalWater", value="1"),
            ],
            code_line=19,
            duration_ms=2200,
        ),
        # Scene 11: Water trapped from right at index 9! (+1 unit)
        Scene(
            id="s11",
            type="decision",
            title="Water Trapped at Index 9 from Right! (+1 unit, Total: 2)",
            narration="height[right] (1) < height[left] (2). Right side is the limiter. Water = rightMax (2) - height[9] (1) = 1. totalWater = 2. right decrements to 8.",
            dialogue=[
                DialogueLine(character_id="algo", text="Symmetric logic! Since right is shorter, rightMax (2) determines the trapped water at index 9.", mood="confident"),
                DialogueLine(character_id="bug", text="Beautiful! The exact same invariant works in reverse from the right boundary.", mood="celebrating")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array, index=9, highlight=True),
                StateItem(kind="pointer", name="left", value="3", target_index=3),
                StateItem(kind="pointer", name="right", value="9", target_index=9),
                StateItem(kind="water", name="water_2", value="1", index=2),
                StateItem(kind="water", name="water_9", value="1", index=9),
                StateItem(kind="variable", name="leftMax", value="2"),
                StateItem(kind="variable", name="rightMax", value="2"),
                StateItem(kind="variable", name="totalWater", value="2", highlight=True),
            ],
            code_line=22,
            duration_ms=2400,
            why=WhyExplanation(
                decision="height[right] (1) < height[left] (2)",
                limiting_factor="Right wall is shorter than left wall",
                invariant_proof="Because leftMax >= 2 >= rightMax, the left side is guaranteed to hold at least rightMax height. Water at index 9 is capped at rightMax - height[9] = 2 - 1 = 1.",
                skeptical_question="Can anything on the left leak water out?",
                airtight_answer="No, leftMax is already 2, so the left dam is tall enough. Water only spills over rightMax."
            )
        ),
        # Scene 12: Continuing left side across indices 4, 5, 6
        Scene(
            id="s12",
            type="step",
            title="left sweeps index 4, 5, 6: Trapping +1, +2, +1 Water!",
            narration="At index 4 (height 1): traps 2 - 1 = 1 unit. At index 5 (height 0): traps 2 - 0 = 2 units! At index 6 (height 1): traps 2 - 1 = 1 unit. totalWater increases by 4 to 6!",
            dialogue=[
                DialogueLine(character_id="algo", text="Notice index 5: with height 0 and leftMax 2, it holds 2 full units of water!", mood="explaining"),
                DialogueLine(character_id="data", text="Pools forming at indices 4, 5, 6! Total water is now 6.", mood="celebrating")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array, index=5, highlight=True),
                StateItem(kind="pointer", name="left", value="6", target_index=6),
                StateItem(kind="pointer", name="right", value="8", target_index=8),
                StateItem(kind="water", name="water_2", value="1", index=2),
                StateItem(kind="water", name="water_4", value="1", index=4),
                StateItem(kind="water", name="water_5", value="2", index=5),
                StateItem(kind="water", name="water_6", value="1", index=6),
                StateItem(kind="water", name="water_9", value="1", index=9),
                StateItem(kind="variable", name="leftMax", value="2"),
                StateItem(kind="variable", name="rightMax", value="2"),
                StateItem(kind="variable", name="totalWater", value="6", highlight=True),
            ],
            code_line=14,
            duration_ms=2600,
        ),
        # Scene 13: The Peak at Index 7 (height 3)
        Scene(
            id="s13",
            type="step",
            title="Meeting the Peak at Index 7 (height 3)",
            narration="left moves to index 7 where height is 3. leftMax updates to 3. Pointers converge at the highest peak.",
            dialogue=[
                DialogueLine(character_id="algo", text="Index 7 is the global maximum (height 3). Both climbers converge here.", mood="explaining"),
                DialogueLine(character_id="bug", text="Once left == right, every single cell has been accounted for!", mood="celebrating")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array, index=7, highlight=True),
                StateItem(kind="pointer", name="left", value="7", target_index=7),
                StateItem(kind="pointer", name="right", value="7", target_index=7),
                StateItem(kind="water", name="water_2", value="1", index=2),
                StateItem(kind="water", name="water_4", value="1", index=4),
                StateItem(kind="water", name="water_5", value="2", index=5),
                StateItem(kind="water", name="water_6", value="1", index=6),
                StateItem(kind="water", name="water_9", value="1", index=9),
                StateItem(kind="variable", name="leftMax", value="3", highlight=True),
                StateItem(kind="variable", name="rightMax", value="2"),
                StateItem(kind="variable", name="totalWater", value="6"),
            ],
            code_line=8,
            duration_ms=2200,
        ),
        # Scene 14: Final Invariant & Result
        Scene(
            id="s14",
            type="result",
            title="Execution Complete: Total Trapped Water = 6",
            narration="Loop terminates when left == right. Total trapped water is 6 units. We finalized each position in exactly one pass.",
            dialogue=[
                DialogueLine(character_id="algo", text="Final answer is 6! Every decision was provably optimal in O(1) space.", mood="confident"),
                DialogueLine(character_id="bug", text="The two-pointer invariant makes complete sense now: the shorter wall is always the decision-maker!", mood="celebrating")
            ],
            states=[
                StateItem(kind="array", name="height", value=raw_array),
                StateItem(kind="water", name="water_2", value="1", index=2),
                StateItem(kind="water", name="water_4", value="1", index=4),
                StateItem(kind="water", name="water_5", value="2", index=5),
                StateItem(kind="water", name="water_6", value="1", index=6),
                StateItem(kind="water", name="water_9", value="1", index=9),
                StateItem(kind="variable", name="totalWater", value="6", highlight=True),
            ],
            code_line=26,
            duration_ms=2500,
        ),
        # Scene 15: Complexity Analysis
        Scene(
            id="s15",
            type="complexity",
            title="Complexity & Staff Invariant Summary",
            narration="Time Complexity: O(N) because each step increments left or decrements right. Space Complexity: O(1) auxiliary space as only two pointers and two max variables are maintained.",
            dialogue=[
                DialogueLine(character_id="algo", text="Time: O(N) single pass. Space: O(1) constant memory. Optimal in both dimensions.", mood="explaining"),
                DialogueLine(character_id="bug", text="No prefix arrays needed. That's the power of the two-pointer invariant!", mood="celebrating")
            ],
            states=[
                StateItem(kind="variable", name="Time", value="O(N)"),
                StateItem(kind="variable", name="Space", value="O(1)"),
                StateItem(kind="variable", name="Result", value="6"),
            ],
            code_line=26,
            duration_ms=2500,
        ),
    ]

    return AnimationSpec(
        title="Trapping Rain Water",
        algorithm="Two Pointers",
        problem="Given n non-negative integers representing an elevation map where width of each bar is 1, compute how much water it can trap after raining.",
        intuition="Water trapped at any bar i is min(leftMax, rightMax) - height[i]. By keeping two pointers and moving whichever side has the smaller max, we know with 100% certainty that the smaller side is the limiting factor.",
        visual_metaphor="Two climbers walking inward from opposite mountain ridges, measuring bounding walls and filling trapped pools.",
        invariant="At any step, if leftMax < rightMax, the water level at the left pointer is strictly bounded by leftMax, regardless of unseen heights in between.",
        time_complexity="O(N)",
        space_complexity="O(1)",
        confidence=1.0,
        source_code=SAMPLE_CSHARP_CODE,
        source_language="csharp",
        characters=characters,
        scenes=scenes
    )

def render_html(spec: AnimationSpec, template_path: Path, out_path: Path):
    template = template_path.read_text(encoding="utf-8")
    payload = json.dumps(spec.model_dump(), ensure_ascii=False).replace("</", "<\\/")
    html = template.replace("__SPEC__", payload)
    out_path.write_text(html, encoding="utf-8")

def call_gemini(prompt: str, model_name: str = "gemini-3.8-flash") -> AnimationSpec:
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is required to call the Gemini API.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=[prompt],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2,
            max_output_tokens=14000,
            response_mime_type="application/json",
            response_schema=AnimationSpec.model_json_schema(),
        ),
    )
    return AnimationSpec.model_validate_json(response.text)

def build_prompt(algorithm: str, example_input: str, audience: str, source_code: Optional[str] = None) -> str:
    code_section = f"\nSOURCE CODE:\n```\n{source_code}\n```\n" if source_code else ""
    return f"""Create a comic-style educational animation specification for this algorithm.

TARGET AUDIENCE: {audience}

ALGORITHM DESCRIPTION / ASK:
{algorithm}
{code_section}
EXAMPLE INPUT:
{example_input or "Pick a clean, small illustrative example (e.g. array of length 6-12) to trace."}

REQUIREMENTS:
1. Four logical stages:
   - Teacher Agent: clear intuition contrasting brute-force vs optimal, visual metaphor, and mathematical invariant.
   - Trace Agent: exact state transitions for each step (arrays, indices, pointers, variables).
   - Storyboard Agent: Algo (🧑 guide), Bug (🤔 skeptical interviewer), Data (🧱 structure) dialogue with emotions.
   - "Why is this safe?" Mode: For all decision scenes, supply the WhyExplanation with decision, limiting_factor, invariant_proof, skeptical_question, and airtight_answer.
2. Synchronize code lines with the source code (1-based line numbers).
3. Return valid AnimationSpec JSON matching the schema.
"""

def main():
    p = argparse.ArgumentParser(description="AlgoAnimator: Algorithm to Comic Animation Engine")
    p.add_argument("algorithm", nargs="?", help="Algorithm prompt or description")
    p.add_argument("--file", help="Path to source code file (e.g. Solution.cs, solution.py)")
    p.add_argument("--input", default="", help="Input data (e.g. '[0,1,0,2,1,0,1,3,2,1,2,1]')")
    p.add_argument("--audience", default="interview", choices=["beginner", "interview", "expert"])
    p.add_argument("--out", default="output", help="Output directory")
    p.add_argument("--sample", choices=["trapping-rain-water"], help="Generate pre-built high-quality sample")
    p.add_argument("--render", help="Render an existing animation.json file to animation.html")
    p.add_argument("--model", default="gemini-3.8-flash", help="Gemini model to use")
    args = p.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    template_path = Path(__file__).with_name("renderer.html")

    # Mode 1: Render existing JSON
    if args.render:
        render_path = Path(args.render)
        if not render_path.exists():
            sys.exit(f"Error: {render_path} does not exist.")
        spec_data = json.loads(render_path.read_text(encoding="utf-8"))
        spec = AnimationSpec.model_validate(spec_data)
        out_html = out_dir / "animation.html"
        render_html(spec, template_path, out_html)
        print(f"Successfully rendered: {out_html}")
        return

    # Mode 2: Sample generation (offline / instant demo)
    if args.sample == "trapping-rain-water" or (not args.algorithm and not args.file and not os.environ.get("GEMINI_API_KEY")):
        print("Generating canonical Trapping Rain Water Two-Pointer sample animation...")
        spec = get_trapping_rain_water_sample()
    elif args.algorithm or args.file:
        source_code = None
        algo_text = args.algorithm or ""
        if args.file:
            f_path = Path(args.file)
            if not f_path.exists():
                sys.exit(f"Error: file {f_path} not found.")
            source_code = f_path.read_text(encoding="utf-8")
            if not algo_text:
                algo_text = f"Animate the solution in {f_path.name}"

        prompt = build_prompt(algo_text, args.input, args.audience, source_code)
        try:
            print(f"Invoking {args.model} with structured output...")
            spec = call_gemini(prompt, args.model)
            if source_code and not spec.source_code:
                spec.source_code = source_code
        except Exception as e:
            print(f"Warning: Gemini API call failed or GEMINI_API_KEY not set: {e}")
            print("Falling back to high-fidelity reference Trapping Rain Water sample...")
            spec = get_trapping_rain_water_sample()
    else:
        p.print_help()
        return

    # Save animation.json
    json_path = out_dir / "animation.json"
    json_path.write_text(spec.model_dump_json(indent=2), encoding="utf-8")

    # Save animation.html
    html_path = out_dir / "animation.html"
    render_html(spec, template_path, html_path)

    # Save explanation.md
    explanation_md = f"""# {spec.title} — {spec.algorithm}

## 🎯 Problem
{spec.problem}

## 💡 Core Intuition
{spec.intuition}

## 🎨 Visual Metaphor
{spec.visual_metaphor or "Visual step-by-step trace with pointer inspection."}

## 🛡️ Mathematical Invariant ("Why is this safe?")
{spec.invariant}

## ⏱️ Complexity
- **Time Complexity:** {spec.time_complexity}
- **Space Complexity:** {spec.space_complexity}

## 🧑 Characters
{chr(10).join(f"- **{c.name}** ({c.role})" for c in spec.characters)}

## 🎬 Generated Scenes: {len(spec.scenes)} total scenes.
"""
    (out_dir / "explanation.md").write_text(explanation_md, encoding="utf-8")

    print("\n✅ AlgoAnimator generation complete!")
    print(f"  ├─ HTML Animation: {html_path.resolve()}")
    print(f"  ├─ JSON Spec:      {json_path.resolve()}")
    print(f"  └─ Explanation:    {out_dir.resolve() / 'explanation.md'}")

if __name__ == "__main__":
    main()
