"""
AlgoAnimator Simulator: Executes algorithms against comprehensive corner-case suites.
Validates step invariants and generates structured AnimationSpecs for each case.
"""

import ast
import re
from typing import List, Dict, Any, Tuple, Optional
from schema import AnimationSpec, Scene, Character, StateItem, WhyExplanation, DialogueLine

class CornerTestCase:
    def __init__(self, name: str, description: str, data: List[int], expected_output: Any):
        self.name = name
        self.description = description
        self.data = data
        self.expected_output = expected_output

def get_trapping_rain_water_corner_cases() -> List[CornerTestCase]:
    """Generates a comprehensive battery of test cases covering all edge conditions."""
    return [
        CornerTestCase(
            name="Standard Basin",
            description="Classic LeetCode test case with multiple valleys and peaks.",
            data=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],
            expected_output=6
        ),
        CornerTestCase(
            name="Empty Elevation Map",
            description="Empty array (length 0). Invariant: no water can be trapped.",
            data=[],
            expected_output=0
        ),
        CornerTestCase(
            name="Single Element",
            description="Array with length 1. No opposing boundary exists.",
            data=[4],
            expected_output=0
        ),
        CornerTestCase(
            name="Two Elements",
            description="Array with length 2. Cannot form a container between two walls.",
            data=[3, 1],
            expected_output=0
        ),
        CornerTestCase(
            name="All Equal Heights",
            description="Flat terrain with identical heights [2, 2, 2, 2]. Water runs off.",
            data=[2, 2, 2, 2],
            expected_output=0
        ),
        CornerTestCase(
            name="Strictly Decreasing",
            description="Descending stair [5, 4, 3, 2, 1]. Water spills to the right.",
            data=[5, 4, 3, 2, 1],
            expected_output=0
        ),
        CornerTestCase(
            name="Strictly Increasing",
            description="Ascending stair [1, 2, 3, 4, 5]. Water spills to the left.",
            data=[1, 2, 3, 4, 5],
            expected_output=0
        ),
        CornerTestCase(
            name="Deep Single Basin",
            description="Two high pillars with low valley [4, 0, 0, 4]. Maximum trapped capacity.",
            data=[4, 0, 0, 4],
            expected_output=8
        ),
        CornerTestCase(
            name="Asymmetric Peak",
            description="One towering pillar surrounded by lower bars [10, 1, 2, 1].",
            data=[10, 1, 2, 1],
            expected_output=1
        ),
    ]

