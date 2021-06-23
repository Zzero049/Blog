# 题目

输入一个递增排序的数组和一个数字S，在数组中查找两个数，使得他们的和正好是S，如果有多对数字的和等于S，输出两个数的乘积最小的。

**输出描述:**

```
对应每个测试案例，输出两个数，小的先输出。
```

## 描述

这是一篇针对初学者的题解。共用两种方法解决。
知识点：数组，哈希，双指针
难度：一星

------

## 题解

题目抽象：给定一个数组，返回两个数字和为sun且乘积最小的两个数字。



## 方法：双指针

因为数组是有序的，所以可以用双指针，指向数组的首尾，具体步骤如下：

1. 初始化：指针i指向数组首， 指针j指向数组尾部
2.  如果arr[i] + arr[j] == sum , 说明是可能解
3.  否则如果arr[i] + arr[j] > sum, 说明和太大，所以--j
4. 否则如果arr[i] + arr[j] < sum, 说明和太小，所以++i
5. 由于在数学上，和相同的中间两个数相乘一定大于左右边的数相乘，只需要第一次找到即返回即可

### 代码

```java
import java.util.ArrayList;
public class Solution {
    public ArrayList<Integer> FindNumbersWithSum(int [] array,int sum) {
        ArrayList<Integer> ans = new ArrayList<>();
        if (array.length <= 1) {
            return ans;
        }
        int left = 0;          			 // 左指针
        int right = array.length-1;     // 右指针
        int len = array.length;
        while (left<right) {			// 小了，左增
            if (array[left] + array[right] < sum) {
                ++left;
            } else if (array[left] + array[right] > sum) {	// 大了，右减
                --right;
            } else {
                ans.add(array[left]);
                ans.add(array[right]);
                break;
            }
        }
        return ans;
    }
}
```

时间复杂度：O(n)
空间复杂度：O(1)