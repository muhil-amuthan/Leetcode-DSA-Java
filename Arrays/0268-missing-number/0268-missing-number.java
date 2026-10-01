class Solution {
    public int missingNumber(int[] nums) {
        int n=nums.length;
        int muhil=n*(n+1)/2;
        int Benz=0;
        for(int ab:nums){
          Benz+=ab;
        }
        return muhil-Benz;
    }
}