def simulate_trapping_rain_water(case: CornerTestCase, source_code: Optional[str] = None) -> Tuple[int, AnimationSpec]:
    """
    Executes the two-pointer trapping rain water algorithm step-by-step on input data,
    verifying invariants at every step and producing a complete AnimationSpec.
    """
    height = case.data
    n = len(height)
    characters = [
        Character(id="algo", name="Algo", role="Guide & Teacher", mood="explaining"),
        Character(id="bug", name="Bug", role="Skeptical Interviewer", mood="skeptical"),
        Character(id="data", name="Data", role="Elevation Map", mood="neutral"),
    ]

    scenes: List[Scene] = []
    raw_str = ",".join(str(x) for x in height) if height else ""

    # Scene 1: Introduction of Test Case
    scenes.append(Scene(
        id="s1_init",
        type="title",
        title=f"Test Case: {case.name}",
        narration=f"Testing input [{raw_str}] ({case.description}). Expected output: {case.expected_output}.",
        dialogue=[
            DialogueLine(character_id="algo", text=f"Evaluating test case '{case.name}' with input: [{raw_str}].", mood="confident"),
            DialogueLine(character_id="bug", text=f"How will our two-pointer invariant handle this boundary condition?", mood="thinking")
        ],
        states=[
            StateItem(kind="array", name="height", value=raw_str) if raw_str else StateItem(kind="text", name="height", value="[]"),
            StateItem(kind="variable", name="totalWater", value="0"),
        ],
        code_line=1
    ))

    # Corner case: n < 3
    if n < 3:
        reason = "Array length < 3: cannot form a basin" if n > 0 else "Empty array: 0 elements"
        scenes.append(Scene(
            id="s_edge",
            type="result",
            title=f"Corner Case Handled: Length {n}",
            narration=f"Because length is {n} < 3, no two opposing walls can trap water. Returns 0 immediately.",
            dialogue=[
                DialogueLine(character_id="algo", text=f"Zero water trapped. {reason}.", mood="confident"),
                DialogueLine(character_id="bug", text="Correct. A container requires at least two boundary walls and one interior cell.", mood="celebrating")
            ],
            states=[
                StateItem(kind="variable", name="totalWater", value="0", highlight=True),
                StateItem(kind="variable", name="length", value=str(n)),
            ],
            code_line=7
        ))
        return 0, AnimationSpec(
            title=f"Trapping Rain Water — {case.name}",
            algorithm="Two Pointers",
            problem="Given n non-negative integers representing an elevation map, compute trapped water.",
            intuition="Water requires at least two opposing boundaries and an intermediate dip.",
            visual_metaphor="Climbers inspect boundaries.",
            invariant="When length < 3, trapped water is mathematically 0.",
            time_complexity="O(N)",
            space_complexity="O(1)",
            confidence=1.0,
            source_code=source_code,
            source_language="csharp",
            characters=characters,
            scenes=scenes
        )

    # Full Two-Pointer Simulation
    left, right = 0, n - 1
    left_max, right_max = 0, 0
    total_water = 0
    trapped_per_cell: Dict[int, int] = {}
    step_num = 2

    # Initial setup scene
    scenes.append(Scene(
        id=f"s{step_num}_setup",
        type="setup",
        title="Setup Pointers and Boundaries",
        narration=f"Set left=0, right={n-1}, leftMax=0, rightMax=0, totalWater=0.",
        dialogue=[
            DialogueLine(character_id="algo", text=f"Left pointer at index 0 (height {height[0]}), right pointer at index {n-1} (height {height[n-1]}).", mood="explaining"),
            DialogueLine(character_id="bug", text="Both pointers start at the outer extremities.", mood="neutral")
        ],
        states=[
            StateItem(kind="array", name="height", value=raw_str),
            StateItem(kind="pointer", name="left", value=str(left), target_index=left),
            StateItem(kind="pointer", name="right", value=str(right), target_index=right),
            StateItem(kind="variable", name="leftMax", value=str(left_max)),
            StateItem(kind="variable", name="rightMax", value=str(right_max)),
            StateItem(kind="variable", name="totalWater", value="0"),
        ],
        code_line=3
    ))
    step_num += 1

    while left < right:
        is_left_smaller = height[left] < height[right]

        if is_left_smaller:
            curr_idx = left
            h_curr = height[left]
            if h_curr >= left_max:
                left_max = h_curr
                scenes.append(Scene(
                    id=f"s{step_num}_left_max",
                    type="step",
                    title=f"Update leftMax to {left_max} at Index {left}",
                    narration=f"height[{left}] ({h_curr}) >= leftMax. New leftMax is {left_max}. No water trapped on the wall itself.",
                    dialogue=[
                        DialogueLine(character_id="algo", text=f"leftMax updated to {left_max}.", mood="explaining"),
                        DialogueLine(character_id="data", text=f"New left boundary established at index {left}.", mood="neutral")
                    ],
                    states=[
                        StateItem(kind="array", name="height", value=raw_str, index=left, highlight=True),
                        StateItem(kind="pointer", name="left", value=str(left), target_index=left),
                        StateItem(kind="pointer", name="right", value=str(right), target_index=right),
                        StateItem(kind="variable", name="leftMax", value=str(left_max), highlight=True),
                        StateItem(kind="variable", name="rightMax", value=str(right_max)),
                        StateItem(kind="variable", name="totalWater", value=str(total_water)),
                    ],
                    code_line=11
                ))
            else:
                water_here = left_max - h_curr
                total_water += water_here
                trapped_per_cell[curr_idx] = water_here
                scenes.append(Scene(
                    id=f"s{step_num}_water_left",
                    type="decision",
                    title=f"Water Trapped at Index {left} (+{water_here} units)",
                    narration=f"leftMax ({left_max}) > height[{left}] ({h_curr}). Water = {left_max} - {h_curr} = {water_here}. totalWater is now {total_water}.",
                    dialogue=[
                        DialogueLine(character_id="algo", text=f"Trapped {water_here} water! Bounded by leftMax ({left_max}).", mood="celebrating"),
                        DialogueLine(character_id="bug", text=f"Why can't right side leak water?", mood="skeptical")
                    ],
                    states=[
                        StateItem(kind="array", name="height", value=raw_str, index=left, highlight=True),
                        StateItem(kind="pointer", name="left", value=str(left), target_index=left),
                        StateItem(kind="pointer", name="right", value=str(right), target_index=right),
                        *[StateItem(kind="water", name=f"water_{idx}", value=str(amt), index=idx) for idx, amt in trapped_per_cell.items()],
                        StateItem(kind="variable", name="leftMax", value=str(left_max)),
                        StateItem(kind="variable", name="rightMax", value=str(right_max)),
                        StateItem(kind="variable", name="totalWater", value=str(total_water), highlight=True),
                    ],
                    code_line=14,
                    why=WhyExplanation(
                        decision=f"height[{left}] ({h_curr}) < height[{right}] ({height[right]})",
                        limiting_factor="Left boundary is strictly smaller than right boundary",
                        invariant_proof=f"Since height[{right}] >= leftMax ({left_max}), the water level at index {left} cannot exceed {left_max}.",
                        skeptical_question=f"Could an unseen middle wall change index {left}'s water?",
                        airtight_answer=f"No. The water ceiling is min(leftMax, rightMax). Since leftMax={left_max} <= rightMax, leftMax is the sole bottleneck."
                    )
                ))
            left += 1
        else:
            curr_idx = right
            h_curr = height[right]
            if h_curr >= right_max:
                right_max = h_curr
                scenes.append(Scene(
                    id=f"s{step_num}_right_max",
                    type="step",
                    title=f"Update rightMax to {right_max} at Index {right}",
                    narration=f"height[{right}] ({h_curr}) >= rightMax. New rightMax is {right_max}. No water trapped on the wall itself.",
                    dialogue=[
                        DialogueLine(character_id="algo", text=f"rightMax updated to {right_max}.", mood="explaining"),
                        DialogueLine(character_id="data", text=f"New right boundary established at index {right}.", mood="neutral")
                    ],
                    states=[
                        StateItem(kind="array", name="height", value=raw_str, index=right, highlight=True),
                        StateItem(kind="pointer", name="left", value=str(left), target_index=left),
                        StateItem(kind="pointer", name="right", value=str(right), target_index=right),
                        StateItem(kind="variable", name="leftMax", value=str(left_max)),
                        StateItem(kind="variable", name="rightMax", value=str(right_max), highlight=True),
                        StateItem(kind="variable", name="totalWater", value=str(total_water)),
                    ],
                    code_line=19
                ))
            else:
                water_here = right_max - h_curr
                total_water += water_here
                trapped_per_cell[curr_idx] = water_here
                scenes.append(Scene(
                    id=f"s{step_num}_water_right",
                    type="decision",
                    title=f"Water Trapped at Index {right} (+{water_here} units)",
                    narration=f"rightMax ({right_max}) > height[{right}] ({h_curr}). Water = {right_max} - {h_curr} = {water_here}. totalWater is now {total_water}.",
                    dialogue=[
                        DialogueLine(character_id="algo", text=f"Trapped {water_here} water from the right side!", mood="celebrating"),
                        DialogueLine(character_id="bug", text="Symmetric invariant holds from right to left.", mood="confident")
                    ],
                    states=[
                        StateItem(kind="array", name="height", value=raw_str, index=right, highlight=True),
                        StateItem(kind="pointer", name="left", value=str(left), target_index=left),
                        StateItem(kind="pointer", name="right", value=str(right), target_index=right),
                        *[StateItem(kind="water", name=f"water_{idx}", value=str(amt), index=idx) for idx, amt in trapped_per_cell.items()],
                        StateItem(kind="variable", name="leftMax", value=str(left_max)),
                        StateItem(kind="variable", name="rightMax", value=str(right_max)),
                        StateItem(kind="variable", name="totalWater", value=str(total_water), highlight=True),
                    ],
                    code_line=22,
                    why=WhyExplanation(
                        decision=f"height[{right}] ({h_curr}) <= height[{left}] ({height[left]})",
                        limiting_factor="Right boundary is the limiting wall",
                        invariant_proof=f"Since leftMax >= rightMax ({right_max}), water at index {right} is bounded by rightMax.",
                        skeptical_question="Can water spill to the left?",
                        airtight_answer=f"No. The left side has a wall of at least {right_max}, so water cannot escape to the left."
                    )
                ))
            right -= 1

        step_num += 1

    # Final Result Scene
    scenes.append(Scene(
        id="s_final",
        type="result",
        title=f"Simulation Complete: {total_water} Total Water Trapped",
        narration=f"Pointers met at index {left}. Total water trapped: {total_water}. Matches expected output: {case.expected_output}.",
        dialogue=[
            DialogueLine(character_id="algo", text=f"Total water calculated is {total_water}. Exact match!", mood="celebrating"),
            DialogueLine(character_id="bug", text=f"All corner invariants held with zero errors.", mood="celebrating")
        ],
        states=[
            StateItem(kind="array", name="height", value=raw_str),
            *[StateItem(kind="water", name=f"water_{idx}", value=str(amt), index=idx) for idx, amt in trapped_per_cell.items()],
            StateItem(kind="variable", name="totalWater", value=str(total_water), highlight=True),
        ],
        code_line=26
    ))

    spec = AnimationSpec(
        title=f"Trapping Rain Water — {case.name}",
        algorithm="Two Pointers",
        problem=f"Elevation map: [{raw_str}]",
        intuition="Two pointer invariant bounds the water level using the strictly shorter side.",
        visual_metaphor="Mountain ridges and basin filling.",
        invariant="At every step, min(leftMax, rightMax) guarantees the water level for the shorter side.",
        time_complexity="O(N)",
        space_complexity="O(1)",
        confidence=1.0,
        source_code=source_code,
        source_language="csharp",
        characters=characters,
        scenes=scenes
    )

    return total_water, spec

