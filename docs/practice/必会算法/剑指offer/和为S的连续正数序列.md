# 题目

小明很喜欢数学,有一天他在做数学作业时,要求计算出9~16的和,他马上就写出了正确答案是100。但是他并不满足于此,他在想究竟有多少种连续的正数序列的和为100(至少包括两个数)。没多久,他就得到另一组连续正数和为100的序列:18,19,20,21,22。现在把问题交给你,你能不能也很快的找出所有和为S的连续正数序列? Good Luck!

**输出描述:**

```
输出所有和为S的连续正数序列。序列内按照从小至大的顺序，序列间按照开始数字从小到大的顺序
```

## 描述

这是一篇针对初学者的题解。共用三种方法解决。
知识点：数学，前缀和，滑动窗口
难度：一星

------

## 题解

题目抽象：给定一个`1到sum`的序列，求所有和为`sum`的连续序列。

### 方法一：暴力方法

求和为`sum`的连续子序列，可用暴力方法，
算法步骤：

1. 用指针`i`枚举目标序列的左边界
2. 用指针`j`枚举目标序列的右边界
3. 用指针`k`枚举区间`[i, j]`，来计算区间和，看是否等于目标`sum`。

代码如下：

```java
	public ArrayList<ArrayList<Integer>> solution01(int sum) {
        ArrayList<ArrayList<Integer>> ans = new ArrayList<>();
        // 左边界
        for (int i = 1; i <= sum / 2; ++i) {
            // 右边界
            for (int j = i + 1; j < sum; ++j) {
                int tmp = 0;
                // 求区间和
                for (int k = i; k <= j; ++k) {    // 每次都求区间和
                    tmp += k;
                }
                if (sum == tmp) {
                    ArrayList<Integer> tmpList = new ArrayList<>();
                    for (int k = i; k <= j; ++k) {
                        tmpList.add(k);
                    }
                    ans.add(tmpList);
                } else if (tmp > sum) { // 剪枝，不和情况提前停止
                    break;
                }

            }
        }
        return ans;
    }
```

时间复杂度：O(N^3)
空间复杂度：O(1)

### 方法二：前缀和（待议）

对于求一个区间和，一贯的优化技巧是使用前缀和。比如：
![image-20200829004522952](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829004522952.png)
sum[i]表示前i个数的和。比如`sum[1] = 1`,表示前一个数的和为`1`，`sum[2] = 3`, 表示前`2`个数的和为`3`.现在我们要求区间`[2,4]`表示求第`2,3,4`个数的和，就等于`sum[4] - sum[1] = 9`
代码中我们用一个变量来模拟这个前缀和。
代码如下：（我感觉参考代码没给出前缀和的思想）

```java
	public ArrayList<ArrayList<Integer>> solution02(int sum) {
        ArrayList<ArrayList<Integer>> ans = new ArrayList<>();
        int tmp = 0;
        for (int i=1; i<=sum/2; ++i) {
            for (int j=i; j<sum; ++j) {
                tmp += j;
                if (sum == tmp) {
                    ArrayList<Integer> tmpList = new ArrayList<>();
                    for (int k = i; k <= j; ++k) {
                        tmpList.add(k);
                    }
                    ans.add(tmpList);
                } else if (tmp > sum) {
                    // 提前剪枝
                    tmp = 0;
                    break;
                }
            }
        }
        return ans;
    }
```

时间复杂度：O(N^2)
空间复杂度：O(1)

### 方法三：固定窗口

由于是求连续序列，那么通过递增子序列长度，去找到对应的平均数位置，判断和是否为sum即可，比如100，如果连续子序列长为3，那么则取到32、33、34，和不为100

```java
public ArrayList<ArrayList<Integer>> solution03(int sum) {
    ArrayList<ArrayList<Integer>> ans = new ArrayList<>();

    for (int i = (sum + 1) / 2; i >= 2; --i) {
        int avg = sum / i;			// 取平均数

        int startNum = avg - (i - 1) / 2;		// 取对应窗口下界
        int tmpSum = 0;
        if (startNum > 0) {
            int tmpNum = startNum;
            for (int j = 0; j < i; j++) {		// 求和
                tmpSum += tmpNum;
                tmpNum++;
            }
            if (tmpSum == sum) {
                ArrayList<Integer> tmpList = new ArrayList<>();
                for (int j = 0; j < i; j++) {
                    tmpList.add(startNum++);
                }
                ans.add(tmpList);
            }
        }
    }

    return ans;
}
```

时间复杂度：O(N^2)
空间复杂度：O(1)

### 方法四：滑动窗口

知识补充：

1. 什么是滑动窗口？
   顾名思义，首先是一个窗口，既然是一个窗口，就需要用窗口的左边界`i`和右边界`j`来唯一表示一个窗口，其次，滑动代表，窗口始终从左往右移动，这也表明左边界`i`和右边界`j`始终会往后移动，而不会往左移动。
   这里我用左闭右开区间来表示一个窗口。比如
   ![image-20200829004540914](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829004540914.png)
2. 滑动窗口的操作

- 扩大窗口，`j += 1`
- 缩小窗口，`i += 1`
  算法步骤：

1. 初始化，`i=1,j=1`, 表示窗口大小为`0`
2. 如果窗口中值的和小于目标值sum， 表示需要扩大窗口，`j += 1`
3. 否则，如果狂口值和大于目标值sum，表示需要缩小窗口，`i += 1`
4. 否则，等于目标值，存结果，缩小窗口，继续进行步骤`2,3,4`

这里需要注意2个问题：

1. 什么时候窗口终止呢，这里窗口左边界走到sum的一半即可终止，因为题目要求至少包含2个数
2. 什么时候需要扩大窗口和缩小窗口？解释可看上述算法步骤。

代码如下：

```java
	public ArrayList<ArrayList<Integer>> solution04(int sum) {
        ArrayList<ArrayList<Integer>> ans = new ArrayList<>();
        int left = 1;			// 左界，从这计算
        int right = 1;			// 右界，取不到
        int regionSum = 0;
        while (left <= sum / 2) {
            if (regionSum < sum) {
                regionSum += right;
                ++right;
            } else if (regionSum > sum) {
                regionSum -= left;
                ++left;
            } else {
                ArrayList<Integer> tmpList = new ArrayList<>();
                for (int j = left; j < right; j++) {
                    tmpList.add(j);
                }
                ans.add(tmpList);
                regionSum -= left;		// 注意匹配了，也需要调整窗口，左界向右移动
                ++left;					

            }
        }
        return ans;
    }
```

时间复杂度：O(N)
空间复杂度：O(1)