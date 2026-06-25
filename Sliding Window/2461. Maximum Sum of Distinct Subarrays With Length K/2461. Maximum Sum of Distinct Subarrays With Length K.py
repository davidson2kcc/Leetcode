class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:

        cnt = {}
        cur = 0
        ans = 0

        for i in range(len(nums)):
            x = nums[i]

            cur += x

            if x in cnt:
                cnt[x] += 1
            else:
                cnt[x] = 1

            if i >= k:
                left = nums[i - k]
                cur -= left

                cnt[left] -= 1

                if cnt[left] == 0:
                    del cnt[left]

            if i >= k - 1 and len(cnt) == k:
                ans = max(ans, cur)

        return ans