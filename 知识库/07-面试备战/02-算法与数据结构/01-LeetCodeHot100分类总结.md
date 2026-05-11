---
title: LeetCode Hot100 分类总结
tags: [算法, LeetCode, Hot100, 八股文]
created: 2026-05-11
updated: 2026-05-11
sources: []
---

# LeetCode Hot100 分类总结

> 按类型分类，每类总结核心套路与高频模板。适合面试前快速过一遍思维框架。

---

## 一、数组与链表

### 1.1 两数之和（两遍哈希）

```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>(); // value → index
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[]{map.get(complement), i};
        }
        map.put(nums[i], i);
    }
    throw new IllegalArgumentException("No two sum");
}
```

**套路**：第一遍存值到哈希表，第二遍查 `target - num` 是否存在。

**变种**：三数之和 → 排序后双指针；四数之和 → 双指针+哈希剪枝。

### 1.2 合并两个有序链表

```java
public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(0);
    ListNode cur = dummy;
    while (l1 != null && l2 != null) {
        if (l1.val <= l2.val) {
            cur.next = l1;
            l1 = l1.next;
        } else {
            cur.next = l2;
            l2 = l2.next;
        }
        cur = cur.next;
    }
    cur.next = (l1 != null) ? l1 : l2;
    return dummy.next;
}
```

**套路**：哑节点(dummy)避免空指针判断，每次选更小的节点接入。

### 1.3 移动零（双指针/快慢指针）

```java
public void moveZeroes(int[] nums) {
    int insertPos = 0; // 慢指针：下一个非零元素应放的位置
    for (int num : nums) {
        if (num != 0) {
            nums[insertPos++] = num;
        }
    }
    while (insertPos < nums.length) {
        nums[insertPos++] = 0;
    }
}
```

**套路**：快指针遍历数组，慢指针记录已处理位置。适用于"把满足条件的元素移到前面"类问题。

### 1.4 轮转数组

```java
// 思路：三次翻转 [0,n-k-1] [n-k,n-1] [0,n-1]
public void rotate(int[] nums, int k) {
    k %= nums.length;
    reverse(nums, 0, nums.length - k - 1);
    reverse(nums, nums.length - k, nums.length - 1);
    reverse(nums, 0, nums.length - 1);
}

private void reverse(int[] nums, int l, int r) {
    while (l < r) {
        int tmp = nums[l];
        nums[l++] = nums[r];
        nums[r--] = tmp;
    }
}
```

---

## 二、哈希表

### 2.1 字母异位词分组

```java
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> map = new HashMap<>();
    for (String s : strs) {
        char[] ca = s.toCharArray();
        Arrays.sort(ca);
        String key = String.valueOf(ca); // 排序后相同 → 同组
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(map.values());
}
```

**套路**：用排序/计数作为 key，将同组字符串聚合。

### 2.2 最长连续序列（O(n) — 并查集或哈希+去重）

```java
public int longestConsecutive(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int num : nums) set.add(num);

    int longest = 0;
    for (int num : set) {
        if (!set.contains(num - 1)) { // 只从序列起点开始扩展
            int curNum = num;
            int curLen = 1;
            while (set.contains(curNum + 1)) {
                curNum++;
                curLen++;
            }
            longest = Math.max(longest, curLen);
        }
    }
    return longest;
}
```

**关键**：通过 `!set.contains(num-1)` 保证每个序列只从起点遍历一次，达到 O(n)。

---

## 三、栈与队列

### 3.1 有效的括号

```java
public boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    Map<Character, Character> pairs = Map.of(')', '(', ']', '[', '}', '{');

    for (char c : s.toCharArray()) {
        if (pairs.containsKey(c)) { // 右括号
            if (stack.isEmpty() || stack.pop() != pairs.get(c)) {
                return false;
            }
        } else { // 左括号
            stack.push(c);
        }
    }
    return stack.isEmpty();
}
```

**套路**：左括号入栈，右括号出栈对比。不匹配或栈不空则失败。

### 3.2 最小栈（辅助栈）