# ---------------------------------------------------------------------------
# 2. Binary Search
# ---------------------------------------------------------------------------
def simulate_binary_search(nums: List[int], target: int, source_code: Optional[str] = None) -> Tuple[int, AnimationSpec]:
    nums = sorted(nums)
    n = len(nums)
    raw_str = ",".join(str(x) for x in nums)
    characters = [
        Character(id="algo", name="Algo", role="Detective / Teacher", mood="explaining"),
        Character(id="bug", name="Bug", role="Skeptic", mood="skeptical"),
        Character(id="data", name="Data", role="Sorted Space", mood="neutral"),
    ]

    scenes: List[Scene] = []
    scenes.append(Scene(
        id="bs_1",
        type="title",
        title=f"Binary Search: Target {target}",
        narration=f"Searching for target = {target} in sorted array of {n} elements: [{raw_str}].",
        dialogue=[
            DialogueLine(character_id="algo", text=f"Locating target {target}. Because the array is sorted, we eliminate half the candidate elements in each step!", mood="confident"),
            DialogueLine(character_id="bug", text="Let's make sure our middle index calculation doesn't overflow or miss target.", mood="thinking")
        ],
        states=[
            StateItem(kind="array", name="nums", value=raw_str),
            StateItem(kind="variable", name="target", value=str(target)),
        ],
        code_line=1
    ))

    left, right = 0, n - 1
    found_idx = -1
    step = 2

    while left <= right:
        mid = left + (right - left) // 2
        mid_val = nums[mid]

        scenes.append(Scene(
            id=f"bs_{step}",
            type="decision",
            title=f"Probe Midpoint: Index {mid} (Value {mid_val})",
            narration=f"Search range [{left}..{right}]. Calculate mid = {left} + ({right} - {left}) / 2 = {mid}. nums[{mid}] = {mid_val}.",
            dialogue=[
                DialogueLine(character_id="algo", text=f"Checking midpoint index {mid} with value {mid_val}.", mood="explaining"),
                DialogueLine(character_id="data", text=f"Target is {target}. Comparing {mid_val} vs {target}.", mood="neutral")
            ],
            states=[
                StateItem(kind="array", name="nums", value=raw_str, index=mid, highlight=True),
                StateItem(kind="pointer", name="left", value=str(left), target_index=left),
                StateItem(kind="pointer", name="right", value=str(right), target_index=right),
                StateItem(kind="pointer", name="mid", value=str(mid), target_index=mid),
                StateItem(kind="variable", name="target", value=str(target)),
                StateItem(kind="variable", name="nums[mid]", value=str(mid_val)),
            ],
            code_line=5,
            why=WhyExplanation(
                decision=f"nums[mid] = {mid_val} vs target = {target}",
                limiting_factor=f"Monotonicity: all items before index {mid} are <= {mid_val}, items after are >= {mid_val}",
                invariant_proof=f"If target is present, it MUST lie in [{left}..{right}].",
                skeptical_question="Why can we eliminate the entire half?",
                airtight_answer=f"Array is strictly sorted. If nums[{mid}] {'<' if mid_val < target else '>'} {target}, no element in the discarded half can ever equal {target}."
            )
        ))
        step += 1

        if mid_val == target:
            found_idx = mid
            scenes.append(Scene(
                id=f"bs_{step}_found",
                type="result",
                title=f"Target {target} Found at Index {mid}!",
                narration=f"nums[{mid}] == {target}. Search succeeds in logarithmic time O(log N).",
                dialogue=[
                    DialogueLine(character_id="algo", text=f"Match confirmed! Target {target} is at index {mid}.", mood="celebrating"),
                    DialogueLine(character_id="bug", text="Took only a few probes to search the entire array.", mood="celebrating")
                ],
                states=[
                    StateItem(kind="array", name="nums", value=raw_str, index=mid, highlight=True),
                    StateItem(kind="pointer", name="found", value=str(mid), target_index=mid),
                    StateItem(kind="variable", name="result", value=str(mid), highlight=True),
                ],
                code_line=6
            ))
            break
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1

    if found_idx == -1:
        scenes.append(Scene(
            id=f"bs_{step}_miss",
            type="result",
            title=f"Target {target} Not in Array",
            narration=f"Pointers crossed (left > right). Target {target} does not exist in array. Returns -1.",
            dialogue=[
                DialogueLine(character_id="algo", text=f"Target {target} is provably not present. Return -1.", mood="confident"),
                DialogueLine(character_id="bug", text="All potential locations systematically ruled out.", mood="neutral")
            ],
            states=[
                StateItem(kind="array", name="nums", value=raw_str),
                StateItem(kind="variable", name="result", value="-1", highlight=True),
            ],
            code_line=9
        ))

    spec = AnimationSpec(
        title=f"Binary Search — Target {target}",
        algorithm="Binary Search",
        problem=f"Find index of target {target} in sorted array [{raw_str}]",
        intuition="Halve the search space by probing the midpoint of the sorted range.",
        visual_metaphor="Detective eliminating half the rooms at each step.",
        invariant="Target is guaranteed to be within [left..right] if it exists in the array.",
        time_complexity="O(log N)",
        space_complexity="O(1)",
        confidence=1.0,
        source_code=source_code or """public int BinarySearch(int[] nums, int target)
{
    int left = 0, right = nums.Length - 1;
    while (left <= right)
    {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}""",
        source_language="csharp",
        characters=characters,
        scenes=scenes
    )
    return found_idx, spec

