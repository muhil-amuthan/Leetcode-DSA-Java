class Solution {
    public String reversePrefix(String s, int k) {
        String m="";
        char[] arr = s.toCharArray();
        for(int i=k-1 ; i>=0 ; i--){
            m+=arr[i];
        }
        for(int j=k ; j<s.length() ; j++){
            m+=arr[j];
        }

        return m;
    }
}