```java
class MinStack {
    private Deque<Integer> stack = new ArrayDeque<>();
    private Deque<Integer> minStack = new ArrayDeque<>(); // 同步维护最小值

    public void push(int val) {
        stack.push(val);
        int min = minStack.isEmpty() ? val : Math.min(val, minStack.peek());
        minStack.push(min);
    }

    public void pop() {
        stack.pop();
        minStack.pop();
    }

    public int top() { return stack.peek(); }
    public int getMin() { return minStack.peek(); }
}
```

**空间换时间**：用一个同步辅助栈记录每个位置的最小值，O(1) 获取最小值。

### 3.3 柱状图中最大的矩形（单调栈）

```java
public int largestRectangleArea(int[] heights) {
    Deque<Integer> stack = new ArrayDeque<>();
    int max = 0;
    for (int i = 0; i <= heights.length; i++) {
        int cur = (i == heights.length) ? 0 : heights[i];
        while (!stack.isEmpty() && cur < heights[stack.peek()]) {
            int h = heights[stack.pop()];
            int w = stack.isEmpty() ? i : i - stack.peek() - 1;
            max = Math.max(max, h * w);
        }
        stack.push(i);
    }
    return max;
}
```

**套路**：维护递增高度的单调栈。遇到更低高度时弹出计算以弹出柱为高的最大矩形。

---

## 四、二叉树

### 4.1 二叉树层序遍历（BFS + 队列）

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;

    Queue<TreeNode> queue = new ArrayDeque<>();
    queue.offer(root);

    while (!queue.isEmpty()) {
        int levelSize = queue.size();
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < levelSize; i++) {
            TreeNode node = queue.poll();
            level.add(node.val);
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        result.add(level);
    }
    return result;
}
```

**套路**：记录每层 size，控制每轮循环处理固定数量的节点。

### 4.2 二叉树最大深度

```java
// DFS：后序遍历
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    int left = maxDepth(root.left);
    int right = maxDepth(root.right);
    return Math.max(left, right) + 1;
}
```

### 4.3 翻转二叉树

```java
public TreeNode invertTree(TreeNode root) {
    if (root == null) return null;
    TreeNode tmp = root.left;
    root.left = invertTree(root.right);
    root.right = invertTree(tmp);
    return root;
}
```

**注意**：经典 `invertTree`，LeetCode 验题思路用。

### 4.4 验证二叉搜索树

```java
public boolean isValidBST(TreeNode root) {
    return validate(root, null, null);
}