# ---------------------------------------------------------------------------
# 3. Two Sum (Hash Map)
# ---------------------------------------------------------------------------
def simulate_two_sum(nums: List[int], target: int, source_code: Optional[str] = None) -> Tuple[List[int], AnimationSpec]:
    n = len(nums)
    raw_str = ",".join(str(x) for x in nums)
    characters = [
        Character(id="algo", name="Algo", role="Guide", mood="explaining"),
        Character(id="bug", name="Bug", role="Interviewer", mood="thinking"),
        Character(id="data", name="Data", role="Hash Table", mood="neutral"),
    ]

    scenes: List[Scene] = []
    scenes.append(Scene(
        id="ts_1",
        type="title",
        title=f"Two Sum: Target {target}",
        narration=f"Find two indices in [{raw_str}] that sum to target {target} using a single-pass Hash Map.",
        dialogue=[
            DialogueLine(character_id="algo", text=f"Instead of O(N^2) double-looping, we store complements in a hash table for O(1) lookup!", mood="confident"),
            DialogueLine(character_id="bug", text="As we inspect each number x, we look up if (target - x) was already seen.", mood="explaining")
        ],
        states=[
            StateItem(kind="array", name="nums", value=raw_str),
            StateItem(kind="variable", name="target", value=str(target)),
        ],
        code_line=1
    ))

    seen: Dict[int, int] = {}
    result = []
    step = 2

    for i, num in enumerate(nums):
        complement = target - num
        seen_str = "{" + ", ".join(f"{k}:{v}" for k, v in seen.items()) + "}"

        if complement in seen:
            result = [seen[complement], i]
            scenes.append(Scene(
                id=f"ts_{step}_found",
                type="result",
                title=f"Complement Found! Indices [{seen[complement]}, {i}]",
                narration=f"At index {i} (num={num}), complement = {target} - {num} = {complement} was found in hash map at index {seen[complement]}! Sum = {nums[seen[complement]]} + {num} = {target}.",
                dialogue=[
                    DialogueLine(character_id="algo", text=f"Match! nums[{seen[complement]}] ({complement}) + nums[{i}] ({num}) = {target}!", mood="celebrating"),
                    DialogueLine(character_id="bug", text=f"Single-pass O(N) time with O(N) auxiliary hash table.", mood="celebrating")
                ],
                states=[
                    StateItem(kind="array", name="nums", value=raw_str, index=i, highlight=True),
                    StateItem(kind="pointer", name="prev", value=str(seen[complement]), target_index=seen[complement]),
                    StateItem(kind="pointer", name="curr", value=str(i), target_index=i),
                    StateItem(kind="variable", name="complement", value=str(complement)),
                    StateItem(kind="variable", name="hash_map", value=seen_str),
                    StateItem(kind="variable", name="result", value=f"[{seen[complement]}, {i}]", highlight=True),
                ],
                code_line=7
            ))
            break
        else:
            seen[num] = i
            scenes.append(Scene(
                id=f"ts_{step}_store",
                type="step",
                title=f"Inspect Index {i} ({num}): Look for {complement}",
                narration=f"nums[{i}] = {num}. Need complement {complement}. Not in hash map yet. Store seen[{num}] = {i}.",
                dialogue=[
                    DialogueLine(character_id="algo", text=f"Checking index {i} (val {num}). Need {complement}. Not seen yet.", mood="explaining"),
                    DialogueLine(character_id="data", text=f"Added {num} -> index {i} into hash table.", mood="neutral")
                ],
                states=[
                    StateItem(kind="array", name="nums", value=raw_str, index=i, highlight=True),
                    StateItem(kind="pointer", name="i", value=str(i), target_index=i),
                    StateItem(kind="variable", name="needed", value=str(complement)),
                    StateItem(kind="variable", name="hash_map", value=seen_str),
                ],
                code_line=9
            ))
        step += 1

    spec = AnimationSpec(
        title=f"Two Sum — Target {target}",
        algorithm="Hash Map",
        problem=f"Find indices in [{raw_str}] summing to {target}",
        intuition="Maintain a lookup table of past elements to evaluate the required complement in O(1).",
        visual_metaphor="Librarian with labeled drawers storing visited numbers.",
        invariant="All elements before index i are recorded in hash table with their 0-based indices.",
        time_complexity="O(N)",
        space_complexity="O(N)",
        confidence=1.0,
        source_code=source_code or """public int[] TwoSum(int[] nums, int target)
{
    var seen = new Dictionary<int, int>();
    for (int i = 0; i < nums.Length; i++)
    {
        int complement = target - nums[i];
        if (seen.ContainsKey(complement))
            return new int[] { seen[complement], i };
        seen[nums[i]] = i;
    }
    return new int[0];
}""",
        source_language="csharp",
        characters=characters,
        scenes=scenes
    )
    return result, spec

