<img src="./pictures/Annotation 2020-04-07 151859.png"  div align=center />


```java
class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode end = head;
        for(int i=0;i<n;i++){
            end = end.next;
        }
        ListNode p = head;
        ListNode pre = head;

        while(end!=null){
            pre = p;
            p = p.next;
            end = end.next;
        }

        if(p==head){
            head = head.next;
            return head
        }
        pre.next = p.next;
        return head;
    }
}
```