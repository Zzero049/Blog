## GOF23
创建型模式：
* 单例模式、工厂模式、抽象工厂模式、建造者模式、原型模式。

结构型模式：是从程序的结构上实现松耦合，从而可以扩大整体的类结构，用来解决更大的问题。
* 适配器模式、桥接模式、装饰模式、组合模式、外观模式、享元模式、代理模式。

行为型模式：行为型模式关注系统中对象之间的相互交互， 研究系统在运行时对象之间的租互通信和作，进一步明确对象的职责，共11种模式。
* 模版方法模式、命令模式、迭代器模式、观察者模式、中介者模式、备忘录模式、解释器模式、状态模式、策略模式、职责链模式、访问者模式。

### 单例模式
保证一个类只有一个实例，并且提供一个访问该实例的全局访问点。

应用场景：
1. Windows的Task Manager（任务管理器）就是很典型的单例模式
1. windows的Recycle Bin（回收站）也是典型的单例应用。在整个系统运行过程中，回收站一直维护着仅有的一个实例。
1. 项目中，读取配置文件的类，一般也只有一个对象。没有必要每次使用配置文件数据，每次new一个对象去读取。
1. 网站的计数器，一般也是采用单例模式实现，否则难以同步。
1. 应用程序的日志应用，一般都何用单例模式实现，这一般是由于共享的日志文件一直处于打开状态，因为只能有一个实例去操作，否则内容不好追加。
1. 数据库连接池的设计一般也是采用单例模式，因为数据库连接是一种数据库资源。
1. 操作系统的文件系统，也是大的单例模式实现的具体例子，一个操作系统只能有一个文件系统。
1. Application 也是单例的典型应用（Servlet编程中会涉及到）
1. 在Spring中，每个Bean默认就是单例的，这样做的优点是Spring容器可以管理
1. 在servlet编程中，每个Servlet也是单例
1. spring MVC框架/struts1框架中，控制器对象也是单例

**优点**

* 由于单例模式只生成一个实例，减少了系统性能开销，当一个对象的产生需要比较多的资源时，如读取配置、产生其他依赖对象时，则可以通过在应用启动时直接产生一个单例对象，然后永久驻留内存的方式来解决
* 单例模式可以在系统设置全局的访问点，优化环共享资源访问，例如可以设计一个单例类，负责所有数据表的映射处理

**常见的五种单例模式实现方式：**
<img src="./pictures/Annotation 2019-12-07 192223.png"  div align=center />


主要；
* 饿汉式（线程安全，调用效率高。但是，不能延时加载。）
```java
public class SingletonDemo1 {
    //类初始化时，立即加载
private static SingletonDemo1 s = new SingletonDemo1();
//私有化构造器
private SingletonDemo1(){ }

public  static SingletonDemo1 getInstance(){
    return s;
    }
}
```
饿汉式单例模式代码中，static变量云在类装载时初始化，此时也不会涉及多个线程对象访问该对象的问题。虚拟机保证只会装载一次该类，肯定不会发生并发访问的问题。因此，可以省略synchronized关键字。

问题：如果只是加载本类，而不是要调用getinstance()，甚至永远没有调用，则会造成资源浪费！

* 懒汉式（线程安全，调用效率不高。但是，可以延时加载。）
```java
public class SingletonDemo02 {
    private static SingletonDemo02 s;

    private SingletonDemo02(){}
    //注意这里要加synchronized保证线程安全（饿汉法由于使用了类加载保证线程同步安全）
    public static synchronized SingletonDemo02 getInstance(){
        if(s==null){
            s = new SingletonDemo02();
        }
        return s;
    }
}

```
资源利用率高了。但是，每次调用getInstance()方法都要同步(考虑到高并发时，多个线程得到cpu都以为没有s对象，会创建多个s对象)，并发效率较低。

