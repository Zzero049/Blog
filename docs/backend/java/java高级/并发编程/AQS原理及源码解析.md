# AQS原理

AQS = AbstractQueuedSynchronizer 抽象队列同步器

JUC的大多数类，如ReentrantLock、ReentrantReadWriteLock、CountDownLatch、Semaphore等都是通过AQS实现的。是 JDK提供的一个框架，用于实现依赖先进先出（FIFO）等待队列的阻塞锁和相关同步器（信号量，事件等）。 



##  锁机制

锁是用来控制多个线程访问共享资源的方式，一般来说，一个锁能够防止多个线程同时访问共享资源（但是有些锁可以允许多个线程并发的访问共享资源，比如读写锁）。**在Lock接口出现之前，Java程序是靠synchronized关键字实现锁功能的，而Java 5之后，并发包中新增了Lock接口（以及相关实现类）用来实现锁功能**，它提供了与synchronized关键字类似的同步功能，只是在使用时需要显式地获取和释放锁。虽然它缺少了（通过synchronized块或者方法所提供的）隐式获取释放锁的便捷性，但是却拥有了**锁获取与释放的可操作性、可中断的获取锁以及超时获取锁**等多种synchronized关键字所不具备的同步特性。

使用Reentrantlock可以进行尝试锁定**tryLock()**，这样无法锁定，或者在指定时间内无法锁定，返回false；

使用ReentrantLock还可以调用**lockInterruptibly()**方法可以对线程interrupt()方法做出响应，在一个线程等待锁的过程中，可以被打断，打断后会抛异常。当两个线程同时通过lock.lockInterruptibly()想获取某个锁时，假若此时线程A获取到了锁，而线程B只有等待，那么对线程B调用threadB.interrupt()方法能够中断线程B的等待过程。**lock()**方法不允许Thread.interrupt中断,即使检测到Thread.isInterrupted,一样会继续尝试获取锁，失败则继续等待。只是在最后获取锁成功后再把当前线程置为interrupted状态,然后再中断线程。

下面是ReentrantLock的一个再熟悉不过的demo，100个线程把 printIndex 从1 加到 10000

```java
public class ReentrantLockDemo01 {
    private static int printIndex = 1;
    
    //定义锁对象
    private static ReentrantLock lock = new ReentrantLock();
    public static void main(String[] args) {
        
		//定义需要保证线程安全的代码块
        for (int i = 0; i < 100; i++) {
            new Thread(() -> {
                try {
                    //加锁
                    lock.lock();
                    for (int j = 0; j < 100; j++) {
                        System.out.println(printIndex);
                        printIndex++;
                    }
                }finally {
                    //使用finally块来保证释放锁
                    lock.unlock();
                }
            }).start();
        }
    }
}
```

Lock锁应用工作流程：

1.	定义锁对象
2.	在需要线程安全的代码块加锁
3.	使用finally块来保证释放锁

### 自己实现一个锁

1、通过**自旋**实现一个锁

```java
public class SpinLock {
    // 使用线程的原子引用，不考虑ABA问题
    AtomicReference<Thread> reference = new AtomicReference<>();
    // 加锁
    public void lock(){
        Thread current = Thread.currentThread();
        // CAS失败则自旋
        while(!reference.compareAndSet(null,current)){
            
        }
    }
    // 解锁
    public void unLock(){
        Thread current = Thread.currentThread();
        // CAS解锁
        reference.compareAndSet(current,null);
    }
}
```

- 缺点：耗费cpu资源。没有竞争到锁的线程会一直占用CPU资源进行CAS操作，假如个线程获得锁后要花费N秒处理业务逻辑，那另外一个线程就会白白的花费N秒的CPU资源

- 改善思路：让得不到锁的线程让出CPU

  1. **yield+自旋**

  ```java
  public void lock(){
          Thread current = Thread.currentThread();
          // CAS失败则自旋
          while(!reference.compareAndSet(null,current)){
              current.yield();	// 让出CPU
          }
      }
  ```

  ​	虽然能改善一部分的CPU空转问题，但是让出CPU后，CPU选取哪个线程再执行依旧是操作系统决定的，操作系统可能下次还是选择该线程进行执行，也就是说CPU空转问题并没有解决。

  2. **sleep+自旋**

  ```java
  public void lock(){
          Thread current = Thread.currentThread();
          // CAS失败则自旋
          while(!reference.compareAndSet(null,current)){
              try {
                  current.sleep(10);		// 睡10毫秒
              } catch (InterruptedException e) {
                  e.printStackTrace();
              }
          }
      }
  ```

  ​	sleep睡眠的时间是无法确定的，睡多了CPU用不上，睡少了CPU还是空转

2、改进为**park+自旋**实现锁

上述两种改进方案都不太合理，我们可以使用**LockSupport**里的park（阻塞指定线程，空参为当前线程）和unpark（唤醒指定线程）来让出线程，还需要维护一个阻塞线程队列

Java提供了一个较为底层的并发工具类：**LockSupport**，可以让线程停止下来(**阻塞**)，还可以唤醒线程。

下面的实现是**非公平的**，在多线程环境下，在CAS解锁瞬间切换了线程的话，那么此时调用lock的线程是可以拿到锁的，直接执行自己的同步代码，这一点来说是不公平的。

```java
public class SpinParkLock {
    // 使用线程的原子引用
    AtomicReference<Thread> reference = new AtomicReference<>();
    // 维护一个阻塞线程队列
    Queue<Thread> parkQueue = new LinkedBlockingQueue<>();

    // 加锁
    public void lock(){
        Thread current = Thread.currentThread();
        // CAS失败则自旋
        while(!reference.compareAndSet(null,current)){
            park();
        }
    }
    // 解锁
    public void unlock(){
        Thread current = Thread.currentThread();
        // CAS解锁
        reference.compareAndSet(current,null);
        // 唤醒一个线程
        unpark();
    }
    // 阻塞线程并加入阻塞队列
    private void park(){
        parkQueue.offer(Thread.currentThread());
        LockSupport.park(Thread.currentThread());
    }
    // 从阻塞队列中唤醒一个线程
    private void unpark(){
        Thread thread = parkQueue.poll();
        LockSupport.unpark(thread);
    }
}
```



## 队列同步器AQS

**队列同步器AbstractQueuedSynchronizer（AQS）是用来构建锁或者其他同步组件的基础框架，它使用了一个int成员变量表示同步状态**，通过内置的**FIFO队列**来完成资源获取线程的排队工作，并发包的作者（Doug Lea）期望它能够成为实现大部分同步需求的基础。在实现上还借助了**LockSupport类**的方法（park，unpark）

使用AQS来实现一个同步器需要覆盖实现如下几个方法，并且使用getState，setState，compareAndSetState这几个方法来设置获取状态 

1. **boolean tryAcquire(int arg)** 
2. **boolean tryRelease(int arg)** 
3. **int tryAcquireShared(int arg)** 
4. **boolean tryReleaseShared(int arg)** 
5. **boolean isHeldExclusively()**

以上方法不需要全部实现，根据获取的锁的种类可以选择实现不同的方法：

- **独占锁：** 支持独占(排他)获取锁的同步器应该实现tryAcquire、 tryRelease、isHeldExclusively
- **共享锁：** 支持共享获取的同步器应该实现tryAcquireShared、tryReleaseShared。

使用AQS只需要重写获取锁和释放锁的代码，而对于同步队列的维护以及其他支持功能，AQS自己写好了方法来实现。

### CLH队列（FIFO）

同步器依赖内部的CLH同步队列（一个FIFO双向队列，CLH的名字由来是三位科学家）来完成同步状态的管理，当前线程获取同步状态失败时，同步器会将当前线程以及等待状态等信息构造成为一个节点（Node）并将其加入同步队列，同时会阻塞当前线程，当同步状态释放时，会把首节点中的线程唤醒，使其再次尝试获取同步状态。

注意如果当前时刻只有一个线程需要用这个锁，队列为空，head，tail都为null

![image-20200614192931803](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200614192931803.png)

在该队列中，存储的是AQS中的静态内部类Node，这里介绍Node节点里比较关键的属性和方法（前面定义的常量不介绍了）

