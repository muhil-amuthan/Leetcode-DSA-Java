class Solution {
    public String reverseStr(String s, int k) {
        char[] arr = s.toCharArray();
        String muhil = "";

        for (int i = 0; i < arr.length; i += 2 * k) {

            int end = Math.min(i + k, arr.length);

            for (int j = end - 1; j >= i; j--) {
                muhil += arr[j];
            }

            for (int j = end; j < Math.min(i + 2 * k, arr.length); j++) {
                muhil += arr[j];
            }
        }

        return muhil;
    }
}