private boolean validate(TreeNode node, Integer low, Integer high) {
    if (node == null) return true;
    if (low != null && node.val <= low) return false;
    if (high != null && node.val >= high) return false;
    return validate(node.left, low, node.val) && validate(node.right, node.val, high);
}
```

**关键**：BST 的中序遍历是有序序列。也可以中序遍历存数组检查有序性。

### 4.5 二叉树最近公共祖先（LCA）

```java
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || root == p || root == q) return root;
    TreeNode left = lowestCommonAncestor(root.left, p, q);
    TreeNode right = lowestCommonAncestor(root.right, p, q);
    if (left != null && right != null) return root;
    return (left != null) ? left : right;
}
```

**套路**：后序遍历。先处理子树，如果 p/q 分别在左右子树，当前节点就是 LCA。

---

## 五、动态规划

### 5.1 爬楼梯（斐波那契）

```java
public int climbStairs(int n) {
    if (n <= 2) return n;
    int a = 1, b = 2;
    for (int i = 3; i <= n; i++) {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}
```

### 5.2 买卖股票的最佳时机

```java
public int maxProfit(int[] prices) {
    int minPrice = Integer.MAX_VALUE;
    int maxProfit = 0;
    for (int price : prices) {
        minPrice = Math.min(minPrice, price);
        maxProfit = Math.max(maxProfit, price - minPrice);
    }
    return maxProfit;
}
```

**变种（冷冻期/无限次/含手续费）**：用 DP 状态机，参考 `bestTimeToBuyAndSellStockII`。

### 5.3 最长递增子序列（LIS）

```java
public int lengthOfLIS(int[] nums) {
    int[] dp = new int[nums.length];
    Arrays.fill(dp, 1);
    int maxLen = 1;
    for (int i = 1; i < nums.length; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
        maxLen = Math.max(maxLen, dp[i]);
    }
    return maxLen;
}
```

**优化**：二分+patience牌堆法 → O(n log n)。

### 5.4 背包问题

```java
// 0-1 背包：dp[j] = max(dp[j], dp[j-w] + v)
public int knapsack(int W, int[] weights, int[] values) {
    int[] dp = new int[W + 1];
    for (int i = 0; i < weights.length; i++) {
        for (int j = W; j >= weights[i]; j--) { // 倒序避免物品复用
            dp[j] = Math.max(dp[j], dp[j - weights[i]] + values[i]);
        }
    }
    return dp[W];
}
```

**关键**：j 倒序遍历保证每个物品只选一次（0-1 背包）；正序则是完全背包（每种物品无限次）。

### 5.5 打家劫舍

```java
public int rob(int[] nums) {
    if (nums.length == 0) return 0;
    if (nums.length == 1) return nums[0];
    int prev2 = 0, prev1 = nums[0];
    for (int i = 1; i < nums.length; i++) {
        int cur = Math.max(prev1, prev2 + nums[i]);
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}
```

**空间优化**：只需保存前两个状态，从 O(n) 空间降到 O(1)。

---

## 六、图论

### 6.1 岛屿数量（DFS/BFS）

```java
// DFS 沉没陆地
public int numIslands(char[][] grid) {
    int count = 0;
    for (int i = 0; i < grid.length; i++) {
        for (int j = 0; j < grid[0].length; j++) {
            if (grid[i][j] == '1') {
                dfs(grid, i, j);
                count++;
            }
        }
    }
    return count;
}

private void dfs(char[][] grid, int i, int j) {
    if (i < 0 || i >= grid.length || j < 0 || j >= grid[0].length || grid[i][j] == '0') return;
    grid[i][j] = '0'; // 沉没
    dfs(grid, i + 1, j);
    dfs(grid, i - 1, j);
    dfs(grid, i, j + 1);
    dfs(grid, i, j - 1);
}
```

### 6.2 课程表（拓扑排序 — BFS）

```java
public boolean canFinish(int numCourses, int[][] prerequisites) {
    int[] inDegree = new int[numCourses];
    List<Integer>[] graph = new ArrayList[numCourses];

    for (int i = 0; i < numCourses; i++) graph[i] = new ArrayList<>();
    for (int[] p : prerequisites) {
        graph[p[1]].add(p[0]);
        inDegree[p[0]]++;
    }

    Queue<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < numCourses; i++) {
        if (inDegree[i] == 0) q.offer(i);
    }

    int visited = 0;
    while (!q.isEmpty()) {
        int course = q.poll();
        visited++;
        for (int next : graph[course]) {
            if (--inDegree[next] == 0) q.offer(next);
        }
    }
    return visited == numCourses;
}
```

---

## 七、字符串

### 7.1 最长回文子串（中心扩展 + 动态规划）

```java
public String longestPalindrome(String s) {
    if (s.length() <= 1) return s;
    int start = 0, maxLen = 1;

    for (int i = 0; i < s.length(); i++) {
        // 奇数长度中心
        int l = i, r = i;
        while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) {
            if (r - l + 1 > maxLen) {
                start = l;
                maxLen = r - l + 1;
            }
            l--; r++;
        }
        // 偶数长度中心
        l = i; r = i + 1;
        while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) {
            if (r - l + 1 > maxLen) {
                start = l;
                maxLen = r - l + 1;
            }
            l--; r++;
        }
    }
    return s.substring(start, start + maxLen);
}
```

### 7.2 字符串解码

```java
public String decodeString(String s) {
    Deque<Integer> countStack = new ArrayDeque<>();
    Deque<String> strStack = new ArrayDeque<>();
    String cur = "";
    int k = 0;

    for (char c : s.toCharArray()) {
        if (Character.isDigit(c)) {
            k = k * 10 + (c - '0');
        } else if (c == '[') {
            countStack.push(k);
            strStack.push(cur);
            k = 0;
            cur = "";
        } else if (c == ']') {
            int repeat = countStack.pop();
            String prev = strStack.pop();
            StringBuilder sb = new StringBuilder(prev);
            for (int i = 0; i < repeat; i++) sb.append(cur);
            cur = sb.toString();
        } else {
            cur += c;
        }
    }
    return cur;
}
```

---

## 八、滑动窗口

### 8.1 无重复字符的最长子串

```java
public int lengthOfLongestSubstring(String s) {
    Set<Character> set = new HashSet<>();
    int l = 0, maxLen = 0;
    for (int r = 0; r < s.length(); r++) {
        while (set.contains(s.charAt(r))) {
            set.remove(s.charAt(l++));
        }
        set.add(s.charAt(r));
        maxLen = Math.max(maxLen, r - l + 1);
    }
    return maxLen;
}
```

### 8.2 最小覆盖子串

```java
public String minWindow(String s, String t) {
    Map<Character, Integer> need = new HashMap<>();
    Map<Character, Integer> window = new HashMap<>();

    for (char c : t.toCharArray()) need.put(c, need.getOrDefault(c, 0) + 1);

    int l = 0, valid = 0, start = 0, minLen = Integer.MAX_VALUE;
    for (int r = 0; r < s.length(); r++) {
        char c = s.charAt(r);
        if (need.containsKey(c)) {
            window.put(c, window.getOrDefault(c, 0) + 1);
            if (window.get(c).equals(need.get(c))) valid++;
        }

        while (valid == need.size()) { // 收缩左边界
            if (r - l + 1 < minLen) {
                start = l;
                minLen = r - l + 1;
            }
            char leftChar = s.charAt(l++);
            if (need.containsKey(leftChar)) {
                if (window.get(leftChar).equals(need.get(leftChar))) valid--;
                window.put(leftChar, window.get(leftChar) - 1);
            }
        }
    }
    return minLen == Integer.MAX_VALUE ? "" : s.substring(start, start + minLen);
}
```

---

## 九、二分查找

### 9.1 搜索旋转排序数组

```java
public int search(int[] nums, int target) {
    int l = 0, r = nums.length - 1;
    while (l <= r) {
        int mid = l + (r - l) / 2;
        if (nums[mid] == target) return mid;

        // 左半边有序
        if (nums[l] <= nums[mid]) {
            if (nums[l] <= target && target < nums[mid]) {
                r = mid - 1;
            } else {
                l = mid + 1;
            }
        } else { // 右半边有序
            if (nums[mid] < target && target <= nums[r]) {
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }
    }
    return -1;
}
```

---

## 十、记忆化搜索 / 回溯

### 10.1 括号生成

```java
public List<String> generateParenthesis(int n) {
    List<String> result = new ArrayList<>();
    backtrack(result, new StringBuilder(), 0, 0, n);
    return result;
}

private void backtrack(List<String> result, StringBuilder sb, int open, int close, int n) {
    if (sb.length() == n * 2) {
        result.add(sb.toString());
        return;
    }
    if (open < n) {
        sb.append('(');
        backtrack(result, sb, open + 1, close, n);
        sb.deleteCharAt(sb.length() - 1);
    }
    if (close < open) {
        sb.append(')');
        backtrack(result, sb, open, close + 1, n);
        sb.deleteCharAt(sb.length() - 1);
    }
}
```

---

## 面试高频题型分布

| 频率 | 类型 | 代表题 |
|---|---|---|
| 🔴 极高频 | 哈希表 + 双指针 | 两数之和、最长无重复子串 |
| 🔴 极高频 | 动态规划 | 爬楼梯、买卖股票、打家劫舍、背包 |
| 🟠 高频 | 二叉树遍历 | 层序、前序、中序、验证BST、LCA |
| 🟠 高频 | 滑动窗口 | 无重复字符、最小覆盖子串 |
| 🟡 中频 | 单调栈 | 柱状图最大矩形、下一个更大元素 |
| 🟡 中频 | 回溯 | 全排列、括号生成、组合总和 |
| 🟢 低频 | 图论 | 岛屿数量、课程表、克隆图 |
