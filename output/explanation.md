# Trapping Rain Water — Two Pointers

## 🎯 Problem
Given n non-negative integers representing an elevation map where width of each bar is 1, compute how much water it can trap after raining.

## 💡 Core Intuition
Water trapped at any bar i is min(leftMax, rightMax) - height[i]. By keeping two pointers and moving whichever side has the smaller max, we know with 100% certainty that the smaller side is the limiting factor.

## 🎨 Visual Metaphor
Two climbers walking inward from opposite mountain ridges, measuring bounding walls and filling trapped pools.

## 🛡️ Mathematical Invariant ("Why is this safe?")
At any step, if leftMax < rightMax, the water level at the left pointer is strictly bounded by leftMax, regardless of unseen heights in between.

## ⏱️ Complexity
- **Time Complexity:** O(N)
- **Space Complexity:** O(1)

## 🧑 Characters
- **Algo** (Guide & Teacher)
- **Bug** (Skeptical Interviewer)
- **Data** (Array Wall)

## 🎬 Generated Scenes: 15 total scenes.
