# JUC

![](https://gitee.com/zero049/MyNoteImages/raw/master/20190906233141903.png)

JUC就是java.util .concurrent工具包的简称。这是一个处理线程的工具包，JDK 1.5开始出现的。

![image-20200515202202288](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200515202202288.png)

## 一些前置知识问题：

**1、java默认有几个线程呢？**

- 2个，一个main线程，一个GC线程

**2、java真的可以开启线程吗**

- 不能，可以看到start()实际是调用了start0()这个本地方法

```java
	public synchronized void start() {
      
        if (threadStatus != 0)
            throw new IllegalThreadStateException();


        group.add(this);

        boolean started = false;
        try {
            start0();
            started = true;
        } finally {
            try {
                if (!started) {
                    group.threadStartFailed(this);
                }
            } catch (Throwable ignore) {
              
            }
        }
    }
	//本地方法，底层的c++，java无法直接操作硬件
	private native void start0();
```

**3、java线程有几个状态**

6个，没有就绪态分为了两个等待

```java
public enum State {
        /**
         * Thread state for a thread which has not yet started.
         */
        NEW,			//线程新生

        RUNNABLE,		//运行

        BLOCKED,		//阻塞

        WAITING,		//等待，死等

        TIMED_WAITING,	//超时等待，约定等多久

        TERMINATED;		//终止
    }
```

**4、sleep和wait的区别**

- 来自类：sleep是Thread类下的方法，而wait来自Object类

- 锁的释放：wait会释放锁，sleep不会
- 使用范围：wait只能在synchronize同步代码块用，sleep可以任意位置
- 捕获异常：sleep需要捕获异常，wait不需要

为了代码的可读性，优先使用TimeUnit.xxx.sleep()而不是Thread.sleep()，这样能明确知道睡眠的单位是具体时间

## Callable

Callable接口类似于 Runnable，因为它们都是为其实例可能由另一个线程执行的类设计的。然而，A Runnable不返回结果，也不能抛出被检查的异常。

与Runnable区别

1、可以有返回值，参数的泛型就是返回值类型

2、可以抛出异常

3、方法不同，run())/call()



Thread只接收Runnable类型的参数

![image-20200516140404253](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516140404253.png)

![image-20200516140956753](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516140956753.png)

```java
public class CallableTest01 {
    public static void main(String[] args) {
        // new Thread(new RunnabLe ()).start();
        // new Thread (new Future Task<v>()).start()
        // new Thread (new Future Task<v>(Callable )).start()
        MyThread01 myThread01 = new MyThread01();
        FutureTask futureTask = new FutureTask(myThread01);
        new Thread(futureTask,"A").start();
        new Thread(futureTask,"B").start();  //结果会被缓存,就不执行call了
        try {
            String result = (String) futureTask.get();      //get方法可能会产生阻塞，把他放在代码最后
            System.out.println("FutureTask取到结果"+result);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }

    }
}

class MyThread01 implements Callable<String> {
    @Override
    public String call() throws Exception {
        System.out.println(Thread.currentThread().getName()+"  执行");
        return "Test Callable";
    }
}
```

![image-20200516142132669](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516142132669.png)

细节:

1、有缓存

2、结果可能需要等待，会阻塞！

## <font color="red">Lock锁(重要)</font>

java.util.concurrent.locks 包下 的接口

![image-20200515224544730](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200515224544730.png)

 Lock接口下有三个是实现类如下![image-20200515211123611](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200515211123611.png)



### ReentrantLock(独占锁)

先看看用synchronized修饰成员方法实现并发访问

```java
public class LockTest02 {
    public static void main(String[] args) {
        Ticket02 ticket = new Ticket02();
        new Thread(()->{
            for(int i=0;i<20;i++){
                ticket.sale();
            }
        },"ThreadA").start();

        new Thread(()->{
            for(int i=0;i<20;i++){
                ticket.sale();
            }
        },"ThreadB").start();
        new Thread(()->{
            for(int i=0;i<20;i++){
                ticket.sale();
            }
        },"ThreadC").start();
    }
}
class Ticket02{
    private int number = 30;
    public synchronized void sale(){
        if(number>0){
            System.out.println(Thread.currentThread().getName()+"卖出了票"+"剩余"+(--number));
        }
    }
}
```

再看看Lock实现类ReentrantLock的实现

```java
public class LockTest01 {
    public static void main(String[] args) {
        Ticket01 ticket = new Ticket01();

        new Thread(()->{
            for(int i=0;i<20;i++){
                ticket.sale();
            }
        },"ThreadA").start();

        new Thread(()->{
            for(int i=0;i<20;i++){
                ticket.sale();
            }
        },"ThreadB").start();
        new Thread(()->{
            for(int i=0;i<20;i++){
                ticket.sale();
            }
        },"ThreadC").start();

    }
}


class Ticket01{

    private int number = 30;
    Lock lock = new ReentrantLock();
    
    public void sale(){
        lock.lock();		//获取锁
        if(number>0){
            System.out.println(Thread.currentThread().getName()+"卖出了票"+"剩余"+(--number));
        }
        lock.unlock();		//释放锁
    }
}
```

可以看到源码ReentrantLock默认是非公平锁（不按线程阻塞顺序唤醒）

![image-20200515212038232](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200515212038232.png)



#### **synchronized和Lock的区别**

- 本质区别：synchronized是java的关键字，Lock是JUC下的一个接口
- 特征区别：synchronized可重入锁、非公平的；Lock可重入锁、默认非公平，也可以设置成公平的
- 锁的状态：synchronized无法获取锁的状态，Lock可以判断是否取到了锁
- 锁的释放：synchronized会自动释放锁（monitorenter、monitorexit），lock必须要手动释放锁，否则会造成**死锁**
- 锁的范围：synchronized可以锁方法、代码块，Lock只能锁代码块
- 阻塞线程：synchronized线程竞争会阻塞，继续等待，Lock线程阻塞不一定继续等待

- 适用场景：synchronized适合竞争激烈的环境，Lock适合竞争少的环境



### ReadWriteLock（写独占，读共享）

![image-20200516162308318](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516162308318.png)



```java
public class ReadWriteLockDemo {
    public static void main(String[] args) {


        MyCache myCache = new MyCache();
        /**
         * 5个读线程，5个写线程
         * 读-读  可以共存
         * 读-写  不能共存
         * 写-写  不能共存
         */
        for (int i = 1; i <= 5; i++) {  //写线程
            int temp = i;
            new Thread(()->{
                myCache.put(String.valueOf(temp),temp);
            },"Thread-"+i).start();
        }


        for (int i = 1; i <= 5; i++) {  //读线程
            int temp = i;
            new Thread(()->{
                myCache.get(String.valueOf(temp));
            },"Thread-"+i).start();
        }
    }
}


class MyCache {
    private volatile Map<String, Object> map = new HashMap<>();
    //读写锁，更加细粒度的控制
    private ReadWriteLock lock = new ReentrantReadWriteLock();
    /**
     * 存，写操作，写入时，只希望只有一个线程写
     */
    public void put(String key, Object val) {
        lock.writeLock().lock();    //写锁
        try{
            System.out.println(Thread.currentThread().getName() + "正在写入" + key);
            map.put(key, val);
            System.out.println(Thread.currentThread().getName() + " 写入OK");
        }finally {
            lock.writeLock().unlock();
        }

    }

    /**
     * 取，读操作，所有线程可以读
     */
    public void get(String key) {
        lock.readLock().lock();
        try{
            System.out.println(Thread.currentThread().getName() + "正在读取" + key);
            map.get(key);
            System.out.println(Thread.currentThread().getName() + "读取OK");
        }finally {
            lock.readLock().unlock();
        }

    }
}
```



### 生产者消费者问题（synchronized）

使用synchronized实现生产者加1，消费者减1，让其维持在0-1之间，当只有一个生产者一个消费者时，代码正常，但是多个生产者消费者则出现**虚假唤醒**

```java
public class PCDemo01 {
    public static void main(String[] args) {
        Data data = new Data();
        new Thread(() -> {    //生产者线程
            for (int i = 0; i < 10; i++) {
                try {
                    data.increment();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }, "生产者1").start();
        new Thread(() -> {    //消费者线程
            for (int i = 0; i < 10; i++) {
                try {
                    data.decrement();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }, "消费者1").start();
        new Thread(() -> {    //生产者线程
            for (int i = 0; i < 10; i++) {
                try {
                    data.increment();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }, "生产者2").start();
        new Thread(() -> {    //消费者线程
            for (int i = 0; i < 10; i++) {
                try {
                    data.decrement();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }, "消费者2").start();
    }
}


class Data {
    private int number = 0;

    /**
     * 生产者自增1
     *
     * @throws InterruptedException
     */
    public synchronized void increment() throws InterruptedException {
        if (number != 0) {
            this.wait();
        }
        number++;
        System.out.println(Thread.currentThread().getName() + "==>" + number);
        this.notifyAll();
    }

    /**
     * 消费者自减1
     *
     * @throws InterruptedException
     */
    public synchronized void decrement() throws InterruptedException {
        if (number == 0) {
            this.wait();
        }
        number--;
        System.out.println(Thread.currentThread().getName() + "==>" + number);
        this.notifyAll();
    }
}
```

