class Solution {
    public boolean validPalindrome(String s) {

        int left = 0;
        int right = s.length() - 1;

        while (left < right) {

            if (s.charAt(left) != s.charAt(right)) {

                StringBuilder str1 = new StringBuilder(s);
                str1.deleteCharAt(left);

                StringBuilder str2 = new StringBuilder(s);
                str2.deleteCharAt(right);

                return str1.toString().equals(str1.reverse().toString())
                    || str2.toString().equals(str2.reverse().toString());
            }

            left++;
            right--;
        }

        return true;
    }
}