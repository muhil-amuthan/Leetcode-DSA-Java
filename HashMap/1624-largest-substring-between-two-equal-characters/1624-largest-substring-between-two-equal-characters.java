class Solution {
    public int maxLengthBetweenEqualCharacters(String s) {
        int muhi=-1;
        
        for(int i=0 ; i<s.length() ; i++){
            for(int j=1+i ; j< s.length() ; j++){
                if(s.charAt(j) == s.charAt(i)){
                    int abi = j-1-i;

                    if(abi > muhi){
                muhi=abi;
            }
                }
            }
            
        }
        return muhi;
    }
}