![image-20200515221203478](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200515221203478.png)

![image-20200515221702732](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200515221702732.png)

把increment和decrement方法的if判断改成while即可

```java
while (number == 0) {
            this.wait();
        }
```

原因是这样的，假设生产者1获取了锁，不满足num != 0，执行wait交出锁，然后假设是生产者2获得了这个锁，也不满足而执行wait交出锁，当他们再次获得锁的时候，会从wait语句之后往下执行，也就是if判断无效了，num经历这两个线程操作后，会+2，而不是原有的生产消费交替执行。而且可能最终程序会仅剩一个进程由于进入了方法判断了num的值而执行wait却没有其他线程notify，发生**饥饿**。

如果条件判断改成循环语句，则每次再次获取锁都会再判断是不是满足wait条件。



### 生产者消费者问题（Lock）

Lock与synchronized 阻塞和唤醒实现区别:

![image-20200515231602201](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200515231602201.png)

```java
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class PCDemo02 {
    public static void main(String[] args) {
        Data02 data = new Data02();
        new Thread(() -> {    //生产者线程
            for (int i = 0; i < 10; i++) {
                try {
                    data.increment();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }, "生产者1").start();
        new Thread(() -> {    //消费者线程
            for (int i = 0; i < 10; i++) {
                try {
                    data.decrement();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }, "消费者1").start();
        new Thread(() -> {    //生产者线程
            for (int i = 0; i < 10; i++) {
                try {
                    data.increment();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }, "生产者2").start();
        new Thread(() -> {    //消费者线程
            for (int i = 0; i < 10; i++) {
                try {
                    data.decrement();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }, "消费者2").start();
    }
}


class Data02 {
    private int number = 0;
    Lock lock = new ReentrantLock();
    Condition condition = lock.newCondition();      //代替了原本wait、signal的监听器

    /**
     * 生产者自增1
     *
     * @throws InterruptedException
     */
    public  void increment() throws InterruptedException {
        lock.lock();
        try{
            while (number != 0) {       //同样用if有虚假唤醒的问题
                condition.await();
            }
            number++;
            System.out.println(Thread.currentThread().getName() + "==>" + number);
            condition.signalAll();
        }finally {
            lock.unlock();
        }

    }

    /**
     * 消费者自减1
     *
     * @throws InterruptedException
     */
    public  void decrement() throws InterruptedException {
        lock.lock();
        try{
            while (number == 0) {//同样用if有虚假唤醒的问题
                condition.await();
            }
            number--;
            System.out.println(Thread.currentThread().getName() + "==>" + number);
            condition.signalAll();
        }finally {
            lock.unlock();
        }
    }
}
```

![image-20200515231346054](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200515231346054.png)



可以利用Condition精准通知和唤醒线程

```java
public class PCDemo03 {
    public static void main(String[] args) {
        Producer01 producer01 = new Producer01();

        new Thread(()->{
            for(int i=0;i<10;i++){
                producer01.ProduceA();
            }
        },"A").start();
        new Thread(()->{
            for(int i=0;i<10;i++){
                producer01.ProduceB();
            }
        },"B").start();
        new Thread(()->{
            for(int i=0;i<10;i++){
                producer01.ProduceC();
            }
        },"C").start();
    }
}


class Producer01 {
    private int number = 1;
    private Lock lock = new ReentrantLock();

    private Condition conditionA = lock.newCondition();
    private Condition conditionB = lock.newCondition();
    private Condition conditionC = lock.newCondition();

    // 假设生产线是A->B->C
    public void ProduceA() {
        lock.lock();
        try {
            while (number != 1) {
                conditionA.await();     //等待
            }
            number = 2;
            System.out.println(Thread.currentThread().getName()+"====>AAAA");
            conditionB.signal();           //唤醒指定的线程，B
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }

    public void ProduceB() {
        lock.lock();
        try {
            while (number != 2) {
                conditionB.await();//等待
            }
            number = 3;
            System.out.println(Thread.currentThread().getName()+"====>BBBB");
            conditionC.signal();//唤醒指定的线程，C
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }

    void ProduceC() {
        lock.lock();
        try {
            while (number != 3) {
                conditionC.await();//等待
            }
            number = 1;
            System.out.println(Thread.currentThread().getName()+"====>CCCC");
            conditionA.signal();//唤醒指定的线程，A
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }
}
```



### synchronized锁作用范围

- 修饰实例方法: 作用于当前**对象加锁**，进入同步代码前要获得当前对象实例的锁
- 修饰代码块: 指定加锁对象，对给定**对象或类加锁**，进入同步代码库前要获得给定对象或类的锁。
- 修饰静态方法: 也就是给**当前类加锁**，会作用于类的所有对象实例，因为静态成员不属于任何一个实例对象，是类成员（ static 表明这是该类的一个静态资源，不管new了多少个对象，只有一份）。所以如果一个线程A调用一个实例对象的非静态 synchronized 方法，而线程B需要调用这个实例对象所属类的静态 synchronized 方法，是允许的，不会发生互斥现象，因为访问静态 synchronized 方法占用的锁是当前类的锁，而访问非静态 synchronized 方法占用的锁是当前实例对象锁。（例如，锁的是Demo.class这个类对象）

- 普通方法不受锁的约束，可以正常访问

即使是锁类，实际上也是锁这个类的Class对象，举个例子，两个线程，跑的是同一个对象的同步静态方法（静态方法做了4秒延迟），再延迟1秒后跑同步实例方法，然后先输出的一定是同步实例方法，由于他们锁的对象是不一样的（实例对象、Class类对象）



## 不安全的集合类

如ArrayList，我们都知道ArrayList不是线程安全的，可以查看源码得到答案

```java
public boolean add(E e) {

    /**
     * 添加一个元素时，做了如下两步操作
     * 1.判断列表的capacity容量是否足够，是否需要扩容
     * 2.真正将元素放在列表的元素数组里面
     */
    ensureCapacityInternal(size + 1);  // Increments modCount!!
    elementData[size++] = e;
    return true;
}

```

ensureCapacityInternal()这个方法的详细代码我们可以暂时不看，它的作用就是判断如果将当前的新元素加到列表后面，列表的elementData数组的大小是否满足，如果size + 1的这个需求长度大于了elementData这个数组的长度，那么就要对这个数组进行扩容。

由此看到add元素时，实际做了两个大的步骤：

1. 判断elementData数组容量是否满足需求
2. 在elementData对应位置上设置值

这样也就出现了第一个导致线程不安全的隐患，在多个线程进行add操作时可能会导致elementData数组越界。具体逻辑如下：

1. 假设列表大小为10，即size=10

2. 线程A开始进入add方法，这时它获取到size的值为10，调用ensureCapacityInternal方法进行容量判断。

3. 线程B此时也进入add方法，它获取到size的值也为10，也开始调用ensureCapacityInternal方法。

4. 线程A发现需求大小为10，而elementData的大小就为10，可以容纳。于是它不再扩容，返回。

5. 线程B也发现需求大小为10，也可以容纳，返回。

6. 线程A开始进行设置值操作， elementData[size++] = e 操作。此时size变为10。

7. 线程B也开始进行设置值操作，它尝试设置elementData[10] = e，而elementData没有进行过扩容，它的下

   标最大为9。于是此时会报出一个数组越界的异常ArrayIndexOutOfBoundsException.

另外第二步 elementData[size++] = e 设置值的操作同样会导致线程不安全。从这儿可以看出，这步操作也不是一个原子操作，它由如下两步操作构成：

1. elementData[size] = e;
2. size = size + 1;

在单线程执行这两条代码时没有任何问题，但是当多线程环境下执行时，可能就会发生一个线程的值覆盖另一个线程添加的值，具体逻辑如下：

1. 列表大小为0，即size=0
2. 线程A开始添加一个元素，值为A。此时它执行第一条操作，将A放在了elementData下标为0的位置上。
3. 接着线程B刚好也要开始添加一个值为B的元素，且走到了第一步操作。此时线程B获取到size的值依然为0，于是它将B也放在了elementData下标为0的位置上。
4. 线程A开始将size的值增加为1
5. 线程B开始将size的值增加为2

这样线程AB执行完毕后，理想中情况为size为2，elementData下标0的位置为A，下标1的位置为B。而实际情况变成了size为2，elementData下标为0的位置变成了B，下标1的位置上什么都没有。并且后续除非使用set方法修改此位置的值，否则将一直为null，因为size为2，添加元素时会从下标为2的位置上开始。



解决ArrayList不安全的三种策略：