```java
static final class Node {
    
    // 下面常量代表状态
  	// 线程已取消
   	static final int CANCELLED =  1;
    // 休眠，等待唤醒
   	static final int SIGNAL = -1;
    // 等待条件唤醒
   	static final int CONDITION = -2;
       
   // 共享状态，无条件传播
    static final int PROPAGATE = -3;

    // 前一个节点
    volatile Node prev;
    // 下一个节点
    volatile Node next;
    // 节点绑定线程
    volatile Thread thread;
    //该节点的等待状态：1 CANCELLED,-1 SIGNAL, -2 CONDITION, -3 PROPAGATE，0 other 以上都不是
    volatile int waitStatus;
    
    static final Node SHARED;//表明该节点在共享模式下等待；

	static final Node EXCLUSIVE;//表明该节点在互斥模式下等待；
    
    //当前节点是否在共享模式下等待；
    final boolean isShared(){
        return nextWaiter == SHARED;
    }

	// 返回当前节点的前驱节点； 
    final Node predecessor(){
        Node p = prev;
            if (p == null)
                throw new NullPointerException();
            else
                return p;
    }

}
```

AQS中维护该队列的主要属性，方法有很多，这里不展开介绍了，后面还会提到，这里知道这三个属性即可，**head、tail、state**

```java
public abstract class AbstractQueuedSynchronizer {
    // 等待队列头结点，一般指向一个绑定thread为null的Node节点
	private transient volatile Node head;
    // 等待队列尾结点
	private transient volatile Node tail;
    //锁状态，加锁成功则为1，重入+1 解锁则为0
	private volatile int state;
    
    //以指定模式创建当前线程的Node，并添加到等待队列中，返回添加的节点。
    private Node addWaiter(Node mode) {
        Node node = new Node(Thread.currentThread(), mode);
        // 进行连接
        Node pred = tail;
        if (pred != null) {
            node.prev = pred;
            if (compareAndSetTail(pred, node)) {
                pred.next = node;
                return node;
            }
        }
        enq(node);		//如果tail指向为空的话，说明队列为空的话，调用enq()完成队列初始化并添加；
        return node;
    }
    
    //将node添加到等待队列中，一直循环直到添加成功
    private Node enq(final Node node) {
        for (;;) {
            Node t = tail;
            if (t == null) { // tail节点为null，说明队列为空
                if (compareAndSetHead(new Node()))
                    tail = head;
            } else {
                node.prev = t;
                if (compareAndSetTail(t, node)) {
                    t.next = node;
                    return t;
                }
            }
        }
    }
    
    // 唤醒给定节点的后继节点
    private void unparkSuccessor(Node node) {
        // 获取节点状态
        int ws = node.waitStatus;
        // 小于0则CAS尝试把status修改为0
        if (ws < 0)
            compareAndSetWaitStatus(node, ws, 0);

       	//释放线程保留在后续线程中，该线程通常只是下一个节点。
        //但是，如果取消了它或显然是null，则从尾部向后遍历以找到实际的非取消后继
        Node s = node.next;
        if (s == null || s.waitStatus > 0) {
            s = null;
            for (Node t = tail; t != null && t != node; t = t.prev)
                if (t.waitStatus <= 0)
                    s = t;
        }
        if (s != null)
            LockSupport.unpark(s.thread);
    }
}
```

### AQS底层使用了模板方法模式

同步器的设计是基于模板方法模式的，如果需要自定义同步器一般的方式是这样（模板方法模式很经典的一个应用）：

1. 使用者继承AbstractQueuedSynchronizer并重写指定的方法。（这些重写方法很简单，无非是对于共享资源state的获取和释放）
2. 将AQS组合在自定义同步组件的实现中，并调用其模板方法，而这些模板方法会调用使用者重写的方法。
   这和我们以往通过实现接口的方式有很大区别，这是模板方法模式很经典的一个运用。

**自定义同步器在实现的时候只需要实现共享资源state的获取和释放方式即可，至于具体线程等待队列的维护，AQS已经在顶层实现好了。**自定义同步器实现的时候主要实现下面几种方法：

1. isHeldExclusively()：该线程是否正在独占资源。只有用到condition才需要去实现它。
2. tryAcquire(int)：独占方式。尝试获取资源，成功则返回true，失败则返回false。
3. tryRelease(int)：独占方式。尝试释放资源，成功则返回true，失败则返回false。
4. tryAcquireShared(int)：共享方式。尝试获取资源。负数表示失败；0表示成功，但没有剩余可用资源；正数表示成功，且有剩余资源。
5. tryReleaseShared(int)：共享方式。尝试释放资源，如果释放后允许唤醒后续等待结点返回true，否则返回false。

这里介绍一下底层使用AQS实现的类：

ReentrantLock为例，（可重入独占式锁）：state初始化为0，表示未锁定状态，A线程lock()时，会调用tryAcquire()独占锁并将state+1.之后其他线程再想tryAcquire的时候就会失败，直到A线程unlock（）到state=0为止，其他线程才有机会获取该锁。A释放锁之前，自己也是可以重复获取此锁（state累加），这就是可重入的概念。

注意：获取多少次锁就要释放多少次锁，保证state是能回到零态的。

以CountDownLatch为例，任务分N个子线程去执行，state就初始化 为N，N个线程并行执行，每个线程执行完之后countDown（）一次，state就会CAS减一。当N子线程全部执行完毕，state=0，会unpark()主调用线程，主调用线程就会从await()函数返回，继续之后的动作。

一般来说，自定义同步器要么是独占方法，要么是共享方式，他们也只需实现tryAcquire-tryRelease、tryAcquireShared-tryReleaseShared中的一种即可。但AQS也支持自定义同步器同时**实现独占和共享两种方式，如ReentrantReadWriteLock。**
　在acquire() acquireShared()两种方式下，线程在等待队列中都是忽略中断的，**acquireInterruptibly()/acquireSharedInterruptibly()是支持响应中断**的。



### 自己实现AQS

实现AQS一般都是定义一个静态内部类叫Sync继承AQS重写相应的方法即可。

这里是官方提供的一个例子：定义了一个Mutex类，是不可重入互斥锁。锁资源（state）只有两种状态：0：未被锁定；1：锁定。

```java
class Mutex implements Lock, java.io.Serializable {
    // 自定义同步器
    private static class Sync extends AbstractQueuedSynchronizer {
        // 判断是否锁定状态
        protected boolean isHeldExclusively() {
            return getState() == 1;
        }

        // 尝试获取资源，立即返回。成功则返回true，否则false。
        public boolean tryAcquire(int acquires) {
            assert acquires == 1; // 这里限定只能为1个量
            if (compareAndSetState(0, 1)) {//state为0才设置为1，不可重入！
                setExclusiveOwnerThread(Thread.currentThread());//设置为当前线程独占资源
                return true;
            }
            return false;
        }

        // 尝试释放资源，立即返回。成功则为true，否则false。
        protected boolean tryRelease(int releases) {
            assert releases == 1; // 限定为1个量
            if (getState() == 0)//既然来释放，那肯定就是已占有状态了。只是为了保险，多层判断！
                throw new IllegalMonitorStateException();
            setExclusiveOwnerThread(null);
            setState(0);//释放资源，放弃占有状态
            return true;
        }
    }

    // 真正同步类的实现都依赖继承于AQS的自定义同步器！
    private final Sync sync = new Sync();

    //lock<-->acquire。两者语义一样：获取资源，即便等待，直到成功才返回。
    public void lock() {
        sync.acquire(1);
    }

    //tryLock<-->tryAcquire。两者语义一样：尝试获取资源，要求立即返回。成功则为true，失败则为false。
    public boolean tryLock() {
        return sync.tryAcquire(1);
    }

    //unlock<-->release。两者语文一样：释放资源。
    public void unlock() {
        sync.release(1);
    }

    //锁是否占有状态
    public boolean isLocked() {
        return sync.isHeldExclusively();
    }
}

```



## 从ReentrantLock看清AQS的工作流程

我们知道ReentrantLock是独占锁，但是有公平锁和非公平锁两种初始化方法，在底层是基于Sync再各自继承了并重写了AQS的tryAcquire方法，具体区别放到下面阐述。

![image-20200614204005681](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200614204005681.png)



在最顶层（应用程序）通过ReentrantLock对象执行lock的执行流程图如下：

**公平锁和非公平锁的区别在于：非公平锁在获取锁的时候不是先执行入队判断，而是直接CAS去尝试获取锁。**

下面先展示流程，具体原理解释放在源码解析

