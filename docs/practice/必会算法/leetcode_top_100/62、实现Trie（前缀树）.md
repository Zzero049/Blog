# 208、实现Trie（前缀树）

实现一个 Trie (前缀树)，包含 `insert`, `search`, 和 `startsWith` 这三个操作。

示例:

```
Trie trie = new Trie();

trie.insert("apple");
trie.search("apple");   // 返回 true
trie.search("app");     // 返回 false
trie.startsWith("app"); // 返回 true
trie.insert("app");   
trie.search("app");     // 返回 true
```


说明:

- 你可以假设所有的输入都是由小写字母 a-z 构成的。
- 保证所有输入均为非空字符串。



## 题解

首先得知道前缀树是什么

前缀树是一种树数据结构，用于检索字符串数据集中的键。这一高效的数据结构有多种应用：

1. 自动补全

   ![](https://gitee.com/zero049/MyNoteImages/raw/master/sdjasdsad.png)

<center>图 1. 谷歌的搜索建议</center>

2. 拼写检查

![image.png](https://gitee.com/zero049/MyNoteImages/raw/master/4d18efbdd4d51ae3935b42cd59b11d66fb62f1586b9638f9499d2a18fa8919d0-image.png)

<center>图2. 文字处理软件中的拼写检查</center>

3. IP 路由 (最长前缀匹配)

![](https://gitee.com/zero049/MyNoteImages/raw/master/20200912172043.png)

<center>图 3. 使用Trie树的最长前缀匹配算法，Internet 协议（IP）路由中利用转发表选择路径。</center>

4. T9 (九宫格) 打字预测

   ![](https://gitee.com/zero049/MyNoteImages/raw/master/20200912172121.png)

<center>图 4. T9（九宫格输入），在 20 世纪 90 年代常用于手机输入</center>

5. 单词游戏

   ![](https://gitee.com/zero049/MyNoteImages/raw/master/20200912172149.png)

<center>图 5. Trie 树可通过剪枝搜索空间来高效解决 Boggle 单词游戏</center>

还有其他的数据结构，如**平衡树和哈希表，使我们能够在字符串数据集中搜索单词。为什么我们还需要 Trie 树呢？尽管哈希表可以在 O(1)时间内寻找键值，却无法高效的完成以下操作：**

- **找到具有同一前缀的全部键值。**
- **按词典序枚举字符串的数据集。**

Trie 树优于哈希表的另一个理由是，随着哈希表大小增加，会出现大量的冲突，时间复杂度可能增加到 O(n)，其中 n 是插入的键的数量。与哈希表相比，Trie 树在存储多个具有相同前缀的键时可以使用较少的空间。此时 Trie 树只需要 O(m) 的时间复杂度，其中 m 为键长。而在平衡树中查找键值需要  O(mlogn) 时间复杂度。

**Trie 树的结点结构**

Trie 树是一个有根的树，其结点具有以下字段：。

- 最多 R个指向子结点的链接，其中每个链接对应字母表数据集中的一个字母。
- 本文中假定 R 为 26，小写拉丁字母的数量。
- 布尔字段，以指定节点是对应键的结尾还是只是键前缀。

树节点实现：

```java
class TrieNode {
        private TrieNode[] charList;				// 按字符找下一个节点，用一个数组方便找到下一个节点
        private final int R = 26;					// 本题只有小写26个字符
        private boolean endFlag;					// 末尾标志，比如"leet"和"leetcode"入树，如果要判断树中究竟
													// 存了什么字符串，需要这个字符串末尾标志
        public TrieNode() {
            charList = new TrieNode[R];				// 数组、标志初始化
            endFlag = false;
        }

        public TrieNode getNodeByChar(char ch) {		// 拿到对应字符下一个节点
            return charList[ch - 'a'];
        }

        public void setNodeByChar(TrieNode node, char ch) {		// 设置对应字符下一个节点
            charList[ch - 'a'] = node;
        }

        public boolean getEndFlag() {					// 获取标志
            return endFlag;
        }

        public void setEndFlag() {						// 修改标志
            endFlag = true;
        }
    }
```

Trie 树中最常见的两个操作是键的插入和查找。

**向 Trie 树中插入键**

我们通过搜索 Trie 树来插入一个键。我们从根开始搜索它对应于第一个键字符的链接。有两种情况：

- 链接存在。沿着链接移动到树的下一个子层。算法继续搜索下一个键字符。
- 链接不存在。创建一个新的节点，并将它与父节点的链接相连，该链接与当前的键字符相匹配。

重复以上步骤，直到到达键的最后一个字符，然后将当前节点标记为结束节点，算法完成。

![](https://gitee.com/zero049/MyNoteImages/raw/master/20200912174729.png)

<center>图 7. 向 Trie 树中插入键</center>



```java
	public void insert(String word) {
        TrieNode p = root;
        int len = word.length();
        for (int i = 0; i < len; ++i) {
            char ch = word.charAt(i);
            if (p.getNodeByChar(ch) == null) {			// 如果树中不存在这条路径，需要自己弄一条
                p.setNodeByChar(new TrieNode(), ch);
            }
            p = p.getNodeByChar(ch);
        }
        p.setEndFlag();								// 设置字符末尾标志
    }
```

**复杂度分析**

时间复杂度：O(m)，其中 m 为键长。在算法的每次迭代中，我们要么检查要么创建一个节点，直到到达键尾。只需要 m 次操作。

空间复杂度：O(m)。最坏的情况下，新插入的键和 Trie 树中已有的键没有公共前缀。此时需要添加 m 个结点，使用 O(m)空间。



**在 Trie 树中查找字符串**

每个键在 trie 中表示为从根到内部节点或叶的路径。我们用第一个键字符从根开始，不断向下查找。检查当前节点中与键字符对应的链接。有两种情况：

- **返回true：**该路径存在该字符，且该路径对应字符串最后一个字符的节点的末尾标记为true
- **返回false：**有两种情况不满足
  - 该路径不存在该字符，节点返回null
  - 该路径存在该字符，但该路径对应字符串最后一个字符的节点的末尾标记为false，说明没有这样的字符入过树，比如存了"leetcode"，但查的是"leet"，因此不满足

![](https://gitee.com/zero049/MyNoteImages/raw/master/20200912192515.png)

```java
	public boolean search(String word) {
        TrieNode node = searchTrie(word);
        if (node == null) {							// 如果路径没有这样的节点
            return false;
        }
        return node.getEndFlag();					// 有这样的节点还要看结尾标志
    }
	
	public TrieNode searchTrie(String word) {
        TrieNode p = root;
        int len = word.length();
        for (int i = 0; i < len; ++i) {
            char ch = word.charAt(i);
            if (p.getNodeByChar(ch) == null) {		// 没有这样的路径则返回null
                return null;
            }
            p = p.getNodeByChar(ch);
        }
        return p;									// 返回字符串最后那个字符对应的节点
    }
```

**复杂度分析**

时间复杂度 : O(m)。算法的每一步均搜索下一个键字符。最坏的情况下需要 m*m* 次操作。

空间复杂度 : O(1)。



**查找 Trie 树中的键前缀**

该方法与在 Trie 树中搜索键时使用的方法非常相似。我们从根遍历 Trie 树，直到键前缀中没有字符，或者无法用当前的键字符继续 Trie 中的路径。与上面提到的“搜索键”算法唯一的区别是，到达键前缀的末尾时，总是返回 true。我们不需要考虑当前 Trie 节点是否是结尾节点，因为我们搜索的是键的前缀，而不是整个键。

```java
	public boolean startsWith(String prefix) {
        TrieNode node = searchTrie(prefix);
        if (node == null) {						// 如果路径没有这样的节点
            return false;
        }
        return true;							// 找前缀就不用判断结尾了
    }

    public TrieNode searchTrie(String word) {
        TrieNode p = root;
        int len = word.length();
        for (int i = 0; i < len; ++i) {
            char ch = word.charAt(i);
            if (p.getNodeByChar(ch) == null) {
                return null;
            }
            p = p.getNodeByChar(ch);
        }
        return p;
    }
```

**复杂度分析**

时间复杂度 : O(m)。

空间复杂度 : O(1)。



### 完整代码

上面解释的差不多了，此处不做注释

```java
class Trie {
    class TrieNode {
        private TrieNode[] charList;
        private final int R = 26;
        private boolean endFlag;

        public TrieNode() {
            charList = new TrieNode[R];
            endFlag = false;
        }

        public TrieNode getNodeByChar(char ch) {
            return charList[ch - 'a'];
        }

        public void setNodeByChar(TrieNode node, char ch) {
            charList[ch - 'a'] = node;
        }

        public boolean getEndFlag() {
            return endFlag;
        }

        public void setEndFlag() {
            endFlag = true;
        }
    }
    
    private TrieNode root;							// 根节点

    public Trie() {
        root = new TrieNode();
    }
    
    
    public void insert(String word) {
        TrieNode p = root;
        int len = word.length();
        for (int i = 0; i < len; ++i) {
            char ch = word.charAt(i);
            if(p.getNodeByChar(ch)==null){
                p.setNodeByChar(new TrieNode(),ch);
            }
            p = p.getNodeByChar(ch);
        }
        p.setEndFlag();
    }
    

    public boolean search(String word) {
        TrieNode node = searchTrie(word);
        if(node==null){
            return false;
        }
        return node.getEndFlag();
    }
    

    public boolean startsWith(String prefix) {
        TrieNode node = searchTrie(prefix);
        if(node==null){
            return false;
        }
        return true;
    }

    public TrieNode searchTrie(String word){
        TrieNode p = root;
        int len = word.length();
        for (int i = 0; i < len; ++i) {
            char ch = word.charAt(i);
            if(p.getNodeByChar(ch)==null){
                return null;
            }
            p = p.getNodeByChar(ch);
        }
        return p;
    }
}
```

