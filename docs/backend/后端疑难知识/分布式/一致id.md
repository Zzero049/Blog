# 分布式ID

项目初期，数据量与访问量还没有那么大的时候，我们可能使用的单库中单表存着，但是随着业务的快速增长，数据的体量与访问量激增，在单机数据库中我们就可能对大表进行分表，比如说我的订单表按照月分表 ；我们单机数据库扛不住访问量的激增的时候，这时候就要进行分库处理，比如说将订单表进行分片操作，每台数据库上保存着订单的某一个部分，之前单库的时候使用主键id可能是自增的，在分表或者是分表片之后**我们就不能使用数据自增的id**了，因为我们在分表或者是分片之后，会存在多个订单表，他们的表结构是一样的，如果使用主键自增id，会出现不同分表中的id是一样的，这样我们在按照id做操作的时候就没有办法确定哪个是你需要的那条数据。

分布式ID问题主要是在于：**分布式数据库下，进行了垂直拆分和水平拆分，这时候再新增数据就会出现ID一致性的问题**

![image-20200925155912173](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200925155912173.png)

## 解决方案

这里介绍一些常见的解决方案

### 1、UUID生成分布式ID

使用UUID 生成分布式ID的方式很简单，java 自带了生成UUID的工具，我们可以直接使用生成。

```java
public static void main(String[] args) {
        String  uuid = UUID.randomUUID().toString().replace("-","");
        System.out.println(uuid);
}
```

**这样就能生成一个uuid了，我们在插入订单数据的时候，每次生成一次就可以了。我**们可以看到这个uuid没有规律可循，**数据库使用这种主键，效率会降低**，要是这种id作为订单号的话肯定不合适的，订单号往往多层含义生成的，而且是纯数字，看起来会舒服点。

**优点**

- 代码实现足够简单易用。
- UUID由本地生成，没有性能问题。
- 因为具备全球唯一的特性，所以对于数据库迁移这种情况不存在问题。

**缺点**

- 每次生成的ID都是无序的，而且不是全数字，且无法保证趋势递增。
- UUID生成的是字符串，字符串存储性能差，查询效率慢。
- UUID长度过长，不适用于存储，耗费数据库性能。
- ID无一定业务含义，可读性差。

**适用场景**

- 可以用来生成如token令牌一类的场景，足够没辨识度，而且无序可读，长度足够。
- 可以用于无纯数字要求、无序自增、无可读性要求的场景。

### 2、数据库主键

使用数据库主键的方式其实也挺简单，就是在插入数据之前，需要去一个专门的主键数据库中获取一下主键就可以了。

![image-20200925154732396](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200925154732396.png)

很简单，首先我们要先有个专门生成主键的数据库，这个库中比如说有一张生成订单id的表order_id，他有两列一列是id，这个id是自增长的，另一列随便搞上列就行，如下图：

| id   | xxx  |
| ---- | ---- |
| 1    | 数据 |

然后我们在往业务库插入数据的时候，**先去这个order_id 插入一条数据**，然后使用数据库 LAST_INSERT_ID()这个函数，**获取到最后一次插入的id**，我们就可以拿着这个id塞到业务插入那条sql里面了。

**优点：**

- 实现简单，依靠数据库即可，成本小。
- ID数字化，单调自增，满足数据库存储和查询性能。
- 具有一定的业务可读性。

**缺点：**

- 强依赖DB，存在单点问题，如果数据库宕机，则业务不可用。
- DB生成ID性能有限，单点数据库压力大，无法扛高并发场景。

**适用场景**

- 小规模的，数据访问量小的业务场景。
- 无高并发场景，插入记录可控的场景。

优化方案：

1）针对主库单点，如果有**多个Master库，则每个Master库设置的起始数字不一样，步长一样**，可以是Master的个数。比如：Master1 生成的是 1，4，7，10，Master2生成的是2,5,8,11 Master3生成的是 3,6,9,12。这样就可以有效生成集群中的唯一ID，也可以大大降低ID生成数据库操作的负载。**缺点是一定确定好步长，将对后续的扩容带来困难，而且单个数据库本身的压力还是大，无法满足高并发。**适用于数据量不大，数据库不需要扩容的场景。



