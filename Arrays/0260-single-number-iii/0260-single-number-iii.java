class Solution {
    public int[] singleNumber(int[] nums) {
        int[] muhi=new int[2];
        int merce=0;
        for(int i=0 ; i<nums.length ; i++){
            int cnt=0;
            for(int j=0;j<nums.length;j++){
                if(nums[i] == nums[j])
                {
                   cnt++; 
                }
            }
            if(cnt ==1){
                muhi[merce]=nums[i];
                merce++;
            }
        }
        return muhi;
    }
}