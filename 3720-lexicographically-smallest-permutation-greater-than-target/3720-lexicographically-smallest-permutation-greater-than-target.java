class Solution {
    public String lexGreaterPermutation(String s, String target) {
        int n = s.length();

        int[] cnt = new int[26];

        for (char c : s.toCharArray()) {
            cnt[c - 'a']++;
        }

        // prefix = part that currently matches target
        StringBuilder prefix = new StringBuilder();

        for (int i = 0; i < n; i++) {

            int x = target.charAt(i) - 'a';

            // If target[i] is unavailable,
            // we cannot continue matching.
            if (cnt[x] == 0) {
                break;
            }

            cnt[x]--;
            prefix.append(target.charAt(i));
        }

        // If we stopped before matching the whole target (because the
        // needed character ran out), first try placing a character
        // strictly greater than target[i] right at that same position,
        // using whatever counts are left (nothing was consumed here yet).
        if (prefix.length() < n) {
            int i = prefix.length();
            int x = target.charAt(i) - 'a';

            for (int c = x + 1; c < 26; c++) {
                if (cnt[c] == 0)
                    continue;

                StringBuilder ans = new StringBuilder(prefix);
                ans.append((char) ('a' + c));

                cnt[c]--;

                for (int ch = 0; ch < 26; ch++) {
                    for (int t = 0; t < cnt[ch]; t++) {
                        ans.append((char) ('a' + ch));
                    }
                }

                return ans.toString();
            }
        }

        // Otherwise (or if that attempt failed), backtrack through the
        // matched prefix from right to left.
        for (int i = prefix.length() - 1; i >= 0; i--) {

            // Restore the character at position i.
            cnt[prefix.charAt(i) - 'a']++;

            prefix.deleteCharAt(prefix.length() - 1);

            int x = target.charAt(i) - 'a';

            // Find smallest character > target[i].
            for (int c = x + 1; c < 26; c++) {

                if (cnt[c] == 0)
                    continue;

                StringBuilder ans = new StringBuilder(prefix);
                ans.append((char) ('a' + c));

                cnt[c]--;

                // Fill remaining characters in sorted order.
                for (int ch = 0; ch < 26; ch++) {
                    for (int t = 0; t < cnt[ch]; t++) {
                        ans.append((char) ('a' + ch));
                    }
                }

                return ans.toString();
            }
        }

        return "";
    }
}