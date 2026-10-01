class Solution {
    public int[] smallerNumbersThanCurrent(int[] nums) {
        int muhil[] =new int[nums.length];
        for(int i=0;i<nums.length;i++){
            int cnt=0;
            for(int j=0 ; j<nums.length ; j++){
                if(nums[j] < nums[i]){
                    cnt++;
                }
            }
            muhil[i]=cnt;
        }
        return muhil;
    }
}