![ReentrantLock](https://gitee.com/zero049/MyNoteImages/raw/master/ReentrantLock.png)



### FairSync的lock流程

FairSync是公平锁部分对于AQS的实现

```java
	// Sync类继承自AQS，公平锁和非公平锁主要区别在于获取锁的步骤上，其他方法在Sync实现
	static final class FairSync extends Sync {	
        private static final long serialVersionUID = -3000897897090466540L;
		
        // 获取锁，根据阻塞队列情况判断是直接执行还是进入阻塞队列
        final void lock() {
            acquire(1);		// AQS实现的方法，往下看代码
        }

        // 重写独占锁 获取锁资源的代码
        protected final boolean tryAcquire(int acquires) {
            final Thread current = Thread.currentThread();
            int c = getState();
            if (c == 0) {
                if (!hasQueuedPredecessors() &&			// 注意公平锁和非公平锁的tryAcquire只有这个条件不同而已
                    compareAndSetState(0, acquires)) {
                    setExclusiveOwnerThread(current);
                    return true;
                }
            }
            else if (current == getExclusiveOwnerThread()) {
                int nextc = c + acquires;
                if (nextc < 0)
                    throw new Error("Maximum lock count exceeded");
                setState(nextc);
                return true;
            }
            return false;
        }
    }

```

AQS部分

需要知道Node节点状态waitStatus= -1说明节点已经被阻塞，具体流程后面慢慢说

```java
public abstract class AbstractQueuedSynchronizer
    extends AbstractOwnableSynchronizer
    implements java.io.Serializable {
    
	public final void acquire(int arg) {
        if (!tryAcquire(arg) &&					// tryAcquire是上面重写的方法
            acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
            selfInterrupt();					// selfInterrupt是上面两个条件都成立时，才触发，在后面响应中断详解
    }
    
    // 维护阻塞线程队列的核心方法，源码解析部分进行逐行解释
    final boolean acquireQueued(final Node node, int arg) {
        boolean failed = true;
        try {
            boolean interrupted = false;
            for (;;) {
                final Node p = node.predecessor();
                if (p == head && tryAcquire(arg)) {
                    setHead(node);
                    p.next = null; // help GC
                    failed = false;
                    return interrupted;
                }
                if (shouldParkAfterFailedAcquire(p, node) &&
                    parkAndCheckInterrupt())
                    interrupted = true;
            }
        } finally {
            if (failed)
                cancelAcquire(node);
        }
    }
    
    // 初始化或添加一个Node
    private Node addWaiter(Node mode) {
        Node node = new Node(Thread.currentThread(), mode);
        Node pred = tail;
        if (pred != null) {
            node.prev = pred;
            if (compareAndSetTail(pred, node)) {
                pred.next = node;
                return node;
            }
        }
        enq(node);
        return node;
    }
    
    // 判断是不是队列头head后的第一个
    public final boolean hasQueuedPredecessors() {
        Node t = tail; // Read fields in reverse initialization order
        Node h = head;
        Node s;
        return h != t &&
            ((s = h.next) == null || s.thread != Thread.currentThread());
    }
	
}
```



### NonFairSync的lock流程

公平锁与非公平锁的区别在于，我入队前就可以用CAS去尝试获取锁，其他部分跟

NonFairSync的lock的实现

```java
	static final class NonfairSync extends Sync {
		final void lock() {
            if (compareAndSetState(0, 1))			// CAS尝试修改state，获取锁，0为解锁状态，可重入锁，每次获取锁+1
                setExclusiveOwnerThread(Thread.currentThread());	// 如果CAS操作成功，则把当前线程设为独占锁线程
            else
                acquire(1);				// CAS不成功，则进行阻塞队列维护
        }
		protected final boolean tryAcquire(int acquires) {
            return nonfairTryAcquire(acquires);	//Sync 写好的方法
        }    
    }

	abstract static class Sync extends AbstractQueuedSynchronizer {
        final boolean nonfairTryAcquire(int acquires) {
            final Thread current = Thread.currentThread();
            int c = getState();
            if (c == 0) {
                if (compareAndSetState(0, acquires)) {
                    setExclusiveOwnerThread(current);
                    return true;
                }
            }
            else if (current == getExclusiveOwnerThread()) {
                int nextc = c + acquires;
                if (nextc < 0) // overflow
                    throw new Error("Maximum lock count exceeded");
                setState(nextc);
                return true;
            }
            return false;
        }
    }
```

AQS部分

```java
public abstract class AbstractQueuedSynchronizer
    extends AbstractOwnableSynchronizer
    implements java.io.Serializable {	
	protected final boolean compareAndSetState(int expect, int update) {
        return unsafe.compareAndSwapInt(this, stateOffset, expect, update);	// unsafe类提供CAS算法实现
    }
	//AbstractOwnableSynchronizer的方法
	protected final void setExclusiveOwnerThread(Thread thread) {
        // AQS继承自AbstractOwnableSynchronizer，这个类专门记录一个的独占线程
        // exclusiveOwnerThread是除了序列化ID的唯一属性
        exclusiveOwnerThread = thread;		
    }

	public final void acquire(int arg) {
        if (!tryAcquire(arg) &&					// tryAcquire是上面重写的方法
            acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
            selfInterrupt();					// selfInterrupt是上面两个条件都成立时，才触发，在后面响应中断详解
    }
    
    // 维护阻塞线程队列的核心方法
    final boolean acquireQueued(final Node node, int arg) {
        boolean failed = true;
        try {
            boolean interrupted = false;
            for (;;) {
                final Node p = node.predecessor();
                if (p == head && tryAcquire(arg)) {
                    setHead(node);
                    p.next = null; // help GC
                    failed = false;
                    return interrupted;
                }
                if (shouldParkAfterFailedAcquire(p, node) &&
                    parkAndCheckInterrupt())
                    interrupted = true;
            }
        } finally {
            if (failed)
                cancelAcquire(node);
        }
    }
    
    // 添加
    private Node addWaiter(Node mode) {
        Node node = new Node(Thread.currentThread(), mode);
        // Try the fast path of enq; backup to full enq on failure
        Node pred = tail;
        if (pred != null) {
            node.prev = pred;
            if (compareAndSetTail(pred, node)) {
                pred.next = node;
                return node;
            }
        }
        enq(node);
        return node;
    }
}
```

实际上，非公平锁和公平锁除了是否立即尝试获取锁的外，另外一个区别就在于获取锁时，公平锁还需要判断该结点是不是队头，具体见源码解析

![image-20200616160608671](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200616160608671.png)

### 源码解析

我们上面看到了公平锁和非公平锁的区别，在实现上，公平锁更为复杂，非公平锁仅仅是多了一次调用lock即CAS尝试获取锁的步骤，因此研究透公平锁如何实现自然非公平锁的实现也可以弄懂，下面我们就**从源码上逐一查看公平锁lock的调用过程**



**1、应用程序 初始化为公平锁，并调用ReentrantLock的lock方法**

```java
public class ReentrantLockDemo02 {
    private static ReentrantLock lock = new ReentrantLock(true);		// 公平锁
    public static void main(String[] args) {
        try{
            lock.lock();
            System.out.println(Thread.currentThread());
        }finally {
            lock.unlock();
        }
    }
}

// ReentrantLock的构造方法，其中sync是静态内部类Sync（重写了AQS框架）的对象
public ReentrantLock(boolean fair) {
        sync = fair ? new FairSync() : new NonfairSync();
    }
```

**2、调用lock方法后，调用acquire(1)**;，这里若是非公平锁，则先尝试获取锁，获取不到再调acquire(1);

```java
	final void lock() {
            acquire(1);		// 1——表示重入后state增加，由于每次调用重入+1
        }
```

**3、acquire方法内实际只是个判断，执行加锁，成功则获取锁，失败则加入队列并阻塞，醒来之后再看中断**，而且这个设置中断也很鸡肋，实际执行加锁和排队阻塞的是tryAcquire和acquireQueued(addWaiter(Node.EXCLUSIVE), arg))

```java
public final void acquire(int arg) {
    //tryAcquire(arg)尝试加锁，如果加锁失败则会调用acquireQueued方法加入队列去排队，如果加锁成功则不会调用
    //acquireQueued方法下文会有解释
    //加入队列之后线程会自旋两次再park，等到解锁之后会被unpark，醒来之后判断自己是否被打断了，如果被打断了则执行selfInterrupt方法
    //为什么需要执行这个方法？下文解释
    if (!tryAcquire(arg) &&		// 加锁失败，返回false（再取非则为true），需要执行入队操作
        acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
        selfInterrupt();
    
    // 实际加锁成功，tryAcquire返回true，if判断不成立，方法结束，线程可以直接执行自己的同步代码了
}

// lock这部分即使中断了也没用，最后调用的这个interrupt()只是修改了一下中断标志而已
static void selfInterrupt() {
        Thread.currentThread().interrupt();
    }
```

