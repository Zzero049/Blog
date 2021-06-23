# volatile底层实现（简要版）

volatile主要解决了内存可见性问题（也叫缓存一致性问题）和指令有序（禁止指令重排）的问题。

## 预备知识：CPU

计算机的硬件之间的交互图如下，是通过各类总线传输二进制数据完成的。

![image-20200610130707218](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200610130707218.png)

由于CPU读写速度往往是内存速度的100倍，为了解决这个矛盾，提出了缓存设计，即存储器的层次结构：

![image-20200611235917240](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200611235917240.png)

各存储结构读写速度对比

![image-20200612000038841](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200612000038841.png)

在现代计算机，一般为多核CPU的三级缓存结构，示意图如下

![image-20200612000012934](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200612000012934.png)

由于每个线程都占用一个PC和Registers，进行切换重写和重指向需要一定时间花销，于是提出了**超线程**，一个核内一个ALU逻辑运算单元，多个PC+Registers（程序计数器和指令寄存器）

下图为四核八线程中一个核的结构：

![image-20200612000617735](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200612000617735.png)

上面了解到三级缓存结构，其中L1，L2放在CPU内部，而L3相当于各个核共享的

![image-20200612000728792](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200612000728792.png)

现在，重点来了，**缓存行cache line**，在现在统一认可的缓存行大小为64B。缓存行越大，局部性空间效率越高，但读取时间慢；缓存行越小，局部性空间效率越低，但读取时间快。

CPU不是按单个Bytes来读取内存数据的，而是以“缓存行“的形式，不可避免的，各个缓存行之间就有数据一致性的问题， 以 i++为例，i的初始值是0.那么在开始每块缓存都存储了i的值0，当第一块内核做i++的时候，其缓存中的值变成了1，即使马上回写到主内存，那么在回写之后第二块内核缓存中的i值依然是0，其执行i++，回写到内存就会覆盖第一块内核的操作，使得最终的结果是1，而不是预期中的2，这就是多核下的缓存一致性问题。

### 缓存一致性问题

CPU对于缓存的设计，为了保证CPU的高效性，并没要求各核的缓存必须要完全一致，而是根据用户需求（程序员），自行决定刷新缓存，而提供保证缓存一致性的方案：

**1、总线锁**

前端总线(也叫CPU总线)是所有CPU与芯片组连接的主干道，负责CPU与外界所有部件的通信，包括高速缓存、内存、北桥，其控制总线向各个部件发送控制信号、通过地址总线发送地址信号指定其要访问的部件、通过数据总线双向传输。在CPU1要做 i++操作的时候，其在总线上发出一个**LOCK#信号**，其他处理器**不能操作所有内存地址的数据**，也就是阻塞了其他CPU，使该处理器可以独享内存。lock前缀的指令在多核处理器下会引发了两件事情

- **将当前处理器缓存行的数据会写回到系统内存。**
- **这个写回内存的操作会引起在其他CPU里缓存了该内存地址的数据无效。**

下图为多个线程读取initFlag的示意图

![image-20200513210054058](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513201942042.png)

扩展：CAS算法底层是一条`lock cmpxchg`汇编指令，至于是锁总线还是锁缓存行，不同机器对lock指令触发的锁也不同，现在的机器基本上先上缓存锁，不行再锁机器。



**2、缓存锁（缓存一致性协议）**

上面提到，总线锁使得锁定期间，其他处理器**不能操作其他内存地址的数据**，**总线锁定的开销比较大**，这种机制显然是**不合适**的。总线锁的力度太大了，最好的方法就是控制锁的保护粒度，只需要保证对于被多个 CPU 缓存的同一个缓存行的数据是一致的就可以了。所以引入了缓存锁。

- 缓存一致性协议

  为了达到数据访问的一致，需要各个处理器在访问缓存时遵循一些协议，在读写时根据协议来操作，常见的协议有 MSI、MESI、MOSI 等。**最常见的就是 MESI 协议**：

  MESI 表示缓存行的四种状态，分别是：

  - **M(Modify)** 表示共享数据只缓存在当前 CPU 缓存中， 并且是被修改状态，也就是缓存的数据和主内存中的数据不一致。
  - **E(Exclusive)** 表示缓存的独占状态，数据只缓存在当前 CPU 缓存中，并且没有被修改。
  - **S(Shared)** 表示数据可能被多个 CPU 缓存，并且各个缓存中的数据和主内存数据一致。
  - **I(Invalid)** 表示缓存已经失效。

在 MESI 协议中，每个缓存的缓存控制器不仅知道自己的 读写操作，而且也监听(snoop)其它 Cache 的读写操作。

