# HashMap底层原理

本篇文章是阅读源码和网上多数博客总结出来的，如果有哪里不对的话，希望指出，共同进步~

## 前置知识

### hashCode与equal的重写

对象在不重写的情况下使用的是Object的equals方法和hashcode方法，从Object类的源码我们知道，默认的**equals** 判断的是两个对象的**引用指向的是不是同一个对象**；而**hashcode**也是**根据对象地址生成一个整数数值**；

另外我们可以看到Object的hashcode()方法的修饰符为native,表明该方法是否操作系统实现，java调用JNI包的c++代码获取哈希值。


```java
public class Object {
 
	public native int hashCode();
 
    
    public boolean equals(Object obj) {
        return (this == obj);
    }
    
    public String toString() {
        return getClass().getName() + "@" + Integer.toHexString(hashCode());
    }
}
```



#### 为什么需要重写equal和hashCode

假设现在有**很多学生对象**，默认情况下，要**判断多个学生对象是否相等**，需要根据地址判断，若对象地址相等，那么对象的实例数据一定是一样的，但**现在我们规定：当学生的姓名、年龄、性别相等时，认为学生对象是相等的，不一定需要对象地址完全相同**，例如学生A对象所在地址为100，学生A的个人信息为（姓名：A,性别:女，年龄：18，住址：北京软件路999号，体重：48），学生A对象所在地址为388，学生A的个人信息为（姓名：A,性别:女，年龄：18，住址：广州暴富路888号，体重：55），这时候如果不重写Object的equals方法，那么返回的一定是false不相等，这个时候就需要我们根据自己的需求重写hashCode和equals()方法了。

```java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Student {
    private String name;// 姓名
    private String sex;// 性别
    private String age;// 年龄
    private float weight;// 体重
    private String addr;// 地址

//     重写hashcode方法
    @Override
    public int hashCode() {
        int result = name.hashCode();
        result = 17 * result + sex.hashCode();
        result = 17 * result + age.hashCode();
        return result;
    }

    // 重写equals方法
    @Override
    public boolean equals(Object obj) {
        if(!(obj instanceof Student)) {
            // instanceof 已经处理了obj = null的情况
            return false;
        }
        Student stuObj = (Student) obj;
        // 地址相等
        if (this == stuObj) {
            return true;
        }
        // 如果两个对象姓名、年龄、性别相等，我们认为两个对象相等
        if (stuObj.name.equals(this.name) && stuObj.sex.equals(this.sex) && stuObj.age.equals(this.age)) {
            return true;
        } else {
            return false;
        }
    }
}
```

在重写了student的equals方法后，即便两个不同的对象，当姓名、年龄、性别相等时，就认为学生对象是相等的，不一定要求对象地址完全相同

```java
public class HashMapTestDemo {
    public static void main(String[] args) {
        Student student1 = new Student("张三","男","22",50,"深圳市");
        Student student2 = new Student("张三","男","22",70,"广州市");

        System.out.println(student1.equals(student2));	//true

    }
}
```

以上面例子为基础，即student1和student2在重写equals方法后被认为是相等的。

在两个对象equals的情况下进行把他们分别放入HashMap和HashSet中，如果不重写hashCode，我们在往HashMap和HashSet上存的时候，则会出现问题，因为Map和Set是基于hashCode先找到对应数组位置再去存的，如果我们认为他们两个是同一个对象，那么在Set和Map里应该只存一份

```java
public class HashMapTestDemo {
    public static void main(String[] args) {
        Student student1 = new Student("张三", "男", "22", 50, "深圳市");
        Student student2 = new Student("张三", "男", "22", 70, "广州市");

        System.out.println(student1.hashCode());        //1956725890
        System.out.println(student2.hashCode());        //356573597

        Map<Student,String> map = new HashMap<>();
        map.put(student1,"zs");
        map.put(student2,"zs");
        System.out.println(map.size());     //2
    }
}
```

![image-20200521163437369](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200521163437369.png)



#### 不重写hashCode，只重写equals会出现的问题

就像上面说的，当我们的需求认为两个对象是一样的时候，存入HashSet或者HashMap里，是根据hashCode计算出一个数组位置（hash&(entry.len-1)），再进行存储，那么如果两个对象hashCode不一样，多数情况计算出来的位置是不一样的，那么就出现问题了

![image-20200521172251159](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200521172251159.png)

![image-20200521163559176](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200521163559176.png)

#### 只重写hashCode，不重写equals会出现的问题

当我们的需求认为两个对象是一样的时候，存入HashSet或者HashMap里，是根据hashCode计算出一个数组位置（hash&(entry.len-1)），再进行存储，那么如果两个对象hashCode一样，但是没有重写equals，那么在我们用equals比对的过程中，必然不相等，也会出现问题

![image-20200521172304233](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200521172304233.png)

内部的Node数组基于调试是很难看到的，我们通过用反射机制去取

```java
/**
     * 打印hashMap内部结构
     *
     * @param map map
     * @param <K> 泛型key
     * @param <V> 泛型value
     * @throws Exception
     */
    public static <K, V> void printHashMapStructures(HashMap<K, V> map) throws Exception {
        Class<?> hashMap = Class.forName("java.util.HashMap");
        Class<?> node = Class.forName("java.util.HashMap$Node");
        Field[] fields = hashMap.getDeclaredFields();
        K[] tableArr = null;
        AccessibleObject.setAccessible(fields, true);
        //获取table
        for (Field field : fields) {
            if ("table".equals(field.getName())) {
                tableArr = ((K[]) field.get(map));
            }
        }
        int i = 0;
        //遍历数组
        for (K o : tableArr) {
            System.out.println("index=" + i++);
            if (o != null) {
                //打印node
                printHashMapNode(node, o);
                Field fieldNode = node.getDeclaredField("next");
                fieldNode.setAccessible(true);
                while ((o = (K) fieldNode.get(o)) != null) {
                    System.out.print("--");
                    printHashMapNode(node, o);
                }
            }
        }
    }

    /**
     * 打印hashMap内部Node
     *
     * @param node
     * @param o
     * @throws Exception
     */
    public static void printHashMapNode(Class node, Object o) throws Exception {
        Field hash1 = node.getDeclaredField("hash");
        Field key1 = node.getDeclaredField("key");
        Field value1 = node.getDeclaredField("value");
        hash1.setAccessible(true);
        key1.setAccessible(true);
        value1.setAccessible(true);
        System.out.println("-->hash=" + hash1.get(o) + ";key=" + key1.get(o) + ";value=" + value1.get(o));
    }
```

![image-20200521164716115](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200521164716115.png)

看到确实有两个对象，在数组中位置一样，形成了一条长度为2的链



## JDK1.7实现

类定义

```javascript
public class HashMap<K,V>extends AbstractMap<K,V>
        implements Map<K,V>, Cloneable, Serializable
```

![image-20200521172424538](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200521172424538.png)

我们都知道，HashMap是基于数组+链表的拉链法实现的。由于哈希碰撞总是无法完全避免的，因此为了解决这一问题，HashMap 用到了 `拉链法`。`拉链法` 的实现比较简单，将链表和数组相结合。数组中的元素称为桶，桶中装的是链表。若遇到哈希冲突，则将冲突的值加到链表中即可。具体到源码进行分析。

### 成员变量

```java
/** 初始容量，默认16 */
    static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; //  aka 16

    /** 最大初始容量，2^30 */
    static final int MAXIMUM_CAPACITY = 1 << 30;

    /** 默认装填因子，默认0.75，根据泊松分布，0.75时hash冲突机率低 */
    static final float DEFAULT_LOAD_FACTOR = 0.75f;

    /** 初始化一个Entry的空数组 */
    static final Entry<?,?>[] EMPTY_TABLE = {};

    /** 将初始化好的空数组赋值给table，table数组是HashMap实际存储数据的地方，并不在EMPTY_TABLE数组中 */
    transient Entry<K,V>[] table = (Entry<K,V>[]) EMPTY_TABLE;

    /** HashMap实际存储的元素个数 */
    transient int size;

    /** 临界值（HashMap 实际能存储的大小）,公式为(threshold = capacity * loadFactor) */
    int threshold;

    /** 装填因子 */
    final float loadFactor;

    /** HashMap的结构被修改的次数，用于迭代器 */
    transient int modCount;
	
	//hash种子默认为0，通常不生成，也设置当数组容量Capacity >= 环境变量jdk.map.althashing.threshole时生成，使哈希算法更加散列
	transient int hashSeed = 0;  
```



