# String 类
1. String类又称作**不可变字符序列**，不能通过下标访问。
2. String位于java.lang包中，Java程序默认导入java.lang包下的所有类。
3. Java字符串就是Unicode字符序列，例如字符串"Java"就是4个Unicode字符"J"、"a"、"v"、"e"组成的。
4. Java没有内置的字符串类型，而是在标准Java类库中提供了一个预定义的类String，每个用双引号括起来的字符串都是String类的一个实例。


<img src="./pictures/Annotation 2019-10-31 103303.png"  div align=center />
我们发现字符串内容全部存储到value[]数组中，而变量value是final类型的，也就是常量（即只能被赋值一次）。这就是“不可变对象”的典型定义方式。
我们发现在前面学习String的某些方法，比如：substring()是对字符串的截取操作，但本质是读取原字符串内容生成了新的字符串。
<br/>
</br>

```java
String a = "aaa";
String b = "aaa";
String c = new String("aaa");

System.out.println(a==b);//true
System.out.println(b==c);//flase
System.out.println(a.equals(c));//true
```

## 常用方法

> **a.charAt(3)** 
取下标为3的元素

> **a.length()** 
字符串长度

> **a.equals(b)** 
比较两个字符串是否相等

> **a.equalsIgnoreCase(b)** 
忽略大小写比较两个字符串是否相等

> **a.indexOf(b)** 
字符串a是否包含b，若不包含返回-1

> **a.replace('a','b')** 
将字符串a中的所有a换成b，但String类只能指向字符串常量，replace **看似“改变”** 字符串，但实际上是指向了新的字符串常量

> **a.startsWith("Hello")**
a字符串是否以Hello开头

> **a.endWith("Java!")**
字符串是否以Java！结尾

> **a.substring(4)**
提取子字符串：从下标为4的开始到字符串结尾为止
**a.substring(4, 7)**
提取子字符串，从下标[4, 7)不包括7

> **a.toLowerCase()**
转小写

> **a.toUpperCase()**
转大写

> **a.trim()**
去除字符串首尾的空格，只是首尾的

在遇到字符串常量之间的拼接时，编译器会做出优化，即在编译期间就会完成字符串的拼接。因此，在使用==进行String对象之间的比较时，我们需要特别注意，值的比较最好用equals。
<img src="./pictures/Annotation 2019-10-31 104425.png"  div align=center />

## StringBuilder类与StringBuffer类

由于String类是不可变序列，对内存不友好（改变字符串是通过new一个对象实现的），于是有StringBuilder和StringBuffer类，产生可变序列。StringBuilder线程不安全，效率高（一般使用它）；StringBuffer线程安全，效率低。

<img src="./pictures/Annotation 2019-10-31 110433.png"  div align=center />

String类和StringBuilder类在增加字符的情况下占用内存和花费时间对比
```java
public static void main(String[] args) {
        long num1 = Runtime.getRuntime().freeMemory();
        long time1 = System.currentTimeMillis();
        String str = "";
        for(int i=0;i<5000;i++){
            str = str +i;
        }
        long num2 = Runtime.getRuntime().freeMemory();
        long time2 = System.currentTimeMillis();

        System.out.println("String类使用内存"+(num1-num2));
        System.out.println("String类运行时间"+(time2-time1));

        long num3 = Runtime.getRuntime().freeMemory();
        long time3 = System.currentTimeMillis();
        StringBuilder string = new StringBuilder("");
        for(int i=0;i<5000;i++){
            string.append(i);
        }
        long num4 = Runtime.getRuntime().freeMemory();
        long time4 = System.currentTimeMillis();

        System.out.println("StringBuilder类使用内存"+(num3-num4));
        System.out.println("StringBuilder类运行时间"+(time4-time3));
    }
```

运行结果，一定不能这么写，程序在多次调用的话，内存会占满，然后崩溃
<img src="./pictures/Annotation 2019-10-31 112601.png"  div align=center />