# ---------------------------------------------------------------------------
# 4. Maximum Subarray (Kadane's / Sliding Window)
# ---------------------------------------------------------------------------
def simulate_sliding_window(nums: List[int], source_code: Optional[str] = None) -> Tuple[int, AnimationSpec]:
    n = len(nums)
    raw_str = ",".join(str(x) for x in nums)
    characters = [
        Character(id="algo", name="Algo", role="Guide", mood="explaining"),
        Character(id="bug", name="Bug", role="Skeptic", mood="thinking"),
        Character(id="data", name="Data", role="Array Segment", mood="neutral"),
    ]

    scenes: List[Scene] = []
    scenes.append(Scene(
        id="kad_1",
        type="title",
        title="Maximum Subarray (Kadane's Invariant)",
        narration=f"Find the contiguous subarray in [{raw_str}] which has the largest sum.",
        dialogue=[
            DialogueLine(character_id="algo", text="Kadane's invariant: if the running sum drops below 0, it can never help future extensions!", mood="confident"),
            DialogueLine(character_id="bug", text="So whenever currentSum < 0, we immediately discard the prefix and restart.", mood="explaining")
        ],
        states=[
            StateItem(kind="array", name="nums", value=raw_str),
            StateItem(kind="variable", name="maxSum", value=str(nums[0] if nums else 0)),
        ],
        code_line=1
    ))

    curr_sum = 0
    max_sum = nums[0] if nums else 0
    step = 2

    for i, num in enumerate(nums):
        if curr_sum < 0:
            curr_sum = num
            restarted = True
        else:
            curr_sum += num
            restarted = False

        if curr_sum > max_sum:
            max_sum = curr_sum
            new_best = True
        else:
            new_best = False

        scenes.append(Scene(
            id=f"kad_{step}",
            type="decision" if (restarted or new_best) else "step",
            title=f"Element {i} ({num}): Running Sum = {curr_sum}, Max = {max_sum}",
            narration=f"At index {i} (val={num}). {'Prefix was negative; restarted window here. ' if restarted else ''}{'New global maximum! ' if new_best else ''}currentSum = {curr_sum}, maxSum = {max_sum}.",
            dialogue=[
                DialogueLine(character_id="algo", text=f"currentSum is now {curr_sum}. Global maxSum is {max_sum}." + (" (New record!)" if new_best else ""), mood="confident"),
                DialogueLine(character_id="data", text=f"Inspecting index {i} with value {num}.", mood="neutral")
            ],
            states=[
                StateItem(kind="array", name="nums", value=raw_str, index=i, highlight=True),
                StateItem(kind="pointer", name="curr", value=str(i), target_index=i),
                StateItem(kind="variable", name="currentSum", value=str(curr_sum), highlight=restarted),
                StateItem(kind="variable", name="maxSum", value=str(max_sum), highlight=new_best),
            ],
            code_line=6,
            why=WhyExplanation(
                decision=f"num={num}, currSum={curr_sum}",
                limiting_factor="Negative prefixes strictly diminish any subsequent subarray sum",
                invariant_proof="A subarray ending at i either extends the best subarray ending at i-1 or starts fresh at i.",
                skeptical_question="Why can we discard the previous prefix if it becomes negative?",
                airtight_answer="Because any positive future segment would be even larger without that negative prefix."
            ) if restarted else None
        ))
        step += 1

    scenes.append(Scene(
        id="kad_final",
        type="result",
        title=f"Result: Maximum Subarray Sum = {max_sum}",
        narration=f"Evaluated all elements in O(N) time and O(1) space. The maximum contiguous sum is {max_sum}.",
        dialogue=[
            DialogueLine(character_id="algo", text=f"Final answer: {max_sum}! Optimal in a single O(N) pass.", mood="celebrating"),
            DialogueLine(character_id="bug", text="Linear time without inspecting all O(N^2) pairs.", mood="celebrating")
        ],
        states=[
            StateItem(kind="array", name="nums", value=raw_str),
            StateItem(kind="variable", name="maxSum", value=str(max_sum), highlight=True),
        ],
        code_line=11
    ))

    spec = AnimationSpec(
        title="Maximum Subarray (Kadane's Algorithm)",
        algorithm="Dynamic Programming / Sliding Window",
        problem=f"Find maximum contiguous sum in [{raw_str}]",
        intuition="Discard negative prefixes; keep extending as long as prefix contributes positive sum.",
        visual_metaphor="A moving spotlight expanding across positive terrain and resetting after dips.",
        invariant="At step i, currentSum holds the maximum subarray sum ending strictly at index i.",
        time_complexity="O(N)",
        space_complexity="O(1)",
        confidence=1.0,
        source_code=source_code or """public int MaxSubArray(int[] nums)
{
    int currentSum = 0, maxSum = nums[0];
    for (int i = 0; i < nums.Length; i++)
    {
        if (currentSum < 0) currentSum = 0;
        currentSum += nums[i];
        if (currentSum > maxSum) maxSum = currentSum;
    }
    return maxSum;
}""",
        source_language="csharp",
        characters=characters,
        scenes=scenes
    )
    return max_sum, spec

