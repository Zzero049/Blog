# ArrayList底层机制

## 构造函数

从源码入手，先看属性值，当我们`List<String> list = new ArrayList<>();`创建一个数组时，默认设置容量为10。

```java
	private static final int DEFAULT_CAPACITY = 10;

    /**
     * 用于传入参数为0，或传入Collection长度0的时候使用，让elementData指向该数组。
     */
    private static final Object[] EMPTY_ELEMENTDATA = {};
	/**
     * 用于默认大小的空实例的共享空数组实例。
     * 我们将其与EMPTY_ELEMENTDATA区分开来，唯一区别在于添加第一个元素时扩容多少。
     * 传入0的扩容为add的数据长度，而空参是扩容到10或者是add的数据长度
     * MARK:无参构造函数 使用该数组初始化 与EMPTY_ELEMENTDATA的区别主要是区分作用，用来减少空数组的存在，优化内存使用 1.8后的优化
     */
	private static final Object[] DEFAULTCAPACITY_EMPTY_ELEMENTDATA = {};
	
	transient Object[] elementData;
```

再来看看三个构造函数，注意**空参构造，即便DEFAULT_CAPACITY = 10，要生成elementData长度为10的Object[]数组，是调用了add才完成的**

```java
/**
     * 构造具有指定初始容量的空列表。
     * @param  initialCapacity  列表的初始容量
     * @throws IllegalArgumentException
     */
    public ArrayList(int initialCapacity) {
        if (initialCapacity > 0) {
            this.elementData = new Object[initialCapacity];
        } else if (initialCapacity == 0) {
            this.elementData = EMPTY_ELEMENTDATA;
        } else {
            throw new IllegalArgumentException("Illegal Capacity: "+
                                               initialCapacity);
        }
    }

    /**
     * 构造一个初始容量为10的空列表。
     * MARK:
     * 这里其实是赋值了一个共享的空数组，数组在第一次添加元素时会判断elementData是否等于DEFAULTCAPACITY_EMPTY_ELEMENTDATA，假如等于则会初始化为DEFAULT_CAPACITY 也就是10
     *
     */
    public ArrayList() {
        this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
    }

    /**
     * 构造一个包含指定元素的列表集合
     * @param c 要将其元素放入此列表的集合
     * @throws NullPointerException if the specified collection is null
     */
    public ArrayList(Collection<? extends E> c) {
        //  这里说明所有的 Collection 都可以用数组来承载
        //  这个步骤可能会抛空指针 NullPointerException
        elementData = c.toArray();
        if ((size = elementData.length) != 0) {
            //必须是Object数组
            if (elementData.getClass() != Object[].class)
                // 然后再copy一份到 elementData 并不是引用 所有改变不会影响到原先的Collection
                elementData = Arrays.copyOf(elementData, size, Object[].class);
        } else {
            // 有参构造函数 当初始化为空数组时 赋值为 EMPTY_ELEMENTDATA
            this.elementData = EMPTY_ELEMENTDATA;
        }
    }
```



## 扩容机制

然后就是扩容机制add方法后调用的各种方法

```java
public boolean add(E e) {
        ensureCapacityInternal(size + 1);  // Increments modCount!!
        elementData[size++] = e;
        return true;
    }
public boolean addAll(Collection<? extends E> c) {
        Object[] a = c.toArray();
        int numNew = a.length;
        ensureCapacityInternal(size + numNew);  // Increments modCount
        System.arraycopy(a, 0, elementData, size, numNew);
        size += numNew;
        return numNew != 0;
    }

// minCapacity就是当前size+1或size+numNew
private void ensureCapacityInternal(int minCapacity) {
        ensureExplicitCapacity(calculateCapacity(elementData, minCapacity));
    }

//空参构造，第一次add需要扩容，也就是jdk1.8 elementData数组并不是默认就是Object[10]，如果不进行add，那也是0
private static int calculateCapacity(Object[] elementData, int minCapacity) {
        if (elementData == DEFAULTCAPACITY_EMPTY_ELEMENTDATA) {
            return Math.max(DEFAULT_CAPACITY, minCapacity);
        }
        return minCapacity;
    }

//如果size+ 1或numNew > elementData.length，则需要扩容
private void ensureExplicitCapacity(int minCapacity) {
        modCount++;

        // overflow-conscious code
        if (minCapacity - elementData.length > 0)
            grow(minCapacity);
    }

//我们熟知的1.5倍扩容
private void grow(int minCapacity) {
        // overflow-conscious code
        int oldCapacity = elementData.length;
        int newCapacity = oldCapacity + (oldCapacity >> 1);// 1.5倍扩容后的容量
        if (newCapacity - minCapacity < 0)	//addAll 方法可能传入的集合很大minCapacity大于1.5倍后的结果
            newCapacity = minCapacity;
        if (newCapacity - MAX_ARRAY_SIZE > 0)
            newCapacity = hugeCapacity(minCapacity);//Integer.MAX_VALUE,考虑到1.5倍后溢出问题
        // minCapacity is usually close to size, so this is a win:
        elementData = Arrays.copyOf(elementData, newCapacity);
    }
```