### 存储结构Entry

HashMap的内部存储结构其实是数组和链表的结合。当实例化一个HashMap时，系统会创建一个长度为Capacity的Entry数组，这个长度被称为容量(Capacity)，在这个数组中可以存放元素的位置我们称之为“桶”(bucket)，每个bucket都有自己的索引，系统可以根据索引快速的查找bucket中的元素。 **每个bucket中存储一个元素，即一个Entry对象，而每一个Entry对象可以带一个引用变量，用于指向下一个元素**，因此，在一个桶中，就有可能生成一个Entry链。 Entry是HashMap的基本组成单元，每一个Entry包含一个key-value键值对。 Entry是HashMap中的一个静态内部类。代码如下：


```java
static class Entry<K,V> implements Map.Entry<K,V> {
        final K key;
        V value;
        Entry<K,V> next;//存储指向下一个Entry的引用，单链表结构
        int hash;//对key的hashcode值进行hash运算后得到的值，存储在Entry，避免重复计算

        /**
         * 构造函数，头插法，让next指向原本的n
         */
        Entry(int h, K k, V v, Entry<K,V> n) {
            value = v;
            next = n;
            key = k;
            hash = h;
        }
}
```

一个Entry实例的图示：

![image-20200521200917111](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200521200917111.png)

上面我们提到过Entry类里面有一个next属性，作用是指向下一个Entry。打个比方， 第一个键值对A进来，通过计算其key的hash得到的index=0，记做:Entry[0] = A。一会后又进来一个键值对B，通过计算其index也等于0，现在怎么办？HashMap会这样做:B.next = A,Entry[0] = B，即**头插法**，主要考虑到发生冲突时的时间局部性原理，头插法最差情况才和尾插法一样，遍历完无冲突插入。（比如一个循环每次put 3个元素，有1条是要发生覆盖，那么头插法显然会比尾插法高效的多）

### 构造方法

HashMap有4个构造器，其他构造器如果用户没有传入initialCapacity 和loadFactor这两个参数，会使用默认值。initialCapacity默认为16，loadFactory默认为0.75。

table的初始化真正在put里，这可以理解成HashMap的懒加载机制，只有用户在Put一个值的时候说明HashMap才真正被使用，也只有在这个时候才需要初始化数组。

```java
// 这个构造方法指定了容量和加载因子，内部实现基本就是参数检查和赋值。    
public HashMap(int initialCapacity, float loadFactor) {
        if (initialCapacity < 0)
            throw new IllegalArgumentException("Illegal initial capacity: " +
                                               initialCapacity);
        if (initialCapacity > MAXIMUM_CAPACITY)
            initialCapacity = MAXIMUM_CAPACITY;
        if (loadFactor <= 0 || Float.isNaN(loadFactor))
            throw new IllegalArgumentException("Illegal load factor: " +
                                               loadFactor);

        this.loadFactor = loadFactor;		//设置装填因子
        threshold = initialCapacity;		//设置阈值
        init();								//HashMap没用上，为空
    }
// 调用了第一种的构造方法，传入指定的容量和默认加载因子。
public HashMap(int initialCapacity) {
        this(initialCapacity, DEFAULT_LOAD_FACTOR);
    }

// 调用了第一种的构造方法，传入默认容量 16 和默认加载因子 0.75。
public HashMap() {
        this(DEFAULT_INITIAL_CAPACITY, DEFAULT_LOAD_FACTOR);
    }

/**
* 构造一个映射关系与指定 Map 相同的新 HashMap。
* 这里先调用 HashMap(int initialCapacity, float loadFactor) 方法指定合适的容量，
* 而后再调用 inflateTable 方法把容量变为 2 次幂，并创建桶数组实例，
* 最后遍历参数中的 map，在新 HashMap 中写入元素。
*/
public HashMap(Map<? extends K, ? extends V> m) {
        this(Math.max((int) (m.size() / DEFAULT_LOAD_FACTOR) + 1,
                DEFAULT_INITIAL_CAPACITY), DEFAULT_LOAD_FACTOR);
    	inflateTable(threshold);
        putAllForCreate(m);
    }


	private void inflateTable(int toSize) {	//threshold
        // capacity设置为2的倍数
        // 17 -> 32
        int capacity = roundUpToPowerOf2(toSize);		//ConcurrentHashMap是通过循环加1实现的	
        //调用Integer.highestOneBit()
        
		//新的阈值就是 装填因子*容量 和 最大容量 + 1的较小值
        threshold = (int) Math.min(capacity * loadFactor, MAXIMUM_CAPACITY + 1);
        // 分配空间
        table = new Entry[capacity];
        //选择合适的Hash因子
        initHashSeedAsNeeded(capacity);
    }
	//分配容量大小调整为2次幂
	private static int roundUpToPowerOf2(int number) {
        // assert number >= 0 : "number must be non-negative";
        return number >= MAXIMUM_CAPACITY
                ? MAXIMUM_CAPACITY
                : (number > 1) ? Integer.highestOneBit((number - 1) << 1) : 1;
    }

```

1+2+4+8+16，刚好正整数的范围2的31次方。确保把正整数i 最高位之后所有位都能变成1，所以要这么多次

![image-20200521211938348](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200521211938348.png)



### hash重新计算与映射位置

```java
	final int hash(Object k) {
        int h = 0;
        if (useAltHashing) {
            if (k instanceof String) {	//如果是String实例
                return sun.misc.Hashing.stringHash32((String) k);
            }
            h = hashSeed;
        }

        h ^= k.hashCode();

        //一种算法，进行4次位移，让高位也能参与运算，而不只是低位参与映射，得到相对比较分散的哈希值
        h ^= (h >>> 20) ^ (h >>> 12);
        return h ^ (h >>> 7) ^ (h >>> 4);
    }

    /**
     * 获取hash对应数组的下标
     */
    static int indexFor(int h, int length) {
        return h & (length-1);
    }
```



### put方法（头插法）

put方法主要是判断，**是否存在冲突**，**存在则覆盖，返回被覆盖的值**，不存在，则进行调用addEntry，创建Entry，返回null

```java
public V put(K key, V value) {	
        //如果table数组为空数组{}，进行数组填充（为table分配实际内存空间），入参为threshold，此时threshold为initialCapacity 默认是1<<4=16
        if (table == EMPTY_TABLE) {
            inflateTable(threshold);//分配数组空间
        }
       //判断key为null，存储位置为table[0]或table[0]的冲突链上
        if (key == null)
            return putForNullKey(value);
    
    	//对key的hashcode进一步计算，确保散列均匀
        int hash = hash(key);
    
    	//获取在table中的实际位置
        int i = indexFor(hash, table.length);
    
        for (Entry<K,V> e = table[i]; e != null; e = e.next) {	//index位置上面的链的遍历
        //如果该对应数据已存在，执行覆盖操作。用新value替换旧value，并返回旧value
            Object k;
            if (e.hash == hash && ((k = e.key) == key || key.equals(k))) {
                V oldValue = e.value;
                e.value = value;
                e.recordAccess(this);//LinkedHashMap才有具体作用
                return oldValue;
            }
        }
    
    	//遍历链表后没有冲突，执行下面的方法
        modCount++;//保证并发访问时，若HashMap内部结构发生变化，快速响应失败
        addEntry(hash, key, value, i);//新增一个entry
        return null;
    }

```



addEntry和createEntry方法

