/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode deleteDuplicates(ListNode head) {

        Set<Integer> set = new LinkedHashSet<>();
        ListNode temp = head;

        while (temp != null ) {
            set.add(temp.val);
            temp = temp.next;
        }

        ListNode muhil = null;
        ListNode abi = null;

        for (int x : set) {
            ListNode node = new ListNode(x);

            if (muhil == null) {
                muhil = node;
                abi = node;}
                
                 else
                 
                 {
                abi.next = node;
                abi = node;
            }
        }

        return muhil;
    }
}