对于 MESI 协议，从 CPU 读写角度来说会遵循以下原则:

- **CPU 读请求**：缓存处于 M、E、S 状态都可以被读取，I 状态 CPU 只能从主存中读取数据。
- **CPU 写请求：**缓存处于 M、E 状态才可以被写。对于 S 状态的写，需要将其他 CPU 中缓存行置为无效才可写 

下表示意了，当一个cache line调整了状态的时候，另外一个cache line 需要调整对应的状态。

|       |  M   |  E   |  S   | **I** |
| :---: | :--: | :--: | :--: | :---: |
| **M** |  ×   |  ×   |  ×   |   √   |
| **E** |  ×   |  ×   |  ×   |   √   |
| **S** |  ×   |  ×   |  √   |   √   |
| **I** |  √   |  √   |  √   |   √   |

使用总线锁和缓存锁机制之后，CPU 对于内存的操作大概 可以抽象成下面这样的结构。从而达到缓存一致性效果。

![img](https://gitee.com/zero049/MyNoteImages/raw/master/2845835-36b631f87f4c89a2.png)



- MESI 优化带来的可见性问题：

  CPU 缓存行的状态是通过消息传递来进行的，如果 CPU0 要对一个在缓存中**共享的变量**进行**写入**，首先发送一个失效的消息给到其他缓存了该数据的 CPU。并且要**等到他们的确认回执**。CPU0 在这段时间内都会处于**阻塞状态**。

  ![img](https://gitee.com/zero049/MyNoteImages/raw/master/2845835-f73a72c5c44371ce.png)

  为了避免阻塞带来的资源浪费。在 cpu 中引入 了 `Store Bufferes（存储缓存）` 和 `Invalidate Queue（无效队列）`。
   CPU0 写入共享数据时，直接把数据写入到 store bufferes 中，同时发送 invalidate 消息到其他CPU的Invalidate Queue，然后继续去处理其他指令。
   当收到其他所有 CPU 发送了 invalidate ACK消息时，再将 store bufferes 中的数据数据存储至 cache 中。最后再从本地Cache同步到主内存。

  ![img](https://gitee.com/zero049/MyNoteImages/raw/master/2845835-0c400f1dcb61f10a.png)

  但是 cpu 中引入 Store Bufferes 优化存在两个问题：

  - 1、第⑥、⑦步骤中，由于Invalidate消息进入队列后就给CPU-0返回了ACK响应，不能保证第⑦步骤一定完成。
  - 2、引入了 Store Bufferes 后，处理器会先尝试从 Store Bufferes 中读取值，如果 Store Bufferes 中有数据，则直接从Store Bufferes 中读取，否则就再从本地Cache中读取，从Store Bufferes读取数据存在脏读。

  

并非所有情况都会使用缓存一致性的，如被操作的数据不能被缓存在CPU内部或操作数据跨越多个缓存行(状态无法标识)，则处理器会调用总线锁定；另外当CPU不支持缓存锁定时，自然也只能用总线锁定了，比如说奔腾486以及更老的CPU。

**现代机器缓存一致性方案的结论：MESI如果能解决，就使用MESI；如果不能解决，就锁总线**



### 指令有序性问题

除了数据一致性问题，导致我们程序与预期结果不同的原因还有一点，就是指令重排的问题，指令重排的目的是优化指令执行顺序从而提高CPU效率，如下图，烧开水的命令是比较耗时的，按下热水壶开关的时候CPU就可以先做洗茶壶和洗茶杯的工作

![image-20200612161354489](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200612161354489.png)

从源代码到最终执行的指令，可能会经过三种重排序：

![img](https://gitee.com/zero049/MyNoteImages/raw/master/2845835-8fc217f556cd34f7.png)

编译器重排序，JMM 提供了禁止特定类型的编译器重排序。
处理器重排序，JMM 会要求编译器生成指令时，会插入内存屏障来禁止处理器重排序。

这里先讲操作系统禁止指令重排提供内存屏障的方案：一是sfence lfence mfence等系统原语，二是锁总线。

**内存屏障的作用**

　　1. 阻止屏障两边的指令重排序
  　　2. 强制把写缓冲区/高速缓存中的脏数据等写回主内存，让缓存中相应的数据失效（意思就是确保读到的数据都是内存中的最新的数据，确保数据的有效性）

**内存屏障的分类**

- **sfence lfence mfence等系统原语**

  硬件层提供了一系列的内存屏障 memory barrier / memory fence(Intel的提法)来提供一致性的能力。拿X86平台来说，有几种主要的内存屏障

  1. lfence，是一种Load Barrier 读屏障。在读指令前插入读屏障，可以让高速缓存中的数据失效，重新从主内存加载数据
  2. sfence, 是一种Store Barrier 写屏障。在写指令之后插入写屏障，能让写入缓存的最新数据写回到主内存
  3. mfence, 是一种全能型的屏障，具备ifence和sfence的能力

- **Lock前缀实现了类似的能力.**

  Lock前缀，Lock不是一种内存屏障，但是它能完成类似内存屏障的功能。Lock会对CPU总线和高速缓存加锁，可以理解为CPU指令级的一种锁。它后面可以跟ADD, ADC, AND, BTC, BTR, BTS, CMPXCHG, CMPXCH8B, DEC, INC, NEG, NOT, OR, SBB, SUB, XOR, XADD, and XCHG等指令。

  1. 它先对总线/缓存加锁，然后执行后面的指令，最后释放锁后会把高速缓存中的脏数据全部刷新回主内存。
  2. 在Lock锁住总线的时候，其他CPU的读写请求都会被阻塞，直到锁释放。Lock后的写操作会让其他CPU相关的cache line失效，从而从新从内存加载最新的数据。这个是通过缓存一致性协议做的。



讲到这里操作系统层级的缓存一致性和指令有序性方案基本就了解了，现在可以看volatile是如何保证缓存一致性和指令有序性的了

## volatile（JMM层级实现）

CPU缓存模型图示

![image-20200513180317012](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513180317012.png)

Java Memory Model简称JMM。Java**线程**内存模型跟CPU缓存模型类似，是基于CPU缓存模型来建立的，Java线程内存模型是标准化的，屏蔽掉了底层不同计算机的区别。（逻辑上的）

![image-20200513185332473](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513185332473.png)



先说结论，**volatile底层就是一条lock 并进行加0操作的指令**，上面说到lock指令即可以保证缓存一致性的问题，也可以当做内存屏障，不允许前后指令重排

orderaccess_linux_x86.inline.hpp

```c++
inline void OrderAccess::fence() {
  if (os::is_MP()) {
    // always use locked addl since mfence is sometimes expensive
#ifdef AMD64
    __asm__ volatile ("lock; addl $0,0(%%rsp)" : : : "cc", "memory");
#else
    __asm__ volatile ("lock; addl $0,0(%%esp)" : : : "cc", "memory");
#endif
  }
}
```



### 内存可见性

上面说到，volatile关键字对应的变量，在读写过程中会有一个lock指令，无论是总线锁还是缓存锁，涉及缓存不一致时，都会使其他CPU的缓存行失效，重新从主存中读取。

在JMM层级上，可以理解为，用volatile修饰的变量修改时，立刻通知 其他线程的工作内存中的该变量失效，重新从主存中读取该变量值



### 指令有序性

先说说为什么要保证指令有序性，即便发生的概率可能是十万或者百万分之一，就拿单例模式里面的DCL双重检测锁单例举例

```java
public class Demo03 {
    private volatile static Demo03 singleton = null;

    private Demo03() {
    }
	// 在字节码层面分配对象是一个 new 和 invokespecial 指令
    // 1.分配空间 2.执行构造方法 3.局部变量表指向该空间
    public static Demo03 getInstance() {
        if (singleton == null) {
            synchronized (Demo03.class) {
                if (singleton == null) {
                    singleton = new Demo03();
                }
            }
        }
        return singleton;
    }

}
```

如果单例对象不是volatile的，那么如果是一个订单系统，我们在获取这个订单管理单例时，发生了指令重排，返回给我们一个默认构造的对象，比如订单总数变为0，我们业务拿到这个单例再去执行业务代码修改数据库，那么可想而知，必然有几条数据是错误的，甚至会更加的严重（并发环境谁也说不准）

**内存屏障**

java层级的内存屏障通常所谓的四种即**LoadLoad（LL）,StoreStore（SS）,LoadStore（LS）,StoreLoad（SL）**实际上也是上述两种的组合，完成一系列的屏障和数据同步功能。

- **LoadLoad（LL）屏障**：对于这样的语句Load1; LoadLoad; Load2，在Load2及后续读取操作要读取的数据被访问前，保证Load1要读取的数据被读取完毕。
- **StoreStore（SS）屏障**：对于这样的语句Store1; StoreStore; Store2，在Store2及后续写入操作执行前，保证Store1的写入操作对其它处理器可见。
- **LoadStore（LS）屏障**：对于这样的语句Load1; LoadStore; Store2，在Store2及后续写入操作被刷出前，保证Load1要读取的数据被读取完毕。
- **StoreLoad（SL）屏障**：对于这样的语句Store1; StoreLoad; Load2，在Load2及后续所有读取操作执行前，保证Store1的写入对所有处理器可见。它的开销是四种屏障中最大的。在大多数处理器的实现中，这个屏障是个万能屏障，兼具其它三种内存屏障的功能。

#### volatile语义中的内存屏障?

- volatile的内存屏障策略非常严格保守，非常悲观且毫无安全感的心态：

  - 在每个volatile写操作前插入**StoreStore（SS）屏障**，在写操作后插入StoreLoad屏障；
  - 在每个volatile读操作前插入**LoadLoad（LL）屏障**，在读操作后插入LoadStore屏障；

  ![img](https://gitee.com/zero049/MyNoteImages/raw/master/timg)

  由于内存屏障的作用，避免了volatile变量和其它指令重排序、线程之间实现了通信，使得volatile表现出了轻量锁的特性。

  

### 缓存行对齐与伪共享问题

由于缓存行大小默认为64B，为了保证空间利用率，一个缓存行一般会塞满数据（64B），除非进行填充，那么如果，要修改的数据在同一个缓存行，不同核进行修改时，无论是总线锁还是缓存锁，都会有一个缓存行重复失效的问题，必然产生一定的时间消耗，可以用程序进行验证

```java
public class CacheInvalid {
    private static class T{
        public volatile long x = 0L;    //long 占8B
    }

    public static T[] arr = new T[2];

    static {
        arr[0] = new T();           //  一个缓存行必然能装下这两个T对象
        arr[1] = new T();
    }

    public static void main(String[] args) throws InterruptedException {

        Thread t1 =new Thread(()->{
            for(long i=0;i<10_000_000L;i++){
                arr[0].x = i;
            }
        });
        Thread t2 = new Thread(()->{
            for(long i=0;i<10_000_000L;i++){
                arr[1].x = i;
            }
        });

        long start = System.nanoTime();	//nanoTime()只和进程已运行的时间有关, 不受调系统时间影响.
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        long end = System.nanoTime();
        System.out.println((end-start)/1000_000);
    }
}

```

![image-20200612152832500](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200612152832500.png)

如果我们进行数据填充，不让两个数组的数据被分配到同一个缓存行里呢，是不是就能提高效率？

下面程序进行验证

```java
public class CacheInvalidWithPadding {
    private static class T{
        public volatile long x = 0L;    //long 占8B
        public long v1,v2,v3,v4,v5,v6,v7; //该对象数据部分填充至64B
    }

    public static T[] arr = new T[2];

    static {
        arr[0] = new T();           //  一个缓存行必然能装下这两个T对象
        arr[1] = new T();
    }

    public static void main(String[] args) throws InterruptedException {

        Thread t1 =new Thread(()->{
            for(long i=0;i<10_000_000L;i++){
                arr[0].x = i;
            }
        });
        Thread t2 = new Thread(()->{
            for(long i=0;i<10_000_000L;i++){
                arr[1].x = i;
            }
        });

        long start = System.nanoTime();
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        long end = System.nanoTime();
        System.out.println((end-start)/1000_000);
    }
}
```

![image-20200612152957884](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200612152957884.png)

JDK1.8以前，就是靠上面这种进行填充的方案避免伪共享，甚至是使用以下这种填充

```java
public final static class VolatileLong {
        public volatile long q1, q2, q3, q4, q5, q6, q7;
        public volatile long value = 0L;
        public volatile long p1, p2, p3, p4, p5, p6, p7;
    }
```

JDK1.8中增加了Contended注解方式来解决缓存伪共享问题。

在JDK1.8中，新增了一种注解@sun.misc.Contended，来使各个变量在Cache line中分隔开。注意，jvm需要添加参数`-XX:-RestrictContended`才能开启此功能 

未进行填充的对象

```java
public class DataPadding{
        int value;
        long modifyTime;
        boolean flag;
        long createTime;
        char key;
    }
```

```bash
# Running 64-bit HotSpot VM.
# Using compressed oop with 0-bit shift.
# Using compressed klass with 0-bit shift.
# Objects are 8 bytes aligned.
# Field sizes by type: 4, 1, 1, 2, 2, 4, 4, 8, 8 [bytes]
# Array element sizes: 4, 1, 1, 2, 2, 4, 4, 8, 8 [bytes]

com.hyr.jol.demo.JOLSample_02_Alignment$DataPadding object internals:
 OFFSET  SIZE                                      TYPE DESCRIPTION                               VALUE
      0    12                                           (object header)                           N/A
     12     4                                       int DataPadding.value                         N/A
     16     8                                      long DataPadding.modifyTime                    N/A
     24     8                                      long DataPadding.createTime                    N/A
     32     2                                      char DataPadding.key                           N/A
     34     1                                   boolean DataPadding.flag                          N/A
     35     1                                           (alignment/padding gap)                  
     36     4   com.hyr.jol.demo.JOLSample_02_Alignment DataPadding.this$0                        N/A
Instance size: 40 bytes
Space losses: 1 bytes internal + 0 bytes external = 1 bytes total
```

使用Contended注解：可以指定数据放在不同的缓存行

```java
public class DataPadding {
        @sun.misc.Contended("group1")
        int value;
        @sun.misc.Contended("group1")
        long modifyTime;
        @sun.misc.Contended("group2")
        boolean flag;
        @sun.misc.Contended("group3")
        long createTime;
        @sun.misc.Contended("group3")
        char key;
}
```

```bash
# Running 64-bit HotSpot VM.
# Using compressed oop with 0-bit shift.
# Using compressed klass with 3-bit shift.
# Objects are 8 bytes aligned.
# Field sizes by type: 4, 1, 1, 2, 2, 4, 4, 8, 8 [bytes]
# Array element sizes: 4, 1, 1, 2, 2, 4, 4, 8, 8 [bytes]

com.hyr.jol.demo.JOLSample_02_Alignment$DataPadding object internals:
 OFFSET  SIZE                                      TYPE DESCRIPTION                               VALUE
      0    12                                           (object header)                           N/A
     12     4   com.hyr.jol.demo.JOLSample_02_Alignment DataPadding.this$0                        N/A
     16   128                                           (alignment/padding gap)                  
    144     4                                       int DataPadding.value                         N/A
    148     4                                           (alignment/padding gap)                  
    152     8                                      long DataPadding.modifyTime                    N/A
    160   128                                           (alignment/padding gap)                  
    288     1                                   boolean DataPadding.flag                          N/A
    289   135                                           (alignment/padding gap)                  
    424     8                                      long DataPadding.createTime                    N/A
    432     2                                      char DataPadding.key                           N/A
    434     6                                           (loss due to the next object alignment)
Instance size: 440 bytes
Space losses: 395 bytes internal + 6 bytes external = 401 bytes total
```



### 扩展：HappenBefore原则

   HappenBefore解决的是可见性问题

​    定义：前一个操作的结果对于后续操作是可见的。在 JMM 中，如果一个操作执行的结果需要对另一个操作可见，那么这两个操作必须要存在 happens-before 关系。这两个操作可以是同一个线程，也可以是不同的线程。

#### JMM 中有哪些方法建立 happen-before 规则：

- 1、**as-if-serial 规则（程序顺序执行）**：单个线程中的代码顺序不管怎么重排序，对于结果来说是不变的。
- 2、**volatile 变量规则**，对于 volatile 修饰的变量的写的操作， 一定 happen-before 后续对于 volatile 变量的读操作;
- 3、**监视器锁规则（monitor lock rule）**：对一个监视器的解锁，happens-before于随后对这个监视器的加锁。
- 4、**传递性规则**：如果A happens-before B，且B happens-before C，那么A happens-before C。

- 5、**start 规则**：如果线程 A 执行操作 ThreadB.start(),那么线程 A 的 ThreadB.start()操作 happens-before 线程 B 中的任意操作。

- 6、**join 规则**：如果线程 A 执行操作 ThreadB.join()并成功返回，那么线程 B 中的任意操作 happens-before 于线程 A 从 ThreadB.join()操作成功返回。

这几条规则单独看上去没有什么厉害的地方，这些规则从来都不是单独出现的。。。综合运用效果？

```java
class VolatileExample {
    int a = 0;
    volatile boolean flag = false;

    public void writer() {
        a = 1;           //1
        flag = true;     //2
    }

    public void reader() {
        if (flag) {       //3
            int i = a;    //4
            ...
        }
    }
}
```

**假设线程A执行writer()方法之后**，线程B执行reader()方法，那么线程B执行4的时候一定能看到线程A写入的值吗？注意，a不是volatile变量。

答案是**肯定的**。因为根据happens-before规则，我们可以得到如下关系：

- 根据**程序顺序规则**，1 happens-before 2；3 happens-before 4。
- 根据**volatile规则**，2 happens-before 3。
- 根据**传递性规则**，1 happens-before 4。


 因此，综合运用**程序顺序规则、volatile规则及传递性规则**，我们可以得到1 happens-before 4，即线程B在执行4的时候一定能看到A写入的值。