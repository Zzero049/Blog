# 容器/集合(Collection)
数组就是一种容器，可以在其中放置对象或基本类型数据。
数组的优势：是一种简单的线性序列，可以快速地访问数组元素，效率高。如果从效率和类型检查的角度讲，数组是最好的
数组的劣势：不灵活。容量需要事先定义好，不能随着需求的变化而扩容。比如：我们在一个用户管理系统中，要把今天注册的所有用户取出来，那么这样的用户有多少个？我们在写程序时是无法确定的。因此，在这里就不能使用数组
<img src="./pictures/Annotation 2019-11-01 111404.png"  div align=center />

## 泛型
泛型的本质就是“数据类型的参数化”。我们可以把“泛型”理解为数据类型的一个占位符（形式参数），即告诉编译器，在调用泛型时必须传入实际类型。

我们可以在类的声明处增加泛型列表，如：<T，E，V>。
此处，字符可以是任何标识符，一般采用这3个字母。

```java
public class GenericT {
    public static void main(String[] args) {
        
        MyCollection<String> myCollection = new MyCollection<>();
        //设置泛型之后，必须都为设置的那种类型
        myCollection.set("小黑", 0);

        String b = myCollection.get(0);
        System.out.println(b);
    }
}

class MyCollection<E>{
    Object[] objs = new Object[5];

    public void set(E e, int index) {
        objs[index]= e;
    }

    public E get(int index){
        return (E) objs[index];
    }
}
```
## Collection接口
Collection表示一组对象，它是集中、收集的意思。Collection接口的两个子接口是List、Set接口
<img src="./pictures/Annotation 2019-11-01 203814.png"  div align=center />
由于List、Set是Collection的子接口，意味着所有List、Set的实现类都有上面的方法。



>**removeAll(Collection c)**
如a.removeAll(b),就是移除a中a，b都有的元素

>**retainAll(Collection c)**
如a.retainAll(b),就是只保留a中a，b都有的元素

### List
List是有序、可重复的容器。
**有序：** List中每个元素都有索引标记。可以根据元素的索引标记（在List中的位置）访问元素，从而精确控制这些元素。除指定位置的元素
**可重复：** List允许加入重复的元素。更确切地讲，List通常允许满足el.equals（e2）的元素重复加入容器。

List接口常用的实现类有3个：ArrayList（底层是数组，线程不安全）、LinkedList（底层是链表）和Vector（底层是数组，线程安全）。

1. 需要线程安全时，用Vector。
2. 不存在线程安全问题时，并且查找较多用ArrayList（一般使用它）。
3. 不存在线程安全问题时，增加或删除元素较多用LinkedList。

#### ArrayList
ArrayList底层是用数组实现的存储。特点：查询效率高，增删效率低，线程不安全。我们一般使用它。
数组长度是有限的而ArrayList是可以存放任意数量的对象，长度不受限制，通过数组扩容的方式实现，每当检查到数组满了，就扩大当前数组大小的一半。
实现代码
<img src="./pictures/Annotation 2019-11-01 212524.png"  div align=center />

#### LinkedList
LinkedList底层用**双向链表**实现的存储。特点：查询效率低，增删效率高，线程不安全。双向链表也叫双链表，是链表的一种，它的每个数据节点中都有两个指针，分别指向前一个节点和后一个节点。所以，从双向链表中的任意一个节点开始，都可以很方便地找到所有节点。

此图是老版本jdk的LinkedList为循环双链表，新版jdk是用双链表了
<img src="./pictures/Annotation 2019-11-02 162126.png"  div align=center />

#### Vector向量
Vector底层是用数组实现的List，相关的方法都加了同步检查，因此“线程安全，效率低”。比如，indexOf方法就增加了synchronized同步标记。
<img src="./pictures/Annotation 2019-11-07 165753.png"  div align=center />


### Set接口
Set接口继承自Collection，Set接口中没有新增方法，方法和Collection保持完全一致。我们在前面通过List学习的方法，在Set中仍然适用。因此，学习Set的使用将没有任何难度。
Set容器特点：**无序、不可重复**。无序指Set中的元素没有索引，我们只能遍历查找。不可重复指不允许加入重复的元素。更确切地讲，新元素如果和Set中某个元素通过equals()方法对比为true，则不能加入；甚至，Set中也只能放入一个null元素，不能多个。
Set常用的实现类有：HashSet、TreeSet等，我们一般使用HashSet。

#### HashSet
HashSet是采用哈希算法实现，底层实际是用HashMap实现的（HashSet本质就是一个简化版的HashMap），因此，查询效率和增删效率都比较高。我们来看一下HashSet的源码：
<img src="./pictures/Annotation 2019-11-07 221326.png"  div align=center />

我们发现里面有个map属性，这就是HashSet的核心秘密。我们再看add()方法，发现增加一个元素说白了就是在map中增加一个键值对，**键对象就是这个元素**，值对象是名为PRESENT的Object对象（常量）。

#### TreeSet
TreeSet底层实际是用TreeMap实现的，内部维持了一个简化版的TreeMap通过key来存储Set的元素。TreeSet内部需要对存储的元素进行排序，因此，我们对应的类需要实现Comparable接口。
这样，才能根据compareTo()方法比较对象之间的大小，才能进行内部排序。

可以通过迭代器Iterator遍历
<img src="./pictures/Annotation 2019-11-09 142432.png"  div align=center />
<img src="./pictures/Annotation 2019-11-09 142706.png"  div align=center />


### 表格数据存储
