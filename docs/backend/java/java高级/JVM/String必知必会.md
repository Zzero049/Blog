String必知必会



## 基本特点

- String：字符串，使用一对""引起来表示

  - `String s1 = "Hello"`		字面量定义方式
  - `String s2 = new String("Hello")`    对象的定义方式
  - 通过字面量的方式（区别于new）给一个字符串赋值，此时的字符串值声明在字符串常量池中，

- String声明为final的，不可被继承

- String实现了 Serializable接口：表示字符串是支持序列化的。

- String实现了 Comparable接口：表示 String可以比较大小

- String内部结构的优化

  - jdk8及以前内部定义了`final char value[] `用于存储字符串数据（数组是无法扩容的，final的指向不能改变，而数据可以改变）。
  - jdk9时改为`final byte[] value`，由于一个字符占用两个bit，对于英文字符来说是空间很浪费的，升级成byte可以将英文字符只占1bit，其他语言占2bit（如中文字符）

  

## 不可变性

- String：代表不可变的字符序列。简称：==**不可变性**==
  - 当对字符串重新赋值时，需要重写指定内存区域赋值，不能使用原有的 value进行赋值。

  ```java
  public void test1() {
          String s1 = "abc";
          String s2 = "abc";
          s1 = "hello";
          System.out.println(s1 == s2);//false，s1指向了新的字符串常量池位置
      }
  ```

  - 当对现有的字符串进行连接操作时，也需要重新指定内存区域赋值，不能使用原有的value进行赋值。

  ```java
  public void test2(){
          String s1 = "abc";
          String s2 = "abc";
          s1 += "def";
          System.out.println(s1 == s2);//false，s1指向了新的字符串常量池位置
      }
  ```

  - 当调用String的`replace()`方法修改指定字符或字符串时，也需要重新指定内存区域赋值，不能使用原有的 value进行赋值。

  ```java
  public void test3(){
          String s1 = "abc";
          String s2 = "abc";
          s1.replace('a', 'z');
          System.out.println(s1 == s2);//false，s1指向了新的字符串常量池位置
      }
  ```



先来看到一道笔试题，注意java就是值传递的https://blog.csdn.net/bntx2jsqfehy7/article/details/83508006，学到这里，要知道main调用change其实是有2个栈桢，main中str指向了"good"，change栈桢中str指向了"test ok"本质这两个str就不在同一张局部变量表

```java
public class StringExer {
    String str = new String("good");
    char[] ch = {'t','e','s','t'};

    public void change(String str,char ch[]){		// 形参涉及一次拷贝，把ex.str拷贝给str去操作，而数组是直接在原地址操作的
        str = "test ok";
        ch[0] = 'b';
    }

    public static void main(String[] args) {
        StringExer ex = new StringExer();
        ex.change(ex.str,ex.ch);
        System.out.println(ex.str);     // good
        System.out.println(ex.ch);      // best
    }
}
```



## 常量池不可重复性

==**字符串常量池中是不会存储相同内容的字符串的**==

Java语言规范里要求完全相同的字符串字面量，应该包含同样的 Unicode字符序列（包含同一份码点序列的常量），并且必须是指向同一个 String类实例。

**底层：**

- String的 String Pool，是一个**固定大小的 Hashtable**（数组+链表+数组无法扩容），默认值大小长度是1009。如果放进 string Pool的 String非常多，就会造成Hash冲突严重，从而导致链表会很长，而链表长了后直接会造成的影响就是当调用`String.intern()`时性能会大幅下降。
- 使用`-XX:StringTableSize`可设置 StringTable 的长度
  - 在jdk6中StringTable 是固定的，就是1009的长度，所以如果常量池中的字符串过多就会导致效率下降很快。StringtableSize设置没有限制
  - 在jdk7中，StringTable 的长度默认值是60013，下限没要求
  - 在jdk8中，默认值是60013，1009是可设置的最小值。



测试：

```java
public class StringTest2 {
    public static void main(String[] args) {
        System.out.println();
        System.out.println("1");
        System.out.println("2");
        System.out.println("3");
        System.out.println("4");
        System.out.println("1");
        System.out.println("2");
    }
}
```

可以看到一开始只有2165个String变量![image-20200606182725794](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200606182725794.png)

执行完也只加了4个

![image-20200606182807580](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200606182807580.png)



## 内存分配

在Java语言中有8种基本数据类型和一种比较特殊的类型 string。这些类型为了使它们在运行过程中速度更快、更节省内存，都提供了一种常量池的概念。

常量池就类似一个Java系统级别提供的缓存。8种基本数据类型的常量池都是系统协调的，**String类型的==常量池==比较特殊。它的主要使用方法有两种。**