```java
public class ListTest {
    public static void main(String[] args) {
        /**
         *  可能会出现java.util.ConcurrentModificationException 并发修改异常
         *
         *  解决方案：
         *  1、List<String> list = new Vector<>();   (不是特别好的方案)
         *  2、List<String> list = Collections.synchronizedList(new ArrayList<>());
         *  3、List<String> list = new CopyOnWriteArrayList<>();
         */

//        List<String> list = new ArrayList<>();
//        List<String> list = new Vector<>();
//        List<String> list = Collections.synchronizedList(new ArrayList<>());
        List<String> list = new CopyOnWriteArrayList<>();
        for (int i = 1; i <= 10; i++) {
            new Thread(() -> {
                list.add(UUID.randomUUID().toString().substring(0, 5));
                System.out.println(list);
            }, String.valueOf(i)).start();
        }
    }
}

```

HashSet底层是基于HashMap实现的，HashSet的元素都是HashMap的key，value为PRESENT，不安全的原因和ArrayList是相似的，就是两个线程拿到了同一份集合长度和元素位置。

```java
public class SetTest {
    public static void main(String[] args) {
        /**
         * 同样，可能会出现java.util.ConcurrentModificationException 并发修改异常
         * 解决方案：
         * 1、Set<String> set= Collections.synchronizedSet(new HashSet<>());
         * 2、Set<String> set= new CopyOnWriteArraySet<>();
         */
//        Set<String> set= new HashSet<>();
//        Set<String> set= Collections.synchronizedSet(new HashSet<>());
        Set<String> set= new CopyOnWriteArraySet<>();
        for(int i=0;i<20;i++){  //20个线程去给set add元素
            new Thread(()->{
                set.add(UUID.randomUUID().toString().substring(0, 5));
                System.out.println(set);
            }).start();
        }
    }
}
```

```java
public class MapTest {
    public static void main(String[] args) {
        //map是这样用的吗？不是，工作中不用 HashMap
        //以初始容量为16，装填因子为0.75默认值创建HashMap
		//Map<String,String> map = new HashMap<>();   //等价于new HashMap<>(16,0.75);
        Map<String,String> map = new ConcurrentHashMap<>();
        for(int i=0;i<20;i++){
            new Thread(()->{
                map.put(Thread.currentThread().getName(), UUID.randomUUID().toString().substring(0, 5));
                System.out.println(map);
            },String.valueOf(i)).start();
        }
    }
}
```

## 安全的集合类

### CopyOnWriteArrayList

虽说他一定程度是线程安全的，采用的Lock实现独占(JDK1.8)，且读不加锁，而Vector是使用synchronized实现的,CopyOnWriteArrayList是根据写入时复制实现的，避免读取时，又发生写入覆盖的情况，造成数据问题，我们可以看他的add方法

```java
public boolean add(E e) {
        final ReentrantLock lock = this.lock;
        lock.lock();
        try {
            Object[] elements = getArray();
            int len = elements.length;
            Object[] newElements = Arrays.copyOf(elements, len + 1);	//拷贝一份
            newElements[len] = e;
            setArray(newElements);
            return true;
        } finally {
            lock.unlock();
        }
    }
```

而读的时候不需要加锁，如果读的时候有多个线程正在向CopyOnWriteArrayList添加数据，读还是会读到旧的数据，因为开始读的那一刻已经确定了读的对象是旧对象（比如一个线程正在改，另一个再读，只要读线程不在调用setArray(newElements)之后读，读都是取到旧数组）。CopyOnWrite并发容器用于**读多写少**的并发场景。比如白名单，黑名单等场景。

**缺点：**

**1、 内存占用问题**。因为CopyOnWrite的写时复制机制，所以在进行写操作的时候，内存里会同时驻扎两个对象的内存，旧的对象和新写入的对象（注意:在复制的时候只是复制容器里的引用，只是在写的时候会创建新对象添加到新容器里，而旧容器的对象还在使用，所以有两份对象内存）。如果这些对象占用的内存比较大，比如说200M左右，那么再写入100M数据进去，内存就会占用300M，那么这个时候很有可能造成频繁的Yong GC和Full GC。之前我们系统中使用了一个服务由于每晚使用CopyOnWrite机制更新大对象，造成了每晚15秒的Full GC，应用响应时间也随之变长。

　　针对内存占用问题，可以通过压缩容器中的元素的方法来减少大对象的内存消耗，比如，如果元素全是10进制的数字，可以考虑把它压缩成36进制或64进制。或者不使用CopyOnWrite容器，而使用其他的并发容器，如ConcurrentHashMap。

**2、数据一致性问题**。CopyOnWrite容器只能保证数据的最终一致性，不能保证数据的实时一致性。所以如果你希望写入的的数据，马上能读到，请不要使用CopyOnWrite容器。



### CopyOnWriteArraySet

注意是ArraySet，不是HashSet，底层是基于CopyOnWriteArrayList实现的，实际上基本在调CopyOnWriteArrayList的方法。

```java
//CopyOnWriteArraySet 源码	
	public CopyOnWriteArraySet() {
        al = new CopyOnWriteArrayList<E>();
    }

	public boolean add(E e) {
        return al.addIfAbsent(e);
    }
```

```java
//CopyOnWriteArrayList 源码		
	public boolean addIfAbsent(E e) {	//判断是否有该元素
        Object[] snapshot = getArray();
        return indexOf(e, snapshot, 0, snapshot.length) >= 0 ? false :
            addIfAbsent(e, snapshot);
    }
	private boolean addIfAbsent(E e, Object[] snapshot) {
        final ReentrantLock lock = this.lock;
        lock.lock();
        try {
            Object[] current = getArray();
            int len = current.length;
            if (snapshot != current) {
                // Optimize for lost race to another addXXX operation
                int common = Math.min(snapshot.length, len);
                for (int i = 0; i < common; i++)
                    if (current[i] != snapshot[i] && eq(e, current[i]))
                        return false;
                if (indexOf(e, current, common, len) >= 0)
                        return false;
            }
            Object[] newElements = Arrays.copyOf(current, len + 1);
            newElements[len] = e;
            setArray(newElements);
            return true;
        } finally {
            lock.unlock();
        }
    }
```



### ConcurrentHashMap  TODO:再深入理解jdk1.8 put、get、size发生扩容的处理原理

先看看线程安全的Hashtable是怎么做的：

HashTable几乎在所有获取map信息的方法（size(),put(),get()）都用了synchronized修饰，相当于给整个Entry数组全表锁（HashTable不是基于JDK1.8HashMap静态内部类Node的数组实现的，而是JDK1.7HashMap静态内部类Entry的数组实现），但实际上是非常**低效**的，因为**即使另一个线程put方法不发生冲突，也不能完成put操作**。（读操作get也是阻塞的）

![image-20200516110824929](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516110824929.png)

再看看ConcurrentHashMap是如何做的：

**JDK1.7 采用Segment + HashEntry + ReentrantLock实现线程安全**

参考https://www.jianshu.com/p/865c813f2726

在这里ConcurrentHashMap在维护Segment数组和HashEntry数组无论在初始化操作和数组下标映射都和HashMap有很大差别

![image-20200516114205148](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516114205148.png)

![image-20200516122342359](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516122342359.png)

**get操作**

**不需要加锁：**get方法里将要使用的共享变量都定义成**volatile**，如用于统计当前Segement大小的count字段和用于存储值的HashEntry的value。定义成volatile的变量，能够在线程之间保持可见性，能够被多线程同时读，并且保证不会读到过期的值，但是只能被单线程写（有一种情况可以被多线程写，就是写入的值不依赖于原值），在get操作里只需要读不需要写共享变量count和value，所以可以不用加锁。

**put操作**

```java
static class  Segment<K,V> extends  ReentrantLock implements  Serializable {
}
```

从上Segment的继承体系可以看出，Segment实现了ReentrantLock,也就带有锁的功能，当执行put操作时，会进行第一次key的hash来定位Segment的位置，如果该Segment还没有初始化，即通过CAS操作进行赋值，然后进行第二次hash操作，找到相应的HashEntry的位置，这里会利用继承过来的锁的特性，在将数据插入指定的HashEntry位置时（链表的尾端），会通过继承**ReentrantLock的tryLock()**方法尝试去获取**对应数组位置的Segmentm锁**，如果获取成功就直接插入相应的位置，如果已经有线程获取该Segment的锁，那当前线程会以自旋的方式去继续的调用tryLock（）方法去获取锁，超过指定次数就挂起，等待唤醒

**size操作**

计算ConcurrentHashMap的元素大小是一个有趣的问题，因为他是并发操作的，就是在你计算size的时候，他还在并发的插入数据，可能会导致你计算出来的size和你实际的size有相差（在你return size的时候，插入了多个数据），要解决这个问题，JDK1.7版本用两种方案

1、第一种方案他会使用不加锁的模式去尝试多次计算ConcurrentHashMap的size，最多三次，比较前后两次计算的结果，结果一致就认为当前没有元素加入，计算的结果是准确的

2、第二种方案是如果第一种方案不符合，他就会给每个Segment加上锁，然后计算ConcurrentHashMap的size返回



