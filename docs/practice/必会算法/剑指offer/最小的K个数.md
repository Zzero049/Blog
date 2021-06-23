# 题目

输入n个整数，找出其中最小的K个数。例如输入4,5,1,6,2,7,3,8这8个数字，则最小的4个数字是1,2,3,4。

## 描述

这是一篇针对初学者的题解。共用三种方法解决。
知识点：数组，堆，快排
难度：二星

------

## 题解

题目抽象：求给定数组的topK小问题。

### 方法一：排序

直接排序，然后去前k小数据。

**代码**

```java
	public ArrayList<Integer> solution01(int[] input, int k) {
        ArrayList<Integer> ans = new ArrayList<>();
        if (input.length == 0 || k > input.length) return ans;
        Arrays.sort(input);	 //Arrays.sort并不是单一的排序，而是插入排序，快速排序，归并排序三种排序的组合
        for (int i = 0; i < k; i++) {
            ans.add(input[i]);
        }
        return ans;
    }
```

时间复杂度：O(nlongn)
空间复杂度：O(1)

Arrays.sort的原理

![img](https://gitee.com/zero049/MyNoteImages/raw/master/9175374-e835c2da97f9d4d1.png)

### 方法二：堆排序

建立一个容量为k的大根堆的优先队列。遍历一遍元素，如果队列大小<k,就直接入队，否则，让当前元素与队顶元素相比，如果队顶元素大，则出队，将当前元素入队

**代码**

java中PriorityQueue优先队列可以实现堆，并进行严格排序（比堆的定义更为严格，如果按默认的从小到大的优先队列，入队12543，出队12345）

```java
ArrayList<Integer> ans = new ArrayList<>();
        int len = input.length;
        if (len == 0 || k > len || k == 0) return ans;
        // 建立大顶堆
        PriorityQueue<Integer> bigHeap = new PriorityQueue<>(k, new Comparator<Integer>() {
            @Override
            public int compare(Integer o1, Integer o2) {
                return o2.compareTo(o1);
            }
        });
        for (int num : input) {
            if (bigHeap.size() < k) {
                bigHeap.add(num);
            } else {
                if (num < bigHeap.peek()) {
                    bigHeap.poll();
                    bigHeap.offer(num);
                }
            }
        }

        while (!bigHeap.isEmpty()) {
            ans.add(bigHeap.poll());
        }
        return ans;
```

时间复杂度：O(nlongk), 插入容量为k的大根堆时间复杂度为O(longk), 一共遍历n个元素
空间复杂度：O(k)

### 方法三：快排思想

对数组[l, r]一次快排partition过程可得到，[l, p), p, [p+1, r)三个区间,[l,p)为小于等于p的值
[p+1,r)为大于等于p的值。
然后再判断p，利用二分法

1. 如果[l,p), p，也就是p+1个元素（因为下标从0开始），如果p+1 == k, 找到答案
   2。 如果p+1 < k, 说明答案在[p+1, r)区间内，
   3， 如果p+1 > k , 说明答案在[l, p)内 

**代码**

```java
public class Solution {
    public ArrayList<Integer> GetLeastNumbers_Solution(int [] input, int k) {
        ArrayList<Integer> ans = new ArrayList<>();
        int len = input.length;
        if (len == 0 || k > len || k == 0) return ans;

        int left = 0, right = input.length - 1;
		// <= 因为当left==right时也要判断flag是否满足flag + 1 == k
        while (left <= right) {
            int flag = quickSort(input, left, right);
            // 枢轴刚好落在k个
            if (flag + 1 == k) {
                for (int i = 0; i < k; i++) {
                    ans.add(input[i]);
                }
                break;
                // 包括枢轴在内的以前的元素不足k个，去后面找枢轴下标满足flag + 1 == k
            } else if (flag + 1 < k) {
                left = flag + 1;
            } else {
                // 包括枢轴在内的以前元素比k个多，去前面找到枢轴下标满足flag + 1 == k
                right = flag - 1;
            }
        }
        return ans;
    }
    
    /**
     * quickSort实现一次局部快排
     */
    public int quickSort(int[] input, int left, int right) {
        int pivot = input[right];// 选取右界作为枢轴
        int flag = left;        // flag表示最后的分界点位置
        // flag指向第一个比枢轴大的元素下标
        // 扫描过程中，遇到比枢轴小的元素,与flag交换，并自增，保证flag前都是比枢轴小的元素
        for (int i = left; i < right; i++) {
            if (input[i] < pivot) {
                swap(input, flag++, i);
            }
        }
        swap(input, flag, right);
        return flag;
    }

    public void swap(int[] input, int i, int j) {
        if(i==j) return;
        int temp = input[i];
        input[i] = input[j];
        input[j] = temp;
    }
}
```

时间复杂度：平均时间复杂度为O(n),每次partition的大小为`n + n/2  +n/4 +... = 2n`,最坏时间复杂度为O(n^2), 因为每次partition都只减少一个元素
空间复杂度：O(1)