- 直接使用双引号声明出来的 string对象会直接存储在常量池中比如：`String info="hello";`
- 如果不是用双引号声明的 string对象，可以使用 string提供的intern()方法。这个后面重点谈

Java6及以前，字符串常量池存放在永久代

Java7中 Oracle的工程师对字符串池的逻辑做了很大的改变，即将字符串常量池的位置调整到 Java堆内。

- **所有的字符串都保存在堆（Heap）中，和其他普通对象一样**，这样可以让你在进行调优应用时仅需要调整堆大小就可以了。
- 字符串常量池概念原本使用得比较多，但是这个改动使得我们有足够的理由让我们重新考虑在Java7中使用 `String.intern()`。

Java8元空间，**字符串常量存在堆**



**StringTable 为什么要调整？**

1. permsize默认比较小
2. 永久代垃圾回收频率低



## <font  color="red">字符串拼接操作</font>

规则

1. 字符串与字符串的拼接结果在字符串常量池，原理是编译期优化（"a"+"b"+"c"编译成class文件就等同于"abc"，final修饰且不存在变量的写法也会进行编译期优化）
2. 常量池中不会存在相同内容的常量
3. 只要其中有一个是变量（final修饰的不能算作这里说的变量，为常量引用），结果就在堆中（相当于新new了一个对象）。变量拼接的原理是 StringBuilder（补充：在jdk5.0之后使用的是 StringBuilder，在jdk5.0之前使用的是 StringBuffer）
4. 如果拼接的结果调用 `intern()`方法
   - 如果常量池没有，则主动将常量池中还没有的字符串对象放入池中，并返回此对象地址。
   - 如果常量池有，则直接返回常量池中该字符串地址



示例：

```java
public class StringTest3 {
    public static void main(String[] args) {
        String s1 = "Hello";
        String s2 = "World";

        String s3 = "HelloWorld";
        String s4 = "Hello" + "World";
        // 拼接前后出现变量，是使用StringBuilder创建一个对象进行append，再toString回来，具体内容为拼接结果
        String s5 = s1 + "World";
        String s6 = "Hello"+s2;
        /*
        类似如下操作：
        StringBuilder s = new StringBuilder();
        s.append("Hello");
        s.append("World");
        s.toString()---->类似于new String("HelloWorld");
        */
        String s7 = s1+s2;

        System.out.println(s3==s4); //true，编译器优化
        System.out.println(s3==s5); //false
        System.out.println(s3==s6); //false
        System.out.println(s3==s7); //false
        System.out.println(s5==s6); //false
        System.out.println(s6==s7); //false

        String s8 = s6.intern();
        System.out.println(s3==s8); //true

    }
}

```

s5创建过程的字节码如下：

看到是通过new 一个StringBuilder再append最后toString去完成拼接的操作

![image-20200606225355784](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200606225355784.png)

![image-20200606231853859](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200606231853859.png)



再来看看使用String进行拼接和StringBuilder进行拼接区别

```java
public class StringTest4 {

    public static void method1(int count){
        //只需要创建一个 StringBuilder
        StringBuilder s = new StringBuilder();
        for(int i=0;i<count;i++){
            s.append("a");
        }
    }
    public static void method2(int count){
        String s = "";
        for(int i=0;i<count;i++){
            s = s + "a";           //每次循环都会创建一个 StringBuilder、String,
            						//相当于各有10万个 StringBuilder、String
        }
    }

    public static void main(String[] args) {
        long start = System.currentTimeMillis();
        method1(100000);       // 10万次  StringBuilder  6ms
        method2(100000);       // 10万次 String   4329ms
        long end = System.currentTimeMillis();
        System.out.println("执行时间"+(end-start)+"ms");
    }
}
```

由于用String拼接涉及StringBuilder和String的创建（判断类加载、分配类内存、并发安全、初始化、设置对象头、执行构造方法），此外，还可能多次GC，因此String拼接远低于StringBuilder的append。

**总结**

体会执行效率：通过 StringBuilder的 append() 的方式添加字符审的效率要远高于使用 String的字符串拼接方式！

原因：

1、创建对象方面：

-  StringBuilder的 append() 的方式：自始至终中只创建过一个 StringBuilder的对象使用 
- String的字符拼接方式：创建过多个 StringBuilder和 String的对象

2、内存占用和GC

- 使用String的字符串拼接方式：内存中由于创建了较多的 StringBuilder和 String的对象，内存占用更大；如果进行GC，需要额外时间

StringBuilder还能进行优化，在实际开发中，如果基本确定要前前后后添加的字符串长度不高于某个限定值 highLevel的情况下，建议使用指定StringBuilder初始长度的构造方法，减少扩容的发生。如 `StringBuilder sb = new StringBuilder(1024);`



## <font  color="red">intern()的使用</font>