**4、tryAcquire尝试获取锁**

如果是第一个线程tf，那么和队列无关，线程直接持有锁。并且也不会初始化队列，如果接下来的线程都是交替执行，那么永远和AQS队列无关，都是直接线程持有锁，如果发生了竞争，比如tf持有锁的过程中T2来lock，那么这个时候就会初始化AQS，初始化AQS的时候会在队列的头部虚拟一个Thread为NULL的Node，因为队列当中的head永远是持有锁的那个node（除了第一次会虚拟一个，其他时候都是持有锁的那个线程锁封装的node），现在第一次的时候持有锁的是tf而tf不在队列当中所以虚拟了一个node节点，队列当中的除了head之外的所有的node都在park，当tf释放锁之后unpark某个（基本是队列当中的第二个，为什么是第二个呢？前面说过head永远是持有锁的那个node，当有时候也不会是第二个，比如第二个被cancel之后，至于为什么会被cancel，不在我们讨论范围之内，cancel的条件很苛刻，基本不会发生）node之后，node被唤醒，假设node是t2，那么这个时候会首先把t2变成head（sethead），在sethead方法里面会把t2代表的node设置为head，并且把node的Thread设置为null，为什么需要设置null？其实原因很简单，现在t2已经拿到锁了，node就不要排队了，那么node对Thread的引用就没有意义了。所以队列的head里面的Thread永远为null。

```java
		// 公平锁FairSync部分
		protected final boolean tryAcquire(int acquires) {
   		 	//获取当前线程
            final Thread current = Thread.currentThread();
            //获取lock对象的上锁状态，如果锁是自由状态则=0，如果被上锁则为1，大于1表示重入
            int c = getState();
            //hasQueuedPredecessors，判断自己是否需要排队这个方法比较复杂，
        	//下面我会单独介绍，如果不需要排队则进行cas尝试加锁，如果加锁成功则把当前线程设置为拥有锁的线程
        	//继而返回true
            if (c == 0) {
                if (!hasQueuedPredecessors() &&		// 判断是否需要排队
                    compareAndSetState(0, acquires)) { 	// 不需要排队则CAS修改重入锁状态state
                    //设置当前线程为拥有锁的线程，方面后面判断是不是重入（只需把这个线程拿出来判断是否当前线程即可判断重入） 
                    setExclusiveOwnerThread(current);	
                    return true;
                }
            }
            // 重入部分代码
            else if (current == getExclusiveOwnerThread()) {
    			//如果C不等于0，但是当前线程等于拥有锁的线程则表示这是一次重入，那么直接把状态+1表示重入次数+1
   				//那么这里也侧面说明了reentrantlock是可以重入的，因为如果是重入也返回true，也能lock成功
                int nextc = c + acquires;
                if (nextc < 0)
                    throw new Error("Maximum lock count exceeded");
                setState(nextc);	// 更新重入锁状态state
                return true;
            }
           	// 返回false有两种情况
            //1、如果C等于0，但是该线程需要排队 if代码内的语句不执行 2、如果C不等于0，且该线程不是占有锁的线程
            return false;
        }

	//AQS部分
	protected final int getState() {
        return state;
    }
```

  **公平锁首先会调用tryAcquire去尝试加锁，当然这里的尝试加锁并不是直接加锁，事实上tryAcquire当中其实是在设置状态**

​	**第一步便是判断锁是不是自由状态**，如果是再判断是否需要排队，如果不需要，则CAS尝试获取锁，设置成功则把自己线程设置为独占线程，

​    **第二步如果不是自由状态再判断是不是重入**，如果不是重入则直接返回false加锁失败，如果是重入则把计数器+1



**5、当锁没有线程持有锁时（state==0），`hasQueuedPredecessors()`判断是否需要排队**

```java
	public final boolean hasQueuedPredecessors() {
        Node t = tail; // t代表tail指针指向的Node节点
        Node h = head; // h为head指针指向的Node节点
        Node s;
    	// 下面这句返回语句非常有意思，蕴涵了设计API的很多考虑
    	// 1、队列未初始化 2、队列已经初始化了（后面会说初始化会head指向一个Thread为null的Node节点）
        return h != t &&
            ((s = h.next) == null || s.thread != Thread.currentThread());
    }
```

1. **h != t**
   - **队列没有初始化（说明这时锁都没有竞争，连阻塞队列都还没建立的那种，直接就可以去获取锁了）**，则此时，t和h都为null，h!=t 返回false，然后CAS获取锁即可。
   - **队列已经初始化了（h会指向一个Thread为null的头结点，代表当前有线程持有锁）**，如果队列里面只有这个一个head指向的节点，显然tail也会指向这个节点（至于为什么初始化后就一定有个节点在队列中，看下文），那么h!=t返回false，可以进行加锁操作，否则（队列中的Node节点大于1个），h!=t为true，进行后面的判断
2. **(s = h.next) == null** ，该条判断在队列元素大于一个才会进行
   - 这里首先弄清楚一个概念，当队列初始化之后，head会指向一个Thread为null的Node结点，这个节点的意义是说明，已经有个线程持有锁了，那么排队的是从哪里算起，当然是head.next了。举个例子，比如你去买火车票，你如果是第一个这个时候售票员已经在给你服务了，你不算排队，你后面的才算排队；
   - 当队列元素大于一个的时候，(s = h.next) == null基本就是false的，除非多线程极端情况，后面排队的Node代表突然全部取消了
3. **s.thread != Thread.currentThread()**
   - 上面说到s是指向真正排队的第一个Node，那么如果这个排队的第一个Node代表的线程不是当前调用lock想进入同步代码块的线程，那么就直接进队就行了，也不用去获取锁了。（因为c==0的时候，即为锁未被持有的状态下进入的这个方法，公平锁理应是第一个排队的人应该去持有锁的）
   - 相等的时候有人说是为了重入，没怎么想明白锁空闲的状态下，这个线程已经在阻塞队列里睡着了，怎么再进到这个方法里执行判断的

**<font color="red">6、加锁失败，则需要排队则会调用acquireQueued(addWaiter(Node.EXCLUSIVE), arg))</font>**，这里先看addWaiter

```java
	// addWiater方法创建一个Node节点
	private Node addWaiter(Node mode) {
        //由于AQS队列当中的元素类型为Node，故而需要把当前线程tc封装成为一个Node对象
        Node node = new Node(Thread.currentThread(), mode);
        // 当前节点要入队，则前一个节点为队尾
        Node pred = tail;
        // 上文说到，有队列为空与队列有节点两种情况。
        // pre!=null 代表队列中有节点的情况
        if (pred != null) {
            // 当队列有节点，那么插入到队尾即可
            node.prev = pred;
            if (compareAndSetTail(pred, node)) {	// 需要CAS设置，因为防止多个线程加锁，确保入队的时候是原子操作，防止尾分叉
                pred.next = node;	// 入队
                return node;		// 返回插入的Node
            }
        }
        enq(node);	// 如果队列为空，enq执行初始化
        return node;
    }
	// 该CAS就是判断pred值是不是当前的tail，是的话将tail更新为node
	private final boolean compareAndSetTail(Node expect, Node update) {
        return unsafe.compareAndSwapObject(this, tailOffset, expect, update);
    }
	
	// enq是个死循环
	private Node enq(final Node node) { // 参数的node为上面需要入队的节点，此时未初始化
        // 死循环，直到执行return
        for (;;) {
            // t记录尾节点
            Node t = tail;
            if (t == null) { // 如果t为空，说明此时队列必须初始化，第二次循环就不为空了
                if (compareAndSetHead(new Node()))	// CAS设置队头，为一个默认构造的Node（Thread为空，其他值为null、0或false）
                    // CAS设置头结点的意义是防止多个线程进入enq方法而混乱，没设置到线程直接下一次循环
                    tail = head;
            } else {
                //第二次循环
            	// 进行连接
                node.prev = t;
                if (compareAndSetTail(t, node)) {	// 和addWaiter一样需要线程安全，防止尾分叉
                    t.next = node;					
                    return t;						// 返回之前的尾节点tail，不知道有什么用，可能代码复用要用到这个
                }
            }
        }
    }

```

