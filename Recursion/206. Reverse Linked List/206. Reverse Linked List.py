# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        if curr:
            if curr.next:
                while curr.next:
                    next_element = curr.next
                    curr.next = prev
                    prev = curr
                    curr = next_element
                curr.next=prev
                return curr
        return head