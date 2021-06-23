# 题目

定义栈的数据结构，请在该类型中实现一个能够得到栈中所含最小元素的min函数（时间复杂度应为O（1））。

注意：保证测试中不会当栈为空的时候，对栈调用pop()或者min()或者top()方法。



## 描述

这是一篇针对初学者的题解。
知识点：栈
难度：一星

------



## 题解

题目抽象：要求实现一个O(1)时间复杂度的返回最小值的栈。正常情况下，栈的push，pop操作都为O(1),
但是返回最小值，需要遍历整个栈，时间复杂度为O(n)，所以这里需要**空间换时间**的思想。

### 方法：双栈法（使用辅助栈）

首先需要一个正常栈normal,用于栈的正常操作，然后需要一个辅助栈minval，专门用于获取最小值，具体操作如下。
![ ](H:\Desktop\新建文件夹\Blog\docs\backend\必会算法\剑指offer\pictures\284295_1587290406796_0EDB8C9599BA026855B6DCCC1D5EDAE5) 

- push操作就如图片上操作。 
- pop操作直接对应弹出就好了。 
- top操作就返回normal的栈顶 
- min操作就返回minval的栈顶 

因此，代码如下：

```java
public class MyStack {
    Stack<Integer> normalStack = new Stack<>(); // 正常栈
    Stack<Integer> minStack = new Stack<>();    // 辅助栈，栈顶能拿到当前最小值


    public void push(int node) {
        normalStack.push(node);
        if(minStack.isEmpty()){         // minStack为空，直接入队，否则栈顶存当前最小
            minStack.push(node);
        }else{
            if(node<=minStack.peek()){
                minStack.push(node);
            }else{
                minStack.push(minStack.peek());
            }
        }
    }

    public void pop() {
        normalStack.pop();
        minStack.pop();
    }

    public int top() {
        return normalStack.peek();
    }

    public int min() {
        return minStack.peek();
    }

}

```

时间复杂度：O(1)
空间复杂度：O(n), 开辟了一个辅助栈。