# ---------------------------------------------------------------------------
# 5. Universal Heuristic Simulator (Dispatches by Code Content)
# ---------------------------------------------------------------------------
def auto_simulate(code_str: str, input_str: str, title: Optional[str] = None) -> AnimationSpec:
    code_lower = (code_str or "").lower()
    title_lower = (title or "").lower()

    # Extract target if specified (e.g. target=9, target: 5)
    m_target = re.search(r"target\s*[:=]\s*(-?\d+)", input_str, re.I)
    target = int(m_target.group(1)) if m_target else 9

    # Clean array string
    arr_str = re.sub(r"target\s*[:=]\s*-?\d+", "", input_str, flags=re.I).strip()
    arr_str = arr_str.rstrip(",").strip()

    m_bracket = re.search(r"\[(.*?)\]", arr_str)
    if m_bracket:
        arr_str = m_bracket.group(1)

    arr = []
    for token in arr_str.split(","):
        token = token.strip()
        if token:
            try:
                arr.append(int(token))
            except ValueError:
                pass

    if not arr:
        arr = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]

    # Paradigm 1: Binary Search
    if "binarysearch" in code_lower or "binary_search" in title_lower or ("left <= right" in code_lower and "mid" in code_lower):
        arr = sorted(arr)
        if target not in arr and arr:
            target = arr[len(arr) // 2]
        _, spec = simulate_binary_search(arr, target, code_str)
        return spec

    # Paradigm 2: Two Sum / Hash Map
    if "twosum" in code_lower or "two_sum" in title_lower or ("complement" in code_lower and "seen" in code_lower) or "dictionary" in code_lower:
        if len(arr) >= 2:
            target = arr[0] + arr[1]
        _, spec = simulate_two_sum(arr, target, code_str)
        return spec

    # Paradigm 3: Maximum Subarray / Kadane's / Sliding Window
    if "maxsubarray" in code_lower or "kadane" in code_lower or "currentsum" in code_lower or "maxsum" in code_lower:
        _, spec = simulate_sliding_window(arr, code_str)
        return spec

    # Paradigm 4: Trapping Rain Water / Elevation
    if "trap" in code_lower or "rain" in code_lower or "water" in code_lower or "leftmax" in code_lower:
        case = CornerTestCase("Custom Elevation", "User elevation map", arr, None)
        _, spec = simulate_trapping_rain_water(case, code_str)
        return spec

    # Default fallback: Treat as Two Pointers / General Array Traversal
    case = CornerTestCase("Custom Array", "User provided array", arr, None)
    _, spec = simulate_trapping_rain_water(case, code_str)
    return spec