```java
//新增一个entry
void addEntry(int hash, K key, V value, int bucketIndex) {
    //当size超过临界阈值threshold，并且即将发生哈希冲突时进行扩容
        if ((size >= threshold) && (null != table[bucketIndex])) {
            //新容量为旧容量的2倍
            resize(2 * table.length);
            
            hash = (null != key) ? hash(key) : 0;
            bucketIndex = indexFor(hash, table.length);//扩容后重新计算插入的位置下标
        }

        //把元素放入HashMap的桶的对应位置
        createEntry(hash, key, value, bucketIndex);
    }

//创建元素  
void createEntry(int hash, K key, V value, int bucketIndex) {  
        Entry<K,V> e = table[bucketIndex];  //获取待插入位置元素
        table[bucketIndex] = new Entry<>(hash, key, value, e);//这里执行链接操作，使得新插入的元素指向原有元素。
//这保证了新插入的元素总是在链表的头  
        size++;//元素个数+1  
    }  
```



### 扩容机制

我们可以看到addEntry方法中，当size超过临界阈值threshold，并且即将发生哈希冲突时进行扩容，新容量为旧容量的2倍

```java
 //按新的容量扩容Hash表  
    void resize(int newCapacity) {  
        Entry[] oldTable = table;//老的数据  
        int oldCapacity = oldTable.length;//获取老的容量值  
        if (oldCapacity == MAXIMUM_CAPACITY) {//老的容量值已经到了最大容量值  
            threshold = Integer.MAX_VALUE;//修改扩容阀值  
            return;  
        }  
        //新的table
        Entry[] newTable = new Entry[newCapacity];  
        //将老的表中的数据转移到新的table
        transfer(newTable, initHashSeedAsNeeded(newCapacity));中  
        table = newTable;//修改HashMap的底层数组  
        threshold = (int)Math.min(newCapacity * loadFactor, MAXIMUM_CAPACITY + 1);//修改阈值
    }  
```

如果数组进行扩容，数组长度发生变化，而存储位置 index = h&(length-1),index也可能会发生变化，需要重新计算index，我们先来看看transfer这个方法：

```java
//将老的表中的数据拷贝到新的结构中  
    void transfer(Entry[] newTable, boolean rehash) {  
        int newCapacity = newTable.length;//容量  
        for (Entry<K,V> e : table) { //遍历所有桶
            while(null != e) {  //遍历桶中所有元素（是一个链表）
                Entry<K,V> next = e.next;  
                if (rehash) {//如果是重新Hash，则需要重新计算hash值  
                    e.hash = null == e.key ? 0 : hash(e.key);  
                }  
                int i = indexFor(e.hash, newCapacity);//定位Hash桶  
                e.next = newTable[i];//元素连接到桶中,这里相当于单链表的插入，总是插入在最前面
                newTable[i] = e;//newTable[i]的值总是最新插入的值
                e = next;//继续下一个元素  
            }  
        }  
    }  
```

上面代码可能不太形象，resize和transfer执行效果如图

![image-20200521225008067](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200521225008067.png)

### transfer多线程下可能的循环链

假设有两个线程，线程1和线程2，同时并发地进行put并发生扩容，

```java
//将老的表中的数据拷贝到新的结构中  
    void transfer(Entry[] newTable, boolean rehash) {  
        int newCapacity = newTable.length;//容量  
        for (Entry<K,V> e : table) { //遍历所有桶
            while(null != e) {  //遍历桶中所有元素（是一个链表）
                Entry<K,V> next = e.next;  
                if (rehash) {//如果是重新Hash，则需要重新计算hash值  
                    e.hash = null == e.key ? 0 : hash(e.key);  
                }  
                int i = indexFor(e.hash, newCapacity);//定位Hash桶  
                e.next = newTable[i];//元素连接到桶中,这里相当于单链表的插入，总是插入在最前面
                newTable[i] = e;//newTable[i]的值总是最新插入的值
                e = next;//继续下一个元素  
            }  
        }  
    }  
```

![image-20200521234332771](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200521234332771.png)

第一趟循环（线程2在Entry<K,V> next = e.next; 卡住），在执行的语句顺序如下图，直接看会有点不清晰，根据结果图去看

![image-20200522001802887](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200522001802887.png)

第一趟循环结果

![image-20200522000806548](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200522000806548.png)

第二趟循环，在执行的语句顺序如下图

![image-20200522001556500](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200522001556500.png)

![image-20200522002208121](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200522002208121.png)

第三次循环，这一次最终e2指向null循环结束，并产生了循环链

![image-20200522002831197](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200522002831197.png)

![image-20200523110455293](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523110455293.png)

可以看到，实际就是因为线程1改变了指向，导致线程2 transfer最后循环过程中出现了一个循环链，下一次执行get或put出现死循环

### get方法

```java
    //获取key值为key的元素值  
    public V get(Object key) {  
        if (key == null)//如果Key值为空，则获取对应的值，这里也可以看到，HashMap允许null的key，其内部针对null的key有特殊的逻辑  
            return getForNullKey();  
        Entry<K,V> entry = getEntry(key);//获取实体  

        return null == entry ? null : entry.getValue();//判断是否为空，不为空，则获取对应的值  
    }  

    //获取key为null的实体  
    private V getForNullKey() {  
        if (size == 0) {//如果元素个数为0，则直接返回null  
            return null;  
        }  
        //key为null的元素存储在table的第0个位置  
        for (Entry<K,V> e = table[0]; e != null; e = e.next) {  
            if (e.key == null)//判断是否为null  
                return e.value;//返回其值  
        }  
        return null;  
    }  
```

get方法通过key值返回对应value，如果key为null，直接去table[0]处检索。我们再看一下getEntry这个方法：

```java
//获取键值为key的元素  
    final Entry<K,V> getEntry(Object key) {  
        if (size == 0) {//元素个数为0  
            return null;//直接返回null  
        }  

        int hash = (key == null) ? 0 : hash(key);//获取key的Hash值  
        for (Entry<K,V> e = table[indexFor(hash, table.length)];//根据key和表的长度，定位到Hash桶  
             e != null;  
             e = e.next) {//进行遍历  
            Object k;  
            if (e.hash == hash &&  
                ((k = e.key) == key || (key != null && key.equals(k))))//判断Hash值和对应的key，合适则返回值  
                return e;  
        }  
        return null;  
    }  

```



## JDK 1.8 实现

绝大多数是和JDK1.7一样的，主要区别在于红黑树部分

### 成员变量

成员变量基本没没太大变化，只是多了一些关于树化或者链表化的阈值，但是**table不再指向一个空的数组**

```java
public class HashMap<K,V> extends AbstractMap<K,V>
    implements Map<K,V>, Cloneable, Serializable {
    //序列号，序列化的时候使用。
    private static final long serialVersionUID = 362498820763181265L;
    /**默认容量，1向左移位4个，00000001变成00010000，也就是2的4次方为16，使用移位是因为移位是计算机基础运算，效率比加减乘除快。**/
    static final int DEFAULT_INITIAL_CAPACITY = 1 << 4;
    //最大容量，2的30次方。
    static final int MAXIMUM_CAPACITY = 1 << 30;
    //加载因子，用于扩容使用。
    static final float DEFAULT_LOAD_FACTOR = 0.75f;
    //当某个桶节点数量大于8时，会转换为红黑树。
    static final int TREEIFY_THRESHOLD = 8;
    //当某个桶节点数量小于6时，会转换为链表，前提是它当前是红黑树结构。
    static final int UNTREEIFY_THRESHOLD = 6;
    //当整个hashMap中元素数量大于64时，也会进行转为红黑树结构。
    static final int MIN_TREEIFY_CAPACITY = 64;
    //存储元素的数组，transient关键字表示该属性不能被序列化
    transient Node<K,V>[] table;
    //将数据转换成set的另一种存储形式，这个变量主要用于迭代功能。
    transient Set<Map.Entry<K,V>> entrySet;
    //元素数量
    transient int size;
    //统计该map修改的次数
    transient int modCount;
    //临界值，也就是元素数量达到临界值时，进行扩容，resize初始化后是容量*加载因子。
    int threshold;
    //也是加载因子，只不过这个是变量。
    final float loadFactor;  
```

### 存储结构Node与TreeNode

先直观认识Node和TreeNode的结构，TreeNode底下还声明了一系列方法，先不作探讨，先认识这两个内部类

