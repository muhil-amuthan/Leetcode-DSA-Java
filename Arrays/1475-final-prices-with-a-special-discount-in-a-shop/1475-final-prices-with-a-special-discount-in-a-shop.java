class Solution {
    public int[] finalPrices(int[] prices) {

        int m=prices.length;

        for(int i=0 ; i<m ; i++){
            for(int j=i+1 ; j<m ; j++){
                if(prices[j] <= prices[i]){
                    prices[i] = prices[i] - prices[j];
                    break;
                }
            }
            
        }
        return prices;
    }
}