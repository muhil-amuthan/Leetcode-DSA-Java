class Solution {
    public int strStr(String muhi, String abi) {
        for (int i = 0; i <= muhi.length() - abi.length(); i++) {
                  if (muhi.substring(i, i + abi.length()).equals(abi)) {
                return i;
               }
        }
           return -1;
        
    }
}