```java
static class Node<K,V> implements Map.Entry<K,V> { 	//Entry换了个名字而已
        final int hash;
        final K key;
        V value;
        Node<K,V> next;

        Node(int hash, K key, V value, Node<K,V> next) {
            this.hash = hash;
            this.key = key;
            this.value = value;
            this.next = next;
        }

        //Node内部类的getValue，equals方法省略
    }

//TreeNode是LinkedHashMap.Entry的子类，而LinkedHashMap.Entry是HashMap.Node的子类
//就是说Node拥有的属性和方法，TreeNode都有，只是多了很多红黑树操作需要用的指针
static final class TreeNode<K,V> extends LinkedHashMap.Entry<K,V> {
        TreeNode<K,V> parent;  // 父节点指针
        TreeNode<K,V> left;		//左孩子
        TreeNode<K,V> right;	//右孩子
        TreeNode<K,V> prev;    // 前一个元素指针，双向链表辅助作用
        boolean red;			//是否是红色
        TreeNode(int hash, K key, V val, Node<K,V> next) {
            super(hash, key, val, next);
        }

        
}
```

![image-20200523105241755](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523105241755.png)

### 构造方法

还是4个构造方法，大致都和JDK1.7相同，除了传入Map会立刻进行resise()，其他三个构造函数都是懒加载，只有put的时候才真正的去修改阈值和创建数组

```java
public HashMap() {
        this.loadFactor = DEFAULT_LOAD_FACTOR; //取默认的装填因子，比1.7节省了再调用HashMap(int initialCapacity, float loadFactor)的步骤
    }
 
//使用默认的装填因子0.75，调用下面的构造
public HashMap(int initialCapacity) {
        this(initialCapacity, DEFAULT_LOAD_FACTOR);
    }
 
 
public HashMap(int initialCapacity, float loadFactor) {
        if (initialCapacity < 0)
            throw new IllegalArgumentException("Illegal initial capacity: " +
                                               initialCapacity);
        if (initialCapacity > MAXIMUM_CAPACITY)
            initialCapacity = MAXIMUM_CAPACITY;
        if (loadFactor <= 0 || Float.isNaN(loadFactor))
            throw new IllegalArgumentException("Illegal load factor: " +
                                               loadFactor);
        this.loadFactor = loadFactor;						//初始化装填因子
        this.threshold = tableSizeFor(initialCapacity);		//原本的inflateTable改名为tableSizeFor，返回结果是得到比initialCapacity大的最小2次幂，并不是容量*装填因子
    }
	

	//不同
public HashMap(Map<? extends K, ? extends V> m) {
        this.loadFactor = DEFAULT_LOAD_FACTOR;
        putMapEntries(m, false);
    }
 
    final void putMapEntries(Map<? extends K, ? extends V> m, boolean evict) {
        //获取该map的实际长度
        int s = m.size();
        if (s > 0) {
            //判断table是否初始化，如果没有初始化
            if (table == null) { // pre-size
                /**求出需要的容量，因为实际使用的长度=容量*0.75得来的，+1是因为小数相除，基本都不会是
                * 整数，容量大小不能为小数的，后面转换为int，多余的小数就要被丢掉，所以+1，
                * 例如，map实际长度22，22/0.75=29.3,所需要的容量肯定为30，
                * 有人会问如果刚刚好除得整数呢，除得整数的话，容量大小多1也没什么影响**/
                float ft = ((float)s / loadFactor) + 1.0F;
                //判断该容量大小是否超出上限。
                int t = ((ft < (float)MAXIMUM_CAPACITY) ?
                         (int)ft : MAXIMUM_CAPACITY);
                /**
                * 对临界值进行初始化，tableSizeFor(t)这个方法会返回大于t值的，且离其最近的2次幂，
                * 例如t为29，则返回的值是32
                **/
                if (t > threshold)
                    threshold = tableSizeFor(t);
            }
            else if (s > threshold)
                //如果table已经初始化，且要加入的map超过容量则进行扩容操作，resize()就是扩容。
                resize();
            //遍历，把map中的数据转到hashMap中。
            for (Map.Entry<? extends K, ? extends V> e : m.entrySet()) {
                K key = e.getKey();
                V value = e.getValue();
                putVal(hash(key), key, value, false, evict);
            }
        }
    }


//找到大于或等于 cap 的最小2的幂，不再是依赖Integer.highestOneBit去计算比其小的最大2次幂再左移一位
// 17 -> 32
	static final int tableSizeFor(int cap) {	
        int n = cap - 1;			// -1，防止cap本来就是2次幂，返回结果却翻倍
        n |= n >>> 1;
        n |= n >>> 2;
        n |= n >>> 4;
        n |= n >>> 8;
        n |= n >>> 16;
        return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1;
    }
```

JDK1.7是依赖Integer.highestOneBit去计算比其小的最大2次幂再左移一位，JDK1.8自己设计了一个直接找到比cap大的最小二次幂数方法tableSizeFor，原理和Integer.highestOneBit是一样的

![image-20200523111335450](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523111335450.png)

### hash重新计算与映射位置

JDK1.7是用了4次位移和，让高位也能参与运算，而不只是低位参与映射，得到相对比较分散的哈希值。

而JDK1.8则只是让hashCode高位16位不变，低16位为高16位与低16位异或的结果，得到相对比较分散的哈希值。

```java
static final int hash(Object key) {
        int h;
        return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);	//高16位与低16位异或
    }
```

### put方法（尾插法）

put方法判断点比较多，一是是否需要扩容，二是需要遍历的节点类型，三是如果Node节点插入后需不需要树化（当链长为8，再进行插入，执行treeifyBin判断是否树化）

![image-20200523124013929](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523124013929.png)

①.判断键值对数组table[i]是否为空或为null，否则执行resize()进行扩容；

②.根据键值key计算hash值得到插入的数组索引i，如果table[i]==null，直接新建节点添加，转向⑥，如果table[i]不为空，转向③；

③.判断table[i]的首个元素是否和key一样，如果相同直接覆盖value，否则转向④，这里的相同指的是hashCode以及equals；

④.判断table[i] 是否为treeNode，即table[i] 是否是红黑树，如果是红黑树，则直接在树中插入键值对，否则转向⑤；

⑤.遍历table[i]，找到尾节点，插入，判断**链表长度是否大于等于8**（并不会统计到新插入的节点，而是原本长度），大于等于8的话（也就是原本有链长为8再进行插入，就是有9个节点，才树化），执行treeifyBin，如果要转换为红黑树，在红黑树中执行插入操作，否则进行链表的插入操作；遍历过程中若发现key已经存在直接覆盖value即可；

⑥.插入成功后，判断实际存在的键值对数量size是否超多了最大容量threshold，如果超过，进行扩容。

```java
public V put(K key, V value) {
    return putVal(hash(key), key, value, false, true);
}

final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
               boolean evict) {
    Node<K,V>[] tab; Node<K,V> p; int n, i;
    // table如果未初始化、传入初始长度为0，或者传入大小长度为0的map，则需要进行扩容
    if ((tab = table) == null || (n = tab.length) == 0)
        n = (tab = resize()).length;
    // 如果桶中不包含键值对节点引用，则将新键值对节点的引用存入桶中即可
    if ((p = tab[i = (n - 1) & hash]) == null)
        tab[i] = newNode(hash, key, value, null);
    else {	//对应下标桶数组的引用不为空	
        Node<K,V> e; K k;
        // 如果键的值以及节点 hash 等于链表中的第一个节点（Node/TreeNode）时，则将 e 指向该节点（Node/TreeNode）
        if (p.hash == hash &&
            ((k = p.key) == key || (key != null && key.equals(k))))
            e = p;
            
        // 如果桶中的引用类型为 TreeNode，则调用红黑树的插入方法
        else if (p instanceof TreeNode)  
            e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
        else {
            // 对链表进行遍历，并统计链表长度
            for (int binCount = 0; ; ++binCount) {
                // 链表中不包含要插入的键值对节点时，则将该节点接在链表的最后
                if ((e = p.next) == null) {
                    //遍历到链表末尾，插入需要插入的Node节点（尾插法）
                    p.next = newNode(hash, key, value, null);
                    // 如果当前链表长度大于或等于树化阈值-1（由于从binCount从0开始遍历，大于等于7时链长为8），则进行树化操作
                    // 并没有统计到新插入的节点，而是以循环次数作为树化依据
                    if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                        treeifyBin(tab, hash);		//树化
                    break;
                }
                
                // 条件为 true，表示当前链表包含要插入的键值对，终止遍历
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    break;
                p = e;
            }
        }
        
        // 判断要插入的键值对是否存在 HashMap 中
        if (e != null) { // existing mapping for key
            V oldValue = e.value;
            // onlyIfAbsent 表示是否仅在 oldValue 为 null 的情况下更新键值对的值
            if (!onlyIfAbsent || oldValue == null)
                e.value = value;
            afterNodeAccess(e);
            return oldValue;
        }
    }
    ++modCount;
    // 键值对数量超过阈值时，则进行扩容
    if (++size > threshold)
        resize();
    afterNodeInsertion(evict);
    return null;
}
```

