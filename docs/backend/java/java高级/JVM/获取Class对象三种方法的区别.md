# Class对象的获取区别

## 获取Class对象的三种方法

1. Class clazz = obj.getClass()/ new Object().getClass()
2. Class clazz = Object.class
3. Class.forName("java.lang.Object")

## 区别

为了更好的演示，我们先创建一个对象Person，对象内部定义了一个静态代码块，一个动态代码块和自定义构造方法。

```java
public class Person {

    static {
        System.out.println("Person：静态代码块");
    }
    {
        System.out.println("Person：动态代码块");
    }
    public Person(){
        System.out.println("Person：构造方法");
    }
}
```

针对上面的实例，我们构建了测试场景，对应代码如下：

```java
public class ClassDemo {
    public static void main(String[] args) throws ClassNotFoundException {
        Class clz1 = Person.class;
        // Class clz2 = new Person().getClass();
        // Class clz3 = Class.forName("org.example.ClassDemo.Person");
    }
}
```

Class clz1 = Person.class;的结果，没有打印任何东西

![image-20200618215523363](H:\Desktop\新建文件夹\Blog\docs\backend\java高级知识\JVM\pictures\image-20200618215523363.png)



Class clz2 = new Person().getClass();的结果，所有代码块和方法都打印了

![image-20200618215602707](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200618215602707.png)



Class clz3 = Class.forName("org.example.ClassDemo.Person");的结果，只打印了静态代码块

![image-20200618215656096](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200618215656096.png)



这里，我们比较一下三种形式获得的Class对象是否是相同的。测试代码如下：

```java
public class ClassDemo02 {
    public static void main(String[] args) throws ClassNotFoundException {
        Class<?> clz1 = Person.class;
        Class<?> clz2 = Class.forName("org.example.ClassDemo.Person");
        Class<?> clz3 = new Person().getClass();

        System.out.println(clz1 == clz2);       // true
        System.out.println(clz2 == clz3);       // true
    }
}
```

三种形式获得的Class对象是同一个对象。这是为什么呢？

这要涉及到类的加载过程，我们知道类加载过程分：加载阶段、连接阶段和初始化阶段。

类的加载阶段是将class文件中的二进制数据读取到内存中，然后将该字节流所代表的静态存储结构转化为方法区中运行时的数据结构，并且在堆内存中生成一个该类的java.lang.class对象，作为方法区数据结构的入口。

类加载阶段的最终产物是堆内存中的class对象，对于同一个Classloader对象，不管某个类被加载多少次，对应堆内存中的class对象始终只有一个。

也就是说无论通过哪种形式来获取Class对象，获得的都是堆内存中对应的Class对象。

## 结论

（1）类名.class：JVM将使用类装载器，将类装入内存(前提是:类还没有装入内存)，不做类的初始化工作，返回Class的对象。

（2）Class.forName("类名字符串")：装入类，并做类的静态初始化，返回Class的对象。

（3）实例对象.getClass()：对类进行静态初始化、非静态初始化；返回引用运行时真正所指的对象(子对象的引用会赋给父对象的引用变量中)所属的类的Class的对象。