**JDK1.8 采用采用Node + CAS + Synchronized实现线程安全，放弃了Segment臃肿的设计**



![image-20200516120440317](F:\Project\cscode\markdown\Java面试\JUC\pictures\image-20200516120440317.png)

**get操作**

1. 计算hash值，定位到该table索引位置，如果是首节点符合就返回
2. 如果遇到扩容的时候，会调用标志正在扩容节点ForwardingNode的find方法，查找该节点，匹配就返回
3. 以上都不符合的话，就往下遍历节点，匹配就返回，否则最后就返回null

**put操作**

1. 如果没有初始化就先调用initTable（）方法来进行初始化过程
2. 如果没有hash冲突就直接CAS插入
3. 如果还在进行扩容操作就先进行扩容
4. 如果存在hash冲突，就**加锁synchronized**来保证线程安全，这里有两种情况，一种是链表形式就直接遍历到尾端插入，一种是红黑树就按照红黑树结构插入，
5. 最后一个如果该链表的数量大于阈值8，就要先转换成黑红树的结构，break再一次进入循环
6. 如果添加成功就调用addCount（）方法统计size，并且检查是否需要扩容

**size操作**

在JDK1.8版本中，对于size的计算，在扩容和addCount()方法就已经有处理了，JDK1.7是在调用size()方法才去计算，其实在并发集合中去计算size是没有多大的意义的，因为size是实时在变的

```java
public int size() {
        long n = sumCount();
        return ((n < 0L) ? 0 :
                (n > (long)Integer.MAX_VALUE) ? Integer.MAX_VALUE :
                (int)n);
    }
```

对比总结：

其实可以看出JDK1.8版本的ConcurrentHashMap的数据结构已经接近HashMap，相对而言，ConcurrentHashMap只是增加了同步的操作来控制并发，从JDK1.7版本的ReentrantLock+Segment+HashEntry，到JDK1.8版本中synchronized+CAS+Node+红黑树,相对而言，总结如下思考

1. **JDK1.8的实现降低锁的粒度，JDK1.7版本锁的粒度是基于Segment的，包含多个HashEntry，而JDK1.8锁的粒度就是HashEntry（首节点）**
2. JDK1.8版本的数据结构变得更加简单，使得操作也更加清晰流畅，因为已经使用synchronized来进行同步，所以不需要分段锁的概念，也就不需要Segment这种数据结构了，由于粒度的降低，实现的复杂度也增加了
3. JDK1.8使用红黑树来优化链表，基于长度很长的链表的遍历是一个很漫长的过程，而红黑树的遍历效率是很快的，代替一定阈值的链表，这样形成一个最佳拍档
4. JDK1.8为什么使用内置锁synchronized来代替重入锁ReentrantLock，我觉得有以下几点
   1. 因为粒度降低了，在相对而言的低粒度加锁方式，synchronized并不比ReentrantLock差，在粗粒度加锁中ReentrantLock可能通过Condition来控制各个低粒度的边界，更加的灵活，而在低粒度中，Condition的优势就没有了
   2. JVM的开发团队从来都没有放弃synchronized，而且基于JVM的synchronized优化空间更大，使用内嵌的关键字比使用API更加自然
   3. 在大量的数据操作下，对于JVM的内存压力，基于API的ReentrantLock会开销更多的内存，虽然不是瓶颈，但是也是一个选择依据
   4. 

## <font color="red">常用辅助类（必会）</font>

### CountDownLatch(减法计数器，只阻塞自己)

![image-20200516142453948](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516142453948.png)

 它允许一个或多个线程一直等待，直到其他线程的操作执行完后再执行。例如，应用程序的主线程希望在负责启动框架服务的线程已经启动所有的框架服务之后再执行

```java
/**
 * 减法计数器
 */
public class CountDownLatchTest {
    public static void main(String[] args) {
        //总数是6
        CountDownLatch countDownLatch = new CountDownLatch(6);
        /**
         * 模拟教室6个人，最后一个人关门
         */
        for(int i=1;i<=6;i++){
            new Thread(()->{
                System.out.println(Thread.currentThread().getName()+" go out");
                //倒计时
                countDownLatch.countDown(); //-1
            },String.valueOf(i)).start();
        }

        try {
            countDownLatch.await(); //等待计数器归零，再向下执行
            System.out.println("close Door");
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

    }
}
```

原理

countDownLatch.countDown();    // 数量-1

countDownLatch.await();  // 等待计数器归零，然后再向下执行

每次有线程调用 countDown()数量-1，假设计数器变为0，countDownLatch.await()就会被唤醒，继续执行！





### CyclicBarrier（屏障，加法计数器，阻塞所有线程）

![image-20200516143758183](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516143758183.png)

比CountDownLatch构造函数多了一种传入number，Runnable实现类的构造函数，CountDownLatch用countDown+await()完成同步，CycliBarrier用await()即可完成

  可循环（Cyclic）使用的屏障。**让一组线程到达一个屏障（也可叫同步点）时被阻塞，直到最后一个线程到达屏障时，屏障才会开门**，所有被屏障拦截的线程才会继续干活，执行完成之后，再执行写进去的线程（如下面的召唤神龙）。

```java
public class CyclicBarrierTest {
    public static void main(String[] args) {
        /**
         * 集齐七颗龙珠召唤神龙
         */
        CyclicBarrier cyclicBarrier = new CyclicBarrier(7, () -> {  //改成8，死循环
            System.out.println("召唤神龙成功！");
        });

        for (int i = 1; i <= 7; i++) {
            int temp = i;
            new Thread(() -> {
                System.out.println(Thread.currentThread().getName() + "收集了1颗龙珠，现在收集了" + temp + "颗");
                try {
                    cyclicBarrier.await();  //阻塞，等待计数器到达7,线程才继续下去
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }, "Thread" + i).start();
        }
    }
}
```



### Semaphore

![image-20200516155850726](F:\Project\cscode\markdown\Java面试\JUC\pictures\image-20200516155850726.png)

举个例子，抢车位，想要停车的车辆必须先拥有停车位，有了停车位才能停在自家小区

```java
public class SemaphoreTest {
    public static void main(String[] args) {
        Semaphore semaphore = new Semaphore(3); //3个车位,可以进行限流

        for (int i = 1; i <= 6; i++) {  //6台车
            new Thread(()->{
                try {
                    semaphore.acquire();
                    System.out.println(Thread.currentThread().getName()+"抢到车位");
                    TimeUnit.SECONDS.sleep(2);

                    System.out.println(Thread.currentThread().getName()+"离开车位");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }finally {
                    semaphore.release();
                }
            },"Thread-"+i).start();
        }
    }
}
```

原理：

semaphore acquire();       获得资源，假设如果已经满了，等待，等待被释放为止

semaphore release()；    释放资源，会将当前的信号量释放+1，然后唤醒等待的线程！

作用：多个共享资源互斥的使用！并发限流，控制最大的线程数



## 阻塞队列

![image-20200516175626873](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516175626873.png)

![image-20200516173558976](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516173558976.png)



BlockingQueue是Collection下的Queue接口的子接口

阻塞：

1、队空出队

2、队满入队



阻塞队列有以下**四组API**

| 操作            | 抛出异常                   | 有返回值，不抛出异常         | 阻塞等待             | 超时等待                                                  |
| --------------- | -------------------------- | ---------------------------- | -------------------- | --------------------------------------------------------- |
| 添加            | add(E e)  (返回true/false) | offer(E e)  (返回true/false) | put(E e)（无返回值） | offer(E e, long timeout, TimeUnit unit)  (返回true/false) |
| 移除(返回E对象) | remove()                   | poll()                       | take()               | poll(long timeout, TimeUnit unit)                         |
| 判断队列头      | element()                  | peek()                       | -                    | -                                                         |

