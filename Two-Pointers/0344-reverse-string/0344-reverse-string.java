class Solution {
    public void reverseString(char[] s) {
        int mm=0;
        int ma=s.length-1;
        
        while(mm<ma){
            char tmp = s[mm];
            s[mm] = s[ma];
            s[ma] = tmp;

            mm++;
            ma--;
        }

        
    }
}