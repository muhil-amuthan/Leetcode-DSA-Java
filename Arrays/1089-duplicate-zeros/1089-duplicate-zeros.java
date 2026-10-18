class Solution {
    public void duplicateZeros(int[] arr) {
        int n = arr.length;
        int m[] = new int[n];
        int x = 0;

        for (int i = 0; i < n && x < n; i++) {
            if (arr[i] != 0) {
                m[x] = arr[i];
                x++;
            }
            else {
                m[x] = 0;
                x++;

                if (x < n) {
                    m[x] = 0;
                    x++;
                }
            }
        }

        for (int z = 0; z < n; z++) {
            arr[z] = m[z];
        }
    }
}