```java
public class QueueTest {
    public static void main(String[] args) throws InterruptedException {
//        test01();
//        test02();
//        test03();
        test04();
    }

    public static void test01(){
        ArrayBlockingQueue queue = new ArrayBlockingQueue(3);
        //入队
        System.out.println(queue.add("aa"));    //true
        System.out.println(queue.add("bb"));    //true
        System.out.println(queue.add("cc"));    //true
//        System.out.println(queue.add("dd")); //抛出IllegalStateException
        System.out.println("===========================");
        //出队
        System.out.println(queue.remove());//返回队列内容,即String
        System.out.println(queue.remove());
        System.out.println(queue.remove());
        //空队取队首
        System.out.println(queue.element());//抛出NoSuchElementException


//        queue.remove();  //抛出NoSuchElementException

    }

    public static void test02(){
        ArrayBlockingQueue queue2 = new ArrayBlockingQueue(3);
        //入队
        System.out.println(queue2.offer("aa"));    //true
        System.out.println(queue2.offer("bb"));    //true
        System.out.println(queue2.offer("cc"));    //true
//        System.out.println(queue.offer("dd"));    //false
        System.out.println("===========================");
        //出队
        System.out.println(queue2.poll());//返回队列内容
        System.out.println(queue2.poll());//返回队列内容
        System.out.println(queue2.poll());//返回队列内容
        System.out.println(queue2.poll());//返回null
        //空队取队首
        System.out.println(queue2.peek());//返回null
    }

    public static void test03() throws InterruptedException {
        ArrayBlockingQueue queue3 = new ArrayBlockingQueue(3);
        //入队
        queue3.put("aa");//无返回值
        queue3.put("bb");//无返回值
        queue3.put("cc");//无返回值
//        queue3.put("dd");//阻塞，一直等待
        System.out.println("===========================");
        //出队
        System.out.println(queue3.take());//返回队列内容
        System.out.println(queue3.take());//返回队列内容
        System.out.println(queue3.take());//返回队列内容
        System.out.println(queue3.take());//阻塞，一直等待

        //空队取队首
        System.out.println(queue3.peek());//返回null
    }

    public static void test04() throws InterruptedException {
        ArrayBlockingQueue queue4 = new ArrayBlockingQueue(3);
        //入队
        System.out.println(queue4.offer("aa"));    //true
        System.out.println(queue4.offer("bb"));    //true
        System.out.println(queue4.offer("cc"));    //true
        System.out.println(queue4.offer("dd", 1, TimeUnit.SECONDS)); //等1秒后，返回fasle
        System.out.println("===========================");
        //出队
        System.out.println(queue4.poll());//返回队列内容
        System.out.println(queue4.poll());//返回队列内容
        System.out.println(queue4.poll());//返回队列内容
        System.out.println(queue4.poll(2,TimeUnit.SECONDS));//等2秒后，返回null
        //空队取队首
        System.out.println(queue4.peek());//返回null
    }
}

```



### SynchronousQueue 同步队列(TODO理解)

SynchronousQueue，实际上它不是一个真正的队列，因为它不会为队列中元素维护存储空间。与其他队列不同的是，**它维护一组线程，这些线程在等待着把元素加入或移出队列**。

如果以洗盘子的比喻为例，那么这就相当于没有盘架，而是将洗好的盘子直接放入下一个空闲的烘干机中。这种实现队列的方式看似很奇怪，但由于可以直接交付工作，从而降低了将数据从生产者移动到消费者的延迟。（在传统的队列中，在一个工作单元可以交付之前，必须通过串行方式首先完成入列[Enqueue]或者出列[Dequeue]等操作。）

直接交付方式还会将更多关于任务状态的信息反馈给生产者。当交付被接受时，它就知道消费者已经得到了任务，而不是简单地把任务放入一个队列——这种区别就好比将文件直接交给同事，还是将文件放到她的邮箱中并希望她能尽快拿到文件。

因为**SynchronousQueue没有存储功能**，因此put和take会一直阻塞，直到有另一个线程已经准备好参与到交付过程中。仅当有足够多的消费者，并且总是有一个消费者准备好获取交付的工作时，才适合使用同步队列。

```java
public class QueueTest02 {
    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> queue = new SynchronousQueue();
        new Thread(()->{
            try {
                queue.put("1");
                System.out.println(Thread.currentThread().getName()+" put 1");

                queue.put("2");
                System.out.println(Thread.currentThread().getName()+" put 2");

                queue.put("3");
                System.out.println(Thread.currentThread().getName()+" put 3");

            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        },"T1").start();

        new Thread(()->{
            try {
                TimeUnit.SECONDS.sleep(1);
                queue.take();
                System.out.println(Thread.currentThread().getName()+" take 1");

                queue.take();
                System.out.println(Thread.currentThread().getName()+" take 2");

                queue.take();
                System.out.println(Thread.currentThread().getName()+" take 3");

            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        },"T2").start();
    }
}
```



## <font color="red">线程池（重要）</font>

### 操作系统两种内核模型

用户线程（ULT）：用户程序实现，不依赖操作系统核心，应用提供创建、同步、调度和管理线程的函数来控制用户线程。不需要用户态/核心态切换，速度快。内核对ULT无感知，线程阻塞则进程（包括它的所有线程）阻塞。

内核线程（KLT）：系统内核管理线程（KLT），内核保存线程的状态和上下文信息，线程阻塞不会引起进程阻塞。在多处理器系统上，多线程在多处理器上并行运行。线程的创建、调度和管理由内核完成，效率比ULT要慢，比进程操作快。

![image-20200513014520079](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513014520079.png)

KLT线程创建需要陷入到内核空间，并在线程表里创建一个线程信息



### 线程池是什么

Java线程创建是依赖于系统内核，通过JVM调用系统库创建内核线程，内核线程与Java-Thread是1：1的映射关系

![image-20200513015906961](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513015906961.png)

线程是稀缺资源，它的创建与销毁是一个相对偏重且耗资源的操作，而Java线程依赖于内核线程，创建线程需要进行**操作系统状态切换**，为避免资源过度消耗需要设法**重用线程**执行多个任务。**线程池就是一个线程缓存，负责对线程进行统一分配、调优与监控。简单来说，就是为了线程复用，方便控制最大并发数、管理线程**

**什么时候使用线程池？**

- 单个任务处理时间比较短
- 需要处理的任务数量很大

**线程池优势**

- 重用存在的线程，减少线程创建，消亡的开销，提高性能
- 提高响应速度。当任务到达时，任务可以不需要的等到线程创建就能立即执行。
- 提高线程的可管理性，可统一分配，调优和监控。



### Executors工具类创建的线程池四大方法

Executors工具类实际上也只是**new ThreadPoolExecutor(...)**完成线程池创建

（1）**newSingleThreadExecutor**：创建一个**单线程**的线程池。这个线程池**只有一个线程在工作**，也就是相当于单线程串行执行所有任务。**如果这个唯一的线程因为异常结束，那么会有一个新的线程来替代它**。此线程池保证所有任务的执行顺序按照任务的提交顺序执行。

（2）**newFixedThreadPool：**创建**固定大小**的线程池。每次提交一个任务就创建一个线程，直到线程达到线程池的最大大小。线程池的大小一旦达到最大值就会保持不变，**如果某个线程因为执行异常而结束，那么线程池会补充一个新线程**。如果希望在服务器上使用线程池，建议使用 newFixedThreadPool方法来创建线程池，这样能获得更好的性能。

（3） **newCachedThreadPool：**创建一个可缓存的线程池。如果线程池的大小超过了处理任务所需要的线程，那么就会回收部分空闲（60 秒不执行任务）的线程，当任务数增加时，此线程池又可以智能的添加新线程来处理任务。此线程池不会对线程池大小做限制，线程池大小完全依赖于操作系统（或者说 JVM）能够创建的最大线程大小。

（4）**newScheduledThreadPool：**创建一个**大小无限**的线程池。此线程池支持定时以及**周期性执行任务**的需求。

```java
public class ExecutorTest01 {
    public static void main(String[] args) {
        ExecutorService threadPool = Executors.newFixedThreadPool(6);
//        Executors.newSingleThreadExecutor();  //单个线程
//        Executors.newFixedThreadPool(6);      //创建固定大小的线程
//        Executors.newCachedThreadPool();      // 可伸缩的
        try {
            for (int i = 0; i < 10; i++) {
                //使用了线程池之后，使用线程池来创建线程
                threadPool.execute(() -> {
                    System.out.println(Thread.currentThread().getName());
                });
            }
        }finally {
            //线程池用完要关闭线程池
            threadPool.shutdown();
        }

    }
}
```

但是Executors提供给我们的创建线程池的方法都是会发生OOM的，**newSingleThreadExecutor**、**newFixedThreadPool**请求队列长度最大可以到2^32^-1，堆积大量请求OOM,**newCachedThreadPool**、**newScheduledThreadPool：**允许创建线程最大到2^32^-1，创建大量线程OOM

![image-20200516194104610](F:\Project\cscode\markdown\Java面试\JUC\pictures\image-20200516194104610.png)

```java
public class ExecutorTest01 {
    public static void main(String[] args) {
        ExecutorService threadPool = Executors.newFixedThreadPool(6);
//        Executors.newSingleThreadExecutor();  //单个线程
//        Executors.newFixedThreadPool(6);      //创建固定大小的线程
//        Executors.newCachedThreadPool();      // 可伸缩的
        try {
            for (int i = 0; i < 10; i++) {
                //使用了线程池之后，使用线程池来创建线程
                threadPool.execute(() -> {
                    System.out.println(Thread.currentThread().getName());
                });
            }
        }finally {
            //线程池用完要关闭线程池
            threadPool.shutdown();
        }

    }
}
```

### ThreadPoolExecutor 7个参数