### 树化（条件是插入后链长大于8，且数组长度大于等于64）

并不是链表长度超过8就可以转化为红黑树的，如果Node数组长度小于64，也不会执行树化，而是执行扩容resize()，思想是扩容也能让我们的链变短，计算索引i的时候，一些Node会映射到i+oldCapacity的位置

实际上**树化流程大致就是，先根据table[i]的Node链表生成一个双向链表，再根据这个双向链表头一步步遍历往红黑树增加节点，最后根据构造好的红黑树去替换掉table[i] 上面的Node链表**（单向链表-》双向链表-》红黑树）

注意：在这个红黑树仍然存在链表，相当于找到并头插了root在链头，其余的Node按原来顺序排列

```java
final void treeifyBin(Node<K,V>[] tab, int hash) {
        int n, index; Node<K,V> e;
    	//数组为空或者长度小于64，执行扩容即可，可能能让一条链变短，部分节点存在table[i+oldCapacity]的链上
        if (tab == null || (n = tab.length) < MIN_TREEIFY_CAPACITY)
            resize();
        else if ((e = tab[index = (n - 1) & hash]) != null) {
            TreeNode<K,V> hd = null, tl = null;
            // 遍历链表的每一个元素，形成一条双向链表
            do {
                // Node -> TreeNode，将Node节点转换为TreeNode
                TreeNode<K,V> p = replacementTreeNode(e, null);
                if (tl == null)		// hd记录table[index]的链头
                    hd = p;
                else {
                    p.prev = tl;	//按table[index]上的顺序连接TreeNode的这条链
                    tl.next = p;
                }
                tl = p;
            } while ((e = e.next) != null);
            if ((tab[index] = hd) != null)
                hd.treeify(tab);		//将双向链表转换成红黑树
        }
    }

final void treeify(Node<K,V>[] tab) {	//tab最后才用到
            TreeNode<K,V> root = null;
            for (TreeNode<K,V> x = this, next; x != null; x = next) {	//x从上面的hd节点开始遍历，声明了一个next
                next = (TreeNode<K,V>)x.next;	// 记录双向链表下一个需要遍历的节点
                x.left = x.right = null;
                if (root == null) {	 	// 第一个节点作为红黑树的root
                    x.parent = null;
                    x.red = false;		// 根节点设置为黑色
                    root = x;
                }
                else {
                    K k = x.key;
                    int h = x.hash;			// 取到x节点的hash值（每个节点创建都会放HashMap的hash(key.hashCode())计算后的hash值）
                    Class<?> kc = null;
                    // 下面这个循环，是在比hash大小，确定我们新节点应该插在叶子节点的哪个位置
                    for (TreeNode<K,V> p = root;;) {
                        int dir, ph;
                        K pk = p.key;
                        if ((ph = p.hash) > h)		// 插入节点h<树结点hash,插入的位置应该在左子树
                            dir = -1;
                        else if (ph < h)		// 插入节点h>树结点hash，插入的位置应该在右子树
                            dir = 1;
                        // 插入节点h==树结点hash哈希值相同，再根据key和未重写的hashCode来判断插入位置
                        else if ((kc == null &&
                                  (kc = comparableClassFor(k)) == null) ||
                                 (dir = compareComparables(kc, k, pk)) == 0)
                            dir = tieBreakOrder(k, pk);

                        TreeNode<K,V> xp = p;
                        // 根据dir判断往左子树还是右子树继续遍历，直到找到要插入的叶子节点位置
                        if ((p = (dir <= 0) ? p.left : p.right) == null) {
                            // 插入x
                            x.parent = xp;		
                            // 根据dir选择作为左孩子还是右孩子
                            if (dir <= 0)
                                xp.left = x;
                            else
                                xp.right = x;
                            root = balanceInsertion(root, x);		//x插入后，对该位置进行调整
                            break;
                        }
                    }
                }
            }
            moveRootToFront(tab, root);  	// 将以root为根的红黑树替换掉table数组中原本Node的链表
        }

// 这个代码就是保证table[i] 指向了红黑树的root，需要修改的是从双向链表取出root放到table[i]的头部而已
static <K,V> void moveRootToFront(Node<K,V>[] tab, TreeNode<K,V> root) {
            int n;
            if (root != null && tab != null && (n = tab.length) > 0) {
                int index = (n - 1) & root.hash;
                TreeNode<K,V> first = (TreeNode<K,V>)tab[index];
                if (root != first) {
                    Node<K,V> rn;
                    tab[index] = root;
                    TreeNode<K,V> rp = root.prev;
                    if ((rn = root.next) != null)
                        ((TreeNode<K,V>)rn).prev = rp;
                    if (rp != null)
                        rp.next = rn;
                    if (first != null)
                        first.prev = root;
                    root.next = first;
                    root.prev = null;
                }
                assert checkInvariants(root);	//判断true or false
            }
        }

```

对于调整的原理，放到红黑树的各种操作讨论

### 扩容机制

JDK1.7的扩容分为扩容+转移 即resize和transfer，而JDK1.8这两步都放在了resize，而且初始化的懒加载规则也有所不同。最主要的是**发生扩容的时机不同和转移方式不同**（不讨论初始化的扩容）：

**发生扩容的时机不同：**

1、JDK1.7是当table数组已用长度size大于等于threshold（容量*装填因子）时，发生了hash碰撞，那么进行扩容

2、 JDK1.8是在**JDK1.7的基础上**，有新的扩容时机：当链表长度小于等于64，发生了hash碰撞，且put的Node节点映射table[i]上是一条大于等于8的链

**转移方式不同：**

1、JDK1.7 遍历旧数组oldTable[i]的链表，对于每一个Node，计算在新数组的下标，逐个**头插**

2、 JDK1.8 先判断是不是TreeNode，是TreeNode 需要拆分，如果不是，先生成对于i位置的链和i+oldCap位置的**两条链**，对于每个Node，根据在新数组的下标，**尾插**在这其中一条链，最后再newTable再进行指向

