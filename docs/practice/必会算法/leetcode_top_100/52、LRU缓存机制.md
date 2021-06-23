# 146、LRU缓存机制

运用你所掌握的数据结构，设计和实现一个  **LRU (最近最久未用)** 缓存机制。它应该支持以下操作： 获取数据 `get `和 写入数据 `put` 。

获取数据 `get(key)` - 如果关键字 (key) 存在于缓存中，则获取关键字的值（总是正数），否则返回 -1。

写入数据` put(key, value) `- 如果关键字已经存在，则变更其数据值；如果关键字不存在，则插入该组「关键字/值」。当缓存容量达到上限时，它应该在写入新数据之前删除最久未使用的数据值，从而为新的数据值留出空间。

 **进阶:**

你是否可以在 O(1) 时间复杂度内完成这两种操作？

示例:

```
LRUCache cache = new LRUCache( 2 /* 缓存容量 */ );

cache.put(1, 1);
cache.put(2, 2);
cache.get(1);       // 返回  1
cache.put(3, 3);    // 该操作会使得关键字 2 作废
cache.get(2);       // 返回 -1 (未找到)
cache.put(4, 4);    // 该操作会使得关键字 1 作废
cache.get(1);       // 返回 -1 (未找到)
cache.get(3);       // 返回  3
cache.get(4);       // 返回  4
```



## 题解

实现本题的两种操作，需要用到一个哈希表和一个双向链表。在面试中，面试官一般会期望读者能够自己实现一个简单的双向链表，而不是使用语言自带的、封装好的数据结构。在 Python 语言中，有一种结合了哈希表与双向链表的数据结构 OrderedDict，只需要短短的几行代码就可以完成本题。在 Java 语言中，同样有类似的数据结构 LinkedHashMap。这些做法都不会符合面试官的要求，因此下面只给出使用封装好的数据结构实现的代码，而不多做任何阐述。

```java
class LRUCache extends LinkedHashMap<Integer, Integer>{
    private int capacity;
    
    public LRUCache(int capacity) {
        super(capacity, 0.75F, true);
        this.capacity = capacity;
    }

    public int get(int key) {
        return super.getOrDefault(key, -1);
    }

    public void put(int key, int value) {
        super.put(key, value);
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
        return size() > capacity; 
    }
}
```



### 方法：哈希+双向链表

首先 `put` 和 `get` 的时间复杂度都是O(1)，我们很容易想到用哈希表，能满足上述实现，但是哈希表无法维护最近最久未用的关系，因此我可以想到用一个双向链表去维护按最近使用排序的关系。

- **双向链表按照被使用的顺序存储了这些键值对，靠近头部的键值对是最近使用的，而靠近尾部的键值对是最久未使用的。**

- **哈希表即为普通的哈希映射（HashMap），通过缓存数据的键映射到其在双向链表中的位置。**

这样一来，我们首先使用哈希表进行定位，找出缓存项在双向链表中的位置，对于get和put操作，将其移动到双向链表的头部，即可在 O(1)的时间内完成。具体的方法如下：

**对于 `get` 操作，首先判断 `key` 是否存在：**

- 如果 `key` 不存在，则返回 -1；
- 如果 `key` 存在，则 `key` 对应的节点要更新为最近被使用的节点。通过哈希表定位到该节点在双向链表中的位置，并将其移动到双向链表的头部，最后返回该节点的值。

**对于put操作，首先判断 `key` 是否存在：**

- 如果 `key` 不存在，判断是否超过容量，超过容量则删去尾部节点，并删除哈希表中对应的项，最后使用 `key` 和 `value` 创建一个新的节点，并将 `key` 和该节点添加进哈希表中，头部添加该节点即可。

- 如果 `key` 存在，则与 `get` 操作类似，先通过哈希表定位，再将对应的节点的值更新为 `value`，并将该节点移到双向链表的头部。

上述各项操作中，访问哈希表的时间复杂度为 O(1)，在双向链表的头部添加节点、在双向链表的尾部删除节点的复杂度也为 O(1)。而将一个节点移到双向链表的头部，可以分成「删除该节点」和「在双向链表的头部添加节点」两步操作，都可以在 O(1) 时间内完成。



**小贴士**

在双向链表的实现中，使用一个**伪头部（dummy head）**和**伪尾部（dummy tail）**标记界限，这样在添加节点和删除节点的时候就不需要检查相邻的节点是否存在。

代码如下

```java
class LRUCache {
    private DoubleListNode head;							// 伪头部
    private DoubleListNode tail;							// 伪尾部

    private int capacity;									// cache容量上限
    private int size;										// cache当前含有元素

    private Map<Integer,DoubleListNode> map;				// map

    class DoubleListNode {									// 双向链表类
        DoubleListNode pre;
        DoubleListNode next;
        int key;
        int value;
        
        public DoubleListNode(int key,int value) {
            this.key = key;
            this.value = value;
        }
        
        @Override
        public String toString() {							// 重写toString不是必须的，为了方便调试
            return "(" + key + ", " + value + ")";
        }
    }

    public LRUCache(int capacity) {						// 初始化
        if (capacity <= 0) {							// 异常判断，传入容量不能为0或负数
            try {
                throw new Exception("the input capacity is negative or zero!");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        head = new DoubleListNode(-1, -1);				
        tail = new DoubleListNode(-1, -1);
        head.next = tail;								// 伪头部、伪尾部建立关系
        tail.pre = head;
        this.capacity = capacity;
        size = 0;
        map = new HashMap<>();
    }
    
    public int get(int key) {				
        if(!map.containsKey(key)){						// 先判断key存在不，不存在直接返回-1
            return -1;
        }
        DoubleListNode node = map.get(key);				// 存在则需要把该节点放到链头
        if(node!=head.next){							// 如果该节点就是链头，不用调整
            removeOneNode(node);
            insertToHead(node);
        }
        return node.value;
    }
    
    public void put(int key, int value) {
        if (map.containsKey(key)) {						// 先判断key存在不，存在则修改值并放到链头即可
            DoubleListNode dNode = map.get(key);
            dNode.value = value;						// 改值
            removeOneNode(dNode);						// 删掉
            insertToHead(dNode);						// 放到链头
            return;
        }

        // 不存在，需要新节点入cache
        if (size == capacity) {							// cache容量如果不够，删尾部，删对应map k-v
            DoubleListNode t = tail.pre;
            map.remove(t.key);
            removeOneNode(t);
        }
        DoubleListNode node = new DoubleListNode(key, value);		// 不存在则要新建节点
        map.put(key, node);											// 放入map中
        insertToHead(node);											// 放入头部
    }
    
    private void removeOneNode(DoubleListNode node) {			// 由于伪头部、伪尾部的帮助，不需要判断空
        DoubleListNode pre = node.pre;							// 直接删
        DoubleListNode next = node.next;
        pre.next = next;
        next.pre = pre;
        --size;
    }

    private void insertToHead(DoubleListNode node) {
        DoubleListNode next = head.next;					// 直接插
        head.next = node;
        node.pre = head;
        node.next = next;
        next.pre = node;
        ++size;
    }
}

```

**复杂度分析**

时间复杂度：对于 put 和 get 都是 O(1)。

空间复杂度：O(capacity)，因为哈希表和双向链表最多存储capacity 个元素。

