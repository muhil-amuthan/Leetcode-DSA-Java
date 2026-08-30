class Solution {
    public int singleNonDuplicate(int[] nums) {
        HashMap<Integer,Integer> m=new HashMap<>();
        for(int i=0 ; i< nums.length ; i++){
            m.put(nums[i],m.getOrDefault(nums[i],0)+1);
        }
        for(int num:nums){
            if(m.get(num) == 1){
                return num;
            }
        }
        return -1;
        
    }
}