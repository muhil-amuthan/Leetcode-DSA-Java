class Solution {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        int y = m;

        for (int i = 0; i < n; i++) {
            nums1[y] = nums2[i];
            y++;
        }

        Arrays.sort(nums1);
    }
}