流程图如下：

![image-20200521083304683](https://gitee.com/zero049/MyNoteImages/raw/master/ArrayList扩容.png)

扩容示例:

![image-20200522005200798](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200522005200798.png)

## 删除机制

接着我们看一下删除的操作。ArrayList支持两种删除方式：

1、按照下标删除

2、按照元素删除，这会删除ArrayList中与指定要删除的元素匹配的第一个元素

对于ArrayList来说，这两种删除的方法差不多，只不过按照元素删除还需要进行一步遍历获取下表index的过程，底层都是通过System.arraycopy将后面的元素复制覆盖到前面，size减一

```java
//按照下标删除
public E remove(int index) {
        rangeCheck(index);

        modCount++;
        E oldValue = elementData(index);

        int numMoved = size - index - 1;//需要移动数量
        if (numMoved > 0)
            System.arraycopy(elementData, index+1, elementData, index,
                             numMoved);
        elementData[--size] = null; // clear to let GC do its work

        return oldValue;
    }
//按照元素删除，这会删除ArrayList中与指定要删除的元素匹配的第一个元素
public boolean remove(Object o) {
        if (o == null) {
            for (int index = 0; index < size; index++)
                if (elementData[index] == null) {
                    fastRemove(index);
                    return true;
                }
        } else {
            for (int index = 0; index < size; index++)
                if (o.equals(elementData[index])) {
                    fastRemove(index);
                    return true;
                }
        }
        return false;
    }

private void fastRemove(int index) {
        modCount++;
        int numMoved = size - index - 1;	//需要移动数量
        if (numMoved > 0)
            System.arraycopy(elementData, index+1, elementData, index,
                             numMoved);
        elementData[--size] = null; // clear to let GC do its work
    }
```

删除实例：

![image-20200522005216923](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200522005216923.png)

## ArrayList的特点

主要特点如下

![image-20200521112023580](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200521112023580.png)

### 优点

1、ArrayList底层以数组实现，是一种随机访问模式，再加上它实现了RandomAccess接口，因此查找也就是get的时候非常快

2、ArrayList在顺序添加一个元素的时候非常方便，只是往数组里面添加了一个元素而已



### 缺点

1、删除元素的时候，涉及到一次元素复制，如果要复制的元素很多，那么就会比较耗费性能

2、插入元素的时候，如果发生扩容涉及到一次元素复制，如果要复制的元素很多，那么就会比较耗费性能

因此，ArrayList比较适合顺序添加、随机访问的场景。



### ArrayList与Vector区别

Vector是ArrayList的线程安全版本，其实现90%和ArrayList都完全一样，区别在于：

1、Vector是线程安全的，几乎所有方法都加上了synchronized修饰，ArrayList是线程非安全的，因此ArrayList更高效

2、Vector可以指定增长因子，如果该增长因子指定了，那么扩容的时候会每次新的数组大小会在原数组的大小基础上加上增长因子；如果不指定增长因子，那么就给原数组大小*2



### 为什么elementData是使用transient修饰的呢

用transient修饰elementData意味着我不希望elementData数组被序列化。这是为什么？因为序列化ArrayList的时候，ArrayList里面的elementData未必是满的，比方说elementData有10的大小，但是我只用了其中的3个，那么是否有必要序列化整个elementData呢？显然没有这个必要，因此ArrayList中重写了writeObject方法：

```java
private void writeObject(java.io.ObjectOutputStream s)
        throws java.io.IOException{
        // Write out element count, and any hidden stuff
        int expectedModCount = modCount;
        s.defaultWriteObject();

        // Write out size as capacity for behavioural compatibility with clone()
        s.writeInt(size);

        // Write out all elements in the proper order.
        for (int i=0; i<size; i++) {
            s.writeObject(elementData[i]);
        }

        if (modCount != expectedModCount) {
            throw new ConcurrentModificationException();
        }
    }
```

每次序列化的时候调用这个方法，**先调用defaultWriteObject()方法序列化ArrayList中的非transient元素，elementData不去序列化它，然后遍历elementData，只序列化那些有的元素**，这样：

1、加快了序列化的速度

2、减小了序列化之后的文件大小

