class Solution {
    public int singleNumber(int[] nums) {
        for(int i=0;i<nums.length;i++){
            int cnt=0;
            for(int j=0 ; j <nums.length;j++){
                if(nums[i] == nums[j]){
                    cnt++;
                }
            }
            if(cnt == 1){
                return nums[i];
            }
        }
       return 0; 
    }
}