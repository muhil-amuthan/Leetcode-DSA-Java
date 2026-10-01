class Solution {
    public int lengthOfLastWord(String s) {
        String[] Muhil = s.trim().split(" ");
        String a = Muhil[Muhil.length - 1];
        return a.length();
    }
}