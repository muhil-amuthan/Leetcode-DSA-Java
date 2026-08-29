class Solution {
    public int diagonalSum(int[][] mat) {
        int n=mat.length-1;
        int sum=0;
        for(int i=0;i<=n;i++){
            sum += mat[i][i];
            int m=n-i;
            if(i != m){
                sum += mat[i][m];
            }
        }
        return sum;
    }
}