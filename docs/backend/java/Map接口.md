# Map接口
Map就是用来存储“键（key）-值（value）对”的。Map类中存储的“键值对”通过键来标识，所以“键对象”不能重复。
Map接口的实现类有HashMap、TreeMap、HashTable、Properties等。
<img src="./pictures/Annotation 2019-11-07 190259.png"  div align=center />

## HashMap
HashMap底层实现采用了哈希表，这是一种非常重要的数据结构。对于我们以后理解很多技术都非常有帮助（比如：redis数据库的核心技术和HashMap一样），因此，非常有必要让大家理解。
数据结构中由数组和链表来实现对数据的存储，他们各有特点。
（1）数组：占用空间连续。寻址容易，查询速度快。但是，增加和删除效率非常低。
（2）链表：占用空间不连续。寻址困难，查询速度慢。但是，增加和删除效率非常高。
哈希表的本质就是“数组+链表”,结合数组和链表的优点。（即查询快，增删效率也高）


一个Entry对象存储了：
1.key：键对象value：值对象
2.next：下一个节点
3.hash：键对象的hash值
显然每一个Entry对象就是一个单向链表结构，我们使用图形表示一个Entry对象的典型示意：
<img src="./pictures/Annotation 2019-11-07 193637.png"  div align=center />
画出Entry[]数组的结构（这也是HashMap的结构）：
<img src="./pictures/Annotation 2019-11-07 193755.png"  div align=center />

#### 数据存储过程
明白了HashMap的基本结构后，我们继续深入学习HashMap如何存储数据。此处的核心是如何产生hash值，该值用来对应数组的存储位置。
<img src="./pictures/Annotation 2019-11-07 194204.png"  div align=center />

我们的目的是将”key-value两个对象”成对存放到HashMap的Entry[]数组中。参见以下步骤：
（1）获得key对象的hashcode首先调用key对象的hashcode（）方法，获得hashcode。
（2）根据hashcode计算出hash值（要求在[0，数组长度-1]区间）hashcode是一个整数，我们需要将它转化成[0，数组长度-1]的范围。我们要求转化后的hash值尽量均匀地分布在[0，数组长度-1]这个区间，减少“hash冲突"
i.一种极端简单和低下的算法是：
hash值=hashcode/hashcode；M也就是说，hash值总是1。意味着，键值对对象都会存储到数组索引1位置，这样就形成一个非常长的链表。相当于每存储一个对象都会发生"hash冲突”，HashMap也退化成了一个“链表”。
ii.一种简单和常用的算法是（相除取余算法）：
hash值 = hachcode%数组长度
这种算法可以让hash值均匀的分布在[0，数组长度-1]的区间。早期的HashTable就是采用这种算法。但是，这种算法由于使用了“除法”，效率低下。JDK后来改进了算法。首先约定数组长度必须为2的整数幂，这样采用位运算即可实现取余（由于数组长度为2的整数幂，-1即位全1）的效果：hash值=hashcode&（数组长度-1）。（效率高）


为了获得更好的散列效果，JDK对hashcode进行了两次散列处理（核心目标就是为了分布更散更均，源码如下：
<img src="./pictures/Annotation 2019-11-07 195235.png"  div align=center />

（3）生成Entry对象
如上所述，一个Entry对象包含4部分：key对象、value对象、hash值、指向下一个Entry对象的用。我们现在算出了hash值。下一个Entry对象的引用为null。
（4）将Entry对象放到table数组中
如果本Entry对象对应的数组索引位置还没有放Entry对象，则直接将Entry对象存储进数组；如果对应索引位置已经有Entry对象，则将已有Entry对象的next指向本Entry对象，形成链表。
#### 总结
当添加一个元素（key-value）时，首先计算key的hash值，以此确定插入数组中的位置，但是可能在同一hash值的元素已经被放在数组同一位置了，这时就添加到同一hash值的元素的后面，他们在数组的同一位置，就形成了链表，同一个链表上的Hash值是相同的，所以说数组存放的是链表。
jdk8中 当链表长度大8时，链表就转换为红黑树这样大大提高了查找的效率

#### 取数据过程get（key）
我们需要通过key对象获得“键值对”对象，进而返回value对象。明白了存储数据过程，取数据就比较简单了，参见以下步骤：
（1）获得key的hashcode，通过hash）散列算法得到hash值，进而定位到数组的位置。
（2）在链表上挨个比较key对象。调用equals）方法，将key对象和链表上所有节点的key对象进行比较，直到碰到返回true的节点对象为止。
（3）返回equals）为true的节点对象的value对象。
明白了存取数据的过程，我们再来看一下hashcode）和equals方法的关系：
Java中规定，两个内容相同（equals）为true）的对象必须具有相等的hashCode。因为如果equals）
为true而两个对象的hashcode不同；那在整个存储过程中就发生了悖论。
#### 扩容问题
HashMap的位桶数组，初始大小为16。实际使用时，显然大小是可变的。如果位桶数组中的元素达到（0.75*数组length（初始12）），就重新调整数组大小变为原来2倍大小。
扩容很耗时。扩容的本质是定义新的更大的数组，并将旧数组内容挨个拷贝到新数组中。


#### HashMap和HashTable的区别
HashTable类和HashMap用法几乎一样，底层实现几乎一样，只不过HashTable的方法添加了synchronized关键字确保线程同步检查，效率较低。
1. HashMap与HashTable的区别1.HashMap：线程不安全，效率高。允许key或value为null。
2. HashTable：线程安全，效率低。不允许key或value为null。


## TreeMap
TreeMap是**红黑树**的典型实现。我们打开TreeMap的源码，发现里面有一行核心代码：

```java
private transient Entry<K,V> root = null;

root用来存储整个树的根节点。我们继续跟踪Entry（是TreeMap的内部类）的代码：
```
<img src="./pictures/Annotation 2019-11-07 215138.png"  div align=center />

可以看到里面存储了本身数据、左节点、右节点、父节点、以及节点颜色。TreeMap的put）/remove0方法大量使用了红黑树的理论。本书限于篇幅，不再展开。需要了解更深入的，可以参考专门的数据结构书籍。
TreeMap和HashMap实现了同样的接口Map，因此，用法对于调用者来说没有区别。HashMap效率高于TreeMap；在需要排序的Map时才选用TreeMap。

如果要实现按指定值排序则需要重写compareTo

和Collection接口一样可以通过迭代器Iterator遍历
<img src="./pictures/Annotation 2019-11-09 142820.png"  div align=center />

### Collections工具类

类java.util.Collections 提供了对Set、List.Map进行排序、填充、查找元素的辅助方法。
1. void sort（List）//对List容器内的元素排序，排序的规则是按照升序进行排序。
2. void shufle（List）//x对List容器内的元素进行随机排列。
3. void reverse（List）//对List容器内的元素进行逆续排列。
4. void fill（List，Object）//用一个特定的对象重写整个List容器。
5. int binarySearch（List，Object）//对于顺序的List容器，采用折半查找的方法查找特定对象。