![图片名称](https://gitee.com/zero049/MyNoteImages/raw/master/尾分叉.png)



我们知道了addWaiter是生成一个结点并入队的过程，再看acquireQueued

```java
	final boolean acquireQueued(final Node node, int arg) {//这里的node 就是当前线程封装的那个node 
    	// 失败标志
        boolean failed = true;
        try {
            // 中断标志
            boolean interrupted = false;
            // 死循环，可以理解为如果是排队第一个节点，求生欲很强，休眠前还要去问拿锁线程搞好没有，我快睡着了；
            // 如果不是第一个线程就直接设置上一个结点状态就阻塞了
            for (;;) {
                // 获取当前线程对应的Node结点的上一个结点，有两种情况；1、上一个节点为头部；2上一个节点不为头部
                final Node p = node.predecessor();
                
                // 如果是排队的第一个，那么去尝试获取锁，tryAcquire方法前面调用过，第一次调用是看能不能直接获取锁（无竞争或重入的情况下直接获取）
                // 如果不能，创建Node节点并加入队列，再第二次调用，判断能不能拿到锁（拿到说明是队列中的第一个）
                // 至于为什么要第二次调用，原因是阻塞线程相对还是比较耗费资源的，如果本来入队就是第一个排队的，那就没必要阻塞
                // 万一上一个线程已经释放锁了，这个排队的阻塞再唤醒就很蠢，所以这里相当于再做了一次询问
                if (p == head && tryAcquire(arg)) {	
                    // 如果拿到锁了，那么head指向的Node可以出队了，就是将head指向，调整Thread指向null，并把prev设置为null
                    setHead(node);
                    p.next = null; // 解除引用方便GC回收
                    failed = false;	// 加锁成失败标志改为false
                    return interrupted;		// 返回false，这里不用纠结，后面会讲到lockInterruptibly()、
                    						// 返回之后acquire方法结束，可以执行自己的同步代码块了
                }
                // 如果自己不是第一个排队的或者自己是第一个，但是上一个线程还没释放锁，那自己乖乖直接去park休眠，等待解锁唤醒即可
                // 下面这两个方法非常有趣，shouldParkAfterFailedAcquire(p, node)需要去修改上一个结点的waitStatus
                 //这里比较难以理解为什么我需要去改变上一个节点的park状态（waitStatus）呢？
                // 每个node都有一个状态，默认为0，表示无状态，-1表示在park；
            	// 当时不能自己把自己改成-1状态？为什么呢？因为你得确定你自己park了才是能改为-1；不然你自己改成自己为-1
              	// 但是改完之后，发生一些奇奇怪怪的事，你迟迟没有park，那不就骗人？
                if (shouldParkAfterFailedAcquire(p, node) &&
                    parkAndCheckInterrupt())
                    interrupted = true;
            }
        } finally {
            if (failed)
                cancelAcquire(node);	// 如果失败了，调用cancelAcquire，这里不做研究
        }
    }

	private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {
        int ws = pred.waitStatus;	// ws记录上一个结点状态
        
        if (ws == Node.SIGNAL)		// Node.SIGNAL为-1，说明是休眠状态
            return true;			// 已经改了，返回true即可（第二次循环）
        
        if (ws > 0) {
           	// ws大于0，主要是Node被取消的状态
            // 循环地把被取消的Node结点剔除
            do {
                node.prev = pred = pred.prev;
            } while (pred.waitStatus > 0);
            pred.next = node;		// 此时pred指向一个最前的未被取消结点，修改其next指向node即可完成剔除
        } else {
            // 非-1或1，那么进入这里（-3 共享模式这里不讨论），主要是无状态0，需要将ws设置为 -1
            compareAndSetWaitStatus(pred, ws, Node.SIGNAL);
        }
        return false;		// 返回false，返回后进入下一次for循环
    }
		

	private final boolean parkAndCheckInterrupt() {		// 正确的修改了上个结点waitStatus之后，
        LockSupport.park(this);							// 利用LockSupport的park方法将这个线程休眠
        return Thread.interrupted();					// interrupted()：获取当前线程的中断状态，并且会清除线程的状态标记。这个返回值主要是给lockInterrupt方法用的
        												// 中断标志置为中断则为true，否则为false
    }

	private void setHead(Node node) {
        head = node;
        node.thread = null;			// head指向的Node结点一定thread为空
        node.prev = null;
    }
```

在这里可以做出公平锁的大致流程如下：

![未命名文件 (7)](https://gitee.com/zero049/MyNoteImages/raw/master/未命名文件 (7).png)

现在就模拟3个线程 t1、t2、t3 （假设t3调用时t1还没释放锁）按序并发调用lock的过程：

1. t1线程，第一个进来，由于此时，没有人获取锁，state==0，且队列尚未初始化，head和tail都为null，不需要排队，则`!tryAcquire(arg)`为false（取非），t1直接执行自己的同步代码块

   ![image-20200617214629211](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200617214629211.png)

2. t2线程进来，此时，state==1，且独占线程为t1，t2要创建节点并入队，但此时队列并未初始化，所以需要先调用`enq(node)`初始化队列，生成一个thread=null的Node节点，再把代表自己的Node节点插入队尾，t2入队完成后，`acquireQueued`方法中有个死循环，会让t2进行队首判断，由于确实t2是第一个排队的，让t2去获取锁，由于t1还是没接释放锁，所以失败了，则将前一个节点，即head指向的节点的waitStatus通过CAS设置为-1，本趟循环结束，开始第二次循环，依旧去获取锁，依旧失败，然后修改waitState，已经修改过直接返回true，并执行`LockSupport.park(this);`将自己休眠

   ![image-20200617230429966](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200617230429966.png)

3. t3线程进来，此时，state==1，且独占线程为t1，t3要创建节点并入队，此时队列已经初始化了，直接入队即可，由于t3并不是排队的第一个，那么自己修改完上一个结点的waitState沉睡就可以了。

   


**<font color="red">7、上面提到加锁过程的CLH队列维护，现在来看解锁时，如何唤醒线程和队列维护</font>**

```java
	// 应用层调用unlock
	public void unlock() {
        sync.release(1);
    }

	// AQS部分
	public final boolean release(int arg) {
        if (tryRelease(arg)) {		// 公平锁和非公平锁释放锁的tryRelease方法都是Sync内的，用的是同一个
           							// 这里的判断主要看是不是重入过的锁，没释放到0都不能释放锁
            Node h = head;			// 先拿到头结点
            if (h != null && h.waitStatus != 0)	// 如果头结点不为空，且状态码修改过，说明后面有排队的Node
                unparkSuccessor(h);				// 唤醒操作，下面说，注意传进来的是head
            return true;
        }
        return false;
    }

	private void unparkSuccessor(Node node) {
        // 获取node的状态
        int ws = node.waitStatus;
        // waitStatus小于0，CAS将其改为0，不知道啥意义
        if (ws < 0)
            compareAndSetWaitStatus(node, ws, 0);

        Node s = node.next;	// s为排队的第一个节点
        if (s == null || s.waitStatus > 0) {		// 没有下一个结点，或者下一个节点被取消了
            s = null;
            for (Node t = tail; t != null && t != node; t = t.prev)	//从tail往前找一个结点唤醒
                if (t.waitStatus <= 0)
                    s = t;
        }
        if (s != null)
            LockSupport.unpark(s.thread);	//不考虑特殊情况，唤醒排队的第一个节点的thread
    }

		//Sync部分
		protected final boolean tryRelease(int releases) {
            // 重入锁计数-1
            int c = getState() - releases;
            // 万一独占线程和当前线程不一致，抛出异常
            if (Thread.currentThread() != getExclusiveOwnerThread())
                throw new IllegalMonitorStateException();
            boolean free = false;
            // 重入次数为0，则修改独占线程为null，设置为null不需要CAS操作
            if (c == 0) {
                free = true;
                setExclusiveOwnerThread(null);
            }
            setState(c);
            return free;
        }

```

是不是有些疑惑，为什么没有head指针的修改等等，而只是唤醒了一个线程，别急，得看我们在哪行代码阻塞了线程，唤醒后，会从那行代码之后继续执行。

```java
	private final boolean parkAndCheckInterrupt() {		// 正确的修改了上个结点waitStatus之后，
        LockSupport.park(this);							// 利用LockSupport的park方法将这个线程休眠
        return Thread.interrupted();					// interrupted()：获取当前线程的中断状态，并且会清除线程的状态标记。
        												// 中断标志置为中断则为true，否则为false
    }


	final boolean acquireQueued(final Node node, int arg) {//这里的node 就是当前线程封装的那个node 
    	// 失败标志
        boolean failed = true;
        try {
            // 中断标志
            boolean interrupted = false;
            // 死循环
            // 当线程被唤醒，此时锁没有人持有（自己是排队的第一个）
            for (;;) {
                final Node p = node.predecessor();
               	// 此时必然能获取到锁
                if (p == head && tryAcquire(arg)) {	
                    setHead(node);				// 调整head和自己的Node
                    p.next = null; 				// 解除引用方便GC回收
                    failed = false;	
                    return interrupted;			// 一路返回就可以执行自己的同步代码了
                    						
                }

                if (shouldParkAfterFailedAcquire(p, node) &&
                    parkAndCheckInterrupt())			// 从这里被唤醒，继续循环
                    interrupted = true;
            }
        } finally {
            if (failed)
                cancelAcquire(node);	
        }
    }

	private void setHead(Node node) {
        head = node;
        node.thread = null;			// head指向的Node结点一定thread为空
        node.prev = null;
    }
	
```

4. 可以接上文提到的t1、t2、t3线程继续讲了，此时假设t1调用unlock释放锁，会修改state为0、独占线程为null并调用`unparkSuccessor(h)`唤醒队列中真正排队的第一个，也就是t2，t2唤醒后，继续循环，此时state==0，且他是队列的第一个，则可以修改state和setExclusiveOwnerThread并返回，执行自己的同步代码，t3唤醒的过程和t2一样，这里就不赘述了，只是最后唤醒t3之后，t3去执行自己的同步代码，执行完了，CLH队列里面都还有一个thread = null的Node节点

   ![image-20200617230507751](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200617230507751.png)



### 可响应中断源码

首先得弄清楚Thread的中断意思

    1. **线程中断仅仅是改变线程的中断状态位，不会停止线程**。需要用户自己去监视线程的状态位并做出相应处理。支持线程中断的方法（也就是线程中断后会抛出`interruptedException`的方法）就是在监视线程的中断状态，**一旦线程的中断状态被置为“中断状态”，就会抛出中断异常。**
       2. **Thread.interrupt()方法不会中断一个正在运行的线程。**
       3. **如果线程在调用 Object 类的 wait()、wait(long) 或 wait(long, int) 方法，或者该类的 join()、join(long)、join(long, int)、sleep(long) 或 sleep(long, int) 方法过程中受阻，则其中断状态将被清除，它还将收到一个InterruptedException异常。这个时候，我们可以通过捕获InterruptedException异常来终止线程的执行，具体可以通过return等退出或改变共享变量的值使其退出。**
       4. **synchronized在获锁的过程中是不能被中断的，意思是说如果产生了死锁，也不可能被中断**（请参考后面的测试例子）。与synchronized功能相似的reentrantLock.lock()方法也是一样，它也不可中断的，即如果发生死锁，那么reentrantLock.lock()方法无法终止，如果调用时被阻塞，则它一直阻塞到它获取到锁为止。但是如果调用带超时的tryLock方法reentrantLock.tryLock(long timeout, TimeUnit unit)，那么如果线程在等待时被中断，将抛出一个InterruptedException异常，这是一个非常有用的特性，因为它允许程序打破死锁。你也可以调用reentrantLock.lockInterruptibly()方法，它就相当于一个超时设为无限的tryLock方法。
       5. 如果该线程在可中断的通道上的 I/O 操作中受阻，则该通道将被关闭，该线程的中断状态将被设置并且该线程将收到一个 ClosedByInterruptException。这时候处理方法一样，只是捕获的异常不一样而已。




**在java的线程Thread类中有三种关于interrupt的方法**

| 方法            | 作用                                                         |
| --------------- | ------------------------------------------------------------ |
| interrupt()     | 将调用该方法的对象所表示的线程标记一个停止标记，并不是真的停止该线程。是一个实例方法。 |
| interrupted()   | 获取**当前线程**的中断状态，并且会清除线程的状态标记。是一个是静态方法。换句话说，如果连续两次调用该方法，则第二次调用将返回 false。 |
| isInterrupted() | 获**取调用该方法的对象所表示的线程**，不会清除线程的状态标记。是一个实例方法。 |

**interrupt机制：**

当外部线程对某线程调用了thread.interrupt()方法后，java语言的处理机制如下：

​    如果该线程处在可中断状态下，（调用了xx.wait()，或者Selector.select(),Thread.sleep()等特定会发生阻塞的api），那么该线程会立即被唤醒，同时会受到一个InterruptedException，同时，如果是阻塞在io上，对应的资源会被关闭。如果该线程接下来不执行“Thread.interrupted()方法（不是interrupt），那么该线程处理任何io资源的时候，都会导致这些资源关闭。当然，解决的办法就是调用一下interrupted()，不过这里需要程序员自行根据代码的逻辑来设定，根据自己的需求确认是否可以直接忽略该中断，还是应该马上退出。**当阻塞状态时，如果有interrupt()发生，系统除了会抛出InterruptedException异常外，还会调用interrupted()函数，调用时能获取到中断状态是true的状态，调用完之后会复位中断状态为false，所以异常抛出之后通过isInterrupted()是获取不到中断状态是true的状态。**

​    如果该线程处在不可中断状态下，就是没有调用上述api，那么java只是设置一下该线程的interrupt状态，其他事情都不会发生，如果该线程之后会调用行数阻塞API，那到时候线程会马上跳出，并抛出InterruptedException，接下来的事情就跟第一种状况一致了。如果不会调用阻塞API，那么这个线程就会一直执行下去。除非你就是要实现这样的线程，一般高性能的代码中肯定会有wait()，yield()之类出让cpu的函数，不会发生后者的情况。

例子1：一个正在运行的线程，interrupt是不会中断的

```java
public class TestThread implements Runnable{ 
 
    boolean stop = false; 
    public static void main(String[] args) throws Exception { 
        Thread thread = new Thread(new TestThread(),"My Thread"); 
        System.out.println( "Starting thread..." ); 
        thread.start(); 
        Thread.sleep( 3000 ); 
        System.out.println( "Interrupting thread..." ); 
        thread.interrupt(); 				// 设置中断状态
        System.out.println("线程是否中断：" + thread.isInterrupted()); 
        Thread.sleep( 3000 ); 
        System.out.println("Stopping application..." ); 
    } 
    public void run() { 
        while(!stop){ 
            System.out.println( "My Thread is running..." ); 
            // 让该循环持续一段时间，使上面的话打印次数少点 
            long time = System.currentTimeMillis(); 
            while((System.currentTimeMillis()-time < 1000)) { 
            } 
        } 
        System.out.println("My Thread exiting under request..." ); 
    } 
} 
```

运行结果：

```
Starting thread...
My Thread is running...
My Thread is running...
My Thread is running...
My Thread is running...
Interrupting thread...
线程是否中断：true
My Thread is running...
My Thread is running...
My Thread is running...
Stopping application...
My Thread is running...
My Thread is running...
……
```

例子2：正确的做法是：

```java
package com.lee.thread.interrupt;
 
public class TestThread2 implements Runnable {
	boolean stop = false;
 
	public static void main(String[] args) throws Exception {
		Thread thread = new Thread(new TestThread2(), "My Thread2");
		System.out.println("Starting thread...");
		thread.start();
		Thread.sleep(3000);
		System.out.println("Interrupting thread...");
		thread.interrupt();
		System.out.println("线程是否中断：" + thread.isInterrupted());
		Thread.sleep(3000);
		System.out.println("Stopping application...");
	}
 
	public void run() {
		while (!stop) {
			System.out.println("My Thread is running...");
			// 让该循环持续一段时间，使上面的话打印次数少点
			long time = System.currentTimeMillis();
			while ((System.currentTimeMillis() - time < 1000)) {
			}
			if (Thread.currentThread().isInterrupted()) {
				return;
			}
		}
		System.out.println("My Thread exiting under request...");
	}
}
```

运行结果： 

```java
Starting thread...
My Thread is running...
My Thread is running...
My Thread is running...
My Thread is running...
Interrupting thread...
线程是否中断：true
Stopping application...
```



知道了**java里面的中断并不是真正的中断线程，而只设置标志位（中断位）来通知用户**，方便我们做自己的业务代码之后，我们来理解一下synchronized不可中断（等待拿锁的线程不可中断）和ReentrantLock的可中断，以及ReentrantLock是如何实现可中断的

我们常说synchronized不可以被中断，并不指synchronized方法不可中断，比如：

```java
public class InterruptSynMethodTest {
	public synchronized void foo() throws InterruptedException {
		System.out.println("foo begin");
		for (int i =0; i < 100; ++i) {
			System.out.println("foo ...");
			Thread.sleep(1000);
		}
	}
 
	public static void main(String[] args) {
		InterruptSynMethodTest it = new InterruptSynMethodTest();
		ExecutorService es = Executors.newCachedThreadPool();
		es.execute(() -> {
	        try {
	            it.foo();
	        } catch (InterruptedException e) {
	        	System.out.println("foo is interrupted, msg=" + e.getMessage());
	        }
	    });
		try {
			Thread.sleep(3000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		es.shutdownNow();
	    System.out.println("Main end");
	}
}
```

synchronized方法foo就可以被中断，执行结果为：

```
foo begin
foo ...
foo ...
foo ...
Main end
foo is interrupted, msg=sleep interrupted
```

**synchronized不可以被中断，指的是synchronized等待不可中断**，比如：

```java
public class InterruptTest {
	
	public synchronized void foo1() {
		System.out.println("foo1 begin");
		for (int i =0; i < 5; ++i) {
			System.out.println("foo1 ...");
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				System.out.println("foo1 sleep is interrupted, msg=" + e.getMessage());
			}
		}
	}
 
	public synchronized void foo2() throws InterruptedException {
		System.out.println("foo2 begin");
		for (int i =0; i < 100; ++i) {
			System.out.println("foo2 ...");
			Thread.sleep(1000);
		}
	}
 
	public static void main(String[] args) {
		InterruptTest it = new InterruptTest();
		ExecutorService es = Executors.newCachedThreadPool();
		es.execute(() -> it.foo1());	
		es.execute(() -> {
	        try {
	            it.foo2();
	        } catch (InterruptedException e) {
	        	System.out.println("foo2 is interrupted, msg=" + e.getMessage());
	        }
	    });	
		try {
			Thread.sleep(3000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		es.shutdownNow();
	    System.out.println("Main end");
	}
}
```

foo2的synchronized在等待foo1时不可被中断，只有在foo2拿到锁之后才可被中断，执行结果为：

```
foo1 begin
foo1 ...
foo1 ...
foo1 ...
foo1 ...
Main end
foo1 sleep is interrupted, msg=sleep interrupted
foo1 ...
foo2 begin
foo2 ...
foo2 is interrupted, msg=sleep interrupted
```

同样的使用lock方法在等待获取锁也是无法做出响应的。

那么ReentrantLock的lockInterruptibly()如何做到线程能在阻塞时响应的，下面我们来看源码

```java
	// ReentrantLock部分
	public void lockInterruptibly() throws InterruptedException {
        sync.acquireInterruptibly(1);
    }
	// AQS部分
	public final void acquireInterruptibly(int arg)
            throws InterruptedException {
        if (Thread.interrupted())			// 获取锁先判断中断标志位，如果被打断了就抛出异常
            throw new InterruptedException();
        if (!tryAcquire(arg))				// tryAcquire方法上文提到了，先判断自己能不能拿到锁
            doAcquireInterruptibly(arg);	// 如果不能获取锁，执行doAcquireInterruptibly，维护队列
    }
	private void doAcquireInterruptibly(int arg)
        throws InterruptedException {
        final Node node = addWaiter(Node.EXCLUSIVE);	// 也是先创建一个代表该线程的Node
        boolean failed = true;
        try {
            for (;;) {
                final Node p = node.predecessor();
                if (p == head && tryAcquire(arg)) {
                    setHead(node);
                    p.next = null; // help GC
                    failed = false;
                    return;
                }
                if (shouldParkAfterFailedAcquire(p, node) &&
                    parkAndCheckInterrupt())
                    throw new InterruptedException();			// 基本上只有这里和acquireQueued方法有区别
            }
        } finally {
            if (failed)
                cancelAcquire(node);
        }
    }

	private final boolean parkAndCheckInterrupt() {		// 正确的修改了上个结点waitStatus之后，
        LockSupport.park(this);							// 利用LockSupport的park方法将这个线程休眠
        return Thread.interrupted();					// interrupted()：获取当前线程的中断状态，并且会清除线程的状态标记。这个返回值主要是给lockInterrupt方法用的
        												// 中断标志置为中断则为true，否则为false
    }
```

为什么lock方法被中断过之后没反应呢？，因为if判断里面仅仅修改了一下变量interrupted，并没有做任何其他操作，而且返回之后也只是调用Thread.currentThread().interrupt()修改中断标志而已，并没有做一些抛出异常或者判断中断其他处理，不像**lockInterruptibly，阻塞的线程睡醒了立马返回是不是被中断过，被中断就会抛出一个InterruptedException**

```java
// lock过程的代码
final boolean acquireQueued(final Node node, int arg) {
        boolean failed = true;
        try {
            boolean interrupted = false;
            for (;;) {
                final Node p = node.predecessor();
                if (p == head && tryAcquire(arg)) {
                    setHead(node);
                    p.next = null; // help GC
                    failed = false;
                    return interrupted;		// 最后拿到锁了，中断过返回true，没中断过返回false
                }
                if (shouldParkAfterFailedAcquire(p, node) &&
                    parkAndCheckInterrupt())
                    interrupted = true;		// 仅仅修改了interrupted变量
            }
        } finally {
            if (failed)
                cancelAcquire(node);
        }
    }

public final void acquire(int arg) {
    if (!tryAcquire(arg) &&		
        acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
        selfInterrupt();	// 仅修改标志
    // 正常返回
}

// lock这部分即使中断了也没用，最后调用的这个interrupt()只是修改了一下中断标志而已
static void selfInterrupt() {
        Thread.currentThread().interrupt();
    }
```

**结论：lockInterruptibly()可响应中断是通过睡醒判断中断标志立马抛出异常实现的。**





## Condition接口

任意一个Java对象，都拥有一组监视器方法（定义在java.lang.Object上），主要包括wait()、wait(long timeout)、notify()以及notifyAll()方法，这些方法与synchronized同步关键字配合，可以实现等待/通知模式。**Condition接口也提供了类似Object的监视器方法，与Lock配合可以实现等待/通知模式。**

**使用方法：**

```java
Lock lock = new ReentrantLock();
Condition condition = lock.newCondition();
public void conditionWait() throws InterruptedException {
    lock.lock();
    try {
        condition.await();
    } finally {
        lock.unlock();
    }
} 

public void conditionSignal() throws InterruptedException {
    lock.lock();
    try {
        condition.signal();
        // condition.signalAll();
    } finally {
        lock.unlock();
    }
}

```

实现原理：

**`ConditionObject`是同步器`AbstractQueuedSynchronizer`的内部类**，因为`Condition`的操作需要获取相关联的锁，所以作为同步器的内部类也较为合理。每个**`ConditionObject`对象都包含着一个队列**（以下称为**等待队列**），该队列是Condition对象实现等待/通知功能的关键。

**等待队列：**

等待队列是一个FIFO的队列，在队列中的每个节点都包含了一个线程引用，该线程就是在Condition对象上等待的线程，**如果一个线程调用了`Condition.await()`方法，那么该线程将会释放锁、构造成节点加入等待队列并进入等待状态。**事实上，节点的定义复用了同步器中节点的定义，也就是说，**同步队列和等待队列中节点类型都是同步器的静态内部类AbstractQueuedSynchronizer.Node。**

**在Object的监视器上，一个对象拥有一个同步队列和等待队列，而同步器拥有一个同步队列和多个等待队列。**
![img](https://gitee.com/zero049/MyNoteImages/raw/master/aHR0cDovL3BpY3R1cmUudGp0dWxvbmcudG9wLyVFNSU5MCU4QyVFNiVBRCVBNSVFOSU5OCU5RiVFNSU4OCU5Ny5KUEc)

**等待await：**

当前线程调用await()方法时，会使当前线程进入等待队列并释放锁，同时线程状态变为等待状态，相当于同步队列的**首节点**（获取了锁的节点）移动到Condition的等待队列中。

![img](https://gitee.com/zero049/MyNoteImages/raw/master/aHR0cDovL3BpY3R1cmUudGp0dWxvbmcudG9wL3dhaXRjb24uSlBH)

ConditionObject的await()方法：

调用await()方法的线程成功获取了锁的线程，也就是同步队列中的首节点，**该方法会将当前线程构造成节点并加入等待队列中，然后释放同步状态，唤醒同步队列中的后继节点，然后当前线程会进入等待状态。**

```java
public final void await() throws InterruptedException {
    if (Thread.interrupted())
        throw new InterruptedException();
    // 当前线程加入等待队列
    Node node = addConditionWaiter();
    
    // 释放同步状态，也就是释放锁
    int savedState = fullyRelease(node);
    int interruptMode = 0;
    while (!isOnSyncQueue(node)) {
        LockSupport.park(this);		// 也是阻塞
        if ((interruptMode = checkInterruptWhileWaiting(node)) != 0)
            break;
    }
    if (acquireQueued(node, savedState) && interruptMode != THROW_IE)
        interruptMode = REINTERRUPT;
    if (node.nextWaiter != null)
        unlinkCancelledWaiters();
    if (interruptMode != 0)
        reportInterruptAfterWait(interruptMode);
}

		
		private Node addConditionWaiter() {
            Node t = lastWaiter;
            // If lastWaiter is cancelled, clean out.
            if (t != null && t.waitStatus != Node.CONDITION) {
                unlinkCancelledWaiters();
                t = lastWaiter;
            }
            Node node = new Node(Thread.currentThread(), Node.CONDITION);
            if (t == null)
                firstWaiter = node;
            else
                t.nextWaiter = node;
            lastWaiter = node;
            return node;
        }

```



**通知signal()：**

**调用Condition的signal()方法，将会唤醒在等待队列中等待时间最长的节点（首节点），在唤醒节点之前，会将节点移到同步队列中。await将该线程阻塞了，当这个节点重新排到同步队列的队首并拿到锁时候才会被唤醒**

![img](https://gitee.com/zero049/MyNoteImages/raw/master/aHR0cDovL3BpY3R1cmUudGp0dWxvbmcudG9wL3NpZ2Nvbi5KUEc)

```java
    public final void signal() {
        if (!isHeldExclusively())
            throw new IllegalMonitorStateException();
        Node first = firstWaiter;
        if (first != null)
            doSignal(first);
    }
        // ConditionObject的方法
        private void doSignal(Node first) {
            do {
                if ( (firstWaiter = first.nextWaiter) == null)
                    lastWaiter = null;
                first.nextWaiter = null;
            } while (!transferForSignal(first) &&
                     (first = firstWaiter) != null);
        }

		final boolean transferForSignal(Node node) {
        /*
         * If cannot change waitStatus, the node has been cancelled.
         */
        if (!compareAndSetWaitStatus(node, Node.CONDITION, 0))
            return false;

        /*
         * Splice onto queue and try to set waitStatus of predecessor to
         * indicate that thread is (probably) waiting. If cancelled or
         * attempt to set waitStatus fails, wake up to resync (in which
         * case the waitStatus can be transiently and harmlessly wrong).
         */
        Node p = enq(node);
        int ws = p.waitStatus;
        if (ws > 0 || !compareAndSetWaitStatus(p, ws, Node.SIGNAL))
            LockSupport.unpark(node.thread);
        return true;
    }
```

通过调用同步器的`enq(Node node)`方法，**等待队列中的头节点线程安全地移动到同步队列。**当节点移动到同步队列后，当前线程再使用LockSupport唤醒该节点的线程。**被唤醒后的线程，将从await()方法中的while循环中退出**（isOnSyncQueue(Node node)方法返回true，节点已经在同步队列中），进而调用同步器的acquireQueued()方法加入到获取同步状态的竞争中。成功获取同步状态之后，被唤醒的线程将从先前调用的await()方法返回，此时该线程已经成功地获取了锁。

**Condition的signalAll()方法，相当于对等待队列中的每个节点均执行一次signal()方法**，效果就是将等待队列中所有节点全部移动到同步队列中，并唤醒每个节点的线程。


## ReentrantReadWriteLock读写锁浅析

**写锁是独占的，**当写锁被获取到时，后续（非当前写操作线程）的读写操作都会被阻塞，写锁释放之后，所有操作继续执行。

**读锁是共享的，**多个线程可以共同读取数据。

一般情况下，读写锁的性能都会比排它锁好，因为大多数场景读是多于写的。在读多于写的情况下，读写锁能够提供比排它锁更好的并发性和吞吐量。Java并发包提供读写锁的实现是ReentrantReadWriteLock。

读写锁使用案例：

```java
public class Cache {
    static Map<String, Object> map = new HashMap<String, Object>();
    static ReentrantReadWriteLock rwl = new ReentrantReadWriteLock();
    static Lock r = rwl.readLock();
    static Lock w = rwl.writeLock();
    
    // 获取一个key对应的value
    public static final Object get(String key) {
        r.lock();
        try {
            return map.get(key);
        } finally {
            r.unlock();
        }
    }

    // 设置key对应的value，并返回旧的value
    public static final Object put(String key, Object value) {
        w.lock();
        try {
            return map.put(key, value);
        } finally {
            w.unlock();
        }
    }
    
    // 清空所有的内容
    public static final void clear() {
        w.lock();
        try {
            map.clear();
        } finally {
            w.unlock();
        }
    }
}

```

**读写锁的实现原理：**

读写锁同样依赖自定义同步器来实现同步功能，而读写状态就是其同步器的同步状态。读写锁的自定义同步器需要在同步状态（一个整型变量）上维护多个读线程和一个写线程的状态。

如果在**一个整型变量上维护多种状态**，就一定需要**按位切割使用**这个变量，读写锁将变量切分成了两个部分，**高16位表示读，低16位表示写**，划分方式如图（当前同步状态表示一个线程已经获取了写锁，且重进入了两次，同时也连续获取了两次读锁）：


![img](https://gitee.com/zero049/MyNoteImages/raw/master/aHR0cDovL3BpY3R1cmUudGp0dWxvbmcudG9wLyVFOCVBRiVCQiVFNSU4NiU5OSVFOSU5NCU4MSVFNyU5QSU4NCVFNSVBRSU5RSVFNyU4RSVCMC5KUEc)

**写锁是一个支持重进入的排它锁**。如果当前线程已经获取了写锁，则增加写状态。如果当前线程在获取写锁时，读锁已经被获取（读状态不为0）或者该线程不是已经获取写锁的线程，则当前线程进入等待状态。

```java
    // 获取写锁
	protected final boolean tryAcquire(int acquires) {
        /*
           1.如果读取计数为非零或写入计数为非零且所有者是另一个线程，则失败
		   2.如果计数饱和，则失败。 （只有在count已经不为零的情况下才可以发生）
           3.否则，如果该线程是可重入获取或队列策略允许的话，则有资格进行锁定。如果是这样，请更新状态并设置所有者
         */
        Thread current = Thread.currentThread();
        int c = getState();
        // 获取写锁状态值
        int w = exclusiveCount(c);
        if (c != 0) {
            // (Note: if c != 0 and w == 0 then shared count != 0)
            if (w == 0 || current != getExclusiveOwnerThread())
                return false;
            if (w + exclusiveCount(acquires) > MAX_COUNT)
                throw new Error("Maximum lock count exceeded");
            // Reentrant acquire
            setState(c + acquires);
            return true;
        }
        if (writerShouldBlock() ||
                !compareAndSetState(c, c + acquires))
            return false;
        setExclusiveOwnerThread(current);
        return true;
    }

```

**读锁是一个支持重进入的共享锁**，它能够被多个线程同时获取，在没有其他写线程访问（或者写状态为0）时，读锁总会被成功地获取，而所做的也只是（线程安全的）增加读状态。

```java
    // 获取读锁
	protected final int tryAcquireShared(int unused) {
        /*
         * Walkthrough:
         * 1.如果另一个线程持有写锁定，则失败
		   2.否则，此线程符合wlock状态，因此请问是否由于队列策略而应阻塞。
		   		如果不是，请尝试通过状态授予和更新计数注意此步骤不检查重入获取，这会推迟到完整版本，以避免在更典型的非重入情况下检查保留计数
           3.如果第2步失败，或者由于线程显然不符合条件或者CA失败或计数饱和，请使用完全重试循环链接到版本
         */
        Thread current = Thread.currentThread();
        int c = getState();
        if (exclusiveCount(c) != 0 &&
                getExclusiveOwnerThread() != current)
            return -1;
        int r = sharedCount(c);
        if (!readerShouldBlock() &&
                r < MAX_COUNT &&
                compareAndSetState(c, c + SHARED_UNIT)) {
            if (r == 0) {
                firstReader = current;
                firstReaderHoldCount = 1;
            } else if (firstReader == current) {
                firstReaderHoldCount++;
            } else {
                HoldCounter rh = cachedHoldCounter;
                if (rh == null || rh.tid != getThreadId(current))
                    cachedHoldCounter = rh = readHolds.get();
                else if (rh.count == 0)
                    readHolds.set(rh);
                rh.count++;
            }
            return 1;
        }
        return fullTryAcquireShared(current);
    }

```