- **corePoolSize ：**核心线程数，线程数定义了最小可以同时运行的线程数量。**如果输入的核心线程数比最大线程数大，报错IllegalArgumentException**
- **maximumPoolSize ：**线程池中允许存在的工作线程的最大数量
- keepAliveTime：线程池中的线程数量大于 corePoolSize 的时候，如果这时没有新的任务提交，核心线程外的线程不会立即销毁，而是会等待，直到等待的时间超过了 keepAliveTime才会被回收销毁；
- unit ：keepAliveTime 参数的时间单位。
- **workQueue：**当新任务来的时候会先判断当前运行的线程数量是否达到核心线程数，如果达到的话，任务就会被存放在队列中。
- threadFactory：为线程池提供创建新线程的线程工厂
- handler ：当前同时运行的线程数量达到最大线程数量并且队列也已经被放满了任务 之后的拒绝策略
  

```java
//newSingleThreadExecutor()
public static ExecutorService newSingleThreadExecutor() {
        return new FinalizableDelegatedExecutorService
            (new ThreadPoolExecutor(1, 1,
                                    0L, TimeUnit.MILLISECONDS,
                                    new LinkedBlockingQueue<Runnable>()));	//请求队列无限长
    }
//newFixedThreadPool
public static ExecutorService newFixedThreadPool(int nThreads) {
        return new ThreadPoolExecutor(nThreads, nThreads,
                                      0L, TimeUnit.MILLISECONDS,
                                      new LinkedBlockingQueue<Runnable>());	//请求队列无限长
    }
//public static ExecutorService newCachedThreadPool() {
        return new ThreadPoolExecutor(0, Integer.MAX_VALUE,			//可以创建的线程无限大
                                      60L, TimeUnit.SECONDS,
                                      new SynchronousQueue<Runnable>());
    }

//最重要的ThreadPoolExecutor
public ThreadPoolExecutor(int corePoolSize,      	//核心线程池大小
                              int maximumPoolSize, 	//最大核心线程池大小
                              long keepAliveTime,	//超时了没有入调用就会释放
                              TimeUnit unit,		//超时单位
                              BlockingQueue<Runnable> workQueue,//阻塞队列
								ThreadFactory threadFactory,//线程工厂：创建线程的
                              RejectedExecutionHandler handler)//拒绝策略
    }
```



```java
public class Test02 {
    public static void main(String[] args) {
        ThreadPoolExecutor threadPool = new ThreadPoolExecutor(2,5,3,
                                                    TimeUnit.SECONDS,new ArrayBlockingQueue<>(10),
                                                    Executors.defaultThreadFactory(),new ThreadPoolExecutor.AbortPolicy());

        try {
            for(int i=1;i<=5;i++){
                threadPool.execute(()->{
                    System.out.println(Thread.currentThread().getName()+" say hello");
                });
            }
        }finally {
            threadPool.shutdown();
        }


    }
}
```



### 线程池执行流程

![image-20200516205134072](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516205134072.png)

### 4种拒绝策略

![image-20200513090045830](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513090045830.png)

- ThreadPoolExecutor.AbortPolicy：抛出 RejectedExecutionException来拒绝新任务的处理。

![image-20200516205322655](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516205322655.png)

- ThreadPoolExecutor.CallerRunsPolicy：返回给执行自己的线程的线程去运行任务。您不会任务请求。但是这种策略会降低对于新任务提交速度，影响程序的整体性能。另外，这个策略喜欢增加队列容量。如果您的应用程序可以承受此延迟并且你不能任务丢弃任何一个任务请求的话，你可以选择这个策略。

![image-20200516205412737](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516205412737.png)

- ThreadPoolExecutor.DiscardPolicy：不处理新任务，直接丢弃掉。
- ThreadPoolExecutor.DiscardOldestPolicy： 此策略将丢弃最早的未处理的任务请求。
  



### 线程池生命状态

有五种

- Running

这是最正常的状态，接受新的任务，处理等待队列中的任务。

- Shutdown

不接受新的任务提交，但是会继续处理等待队列中的任务。

- Stop

不接受新的任务提交，不再处理等待队列中的任务，中断正在执行任务的线程。

- Tidying

所有的任务都销毁了，workCount 为 0，线程池的状态在转换为 TIDYING 状态时，会执行 terminated()。

- Terminated

terminated()方法结束后，线程池的状态就会变成这个。

![image-20200513092139584](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513092139584.png)

线程池生命状态是通过一个INT型进行记录的，高3位记录线程池生命状态，低29位记录当前工作线程数

```java
	private static final int COUNT_BITS = Integer.SIZE - 3;
    private static final int CAPACITY   = (1 << COUNT_BITS) - 1;

    // runState is stored in the high-order bits
    private static final int RUNNING    = -1 << COUNT_BITS;		//111
    private static final int SHUTDOWN   =  0 << COUNT_BITS;		//000
    private static final int STOP       =  1 << COUNT_BITS;		//001
    private static final int TIDYING    =  2 << COUNT_BITS;		//010
    private static final int TERMINATED =  3 << COUNT_BITS;		//011
```



![image-20200513092901366](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513092901366.png)



### 如何合理配置线程池的最大大小

1、CPU密集型（需要一直计算）最大线程数和电脑保持一致即可

```java
System.out.println(Runtime.getRuntime().availableProcessors());
```

2、IO密集型 判断你程序中十分耗IO的线程，大于其两倍就好



## ForkJoin（TODO:再理解）

Forkjoin在JDK1.7之后，并行执行任务！提高效率。大数据量！

大数据：Map Reduce（把大任务拆分为小任务）

![image-20200516231717302](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516231717302.png)

ForkJoin特点：

1、任务划分

2、工作窃取

通过维护双端队列来实现的

![image-20200516232122109](F:\Project\cscode\markdown\Java面试\JUC\pictures\image-20200516232122109.png)

使用ForkJoin

1、forkjoinPooL通过它来执行

2、计算任务 forkjoinPool.execute（ForkJoinTask<？>task）

3、计算类要继承 ForkjoinTask



![image-20200517010740843](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517010740843.png)

示例：

```java
/**
 * 如何使用 forkjoin
 * 1、forkjoinPooL通过它来执行
 * 2、计算任务 forkjoinPool.execute（ForkJoinTask<？>task）
 * 3.计算类要继承 ForkjoinTask
 */
public class ForkJoin extends RecursiveTask<Long> {
    private Long start;
    private Long end;

    private Long temp = 10000L;//临界值


    public ForkJoin(Long start, Long end) {
        this.start = start;
        this.end = end;
    }


    @Override
    protected Long compute() {
        if (end - start > temp) {
            //分支合并计算
            Long middle = (start + end) / 2;    //中间值
            ForkJoin task1 = new ForkJoin(start, middle);
            task1.fork();   //拆分任务，把任务压入线程队列，跟CSAPP linux fork差不多
            ForkJoin task2 = new ForkJoin(start, middle);
            task2.fork();
            return task1.join() + task2.join(); //合并结果
        } else {
            //正常运算
            Long sum = 0L;
            for (Long i = start; i < end; i++) {
                sum += i;
            }
            return sum;

        }
    }

    

    public static void test1() {
        // 普通进行求和
        long start = System.currentTimeMillis();
        Long sum = 0L;
        for (Long i = 0L; i < 10_0000_0000; i++) {
            sum += i;
        }

        long end = System.currentTimeMillis();
        System.out.println("普通加法执行时间" + (end - start)+"，结果为"+sum);

    }

    public static void test2() throws ExecutionException, InterruptedException {
        long start = System.currentTimeMillis();

        ForkJoinPool forkJoinPool = new ForkJoinPool();
        ForkJoinTask<Long> task = new ForkJoin(0L, 10_0000_0000L);
        ForkJoinTask<Long> submit = forkJoinPool.submit(task);
        Long result = submit.get();
        long end = System.currentTimeMillis();
        System.out.println("ForkJoin执行时间" + (end - start)+"，结果为"+result);
    }

    public static void test3() {
        long start = System.currentTimeMillis();
        Long result = LongStream.range(0L,10_0000_0000L).parallel().reduce(0,Long::sum);
        long end = System.currentTimeMillis();
        System.out.println("Stream并行流执行时间" + (end - start)+"，结果为"+result);
    }

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        /**
         * 计算10亿累加和 10_0000_0000
         * 实现方案
         * 1、普通循环
         * 2、ForkJoin
         * 3、Stream并行流
         */

        //普通
        test1();
        //ForkJoin
        test2();
        //Stream并行流
        test3();
    }
}
```

![image-20200517013613617](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517013613617.png)



## 异步调用(TODO)

类似ajax，不要求立刻处理任务

![image-20200517014041041](F:\Project\cscode\markdown\Java面试\JUC\pictures\image-20200517014041041.png)

CompletableFuture来实现

![image-20200517014133816](F:\Project\cscode\markdown\Java面试\JUC\pictures\image-20200517014133816.png)··

