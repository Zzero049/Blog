## 1.双向链表



```java
package LRU;

import java.util.Iterator;
import java.util.LinkedList;

/**
 * LRU: 最近最少使用算法 。 最近最少使用的元素，在接下来一段时间内，被访问的概率也很低。
 * 即最近被使用的元素，在接下来一段时间内，被访问概率较高。
 * <p>
 * 用链表的结构：
 * 链表尾表示最近被访问的元素，越靠近链表头表示越早之前被访问的元素
 * <p>
 * 插入一个元素，cache 不满，插到链表尾，满，移除cache链头元素再插入链表尾
 * 访问一个元素，从链表头部开始遍历, 访问到之后，将其从原位置删除，重新加入链表尾部
 * <p>
 * 实现1：用双向链表实现。
 * put、get 时间复杂度:O(n)       效率低
 * <p>
 * created by Ethan-Walker on 2019/2/16
 */
public class LRUCache {

    LinkedList<Node> cache;

    int capacity;

    public LRUCache(int capacity) {
        this.cache = new LinkedList<>();
        this.capacity = capacity;
    }

    // -1 表示没找到
    public int get(int key) {
        Iterator<Node> iterator = cache.descendingIterator();
        int result = -1;
        while (iterator.hasNext()) {
            Node node = iterator.next();
            if (node.key == key) {
                result = node.val;
                iterator.remove();
                put(key, result); //添加到链表尾部
                break;
            }
        }
        return result;
    }

    public void put(int key, int value) {
        //先遍历查找是否有key 的元素, 有则删除，重新添加到链尾
        Iterator<Node> iterator = cache.iterator();
        while (iterator.hasNext()) {
            Node node = iterator.next();
            if (node.key == key) {
                iterator.remove();
                break;
            }
        }

        if (capacity == cache.size()) {
            //缓存已满，删除一个 最近最少访问的元素（链表头）
            cache.removeFirst();
        }
        cache.add(new Node(key, value));
    }


    class Node {
        int key;
        int val;

        public Node(int key, int val) {
            this.key = key;
            this.val = val;
        }
    }

}
```

## 2. LinkedHashMap



```java
package LRU;

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Set;

/**
 * LinkedHashMap 实现
 * put /get 操作 O(1)
 * 特殊情况：缓存已满，需要删除链表头
 * created by Ethan-Walker on 2019/2/16
 */
public class LRUCache2 {
    LinkedHashMap<Integer, Integer> cache;
    int capacity;

    public LRUCache2(int capacity) {
        cache = new LinkedHashMap<>(capacity);
        this.capacity = capacity;
    }

    public int get(int key) {
        if (!cache.containsKey(key)) return -1;

        int val = cache.get(key);
        cache.remove(key); // 从链表中删除
        cache.put(key, val); // 添加到链尾

        return val;

    }

    public void put(int key, int value) {
        if (cache.containsKey(key)) {
            cache.remove(key); // 已经存在，链表中删除
        }

        if (capacity == cache.size()) {
            // cache 已满,删除链表头
            Set<Integer> keySet = cache.keySet();
            Iterator<Integer> iterator = keySet.iterator();
            cache.remove(iterator.next());
        }
        cache.put(key, value);// 添加到链尾
    }
}
```

借助 LinkedHashMap 已经实现的 删除最近最少使用的元素 方法 `removeEldestEntry`



```java
/**
 * LinkedHashMap 本身内部有一个触发条件则自动执行的方法：删除最老元素（最近最少使用的元素）
 * 由于最近最少使用元素是 LinkedHashMap 内部处理
 * 故我们不再需要维护 最近访问元素放在链尾，get 时直接访问/ put 时直接存储
 * created by Ethan-Walker on 2019/2/16
 */
class LRUCache3 {
    private Map<Integer, Integer> map;
    private final int capacity;

    public LRUCache3(int capacity) {
        this.capacity = capacity;
        map = new LinkedHashMap<Integer, Integer>(capacity, 0.75f, true) {
            @Override
            protected boolean removeEldestEntry(Map.Entry eldest) {
                return size() > capacity;  // 容量大于capacity 时就删除
            }
        };
    }
    public int get(int key) {
        return map.getOrDefault(key, -1);
    }

    public void put(int key, int value) {
        map.put(key, value);
    }
}
```

## 3. 手动实现

- HashMap 中存储每个key 对应的节点Node<key，value>， Node节点之间再通过 prev、next 链接，实现有序的双向链表



```java
package LRU;

import java.util.HashMap;

/**
 * created by Ethan-Walker on 2019/2/16
 */
public class LRUCacheByself {

    // 双向链表节点结构
    private class Node {
        public Node pre;
        public Node next;
        public int key;
        public int val;

        public Node(int k, int v) {
            this.key = k;
            this.val = v;
            this.pre = null;
            this.next = null;
        }
    }

    // 双向链表 头部是最老的
    private class DoublyLinkedList {
        public Node head;
        public Node tail;

        public DoublyLinkedList() {
            this.head = null;
            this.tail = null;
        }

        public void moveToTail(Node n) {
            // 将节点移动至尾部
            if (n == null || n == tail) return;
            if (head == n) {
                head = n.next;
                head.pre = null;
            } else {
                n.pre.next = n.next;
                n.next.pre = n.pre;
            }

            tail.next = n;
            n.pre = tail;
            n.next = null;
            tail = tail.next;
        }

        public void addToTail(Node n) {
            if (n == null) return;
            // 添加新的节点
            if (head == null) {
                head = n;
                tail = n;
            } else {
                tail.next = n;
                n.pre = tail;
                tail = n;
            }
        }

        public Node removeHead() {
            // 删除头部（最老的）节点
            if (head == null) return null;
            Node n = head;
            if (head == tail) {
                head = null;
                tail = null;
            } else {
                head = head.next;
                head.pre = null;
            }
            return n;
        }
    }

    private DoublyLinkedList list;
    private HashMap<Integer, Node> map;
    private int capacity;

    public LRUCacheByself(int capacity) {
        this.list = new DoublyLinkedList();
        this.map = new HashMap<>();
        this.capacity = capacity;
    }

    public int get(int key) {
        if (!map.containsKey(key)) {
            return -1;
        }
        Node n = map.get(key);
        list.moveToTail(n);
        return n.val;
    }

    public void put(int key, int value) {
        if (!map.containsKey(key)) {
            Node n = new Node(key, value);
            map.put(key, n);
            list.addToTail(n);

            if (map.size() > capacity) {
                Node rmv = list.removeHead();
                map.remove(rmv.key);
            }
        } else {
            Node n = map.get(key);
            n.val = value;
            list.moveToTail(n);
        }
    }
}
```

