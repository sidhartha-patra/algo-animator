# Trapping Rain Water — Custom Elevation — Two Pointers

## 🎯 Problem
Elevation map: [0,1,0,2,1,0,1,3,2,1,2,1]

## 💡 Core Intuition
Two pointer invariant bounds the water level using the strictly shorter side.

## 🎨 Visual Metaphor
Mountain ridges and basin filling.

## 🛡️ Mathematical Invariant ("Why is this safe?")
At every step, min(leftMax, rightMax) guarantees the water level for the shorter side.

## ⏱️ Complexity
- **Time Complexity:** O(N)
- **Space Complexity:** O(1)

## 🧑 Characters
- **Algo** (Guide & Teacher)
- **Bug** (Skeptical Interviewer)
- **Data** (Elevation Map)

## 🎬 Generated Scenes: 14 total scenes.