```java
/**
 * 异步调用：CompLetabLeFuture
 * 异步执行
 * 成功回调
 * 失败回调
 */
public class FutureTest {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        //发起一个请求,没有返回值的异步回调
        CompletableFuture<Void> completableFuture = CompletableFuture.runAsync(()->{

            System.out.println(Thread.currentThread().getName()+ " say aaaaaa");
        });
        
        TimeUnit.SECONDS.sleep(2);
        System.out.println("111111");
        completableFuture.get();//阻塞获取结果，获取到一个Void对象

        System.out.println("================================");

        //发起一个请求,有返回值的异步回调
        CompletableFuture<Integer> completableFuture2 = CompletableFuture.supplyAsync(()->{
            System.out.println(Thread.currentThread().getName()+"supplyAsync=>Integer");
            return 1024;
        });

        //请求成功时，调用
        completableFuture2.whenComplete((t,u)->{
            System.out.println("t->"+t+",u->"+u);       //t是正常返回结果 u为null
        }).exceptionally((e)->{                         //u是错误信息 t为null
            System.out.println(e.getMessage());
            return 233;
        });
    }
}

```



## volatile

Volatile是Java虚拟机提供**轻量级的同步机制**，底层原理放到另外再讲

1、保证可见性（底层通过lock锁总线，并没有使用MESI的优化策略）

2、不保证原子性

3、禁止指令重排（因为lock总线，可以禁止指令重排）

### JMM内存模型

JMM:Java内存模型

CPU缓存模型图示

![image-20200513180317012](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513180317012.png)

Java Memory Model简称JMM。Java**线程**内存模型跟CPU缓存模型类似，是基于CPU缓存模型来建立的，Java线程内存模型是标准化的，屏蔽掉了底层不同计算机的区别。（逻辑上的）

![image-20200513185332473](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513185332473.png)

### JMM数据原子操作

read（读取）：从主内存读取数据

load（载入）：将主内存读取到的数据写入工作内存

use（使用）：从工作内存读取数据来计算

assign（赋值）：将计算好的值重新赋值到工作内存中

store（存储）：将工作内存数据写入主内存

write（写入）：将store过去的变量值赋值给主内存中的变量

lock（锁定）：将主内存变量加锁，标识为线程独占状态

unlock（解锁）：将主内存变量解锁，解锁后其他线程可以锁定该变量

对于上面的原子操作，有以下规定

1. 不允许read和load、store和 write操作之一单独出现。即使用了read必须load，使用了 store必须wite
2. 不允许线程丢弃他最近的asgn操作，即工作变量的数据改变了之后，必须告知主存
3. 不允许一个线程将没有 assign的数据从工作内存同步回主内存
4. 一个新的变量必须在主内存中诞生，不允许工作内存直接使用一个未被初始化的变量。就是对变量实施use、store操作之前必须经过assign和load操作
5. 一个变量同一时间只有一个线程能对其进行lock。多次lock后，必须执行相同次数的 unlock才能解锁
6. 如果对一个变量进行lock操作，会清空所有工作内存中此变量的值，在执行引擎使用这个变量前，必须重新load或assign操作
7. 如果一个变量没有被lock，就不能对其进行 unlock操作。也不能 unlock一个被其他线程锁住的变量
8. 对一个变量进行 unlock操作之前，必须把此变量同步回主内存

### 内存可见性问题：

```java
public class ThreadTest {
    private static  boolean initFlag = false;

    public void refresh(){
        this.initFlag = true;		//修改initFlag
        String threadName = Thread.currentThread().getName();
        System.out.println("线程:"+threadName+":修改共享变量initFlag");	
    }

    public void load(){
        String threadName = Thread.currentThread().getName();
        while(!initFlag){			//initFlag为false时死循环
        }
        System.out.println("线程:"+threadName+":探测到initFlag改变");
    }

    public static void main(String[] args) {
        ThreadTest sample = new ThreadTest();
        Thread threadA = new Thread(()->{
            sample.refresh();
        },"threadA");

        Thread threadB = new Thread(()->{
            sample.load();
        },"threadB");

        threadB.start();

        try{
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        threadA.start();
    }
}
```

![image-20200513195039917](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513195039917.png)

threadB并没有取到threadA修改后的initFlag

![image-20200513201518700](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513201518700.png)

### CPU层级的缓存一致性

解决方案：

1、总线加锁（性能太低）

CPU从主内存读取数据到高速缓存，会在总线对这个数据加锁，这样其它CPU没法去读或写这个数据，直到这个CPU使用完数据释放锁之后其它CPU才能读取该数据

![image-20200513210054058](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513201942042.png)



2、MESI缓存一致性协议

多个CPU从主内存读取同一个数据到各自的高速缓存，当其中某个CPU修改了缓存里的数据，该数据会马上同步回主内存，其它CPU通过**总线嗅探**机制可以感知到数据的变化从而将自己缓存里的数据失效

![image-20200513210802887](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513202757446.png)

使用volatile关键字，问题解决，但 JVM的 volatile的实现和CPU的实现完全是两码事，这里不作具体展开。

```java
private static volatile  boolean initFlag = false;
```

![image-20200513201942042](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513195551851.png)

volatile底层实现主要是通过汇编**lock前缀指令**，如果满足MESI，它会锁定这块内存区域的缓存并回写到主内存，此操作被称为“**缓存锁定**”，MESI缓存一致性协议机制会阻止同时修改被两个以上处理器缓存的内存区域数据。一个处理器的缓存值通过总线回写到内存会导致其他处理器相应的缓存失效。如果不满足则进行**总线加锁**，也是导致缓存行失效。

### volatile不保证原子性问题

先看示例

```java
public class ThreadTest2 {
    private static volatile int sum = 0; //初始化sum为0

    public static void main(String[] args) {

        for(int i=0;i<10;i++){
            new Thread(()->{
                for(int j=0;j<1000;j++){
                    sum++;
                }
            }).start();
        }
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println(sum);
    }
}
```

输出并不总是10000

![image-20200513202757446](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513210054058.png)

原因如下

![image-20200513211245854](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513211245854.png)

### 有序性分析

cpu指令重排案例：

```java
public class ThreadTest3 {
    private static int a = 0, b = 0, x = 0, y = 0;

    public static void main(String[] args) throws InterruptedException {

        while (true) {
            a = 0;
            b = 0;
            x = 0;
            y = 0;
            //下面两个线程如果顺序执行，并不会出现x=0，y=0的情况，而事实上并不是，原因是有指令重排
            Thread thread1 = new Thread(() -> {
                try {
                    Thread.sleep(200);
                    a = 1;
                    x = b;
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });

            Thread thread2 = new Thread(() -> {
                try {
                    Thread.sleep(200);
                    b = 2;
                    y = a;
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });

            thread1.start();
            thread2.start();

            thread1.join();
            thread2.join();
            System.out.println("a:" + a + " b:" + b + " x:" + x + " y:" + y);

            if (x == 0 && y == 0) {
                break;
            }
        }

    }
}
```

由于x=b与a=1并没有依赖关系，y = a与b = 2也没有依赖关系，则存在指令重排，可能造成结果是

| 线程A | 线程B |
| ----- | ----- |
| x=b   | y=a   |
| a=1   | b=2   |

出现x=0，y=0的情况



#### 内存屏障

为了解决上述问题，需要处理器提供**内存屏障**（Memory Barrier）禁止指令重排，在JSR（java规范）中定义了4种内存屏障：

LoadLoad屏障：（指令Load1; LoadLoad; Load2），在Load2及后续读取操作要读取的数据被访问前，保证Load1要读取的数据被读取完毕。

LoadStore屏障：（指令Load1; LoadStore; Store2），在Store2及后续写入操作被刷出前，保证Load1要读取的数据被读取完毕。

StoreStore屏障：（指令Store1; StoreStore; Store2），在Store2及后续写入操作执行前，保证Store1的写入操作对其它处理器可见。

StoreLoad屏障：（指令Store1; StoreLoad; Load2），在Load2及后续所有读取操作执行前，保证Store1的写入对所有处理器可见。**它的开销是四种屏障中最大的。在大多数处理器的实现中，这个屏障是个万能屏障，兼具其它三种内存屏障的功能**

对于volatile关键字，按照规范会有下面的操作：

- 在每个volatile写入之前，插入一个StoreStore，写入之后，插入一个StoreLoad

- 在每个volatile读取之前，插入一个LoadLoad，读入之后，再插入一个LoadStore