查看源码，发现是本地方法

```java
public native String intern();
```

阅读其说明：

```
Returns a canonical representation for the string object.
A pool of strings, initially empty, is maintained privately by the class String.
When the intern method is invoked, if the pool already contains a string equal to this String object as determined by the equals(Object) method, then the string from the pool is returned. Otherwise, this String object is added to the pool and a reference to this String object is returned.
It follows that for any two strings s and t, s.intern() == t.intern() is true if and only if s.equals(t) is true.
All literal strings and string-valued constant expressions are interned. String literals are defined in section 3.10.5 of the The Java™ Language Specification.

```

就是说字符串常量池初始是空的，是String类私有维护的

调用intern方法时，如果池已经包含等于equals（Object）方法确定的此String对象的字符串，则返回池中的字符串。否则，将此String对象添加到池中，并返回对此String对象的引用。因此，对于s和t的任何两个字符串，s.intern()= t.intern()为true 当且仅当s.equals(t)为true时。



如果不是用双引号（字面量）声明的 string对象，可以使用 String提供的 intern方法：intern方法会从字符串常量池中查询当前字符串是否存在，若不存在就会将当前字符串放入常量池中。

- 比如：`String myInfo= new String("I love JVM").intern()`

也就是说，如果在任意字符串上调用 String.intern()方法，那么其返回结果所指向的那个类实例，必须和直接以常量形式出现的字符串实例完全相同。因此，下列表达式的值必定是true：

`("a"+"b"+"c").intern() == "abc"`

通俗点讲，Interned String就是确保字符串在内存里（字符串常量池里）只有一份拷贝，这样可以节约内存空间，加快字符串操作任务的执行速度。注意，这个值会被存放在字符串内部池（String Intern Pool）。

**如何保证变量s指向的是字符串常量池中的数据呢？**

1. 使用字面量：`String s = "sss"`
2. 调用intern()：`String s = new String("sss").intern()`



**首先得明确一点， jdk7 及以后 字符串常量池 既可以保存 String 对象，又可以保存 String 对象的引用。**



**例题：**

**1、`new String("ab")` 会创建几个对象？**

​	不考虑之前有创建过"ab"，是2个

​	看字节码，一个对象是：new关键字在堆空间创建的；另一个对象是：ldc 指令在字符串常量池创建一个String对象

![image-20200607015839687](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200607015839687.png)



**2、`new String("a") + new String("b")`会创建几个对象？**

一共6个

	1. new StringBuilder 1个
 	2. new String("a")、new String("b") 各1个，共2个
 	3. `ldc #5 <a>` 和 `ldc #6 <b>` 即"a"、"b"也要在字符串常量池各放一份，共2个
 	4. StringBuilder的toString也会创建一个String("ab")，但不会触发ldc指令，即**常量池中没有"ab"**，共1个

![image-20200607004346305](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200607004346305.png)

但是Debug查看内存发现只加了3个，可以开启追踪，看到确实是多了5个，原因是idea无法追踪到字符串常量池的内容，拼接操作就隐藏常量池变化了

![image-20200607014135889](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200607014135889.png)

![image-20200608002539302](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200608002539302.png)

![image-20200608002519227](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200608002519227.png)

![image-20200608002742885](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200608002742885.png)

堆上的String对象事实上是可以看到的，可能字符串常量池虽然在堆中，但是和堆还是有一定区别的

![image-20200608002826328](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200608002826328.png)

**3、下面输出分别是什么（jdk6与jdk7/jdk8不同）**

```java
public class StringTest5 {
    public static void main(String[] args) {
        String s1 = new String("1");
        s1.intern();
        String s2 = "1";
        System.out.println(s1==s2);     //?

        String s3 = new String("1") + new String("1");
        s3.intern();
        String s4 = "11";
        System.out.println(s3==s4);         //?

    }
}
```

jdk6 false、false

jdk7/8 false、true

对于第一个判断，容易被`s1.intern();`误导，实际上调用该方法，不管字符串存不存在都会返回常量池"1"的地址，注意只是返回，s1的引用并没有被修改，因此s1和s2地址必然不同，修改`s1 = s1.intern();`结果就为true

对于第二个判断，`String s3 = new String("1") + new String("1");` 前面提到不会在常量池创建"11"

- 对于JDK6，字符串常量池在方法区中，执行`s3.intern()`，会在常量池创建一个"11"，然后严格判断二者地址是否相等，显然是不相等的，因此判断是false

