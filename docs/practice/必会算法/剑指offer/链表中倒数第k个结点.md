# 题目

输入一个链表，输出该链表中倒数第k个结点。



# 描述

这是一篇针对初学者的题解。用2种方法解决。
知识点：链表，链表的快慢指针
难度：一星

------

# 题解

## 方法一：普通解法

很显然，求倒数第k个，可以转换成求正数第多少个呢？
看个例子：
![image-20200829004940773](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829004940773.png)
假设有5个节点，序号1表示第1个节点，假设求倒数第K个，那么正数就应该是从头结点开始往后推（n-k）个，n自然代表所有节点的个数（不包含空节点），也可以说n代表指针的个数，为啥这么说呢？因为一个节点后面跟着一个指向下一节点的指针。
这里n=5，所以需要从头结点往后经过n-K = 3个指针。
![图片说明](H:\Desktop\新建文件夹\Blog\docs\backend\必会算法\剑指offer\pictures\284295_1586659791197_9BA2F66B522AB7AE08799525A7D3EE27) 

有了上面的过程，还需要考虑2个细节

1. k<=0 或者头结点最开始就为空，也就是没有节点 
2. 节点的总个数 < K 

### 代码

```java
/**
     * 遍历两遍链表，第一遍查出有多少个节点n，第二遍从向前移动n-k次得到结果
     */
    public Node solution02(Node head, int k){
        if(head==null||k<=0){
            return null;
        }
        Node p = head;
        int count = 0;
        while(p!=null){
            p = p.next;
            count++;
        }
        int step = count-k;
        Node ans=null;
        if(step<0){
            return null;
        }else{
            ans = head;
            while(step>0){
                step--;
                ans = ans.next;
            }
        }
        return ans;
    }
```

时间复杂度：O(2*n),n为链表的总长度，如果k总是在倒数第一个节点，那么此方法需要遍历链表2次
空间复杂度：O(1)

## 方法二：严格的O(n)解法，快慢指针

如下图：
![image-20200829004927820](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829004927820.png) 

我们从图中可以看出，倒数第k个节点与最后的空节点之间有2个指针，此时的2正好就是k，于是我们可以想到可以通过平移来到达最后的状态。
如图：
![image-20200829005045096](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829005045096.png)

![image-20200829005110689](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829005110689.png)

 

如果懂了上面的过程，接下来再说说具体编程要怎么写？
![image-20200829005130212](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829005130212.png)
使用如图的快慢指针，首先让快指针先行k步，然后让快慢指针每次同行一步，直到快指针指向空节点，慢指针就是倒数第K个节点。

## 代码

```java
public Node solution01(Node head, int k) {
        if(head==null||k<=0){
            return null;
        }
        Node p = head;
        while(k>1){
            p = p.next;
            k--;
            if(p==null){
                return null;
            }
        }
        Node ans = head;
        while(p.next!=null){
            p = p.next;
            ans = ans.next;
        }
        return ans;
    }
```

时间复杂度：O(n),不管如何，都只遍历一次单链表
空间复杂度：O(1)