### 3、雪花算法

雪花算法是Twitter推出的一个**用于生成分布式ID**的算法，雪花算法是一个算法，我们可以基于这个算法生成一个分布式id出来。

![Snowflake图示](https://gitee.com/zero049/MyNoteImages/raw/master/snowflake.png)

- 1bit 符号位，代表正负

- 41 bit 作为毫秒数 - **41位的长度可以使用69年**
- 10 bit 作为机器编号 （5个bit是数据中心，5个bit的机器ID） - **10位的长度最多支持部署1024个节点**，这10位还可以拆分，比如5位表示机房ID，5位表示机器ID，这样就有32*32种组合，一般来说是足够了
- 12 bit 作为毫秒内序列号 - **12位的计数顺序号支持每个节点每毫秒产生4096个ID序号**

算法单机每秒内理论上最多可以生成1000*(2^12)，也就是400W的ID，完全能满足业务的需求。

**优点**

- 每秒能够生成百万个不同的ID，性能佳。
- 时间戳值在高位，中间是固定的机器码，自增的序列在地位，整个ID是趋势递增的。
- 能够根据业务场景数据库节点布置灵活挑战bit位划分，灵活度高。

**缺点**

- **强依赖于<font color="red">机器时钟</font>**，**如果时钟回拨，会导致重复的ID生成，所以一般基于此的算法发现时钟回拨，都会抛异常处理，阻止ID生成**，这可能导致服务不可用。

**适用场景**

- 雪花算法有很明显的缺点就是时钟依赖，如果确保机器不存在时钟回拨情况的话，那使用这种方式生成分布式ID是可行的，当然小规模系统完全是能够使用的。



像百度的uidgenerator 是基于雪花算法的，然后美团的leaf是基于雪花算法与数据库的方式封装而成的。

```java
public class IdWorker{

    //下面两个每个5位，加起来就是10位的工作机器id
    private long workerId;    //工作id
    private long datacenterId;   //数据id
    //12位的序列号
    private long sequence;

    public IdWorker(long workerId, long datacenterId, long sequence){
        // sanity check for workerId
        if (workerId > maxWorkerId || workerId < 0) {
            throw new IllegalArgumentException(String.format("worker Id can't be greater than %d or less than 0",maxWorkerId));
        }
        if (datacenterId > maxDatacenterId || datacenterId < 0) {
            throw new IllegalArgumentException(String.format("datacenter Id can't be greater than %d or less than 0",maxDatacenterId));
        }
        System.out.printf("worker starting. timestamp left shift %d, datacenter id bits %d, worker id bits %d, sequence bits %d, workerid %d",
                timestampLeftShift, datacenterIdBits, workerIdBits, sequenceBits, workerId);

        this.workerId = workerId;
        this.datacenterId = datacenterId;
        this.sequence = sequence;
    }

    //初始时间戳
    private long twepoch = 1288834974657L;

    //长度为5位
    private long workerIdBits = 5L;
    private long datacenterIdBits = 5L;
    //最大值
    private long maxWorkerId = -1L ^ (-1L << workerIdBits);
    private long maxDatacenterId = -1L ^ (-1L << datacenterIdBits);
    //序列号id长度
    private long sequenceBits = 12L;
    //序列号最大值
    private long sequenceMask = -1L ^ (-1L << sequenceBits);
    
    //工作id需要左移的位数，12位
    private long workerIdShift = sequenceBits;
   //数据id需要左移位数 12+5=17位
    private long datacenterIdShift = sequenceBits + workerIdBits;
    //时间戳需要左移位数 12+5+5=22位
    private long timestampLeftShift = sequenceBits + workerIdBits + datacenterIdBits;
    
    //上次时间戳，初始值为负数
    private long lastTimestamp = -1L;

    public long getWorkerId(){
        return workerId;
    }

    public long getDatacenterId(){
        return datacenterId;
    }

    public long getTimestamp(){
        return System.currentTimeMillis();
    }

     //下一个ID生成算法
    public synchronized long nextId() {
        long timestamp = timeGen();

        //获取当前时间戳如果小于上次时间戳，则表示时间戳获取出现异常
        if (timestamp < lastTimestamp) {
            System.err.printf("clock is moving backwards.  Rejecting requests until %d.", lastTimestamp);
            throw new RuntimeException(String.format("Clock moved backwards.  Refusing to generate id for %d milliseconds",
                    lastTimestamp - timestamp));
        }

        //获取当前时间戳如果等于上次时间戳
        //说明：还处在同一毫秒内，则在序列号加1；否则序列号赋值为0，从0开始。
        if (lastTimestamp == timestamp) {  // 0  - 4095
            sequence = (sequence + 1) & sequenceMask;
            if (sequence == 0) {
                timestamp = tilNextMillis(lastTimestamp);
            }
        } else {
            sequence = 0;
        }
        
        //将上次时间戳值刷新
        lastTimestamp = timestamp;

        /**
          * 返回结果：
          * (timestamp - twepoch) << timestampLeftShift) 表示将时间戳减去初始时间戳，再左移相应位数
          * (datacenterId << datacenterIdShift) 表示将数据id左移相应位数
          * (workerId << workerIdShift) 表示将工作id左移相应位数
          * | 是按位或运算符，例如：x | y，只有当x，y都为0的时候结果才为0，其它情况结果都为1。
          * 因为个部分只有相应位上的值有意义，其它位上都是0，所以将各部分的值进行 | 运算就能得到最终拼接好的id
        */
        return ((timestamp - twepoch) << timestampLeftShift) |
                (datacenterId << datacenterIdShift) |
                (workerId << workerIdShift) |
                sequence;
    }

    //获取时间戳，并与上次时间戳比较
    private long tilNextMillis(long lastTimestamp) {
        long timestamp = timeGen();
        while (timestamp <= lastTimestamp) {
            timestamp = timeGen();
        }
        return timestamp;
    }

    //获取系统时间戳
    private long timeGen(){
        return System.currentTimeMillis();
    }
    public static void main(String[] args) {
        IdWorker worker = new IdWorker(21,10,0);
        System.out.println(worker.nextId());
    }

}
```



### 4、Redis的incr生成

我们可以使用redis incr命令来获取这个分布式id，redis中的incr命令生成的id是自增的，而且能保证唯一

**优点**

- 有序递增，可读性强。
- 能够满足一定性能。

**缺点**

- 强依赖于Redis，可能存在单点问题。
- 占用宽带，而且需要考虑网络延时等问题带来地性能冲击。

**适用场景**

- 对性能要求不是太高，而且规模较小业务较轻的场景，而且Redis的运行情况有一定要求，注意网络问题和单点压力问题，如果是分布式情况，那考虑的问题就更多了，所以一帮情况下这种方式用的比较少。

我这里是使用了Redis集群模拟的（这里redis 集群不会使用的可以参考下这个链接：[我是个链接](https://www.cnblogs.com/c-xiaohai/p/8376364.html)），我们可以看下test代码：

```java
@SpringBootTest
@RunWith(SpringRunner.class)
public class RedisIncrCommandTest {

    @Autowired
    private JedisCluster jedisCluster;
    private static Executor pool = Executors.newFixedThreadPool(10);
    @Test
    public void testRedisincr() throws InterruptedException {
        CyclicBarrier barrier = new CyclicBarrier(10);
        for (int i=0;i<10;++i){
            pool.execute(new Runnable() {
                @Override
                public void run() {
                    try {
                        int await = barrier.await();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    } catch (BrokenBarrierException e) {
                        e.printStackTrace();
                    }
                    System.out.println(Thread.currentThread().getName()+":"+jedisCluster.incr("gid_key"));
                }
            });
        }
        Thread.sleep(10000);
    }
}
```

这里使用了10个线程的线程池模拟并发情况，然后使用CyclicBarrier 栅栏，等着这10个线程都准备好了，才放开，能够更接近并发场景。使用incr(key) 的时候，如果这个key没有他会先给你创建一个0。我们来看下结果：

![image-20200925155317868](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200925155317868.png)

### 5、基于美团的Leaf方案

从上面的几种分布式ID方案可以看出，能够解决一定问题，但是都有明显缺陷，为此，美团在数据库的方案基础上做了一个优化，提出了一个叫做**Leaf-segment**的数据库方案。

原方案我们每次获取ID都需要去读取一次数据库，这在高并发和大数据量的情况下很容易造成数据库的压力，那能不能一次性获取一批ID呢，这样就无需频繁的造访数据库了。

Leaf-segment的方案就是**采用每次获取一个ID区间段**的方式来解决，区间段用完之后再去数据库获取新的号段，这样一来可以大大减轻数据库的压力，那怎么做呢？

很简单，我们设计一张表如下：

[![复制代码](pictures/copycode.gif)](javascript:void(0);)

```
+-------------+--------------+------+-----+-------------------+-----------------------------+
| Field       | Type         | Null | Key | Default           | Extra                       |
+-------------+--------------+------+-----+-------------------+-----------------------------+
| biz_tag     | varchar(128) | NO   | PRI |                   |                             |
| max_id      | bigint(20)   | NO   |     | 1                 |                             |
| step        | int(11)      | NO   |     | NULL              |                             |
| desc        | varchar(256) | YES  |     | NULL              |                             |
| update_time | timestamp    | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
+-------------+--------------+------+-----+-------------------+-----------------------------+
```

[![复制代码](pictures/copycode.gif)](javascript:void(0);)

其中biz_tag用来区分业务，max_id表示该biz_tag目前所被分配的ID号段的最大值，step表示每次分配的号段长度，后面的desc和update_time分别表示业务描述和上一次更新号段的时间。原来每次获取ID都要访问数据库，现在只需要把Step设置的足够合理如1000，那么现在可以在1000个ID用完之后再去访问数据库了，看起来真的很酷。

我们现在可以这样设计整个获取分布式ID的流程了：

1. **用户服务在注册一个用户时，需要一个用户ID；会请求生成ID服务(是独立的应用)的接口**
2. **生成ID的服务会去查询数据库，找到user_tag的id，现在的max_id为0，step=1000**
3. **生成ID的服务把max_id和step返回给用户服务，并且把max_id更新为max_id = max_id + step，即更新为1000**
4. **用户服务获得max_id=0，step=1000；**
5. **这个用户服务可以用[max_id + 1，max_id+step]区间的ID，即为[1，1000]**
6. **用户服务把这个区间保存到jvm中**
7. **用户服务需要用到ID的时候，在区间[1，1000]中依次获取id，可采用AtomicLong中的getAndIncrement方法。**
8. **如果把区间的值用完了，再去请求生产ID的服务的接口，获取到max_id为1000，即可以用[max_id + 1，max_id+step]区间的ID，即为[1001，2000]**

显而易见，这种方式很好的解决了数据库自增的问题，而且可以自定义max_id的起点，可以自定义步长，非常灵活易于扩容，于此同时，这种方式也很好的解决了数据库压力问题，而且ID号段是存储在JVM中的，性能获得极大的保障，可用性也过得去，即时数据库宕机了，因为JVM缓存的号段，系统也能够因此撑住一段时间。

优点

- 扩张灵活，性能强能够撑起大部分业务场景。
- ID号码是趋势递增的，满足数据库存储和查询性能要求。
- 可用性高，即使ID生成服务器不可用，也能够使得业务在短时间内可用，为排查问题争取时间。
- 可以自定义max_id的大小，方便业务迁移，方便机器横向扩张。

缺点

- ID号码不够随机，完整的顺序递增可能带来安全问题。
- DB宕机可能导致整个系统不可用，仍然存在这种风险，因为号段只能撑一段时间。
- 可能存在分布式环境各节点同一时间争抢分配ID号段的情况，这可能导致并发问题而出现ID重复生成。

上面的缺点同样需要引起足够的重视，美团技术团队同样想出了一个妙招——**双Buffer**。

正如上所述，既然可能存在多个节点同时请求ID区间的情况，那么避免这种情况就好了，Leaf-segment对此做了优化，**将获取一个号段的方式优化成获取两个号段，在一个号段用完之后不用立马去更新号段，还有一个缓存号段备用**，这样能够有效解决这种冲突问题，而且**采用双buffer的方式，在当前号段消耗了10%的时候就去检查下一个号段有没有准备好，如果没有准备好就去更新下一个号段，当当前号段用完了就切换到下一个已经缓存好的号段去使用，同时在下一个号段消耗到10%的时候，又去检测下一个号段有没有准备好，如此往复。**

下面简要梳理下流程：

1. **当前获取ID在buffer1中，每次获取ID在buffer1中获取**
2. **当buffer1中的Id已经使用到了100，也就是达到区间的10%**
3. **达到了10%，先判断buffer2中有没有去获取过，如果没有就立即发起请求获取ID线程，此线程把获取到的ID，设置到buffer2中。**
4. **如果buffer1用完了，会自动切换到buffer2**
5. **buffer2用到10%了，也会启动线程再次获取，设置到buffer1中**
6. **依次往返**

双buffer的方案考虑的很完善，有单独的线程去观察下一个buffer何时去更新，两个buffer之间的切换使用也解决了临时去数据库更新号段可能引起的并发问题。这样的方式能够增加JVM中业务ID的可用性，而且建议segment的长度为业务高峰期QPS的100倍（经验值，具体可根据自己业务来设定），这样即使DB宕机了，业务ID的生成也能够维持相当长的时间，而且可以有效的兼容偶尔的网络抖动等问题。

优点

- 基本的数据库问题都解决了，而且行之有效。
- 基于JVM存储双buffer的号段，减少了数据库查询，减少了网络依赖，效率更高。

缺点

- segment号段长度是固定的，业务量大时可能会频繁更新号段，因为原本分配的号段会一下子用完。
- 如果号段长度设置的过长，但凡缓存中有号段没有消耗完，其他节点重新获取的号段与之前相比可能跨度会很大。

针对上面的缺点，美团有重新提出动态调整号段长度的方案。

**动态调整Step**

一般情况下，如果你的业务不会有明显的波峰波谷，可以不用太在意调整Step，因为平稳的业务量长期运行下来都基本上固定在一个步长之间，但是如果是像美团这样有明显的活动期，那么Step是要具备足够的弹性来适应业务量不同时间段内的暴增或者暴跌。

假设服务QPS为Q，号段长度为L，号段更新周期为T，那么Q * T = L。最开始L长度是固定的，导致随着Q的增长，T会越来越小。但是本方案本质的需求是希望T是固定的。那么如果L可以和Q正相关的话，T就可以趋近一个定值了。所以本方案每次更新号段的时候，会根据上一次更新号段的周期T和号段长度step，来决定下一次的号段长度nextStep，下面是一个简单的算法，意在说明动态更新的意思：

```
T < 15min，nextStep = step * 2
15min < T < 30min，nextStep = step
T > 30min，nextStep = step / 2
```

至此，满足了号段消耗稳定趋于某个时间区间的需求。当然，面对瞬时流量几十、几百倍的暴增，该种方案仍不能满足可以容忍数据库在一段时间不可用、系统仍能稳定运行的需求。因为本质上来讲，此方案虽然在DB层做了些容错方案，但是ID号段下发的方式，最终还是需要强依赖DB，最后，还是需要在数据库高可用上下足工夫。