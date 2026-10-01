class Solution {
    public boolean uniformArray(int[] nums1) {

        int min = nums1[0];
        boolean muhi = false;

        for (int x : nums1) {
            if (x < min) {
                min = x;
            }

            if (x % 2 != 0) {
                muhi = true;
            }
        }

        if (!muhi) {
            return true;
        }

        return min % 2 != 0;
    }
}