import java.util.HashMap;

class Solution {
    public int sumOfUnique(int[] nums) {
        HashMap<Integer, Integer> muhi = new HashMap<>();

        for (int num : nums) {
            muhi.put(num, muhi.getOrDefault(num, 0) + 1);
        }

        int sum = 0;
        for (int num : muhi.keySet()) {
            if (muhi.get(num) == 1) {
                sum += num;
            }
        }

        return sum;
    }
}