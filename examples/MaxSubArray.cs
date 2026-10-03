using System;

public class Solution
{
    public int MaxSubArray(int[] nums)
    {
        int currentSum = 0;
        int maxSum = nums[0];

        for (int i = 0; i < nums.Length; i++)
        {
            if (currentSum < 0)
            {
                currentSum = 0;
            }

            currentSum += nums[i];

            if (currentSum > maxSum)
            {
                maxSum = currentSum;
            }
        }

        return maxSum;
    }
}