![jdk6图](https://gitee.com/zero049/MyNoteImages/raw/master/4903ce64.png)

- 对于JDK7/8，字符串常量池在堆中，执行`s3.intern()`，不再是直接创建"11"，而是在字符串常量池添加一个对s3的引用，也就是这个s3指向的对象作为常量池的"11"对象，因此判断是true

![jdk7图1](https://gitee.com/zero049/MyNoteImages/raw/master/1bdc831a.png)

![jdk7图2](https://gitee.com/zero049/MyNoteImages/raw/master/425a283c.png)

- 拓展

  ```java
  public class StringTest7 {
      public static void main(String[] args) {
          String s3 = new String("1") + new String("1");
          String s4 = "11";
          s3.intern();
          System.out.println(s3==s4);         //?
      }
  }
  ```

  输出false，字面量形式在字符常量池中生成对象"11"，那么这两个地址是不同的



**总结**

 string的 intern()的使用

- jdk1.6中，将这个字符串对象尝试放入串池。
  - 如果串池中有，则并不会放入。返回已有的串池中的对象的地址
  - 如果没有，会把此**对象复制一份**，放入串池，并返回串池中的对象地址
- Jdk1.7起，将这个字符串对象尝试放入串池
  - 如果串池中有，则并不会放入。返回已有的串池中的对象的地址
  - 如果没有，则会把对象的**引用地址复制一份**，放入串池，并返回串池中的引用地址

- String s = new String("xx") 会触发 ldc，在字符串常量池创建一个"xx"对象，包括在堆中创建的"xx"，一共两个
- String s = new String("x") + new String("x") toString后不会触发ldc，在字符串常量池不存在一个"xx"对象。后面根据调用intern()或者字面量创建String的先后确定字符串常量池到底存的是引用还是对象



## intern()效率测试

用1000万条创建String对象

```java
public class StringInternTest {
    static final int MAX_COUNT = 1000 * 10000; // 1000万
    static final String[] arr = new String[MAX_COUNT];  //数组长度为1000万

    public static void main(String[] args) throws InterruptedException {
        Integer[] data = new Integer[]{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

        long start = System.currentTimeMillis();
        for (int i = 0; i < MAX_COUNT; i++) {   // 重复的存 1 2 3 4 5 6 7 8 9 10
            // 不使用intern
//            arr[i] = new String(String.valueOf(data[i % data.length]));
            //使用intern
            arr[i] = new String(String.valueOf(data[i % data.length])).intern();
        }

        long end = System.currentTimeMillis();

        System.out.println("执行时间："+(end-start)+"ms");
        TimeUnit.SECONDS.sleep(2000);
        System.gc();
    }
}
```



不使用intern可以看到有1000万以上的String实例对象

![image-20200607025042314](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200607025042314.png)



使用intern可以看到只有100万以上的String实例对象，而且运行速度更快，由于new String还是会创建堆，但是由于intern返回的引用是字符串常量池的引用，所以堆中的String类型是可以被回收的（没有被指向），因此查到的实例数会小

![image-20200607025911438](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200607025911438.png)



**垃圾回收查看**

想要查看字符串常量池的垃圾回收，需要设置：`-XX:+PrintStringTableStatistics` `-XX:+PrintGCDetails`



**G1的String去重操作**

背景：对许多Java应用（有大的也有小的）做的测试得出以下结果：

- 堆存活数据集合里面 string对象占了25%
- 堆存活数据集合里面重复的 string对象有13.5%
- String对象的平均长度是45

许多大规模的 Java应用的瓶颈在于内存，测试表明，在这些类型的应用里面，**Java堆中存活的数据集合差不多25%是 String对象**。更进一步这里面差不多一半 String对象是重复的，重复的意思是说：string1.equals(string2)=true。**堆上存在重复的 String对象必然是一种内存的浪费。**这个项目将在G1垃圾收集器中实现自动持续对重复的 String对象进行去重，这样就能避免浪费内存。

**实现：**

- 当垃圾收集器工作的时候，**会访问堆上存活的对象。对每一个访问的对象都会检查是否是候选的要去重的 String对象。**
- 如果是，把这个对象的一个引用插入到队列中等待后续的处理。一个去重的线程在后台运行，处理这个队列。处理队列的一个元素意味着从队列删除这个元素，然后尝试去重它引用的 String对象。
- 使用一个 hashtable来记录所有的被 string对象使用的不重复的char数组。当去重的时候，会查这个 hashtable，来看堆上是否已经存在一个一模一样的char数组
- 如果存在，string对象会被调整引用那个数组，释放对原来的数组的引用，最终会被垃圾收集器回收掉。
- 如果査找失败，char数组会被插入到 hashtable，这样以后的时候就可以共享这个数组了。

命令行选项

- UseStringDeduplication（bool）：开启 string去重，默认是不开启的，需要手动开启。

- PrintStringDeduplicationStatistics（bool）：打印详细的去重统计信息
- StringDeduplicationAgeThreshold（uinta）：达到这个年龄的 String对象被认为是去重的候选对象