其他：
* 双重检测锁式（由于JVM底层内部模型原因，偶尔会出问题。不建议使用）
```java
public class SingletonDemo03 {
    private static SingletonDemo03 s=null;
    private SingletonDemo03(){}
    public static SingletonDemo03 getInstance(){
        if(s==null){
            SingletonDemo03 sc;
            synchronized (SingletonDemo03.class){
                sc = s;
                if(sc==null){
                    synchronized (SingletonDemo03.class){
                        if(sc==null){
                            sc = new SingletonDemo03();
                        }
                    }
                    s = sc;
                }
            }
        }
        return s;
    }
}

```

这个模式将同步内容下方到if内部，提高了执行的效率不必每次获取对象时都进行同步(双重检测)，只有第一次才同步,创建了以后就没必要了。

* 静态内部类式（线程安全，调用效率高。但是，可以延时加载） 
```java
public class SingletonDemo04 {
    private SingletonDemo04(){}
    //静态内部类
    private static class SingletonClassinstance{
        private static final SingletonDemo04 instance = new SingletonDemo04();
    }
    
    public static SingletonDemo04 getInstance(){
        return SingletonClassinstance.instance;
    }
}
```
1. 外部类没有static属性，则不会像饿汉式那样立即加载对象。
2. 只有真正调用getinstance()，才会加载静态内部类。加载类时是线程安全的。instance是static final类型，保证了内存中只有这样一个实例存在，而且只能被赋值一次，从而保证了线程安全性.
3. 兼备了并发高效调用和延迟加载的优势！

* 枚举单例（线程安全，调用效率高，不能延时加载）
```java
public enum SingletonDemo05 {
    //这个枚举元素本身就是一个单例,通过SingletonDemo05.INSTANCE使用
    INSTANCE;
    //添加自己需要的操作
    public void singletonOperation(){
    }
}
```
优点是实现简单，枚举本身就是单例模式。由JVM从根本上提供保障！避免通过反射和反序列化的漏洞！缺点是无延时加载。

效率对比：
<img src="./pictures/Annotation 2019-12-07 200142.png"  div align=center />
一般来说选择
需要加载延迟：静态内部类>懒汉式
不需要加载延迟：枚举>饿汉


##### 漏洞
但是，**反射、反序列化可以破解**上面几种（不包含枚举式）实现方式！（可以在构造方法中手动


```java
//反射跳过单例
public static void main(String[] args) throws ClassNotFoundException, NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {
        Class<SingletonDemo02> clazz = (Class<SingletonDemo02>) Class.forName("GOF23.SingletonDemo02");
        Constructor<SingletonDemo02> co = clazz.getDeclaredConstructor(null);
        co.setAccessible(true);
        SingletonDemo02 s1 = co.newInstance();
        SingletonDemo02 s2 = co.newInstance();

        System.out.println(s1);
        System.out.println(s2);
    }
```
<img src="./pictures/Annotation 2019-12-07 194337.png"  div align=center />

<br>对于这种情况，可以在对象构造器里面增加一条instance是否为空的判断，不为空则抛出异常</br>


```java
public static void main(String[] args) throws IOException, ClassNotFoundException {
    //反序列化跳过单例
        SingletonDemo02 s1 = SingletonDemo02.getInstance();
        System.out.println(s1);

        FileOutputStream fos = new FileOutputStream("H:/Desktop/abc.txt");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(s1);
        fos.close();
        oos.close();

        ObjectInputStream ois = new ObjectInputStream(new FileInputStream("H:/Desktop/abc.txt"));
        SingletonDemo02 s2 = (SingletonDemo02) ois.readObject();
        System.out.println(s2);

    }
```

<img src="./pictures/Annotation 2019-12-07 195435.png"  div align=center />

对于反序列化的漏洞，可以通过在单例类中定义readResolve()防止获得不同对象。
（反序列化时，如果对象所在类定义了readResolve()，（实际是一种回调），定义返回哪个对象。 ）
```java
private  Object readResolve(){
        return s;
    }
```
