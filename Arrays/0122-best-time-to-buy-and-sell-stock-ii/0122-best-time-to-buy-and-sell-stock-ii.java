class Solution {
    public int maxProfit(int[] prices) {
        int muhil=0;
        for(int i=1;i<prices.length;i++){
            if(prices[i]>prices[i-1]){
                muhil+=prices[i]-prices[i-1];
                continue;
            }

        }
        return muhil;
        
    }
}