```java
    final Node<K,V>[] resize() {
        //把没插入之前的Node数组叫做oldTal
        Node<K,V>[] oldTab = table;
        //old的长度
        int oldCap = (oldTab == null) ? 0 : oldTab.length;
        //old的临界值，如果是无参构造，则为0
        int oldThr = threshold;
        //初始化new的长度和临界值
        int newCap, newThr = 0;
        //oldCap > 0，也就是说不是首次初始化或数组长度真的为0
        if (oldCap > 0) {
            if (oldCap >= MAXIMUM_CAPACITY) {//大于最大值 
                threshold = Integer.MAX_VALUE;//临界值为整数的最大值
                return oldTab;
            }
            //扩容后的长度要小于最大值，old长度也要大于等于16
            else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY &&
                     oldCap >= DEFAULT_INITIAL_CAPACITY)
                //临界值也扩容为old的临界值2倍
                newThr = oldThr << 1; 
        }
		//oldCap=0，但已经设置了阈值
        else if (oldThr > 0) 
            newCap = oldThr;
        //无参构造的首次初始化，给与默认的值
        else {               
            newCap = DEFAULT_INITIAL_CAPACITY;
            //临界值等于容量*加载因子
            newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);
        }
        //此处的if为 else if (oldThr > 0)的补充，也就是初始化时容量小于默认值16的，此时newThr没有赋值
        if (newThr == 0) {
            //new的临界值
            float ft = (float)newCap * loadFactor;
            //判断是否new容量是否大于最大值，临界值是否大于最大值
            newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ?
                      (int)ft : Integer.MAX_VALUE);
        }
        //把上面各种情况分析出的临界值，在此处真正进行改变，也就是容量和临界值都改变了。
        threshold = newThr;
        //表示忽略该警告
        @SuppressWarnings({"rawtypes","unchecked"})
            //初始化分配空间
            Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
        //赋予当前的table
        table = newTab;
        //此处相当于是JDK1.7的transfer操作，将原本元素转移到新的数组
        if (oldTab != null) {
            for (int j = 0; j < oldCap; ++j) {
                //临时变量
                Node<K,V> e;
                //当前哈希桶的位置值不为null，也就是数组下标处有值，因为有值表示可能会发生冲突
                if ((e = oldTab[j]) != null) {
                    //把已经赋值之后的变量置位null，当然是为了好回收，释放内存
                    oldTab[j] = null;
                    
                    if (e.next == null)// 如果table[i]只有一个Node，直接指向即可
                        newTab[e.hash & (newCap - 1)] = e;
                    else if (e instanceof TreeNode)    //该节点为红黑树结构，把此树进行转移到newCap中
                        ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
                    else { 
                       //说明是链表结构
                        Node<K,V> loHead = null, loTail = null;
                        Node<K,V> hiHead = null, hiTail = null;
                        Node<K,V> next;
                        // 这个循环实现连接，newCap是oldCap 2倍，所以Node只可能在新数组的两个位置
                        // 要么为i 要么为 i + oldCap，JDK1.7是靠transfer逐个去放的
                        // 而JDK1.8 则是先遍历一遍，生成i和i + oldCap两条链，新数组再对应位置指向这两条链
                        do {
                            next = e.next;
                            if ((e.hash & oldCap) == 0) {	 // oldCap是2次幂，(e.hash & oldCap) == 0,说明下标不变
                                if (loTail == null)
                                    loHead = e;
                                else
                                    loTail.next = e;
                                loTail = e;
                            }
                            else {		// e在新数组的下标位置是 i + oldCap
                                if (hiTail == null)
                                    hiHead = e;
                                else
                                    hiTail.next = e;
                                hiTail = e;
                             }
                        } while ((e = next) != null);
                        if (loTail != null) {
                            loTail.next = null;
                            newTab[j] = loHead;
                        }
                        if (hiTail != null) {
                            hiTail.next = null;
                            newTab[j + oldCap] = hiHead;
                        }
                    }
                }
            }
        }
        //返回扩容后的hashMap
        return newTab;
    }
```

如果节点是 TreeNode 类型，则需要拆分红黑树，通过前面建树已经维护了一个双向链表实现，转移过程与链表一样但是要统计低位链和高位链长度，小于等于6需要链化，否则则树化

```java
final void split(HashMap<K,V> map, Node<K,V>[] tab, int index, int bit) {
            TreeNode<K,V> b = this;
            // 基本上和链表是一样的，用两条链
            TreeNode<K,V> loHead = null, loTail = null;
            TreeNode<K,V> hiHead = null, hiTail = null;
            int lc = 0, hc = 0;
            for (TreeNode<K,V> e = b, next; e != null; e = next) {
                next = (TreeNode<K,V>)e.next;
                e.next = null;
                if ((e.hash & bit) == 0) {
                    if ((e.prev = loTail) == null)
                        loHead = e;
                    else
                        loTail.next = e;
                    loTail = e;
                    ++lc;		// 统计低位链表长度
                }
                else {
                    if ((e.prev = hiTail) == null)
                        hiHead = e;
                    else
                        hiTail.next = e;
                    hiTail = e;
                    ++hc;		// 统计高位链表长度
                }
            }

            if (loHead != null) {
                if (lc <= UNTREEIFY_THRESHOLD)	// 链表长度小于等于6改变成链表
                    tab[index] = loHead.untreeify(map);	// 链化很简单，就是根据双向链表遍历创建Node连接
                else {
                    tab[index] = loHead;
                    if (hiHead != null) 		// hiHead为空，则说明节点全在低位链，不需要再树化
                        loHead.treeify(tab);	// 分成了两条链，且链长大于6需要树化
                }
            }
            if (hiHead != null) {
                if (hc <= UNTREEIFY_THRESHOLD)	// 链表长度小于等于6改变成链表
                    tab[index + bit] = hiHead.untreeify(map);
                else {
                    tab[index + bit] = hiHead;
                    if (loHead != null)
                        hiHead.treeify(tab);	// 分成了两条链，且链长大于6需要树化
                }
            }
        }
```



### 链化

红黑树中仍然保留了原链表节点顺序。有了这个前提，再将红黑树转成链表就简单多了，仅需将 TreeNode 链表转成 Node 类型的链表即可。

```java
final Node<K,V> untreeify(HashMap<K,V> map) {
    Node<K,V> hd = null, tl = null;
    // 遍历 TreeNode 链表，并用 Node 替换
    for (Node<K,V> q = this; q != null; q = q.next) {
        // 替换节点类型
        Node<K,V> p = map.replacementNode(q, null);
        if (tl == null)
            hd = p;
        else
            tl.next = p;
        tl = p;
    }
    return hd;
}

Node<K,V> replacementNode(Node<K,V> p, Node<K,V> next) {
    return new Node<>(p.hash, p.key, p.value, next);
}
```

### get方法

HashMap 的查找操作比较简单，先定位键值对所在的桶的位置，然后再对链表或红黑树进行查找。通过这两步即可完成查找，该操作相关代码如下：

```java
public V get(Object key) {
    Node<K,V> e;
    return (e = getNode(hash(key), key)) == null ? null : e.value;
}

final Node<K,V> getNode(int hash, Object key) {
    Node<K,V>[] tab; Node<K,V> first, e; int n; K k;
    //定位键值对所在桶的位置
    if ((tab = table) != null && (n = tab.length) > 0 &&
        (first = tab[(n - 1) & hash]) != null) {
        if (first.hash == hash && // always check first node
            ((k = first.key) == key || (key != null && key.equals(k))))
            return first;
        if ((e = first.next) != null) {
            // 如果 first 是 TreeNode 类型，则调用黑红树查找方法
            if (first instanceof TreeNode)
                return ((TreeNode<K,V>)first).getTreeNode(hash, key);
                
            // 对链表进行查找
            do {
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    return e;
            } while ((e = e.next) != null);
        }
    }
    return null;
}

// 遍历红黑树
final TreeNode<K,V> getTreeNode(int h, Object k) {
            return ((parent != null) ? root() : this).find(h, k, null);
        }
// 实际上就是判断往左找还是往右找的过程，类似二叉查找树的搜索
final TreeNode<K,V> find(int h, Object k, Class<?> kc) {
            TreeNode<K,V> p = this;
            do {
                int ph, dir; K pk;
                TreeNode<K,V> pl = p.left, pr = p.right, q;
                if ((ph = p.hash) > h)
                    p = pl;
                else if (ph < h)
                    p = pr;
                else if ((pk = p.key) == k || (k != null && k.equals(pk)))
                    return p;		// 找到了，返回
                else if (pl == null)	// 没有左子树，直接走右子树
                    p = pr;
                else if (pr == null)	// 没有右子树，直接走左子树
                    p = pl;
                else if ((kc != null ||
                          (kc = comparableClassFor(k)) != null) &&
                         (dir = compareComparables(kc, k, pk)) != 0)
                    p = (dir < 0) ? pl : pr;		// 向左遍历还是向右遍历
                else if ((q = pr.find(h, k, kc)) != null)	// 递归，右子树看有没有结果
                    return q;
                else
                    p = pl;				// 向左遍历
            } while (p != null);		// 移动和查找两次循环才完成
            return null;
        }
```