![img](https://gitee.com/zero049/MyNoteImages/raw/master/timg)

## Atomic包

![image-20200517022521666](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517022521666.png)

如何不加锁或者用synchronize修饰，要保证原子性操作，那么需要Atomic的原子类解决原子问题，是基于CAS算法实现的。

```java
public class AtomicTest {
    private static AtomicInteger sum = new AtomicInteger(0); // 初始化sum为0

    public static void main(String[] args) {

        for(int i=0;i<10;i++){
            new Thread(()->{
                for(int j=0;j<1000;j++){
                    sum.getAndIncrement();
                }
            }).start();
        }
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println(sum);
    }
}
```

![image-20200517022937444](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517022937444.png)



这些类的底层都直接和操作系统挂钩！在内存中修改值！Unsafe类是一个很特殊的存在

![image-20200517114017792](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517114017792.png)



## CAS算法（Compare And Swap）

即 compare and swap（比较与交换），是一种有名的无锁算法，是CPU的并发原语。

无锁编程，即不使用锁的情况下实现多线程之间的变量同步，也就是在没有线程被阻塞的情况下实现变量的同步，所以也叫非阻塞同步（Non-blocking Synchronization）。

CAS算法涉及到三个操作数（下图E为V，N为A）

- 获得CPU时，从内存中读出的值A
- 需要读写的最新内存值V
- 拟写入的新值B

![image-20200609211254689](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200609211254689.png)

当且仅当Ⅴ的值等于A时，CAS通过原子方式用新值B来更新Ⅴ的值，否则不会执行任何操作（比较和替换是一个原子操作）。**一般情况下是一个自旋操作，即不断的重试。**

先看看案例

```java
public class CASDemo01 {
    public static void main(String[] args) {
        AtomicInteger atomicInteger = new AtomicInteger(200);

        //期望、更新
        //public final booLean compareAndSet(int expect，int update)
        //如果我期望的值达到了，那么就更新，否则，就不更新
        System.out.println(atomicInteger.compareAndSet(200,201));
        System.out.println(atomicInteger.get());    //修改成功
        System.out.println(atomicInteger.compareAndSet(200,202));//修改失败
        System.out.println(atomicInteger.get());       
    }
}
```

看到Atom类实际是通过Unsafe类去实现修改的

![image-20200517135143699](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517135143699.png)

我们可以看getAndIncrement方法去理解这个CAS算法（感觉画错了，应该var1，var2能取到实际内存值，v5是取到当时的一个内存值）

![image-20200517140311136](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517140311136.png)

可以看到do while循环就是一个**自旋锁**，如果不成功则继续循环

**缺点：**

1、循环（自旋）会耗时，在高竞争环境下，很耗费CPU

2、一次性只能保证一个共享变量的原子性

3、ABA问题

### ABA问题（狸猫换太子）

如果一个变量V初次读取的时候是A值，并且在准备赋值的时候检査到它仍然是A值，那我们就能说明它的值没有被其他线程修改过了吗？很明显是不能的，因为在这段时间它的值可能被改为其他值，然后又改回A，那CAS操作就会误认为它从来没有被修改过。这个问题被称为CAS操作的"ABA"问题

![image-20200517141210112](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517141210112.png)

```java
public class CASDemo01 {
    public static void main(String[] args) {
        AtomicInteger atomicInteger = new AtomicInteger(200);

        //期望、更新
        //public final booLean compareAndSet(int expect，int update)
        //如果我期望的值达到了，那么就更新，否则，就不更新
        
        //==================捣乱的线程============================
        System.out.println(atomicInteger.compareAndSet(200,7777));
        System.out.println(atomicInteger.get());    //修改成功
        System.out.println(atomicInteger.compareAndSet(7777,200));
        System.out.println(atomicInteger.get());

        //==================期望的线程============================
        System.out.println(atomicInteger.compareAndSet(200,999));
        System.out.println(atomicInteger.get());    //修改成功
      
    }
}
```

针对上面的问题，通过原子引用来解决



### 原子引用类

通过以下的类实现，本质就是乐观锁的版本号机制

![image-20200517141839763](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517141839763.png)

先看看案例

```java
public class CASDemo02 {
    public static void main(String[] args) {

//        AtomicInteger atomicInteger = new AtomicInteger(200);

        //初始值为200,版本号为1
        //注意
        // 这里有个坑对于 Integer var=？在-128至127之间的赋值，Integer对象是在IntegerCache.cache产生，会复用己有对象
        AtomicStampedReference<Integer> atomicStampedReference= new AtomicStampedReference<>(1,1);


        //==================捣乱的线程============================
        new Thread(()->{
            int versionA = atomicStampedReference.getStamp(); // 获得版本号
            System.out.println("A1=>"+versionA);

            try {
                TimeUnit.SECONDS.sleep(1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            Integer a = new Integer(8888);
            //CAS修改
            System.out.println(atomicStampedReference.compareAndSet(1, a, atomicStampedReference.getStamp(), atomicStampedReference.getStamp() + 1));

            System.out.println("A2=>"+atomicStampedReference.getStamp());
            System.out.println(atomicStampedReference.compareAndSet(a, 1, atomicStampedReference.getStamp(), atomicStampedReference.getStamp() + 1));

            System.out.println("A3=>"+atomicStampedReference.getStamp());

        },"A").start();

        new Thread(()->{
            int versionB = atomicStampedReference.getStamp(); // 获得版本号
            try {
                TimeUnit.SECONDS.sleep(2);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("B1=>"+versionB);
            Integer b = new Integer(2222);	//不复用
            System.out.println(atomicStampedReference.compareAndSet(1, b, versionB, versionB + 1));
            System.out.println("B2=>"+atomicStampedReference.getStamp());


        },"B").start();
    }
}
```

注意如果泛型是一个包装类，注意引用问题，由于是包装类，即使你参数上写2222，也是new了一个Integer，下一次再在参数写2222也不是同一个了

![image-20200517142713977](F:\Project\cscode\markdown\Java面试\JUC\pictures\image-20200517142713977.png)



## 各种锁的理解

### 公平锁、非公平锁

公平锁：非常公平，不能够插队，必须先来后到！

非公平锁：非常不公平，可以插队（lock默认、synchronize）

公平锁效率低，一个运行3s的线程可能要等运行3h的线程执行完才能执行，因此应该将非公平锁作为默认的



### 可重入锁/递归锁



![image-20200517150233957](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517150233957.png)

​	

```java
public class ChongruTes {
    public static void main(String[] args) {
        Phone phone = new Phone();
        new Thread(()->{
            phone.sms();
        },"A").start();
        new Thread(()->{
            phone.sms();
        },"B").start();
    }
}


class Phone{

    public synchronized void sms(){
        System.out.println(Thread.currentThread().getName()+" sms");
        call();	//这个方法也是加锁了
    }

    public synchronized void call(){
        System.out.println(Thread.currentThread().getName()+" call");
    }
}
```

输出结果

![image-20200517151443223](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517151443223.png)



### 自旋锁

主要通过CAS实现，下面是一个自定义实现

```java
//CAS实现
public class ZiXuanTest {
    //默认为null
    private AtomicReference<Thread> atomicReference = new AtomicReference<>();

    //加锁
    public void myLock(){
        Thread thread = Thread.currentThread();


        //自旋
        while(!atomicReference.compareAndSet(null,thread)){
            //如果atomicReference为空才跳出循环,如果atomicReference已经被设置成了一个thread，那就会循环
        }
        System.out.println(Thread.currentThread().getName()+"======>获取myLock" );
    }

    //解锁
    public void myUnLock(){
        Thread thread = Thread.currentThread();

        atomicReference.compareAndSet(thread,null); //把atomicReference设置回空，别的线程可以使用了
        System.out.println(Thread.currentThread().getName()+"======>释放myUnLock" );
    }
}

```





### 死锁

产生死锁的必要条件：

1、互斥条件：所谓互斥就是进程在某一时间内独占资源。

2、请求与保持条件：一个进程因请求资源而阻塞时，对已获得的资源保持不放。

3、不剥夺条件：进程已获得资源，在末使用完之前，不能强行剥夺。

4、循环等待条件：若干进程之间形成一种头尾相接的循环等待资源关系。

这四个条件是死锁的必要条件，只要系统发生死锁，这些条件必然成立，而只要上述条件之 一不满足，就不会发生死锁。
![image-20200517154412654](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517154412654.png)

模拟A持有A锁要获取B锁，B持有B锁要获取A锁

```java
public class SisuoTest {
    public static void main(String[] args) throws InterruptedException {
        //"lockA","lockB"是常量因此能保证锁到的是同一个
        new Thread(new MyThread("lockA","lockB"),"T1").start();
        TimeUnit.SECONDS.sleep(1);
        new Thread(new MyThread("lockB","lockA"),"T2").start();
    }
}


class MyThread implements Runnable{

    private String lockA;
    private String lockB;

    public MyThread(String lockA, String lockB) {
        this.lockA = lockA;
        this.lockB = lockB;
    }

    @Override
    public void run() {
        synchronized (lockA){

            System.out.println(Thread.currentThread().getName()+" have "+lockA+" want to get "+lockB);
            try {
                TimeUnit.SECONDS.sleep(2);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            synchronized (lockB){
                System.out.println(Thread.currentThread().getName()+" have "+lockB+" want to get "+lockA);

            }
        }
    }
}
```



![image-20200517155641760](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517155641760.png)



#### java工具监测死锁

1、使用jps - l定位进程号

```java
jps - l
```

![image-20200517160625426](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517160625426.png)

2、使用 jstack 进程号 查看堆栈信息

```java
jstack 进程号 
```

![image-20200517160756846](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200517160756846.png)

平时如何排查问题：

1、日志

2、堆栈信息





