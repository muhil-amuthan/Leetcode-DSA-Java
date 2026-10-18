import java.util.Arrays;

class Solution {
    public int thirdMax(int[] nums) {
        Arrays.sort(nums);

        int cnt = 1;
        int max = nums[nums.length - 1];

        for (int i = nums.length - 2; i >= 0; i--) {
            if (nums[i] != max) {
                cnt++;
                max = nums[i];
            }

            if (cnt == 3) {
                return max;
            }
        }

        return nums[nums.length - 1];
    }
}