### remove方法

HashMap 的删除操作并不复杂，仅需三个步骤即可完成。第一步是定位桶位置，第二步遍历链表并找到键值相等的节点，第三步删除节点。相关源码如下：

```java
public V remove(Object key) {
    Node<K,V> e;
    return (e = removeNode(hash(key), key, null, false, true)) == null ?
        null : e.value;
}


final Node<K,V> removeNode(int hash, Object key, Object value,
                           boolean matchValue, boolean movable) {
    Node<K,V>[] tab; Node<K,V> p; int n, index;
    if ((tab = table) != null && (n = tab.length) > 0 &&
        // 1. 定位桶位置
        (p = tab[index = (n - 1) & hash]) != null) {
        Node<K,V> node = null, e; K k; V v;
        // 如果键的值与链表第一个节点相等，则将 node 指向该节点
        if (p.hash == hash &&
            ((k = p.key) == key || (key != null && key.equals(k))))
            node = p;
        else if ((e = p.next) != null) {  
            // 如果是 TreeNode 类型，调用红黑树的查找逻辑定位待删除节点
            if (p instanceof TreeNode)
                node = ((TreeNode<K,V>)p).getTreeNode(hash, key);
            else {
                // 2. 遍历链表，找到待删除节点
                do {
                    if (e.hash == hash &&
                        ((k = e.key) == key ||
                         (key != null && key.equals(k)))) {
                        node = e;
                        break;
                    }
                    p = e;
                } while ((e = e.next) != null);
            }
        }
        
        // 3. 删除节点，并修复链表或红黑树
        if (node != null && (!matchValue || (v = node.value) == value ||
                             (value != null && value.equals(v)))) {
            if (node instanceof TreeNode)
                ((TreeNode<K,V>)node).removeTreeNode(this, tab, movable);	// 修复
            else if (node == p)
                tab[index] = node.next;
            else
                p.next = node.next;
            ++modCount;
            --size;
            afterNodeRemoval(node);
            return node;
        }
    }
    return null;
}

// 删除红黑树节点的操作,可能会链化
final Node<K,V> removeNode(int hash, Object key, Object value,
                               boolean matchValue, boolean movable) {
        Node<K,V>[] tab; Node<K,V> p; int n, index;
        if ((tab = table) != null && (n = tab.length) > 0 &&
            (p = tab[index = (n - 1) & hash]) != null) {
            Node<K,V> node = null, e; K k; V v;
            if (p.hash == hash &&
                ((k = p.key) == key || (key != null && key.equals(k))))
                node = p;
            else if ((e = p.next) != null) {
                if (p instanceof TreeNode)
                    node = ((TreeNode<K,V>)p).getTreeNode(hash, key);
                else {
                    do {
                        if (e.hash == hash &&
                            ((k = e.key) == key ||
                             (key != null && key.equals(k)))) {
                            node = e;
                            break;
                        }
                        p = e;
                    } while ((e = e.next) != null);
                }
            }
            if (node != null && (!matchValue || (v = node.value) == value ||
                                 (value != null && value.equals(v)))) {
                if (node instanceof TreeNode)
                    ((TreeNode<K,V>)node).removeTreeNode(this, tab, movable);
                else if (node == p)
                    tab[index] = node.next;
                else
                    p.next = node.next;
                ++modCount;
                --size;
                afterNodeRemoval(node);
                return node;
            }
        }
        return null;
    }
```



### 红黑树的各种操作

**红黑树的定义**

性质1：每个节点要么是黑色，要么是红色。

性质2：根节点是黑色。

性质3：每个叶子节点（NIL）是黑色。

性质4：每个红色结点的两个子结点一定都是黑色。

<mark>性质5：任意一结点到每个叶子结点的路径都包含数量相同的黑结点。</mark>

#### 基本操作

1、 左旋   &emsp;2、 右旋

![image-20200523191432357](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523191432357.png)

#### 插入（考虑对称，左右旋操作不明确写了）

**插入的节点都为红色，减少调整的次数**

1. 插入节点为根节点，直接插入，再变黑色
2. 父节点是黑色，直接插入，不需要调整

![image-20200523192528630](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523192528630.png)

3. 调整节点的**父节点红，叔叔红**，则把父节点和叔叔节点变黑，爷爷变红，调整指针转到爷爷节点

   ![image-20200523195306349](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523195306349.png)

   4. 调整节点的**父节点红，叔叔黑**

      1. 直线型，为了方便理解，当父节点和插入节点都是左孩子或者右孩子时，形象的认为是一个直线

         - 两步操作，父节点右旋/左旋，爷爷节点与父节点交换颜色

         ![image-20200523195400937](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523195400937.png)

      2. 破折号型，当父节点和插入节点不都是左孩子或者右孩子时，形象的认为是一个破折号

         - 左/右旋，先转换成直线型

         - 再执行直线型的两步调整（父节点右旋/左旋，爷爷节点与父节点交换颜色）

           ![image-20200523200036161](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523200036161.png)

             

HashMap里面的代码实现

```java
static <K,V> TreeNode<K,V> balanceInsertion(TreeNode<K,V> root,
                                                    TreeNode<K,V> x) {
            x.red = true;
            for (TreeNode<K,V> xp, xpp, xppl, xppr;;) {
                if ((xp = x.parent) == null) {
                    x.red = false;
                    return x;
                }
                else if (!xp.red || (xpp = xp.parent) == null)
                    return root;
                if (xp == (xppl = xpp.left)) {
                    if ((xppr = xpp.right) != null && xppr.red) {
                        xppr.red = false;
                        xp.red = false;
                        xpp.red = true;
                        x = xpp;
                    }
                    else {
                        if (x == xp.right) {
                            root = rotateLeft(root, x = xp);
                            xpp = (xp = x.parent) == null ? null : xp.parent;
                        }
                        if (xp != null) {
                            xp.red = false;
                            if (xpp != null) {
                                xpp.red = true;
                                root = rotateRight(root, xpp);
                            }
                        }
                    }
                }
                else {
                    if (xppl != null && xppl.red) {
                        xppl.red = false;
                        xp.red = false;
                        xpp.red = true;
                        x = xpp;
                    }
                    else {
                        if (x == xp.left) {
                            root = rotateRight(root, x = xp);
                            xpp = (xp = x.parent) == null ? null : xp.parent;
                        }
                        if (xp != null) {
                            xp.red = false;
                            if (xpp != null) {
                                xpp.red = true;
                                root = rotateLeft(root, xpp);
                            }
                        }
                    }
                }
            }
        }
```



#### 删除（考虑对称，左右旋操作不明确写了）

红黑树和二叉搜索树的删除类似，只不过加上颜色属性（**这里的子节点均指非NULL节点**）：

1. 无子节点时，删除节点可能为红色或者黑色；

   - 如果为红色，直接删除即可，不会影响黑色节点的数量；

   - 如果为黑色，则需要进行删除平衡的操作了；

   ![image-20200523201413998](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523201413998.png)

2. 只有一个子节点时，删除节点只能是黑色，其子节点为红色

   否则无法满足红黑树的性质了。 此时用删除节点的子节点接到父节点，且将子节点颜色涂黑，保证黑色数量。

   ![image-20200523203859076](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523203859076.png)

3. 有两个子节点时，与二叉搜索树一样，使用后继节点作为替换的删除节点，情形转至为1或2处理。

![image-20200523201919080](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523201919080.png)

