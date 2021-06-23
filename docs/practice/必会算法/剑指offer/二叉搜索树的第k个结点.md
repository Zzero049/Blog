# 题目

给定一棵二叉搜索树，请找出其中的第k小的结点。例如， （5，3，7，2，4，6，8）  中，按结点数值大小顺序第三小结点的值为4。

## 描述

这是一篇针对初学者的题解，用递归方法实现。
知识点：树，递归
难度：一星

------

## 题解

本题主要考察中序遍历



### 递归版本

中序遍历找到第k个即可

```java
public class Solution {
    private int index = 0;
    private TreeNode ans= null;
    TreeNode KthNode(TreeNode pRoot, int k)
    {
        inOrder(pRoot,k);
        return ans;
    }
     private void inOrder(TreeNode pRoot, int k){	// 找第k个
        if(pRoot==null){
            return;
        }
        inOrder(pRoot.left,k);
        ++index;
        if(index==k){			// 找到第k个，则停止递归
            ans = pRoot;
            return;
        }
        inOrder(pRoot.right,k);
    }
}
```

时间复杂度:O(n)

空间复杂度: 最差为O(n)，平均O(logn)



### 非递归版本

就是用栈，实现循环的中序遍历

```java
	public TreeNode solution02(TreeNode pRoot, int k){
        if(pRoot == null || k==0){
            return null;
        }
        Stack<TreeNode> stack = new Stack<>();
        TreeNode p = pRoot;					// 记录节点
        int index = 0;
        while(!stack.isEmpty()||p!=null){	// 注意条件，中序可能会退到栈空
            while(p!=null){					// 放左子树
                stack.push(p);
                p = p.left;
            }
            TreeNode node = stack.pop();
            ++index;
            if(index==k){				// 寻找
                return node;
            }
            p = node.right;				// 放右孩子，同上述规则
        }
        return null;
    }
```