**删除平衡操作**

  1.   红色直接删除（由于红色节点要么有两个孩子，要么是叶子）

  2.   如果待删除结点为黑色，这种情况下，此条分支不可能通过涂色的方式弥补缺少的黑色，所以要判断其父亲、兄弟和侄子的状况，通过旋转来保持黑色的数量

         1.   兄弟是黑色，且兄弟的子节点全为黑色

              1、父节点红色，把兄弟和父节点颜色替换即可

              ![image-20200523212504207](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523212504207.png)

              2、父节点黑色，将兄弟节点染成红色向上逐层调整，直到符合黑高相等为止

              ![image-20200523212407459](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523212407459.png)

       2. 兄弟是黑色，且兄弟的子节点不全为黑色

          1、兄弟子节点全是红色

          兄弟节点左旋/右旋，染红，远侄子染黑，转换成其他情况，继续调整

          ![image-20200523214014326](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523214014326.png)

          2、兄弟近侄子为红，远侄子为黑（近朱者赤）近侄子左旋/右旋，交换颜色（转换成近墨者黑）

          ![image-20200523214629711](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523214629711.png)

          3、 兄弟远侄子为红，近侄子为黑（近墨者黑）远侄子节点右旋，兄弟染红，远侄子和父节点染黑，在兄弟节点继续调整

          ![image-20200523215821582](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523215821582.png)

       3. 兄弟节点为红色

          兄弟为红色、进行左旋/右旋，再向下逐一调整

​			![image-20200523221721398](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200523221721398.png)

HashMap实现删除节点源码

```java
final void removeTreeNode(HashMap<K,V> map, Node<K,V>[] tab,
                                  boolean movable) {
            int n;
            if (tab == null || (n = tab.length) == 0)
                return;
            int index = (n - 1) & hash;
            TreeNode<K,V> first = (TreeNode<K,V>)tab[index], root = first, rl;
            TreeNode<K,V> succ = (TreeNode<K,V>)next, pred = prev;
            if (pred == null)
                tab[index] = first = succ;
            else
                pred.next = succ;
            if (succ != null)
                succ.prev = pred;
            if (first == null)
                return;
            if (root.parent != null)
                root = root.root();
            if (root == null
                || (movable
                    && (root.right == null
                        || (rl = root.left) == null
                        || rl.left == null))) {
                tab[index] = first.untreeify(map);  // too small
                return;
            }
            TreeNode<K,V> p = this, pl = left, pr = right, replacement;
            if (pl != null && pr != null) {
                TreeNode<K,V> s = pr, sl;
                while ((sl = s.left) != null) // find successor
                    s = sl;
                boolean c = s.red; s.red = p.red; p.red = c; // swap colors
                TreeNode<K,V> sr = s.right;
                TreeNode<K,V> pp = p.parent;
                if (s == pr) { // p was s's direct parent
                    p.parent = s;
                    s.right = p;
                }
                else {
                    TreeNode<K,V> sp = s.parent;
                    if ((p.parent = sp) != null) {
                        if (s == sp.left)
                            sp.left = p;
                        else
                            sp.right = p;
                    }
                    if ((s.right = pr) != null)
                        pr.parent = s;
                }
                p.left = null;
                if ((p.right = sr) != null)
                    sr.parent = p;
                if ((s.left = pl) != null)
                    pl.parent = s;
                if ((s.parent = pp) == null)
                    root = s;
                else if (p == pp.left)
                    pp.left = s;
                else
                    pp.right = s;
                if (sr != null)
                    replacement = sr;
                else
                    replacement = p;
            }
            else if (pl != null)
                replacement = pl;
            else if (pr != null)
                replacement = pr;
            else
                replacement = p;
            if (replacement != p) {
                TreeNode<K,V> pp = replacement.parent = p.parent;
                if (pp == null)
                    root = replacement;
                else if (p == pp.left)
                    pp.left = replacement;
                else
                    pp.right = replacement;
                p.left = p.right = p.parent = null;
            }

            TreeNode<K,V> r = p.red ? root : balanceDeletion(root, replacement);

            if (replacement == p) {  // detach
                TreeNode<K,V> pp = p.parent;
                p.parent = null;
                if (pp != null) {
                    if (p == pp.left)
                        pp.left = null;
                    else if (p == pp.right)
                        pp.right = null;
                }
            }
            if (movable)
                moveRootToFront(tab, r);
        }

```

如果想直观的看插入删除，有一个可视化调整红黑树的网址：[数据结构可视化](https://www.cs.usfca.edu/~galles/visualization/Algorithms.html)

### 线程不安全

前面说到jdk 1.7存在并发情况下出现死链的情况，而jdk1.8使用尾插法修复了这个问题，但依旧是线程不安全的，比如有两个待写入的键值对{"a": 1, "b": 2}，刚好落到同一个桶里，假设这个桶是0号桶，这个桶里有一个元素c。

单线程环境下，我们先查a准备写入的位置，查到是0号桶的c后面的位置，之后写入a。然后查b准备写入的位置，查到是0号桶的a后面的位置，之后写入b。两个键值对都能正常被写入。

多线程环境下，a的查询可能和b是同步进行的。线程t1的查询里，a的写入位置是c后面，c.next=a；线程t2的查询里，b的写入位置也是c后面（因为此刻a尚未插入）, c.next=b。最终先插入c后面的会被后写的覆盖，只有后写的那个会被实际成功写入。



## 总结HashMap 1.7和1.8的区别

1. jdk8中会将链表会转变为红黑树
2. 新节点插入链表的顺序不相同（dk7是插入头结点，jdk8插入尾结点）
3. .hash算法简化
4. resize的逻辑修改和新增发生条件（jdk7会出现死循环，jk8不会）



## modCount与快速失败机制fast-fail

```java
public class HashMapTestDemo2 {
    public static void main(String[] args) {
        Map<String,String> map = new HashMap<>();
        map.put("1","1");
        map.put("2", "2");
        for(String s:map.keySet()){
            if(s.equals("1")){
                map.remove("1");
            }
        }
    }
}
```

可以看到抛出了一个ConcurrentModificationException异常，下面用1.8的代码查看，实际和1.7是差不多的Node和Entry数组名字不同而已

![image-20200522010726709](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200522010726709.png)

我们可以拿到编译后的class文件查看，实际上是隐式地使用了迭代器去完成我们的遍历

```java
public class HashMapTestDemo2 {
    public HashMapTestDemo2() {
    }

    public static void main(String[] args) {
        Map<String, String> map = new HashMap();
        map.put("1", "1");
        map.put("2", "2");								//
        Iterator var2 = map.keySet().iterator();		//返回KeyIterator，继承父类HashIterator
        												//modCount=2,expectedModCount=2

        while(var2.hasNext()) {
            String s = (String)var2.next();
            if (s.equals("1")) {
                map.remove("1");				//实际上执行了remove，而modCount++
                								//下一次next操作判断时，modCount!=expectedModCount抛出异常
            }
        }

    }
}
```

![image-20200522011808260](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200522011808260.png)

![image-20200522012636795](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200522012636795.png)

put、remove操作都会执行modCount++，而迭代器父类的expectedModCount是不变的，因此第二次next时，`modCount != expectedModCount`抛出异常，这就是**fast-fail的机制**，应该使用迭代器的remove方法(会同步expectedModCount)。

注意如果使用普通for循环，会出现同样两个相邻变量值只删除一个的情况

```java
public class HashMapTestDemo2 {
    public static void main(String[] args) throws Exception {
        Map<String,String> map = new HashMap<>();
        map.put("1","1");
        map.put("2", "2");

        Iterator iterator = map.keySet().iterator();
        while(iterator.hasNext()){
            String key = (String) iterator.next();
            if(key.equals("1")){
                iterator.remove();
            }

        }
    }
}
```

**fast-fail**

java集合的一种错误检测机制，当多个线程对集合进行结构上的改变的操作时，有可能会产生 fail-fast 机制。

例如：假设存在两个线程（线程1、线程2），线程1通过Iterator在遍历集合A中的元素，在某个时候线程2修改了集合A的结构（是put或remove结构上面的修改，而不是简单的修改集合元素引用），那么这个时候程序就会抛出 ConcurrentModificationException 异常，从而产生fail-fast机制。

原因：迭代器在遍历时直接访问集合中的内容，并且在遍历过程中使用一个 **modCount 变量**。集合在被遍历期间如果内容发生变化，就会改变modCount的值。每当迭代器使用**hashNext()/next()**遍历下一个元素之前，都会**检测modCount变量是否为expectedModCount**值，是的话就返回遍历；否则抛出异常，终止遍历。

解决办法：

1. 在遍历过程中，所有涉及到改变modCount值得地方全部加上synchronized。

2. 使用CopyOnWriteArrayList来替换ArrayList



