# Redis缓存问题 

redis作为缓存理论上并发可以达到10w

redis缓存模型

![image-20200530162924731](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530162924731.png)

## 缓存穿透（redis缓存和数据库都没有）

缓存穿透的概念很简单，用户想要査询一个数据，发现 redis内存数据库没有，也就是缓存没有命中，于是向持久层数据库查询。发现也没有，于是本次査询失败，也不会写回到缓存中。当用户很多的时候或者恶意请求，缓存都没有命中，于是都去请求了持久层数据库。这会给持久层数据库造成很大的压力，这时候就相当于出现了缓存穿透。

![image-20200530163809265](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530163809265.png)

试想，如果一条sql语句同一个时间频繁执行（网络攻击），MySQL服务器都去自己去查，那和没有redis缓存有什么区别（缓存就是为了提高性能和减轻负担）直接查询数据库。

**对数据库造成很大的压力的理解**

宕机：每次查询都是访问数据库的，如果sql语句写的烂（索引失效），而且是大量并发请求，容易把CPU占满，服务被kill掉导致宕机，MySQL服务器没有时间去处理别的用户sql请求，一样的相当于无法服务

卡顿：并发请求sql语句，导致运行Mysql服务的机器瞬间CPU飙升导致性能下降。

### 解决方案

#### **1、布隆过滤器（Bloom Filter）**

![image-20200530192855391](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530192855391.png)

布隆过滤器是由一个**长度为==m比特==的位数组（bit array）**与**k个哈希函数（hash function）**组成的数据结构。位数组均初始化为0，所有哈希函数都可以分别把输入数据尽量均匀地散列。

- 当要**插入**一个元素时，将其数据分别输入k个哈希函数，产生k个哈希值。以哈希值作为位数组中的下标，将所有k个对应的比特置为1。
- 当要**查询**（即判断是否存在）一个元素时，同样将其数据输入哈希函数，然后检查对应的k个比特。如果有任意一个比特为0，表明该元素一定不在集合中。如果所有比特均为1，表明该集合有（较大的）可能性在集合中。为什么不是一定在集合中呢？因为一个比特被置为1有可能会受到其他元素的影响，这就是所谓“可能存在”（。

　　下图示出一个m=18, k=3的BF示例。集合中的x、y、z三个元素通过3个不同的哈希函数散列到位数组中。当查询元素w时，因为有一个比特为0，因此w不在该集合中。

![img](https://gitee.com/zero049/MyNoteImages/raw/master/1010726-20200513064355118-157141868.png)

**优点：**

- 不需要存储数据本身，只用比特表示，因此空间占用相对于传统方式有巨大的优势，并且能够保密数据；（512MB=42亿bit）
- 时间效率也较高，插入和查询的时间复杂度均为O(k)；
- 哈希函数之间相互独立，可以在硬件指令层面并行计算。

**缺点：**

- 存在假阳性的概率，不适用于任何要求100%准确率的情境；
- 只能插入和查询元素，不能删除元素，这与产生假阳性的原因是相同的。我们可以简单地想到通过计数（即将一个比特扩展为计数值）来记录元素数，但仍然无法保证删除的元素一定在集合中。

**特点：**

- 哈希函数个数k越多，假阳性概率越低；
- 位数组长度m越大，假阳性概率越低；
- 已插入元素的个数n越大，假阳性概率越高。



布隆过滤器有两种实现，一个是redis，另一个是google的，在java代码层面，使用google布隆过滤器，这里进行介绍

1、导入依赖

```xml
        <dependency>
            <groupId>com.google.guava</groupId>
            <artifactId>guava</artifactId>
            <version>27.0.1-jre</version>
        </dependency>

```

2、进行测试

```java
import com.google.common.hash.BloomFilter;
import com.google.common.hash.Funnels;

import java.util.ArrayList;
import java.util.List;

public class BloomFilterDemo1 {

    // 预存的数据量 100w
    private static int size = 1000000;

    // 创建布隆过滤器对象
    // 接受3个参数，1、数据类型 2、数据容量 3、允许的误差率
    // 创建的bit数组长度9585058，7个哈希函数
    private static BloomFilter<Integer> bloomFilter = BloomFilter.create(Funnels.integerFunnel(), size, 0.01);

    public static void main(String[] args) {
        for (int i = 0; i < size; i++) {
            // 向布隆过滤器存储数据（hash计算对应位置，设置为1）
            bloomFilter.put(i);
        }

        // 创建list
        List<Integer> list = new ArrayList<>();

        // j从101w开始 ,判断布隆过滤器是否包含j
        for (int j = size + 10000; j < size + 20000; j++) {
            // 如果存在
            if(bloomFilter.mightContain(j)){
                list.add(j);
            }
        }

        System.out.println(list.size());
    }
}

```

可以看到10000个测试数据，最终误差有94个

![image-20200530200759296](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530200759296.png)

3、实际用法，就是按上面的流程来算的

```java
@Component
public class BloomFilterDemo2 {
    // 预存的数据量 100w
    private static int size = 1000000;

    // 创建布隆过滤器对象
    // 接受3个参数，1、数据类型 2、数据容量 3、允许的误差率
    private static BloomFilter<Integer> bloomFilter = BloomFilter.create(Funnels.integerFunnel(), size, 0.01);

    @Resource
    private UserDao userDao;

    /**
     * BloomFilterDemo2对象被创建之后，初始化的方法
     */
    @PostConstruct
    public void initData(){
        //查询数据库中所有的id值
        List<Integer> ids = userDao.selectAllIds();

        for(Integer id:ids){
            bloomFilter.put(id);
        }
    }

    /**
     * 模拟从数据库查指定id的数据
     * @param id
     * @return
     */
    public User selectUserById(Integer id){
        //先从缓存中查询
        RedisTemplate<Object,Object> template = new RedisTemplate<>();
        String result = (String)template.opsForValue().get(id);
        //如果不为空，返回即可
        if(result!=null){
            return new User(result);
        }else{
            //从布隆过滤器判断是否存在
            if(bloomFilter.mightContain(id)){
                // 通过Mybatis查询数据库
                User user = userDao.selectById(id);
                if(user!=null){
                    //存在则写回缓存
                    template.opsForValue().set(String.valueOf(id),user.getName());
                }else{
                    // 不存在返回空
                    return null;
                }
            }
        }
        return null;
    }
}
```

**ps：布隆过滤器另一个用途——推荐去重**
例如新闻客户端的推送去重功能，当推荐系统推荐新闻时会从每个用户的历史记录里进行筛选，过滤掉那些已经存在的记录。

实际上，如果历史记录存储在关系数据库里，去重就需要频繁地对数据库进行 exists 查询，当系统并发量很高时，数据库是很难扛住压力的。如果使用缓存把历史记录都放入缓存里，占用空间太大明显不现实，这个时候布隆过滤器就登场了，它就是专门用来解决这种去重问题的。它在起到去重的同时，在空间上还能节省 90% 以上，只是稍微有那么点不精确，也就是有一定的误判概率。

**用户浏览记录存入数据库时，会在Filter上通过key的hash算法存储判断其是否存在，类似于数据存在数据库中，判断该数据是否存在的信息即元数据存放在BloomFilter中，避免了每次判断数据是否存在都要去数据库exist一遍**；这样推送新闻时通过布隆过滤器判断，推送内容是否已经存在，如果存在则不推送，如果不存在则推送；



#### **2、缓存空对象**

将数据库中的空值也缓存到缓存层中，这样查询该空值就不会再访问DB，而是直接在缓存层访问就行。

但是这样有个弊端就是缓存太多空值占用了更多的空间，可以通过给缓存层空值设立一个较短的过期时间来解决，例如60s；但是缓存放空值也是没什么意义的事情。

**布隆过滤器适合于大量的key不存在防止别人恶意攻击的，而缓存空对象适合那种大部分key存在的情况，偶尔拿空缓存**

## 缓存击穿（redis缓存过期导致没有，数据库有）

这里需要注意和缓存击穿的区别，缓存击穿，是指一个key非常热点，在不停的扛着大并发，大并发集中对这一个点进行访问，**当这个key在失效的瞬间（可能设置了ttl）**，持续的大并发就穿破缓存，**直接请求数据库**，就像在一个屏障上凿开了一个洞当某个key在过期的瞬间，有大量的请求并发访问，这类数据一般是热点数据，由于缓存过期，会同时访问数据库来査询最新数据，并且回写缓存，会导使数据库瞬间压力过大。

![image-20200530180348462](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530180348462.png)

### 解决方案

#### 1、设置热点数据不过期

从缓存层面来看，没有设置过期时间，所以不会出现热点key过期后产生的问题。

#### 2、分布式锁

在分布式场景下为了保证数据最终一致性。在单进程的系统中，**存在多个线程可以同时改变某个变量**（可变共享变量）时，就需要对变量或代码块做**同步**(lock—synchronized)，使其在修改这种变量时能够**线性执行消除并发修改变量**。==但分布式系统是多部署、多进程的，==开发语言提供的并发处理API在此场景下就无能为力了。（超卖问题）



实际上分布式锁，是作用在redis缓存层和存储层之间的，当缓存击穿时，每个key只允许一个线程进入数据库，达到减轻数据库压力的效果和防止超卖现象。实际上也就是保证**在集群环境下，保证只允许有一个jvm进行执行。**



**案例：**

一个减库存的操作，如果不进行任何并发同步处理，假设1000个并发请求在一瞬间完成减库存，实际上最后库存可能只减了50。

当然如果是单体的架构，加一个synchronized或者Lock能解决这个问题，但是实际上我们的生产环境是服务器做了nginx负载均衡的，比如springboot运行了2个tomcat服务器，我们的浏览器请求通过nginx配置会选择其中一个tomcat服务器，而一个tomcat只启动一个JVM，synchronized或者Lock又是运行在本JVM上的，因此在分布式的环境中，synchronized或者Lock是不能解决并发问题的。

**1、redis解决方案：**

利用redis是单线程的，而且命令都是原子性的，通过redis的**setnx命令**可以实现分布式锁 

```java
/**
     * 减库存
     */
    @RequestMapping("/deduct_stock")
    public String decrStock(){
        int stock = Integer.parseInt(stringRedisTemplate.opsForValue().get("stock"));

        //redis的setnx命令实现分布式锁
        String lockKey = "lockkey"; //分布式锁的key
        try{
            // setnx + setex
            Boolean getLock = stringRedisTemplate.opsForValue().setIfAbsent(lockKey,"lock", 10,TimeUnit.SECONDS);
            //如果该key已经设置,说明已经有线程获得了
            if(!getLock){
                // 不保证所有线程按先来后到的方式去减库存，没拿到锁的线程直接返回
                return "";
            }
            // 如果没有线程设置该key
            if(stock>0){
                // 库存-1
                int realStock = stock -1;

                stringRedisTemplate.opsForValue().set("stock",realStock+"");
                System.out.println("扣除成功，剩余库存："+realStock+"");
            }else{
                System.out.println("扣除失败，库存不足");
            }
        }finally {
            // 记得使用finally，如果try过程中redis挂掉或者有异常了，也不至于让其他线程一直无法执行
            stringRedisTemplate.delete(lockKey);
        }
        return "end";
    }
```

记得要用try-finally，防止redis挂掉或者有异常了，也不至于让其他线程一直无法执行

但是这个程序依然是有超卖问题的

![image-20200531011536225](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200531011536225.png)

相当于锁压根没加，会出现严重的超卖现象，解决方案也很简单，自己加的锁让自己释放即可

```java
String value = UUID.randomUUID().toString();	// 该线程随机生成一个UUID作为自己唯一的value
Boolean getLock = stringRedisTemplate.opsForValue().setIfAbsent(lockKey, value, 10, TimeUnit.SECONDS);


finally {
    //自己的锁才解锁
            if (value.equals(stringRedisTemplate.opsForValue().get(lockKey))) {
                stringRedisTemplate.delete(lockKey);
            }
        }
```

然而设置过期时间，无法平衡系统安全性和用户体验，太短了容易出现锁失效，太长了redis出故障了用户要等很久才能响应，那么可以进行“续命”操作，可以设置一个分线程，进行一些判断，再给这个key增加存活时间，主要用到的是**getset命令**。再不断优化的过程中，redission就诞生了。

**2、redission解决方案**

redission堪称redis分布式锁最完美实现，他对Redis分布式锁的实现非常完善，实现可重入锁、读写锁、公平锁、信号量、CountDownLatch等很多种复杂的锁的语义，满足我们对分布式锁的不同层次的需求，这一点来说ZK分布式锁就显得匮乏一些了，因此redis官方推荐用redission解决分布式锁的问题。

依赖：

```xml
        <dependency>
            <groupId>org.redisson</groupId>
            <artifactId>redisson</artifactId>
            <version>3.8.2</version>
        </dependency>
```

接着上面的实例演示：

先实现自动装配和redission的一些配置

```java
@SpringBootApplication
public class Redis02SpringbootApplication {

    public static void main(String[] args) {
        SpringApplication.run(Redis02SpringbootApplication.class, args);
    }

    @Bean
    public Redisson redisson(){

        Config config = new Config();
        // 在此用单机模式，也可以支持集群、主从、哨兵模式
        config.useSingleServer().setAddress("redis://localhost:6379").setDatabase(0);
        return (Redisson) Redisson.create(config);
    }
}

```

实例

```java
@RestController
public class IndexController2 {
    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    @Autowired
    private Redisson redisson;

    @RequestMapping("/deduct_stock")
    public String decrStock() {

        int stock = Integer.parseInt(stringRedisTemplate.opsForValue().get("stock"));
        //redis的setnx命令实现分布式锁
        String lockKey = "lockkey"; //分布式锁的key

        // 获取对于该key的锁对象
        RLock lock = redisson.getLock(lockKey);

        try{
            // 加锁，默认超时时间
            lock.lock();    //底层相当于setIfAbsent(lockKey, value, 30, TimeUnit.SECONDS)
            
            // 成功获取锁则执行
            if (stock > 0) {
                // 库存-1
                int realStock = stock - 1;

                stringRedisTemplate.opsForValue().set("stock", realStock + "");
                System.out.println("扣除成功，剩余库存：" + realStock + "");
            } else {
                System.out.println("扣除失败，库存不足");
            }
        }finally {
            lock.unlock();
        }

        return "end";
    }
}
```



图示：

![img](https://gitee.com/zero049/MyNoteImages/raw/master/1090617-20190618183025891-1248337684.jpg)

- **1、加锁机制**

线程去获取锁，获取成功: **执行lua脚本**，保存数据到redis数据库。

线程去获取锁，获取失败: 一直通过while循环尝试获取锁，获取成功后，执行lua脚本，保存数据到redis数据库。

- **2、watch dog自动延期机制**

跟上面redis的分布式锁提到的一样，如果一个线程的业务代码还没执行完，该key有效时间就过了，这就会导致另一个线程拿到这个锁，可能会有一个超卖现象。

于是设计了看门狗线程，定时（一般是存活时间的1/3）的查看当前线程任务是否执行完（unlock），如果没有执行完，适当的增加锁的时间。

- **3、为啥要用lua脚本呢？**

通过封装在lua脚本中发送给redis的代码执行是原子性的，而且redis是单线程的，这样就保证这段复杂业务逻辑执行的**原子性**。

- **4、可重入加锁机制**

Redisson可以实现可重入加锁机制的原因，我觉得跟两点有关：

- Redis存储**锁的数据类型是 Hash**类型
- **Hash数据类型的key值包含了当前线程信息**。

下面是redis存储的数据
![img](https://gitee.com/zero049/MyNoteImages/raw/master/1090617-20190618183037704-975536201.png)

这里表面数据类型是Hash类型,Hash类型是`<field,<key,value>>` 类型,这里field是指 “redission”（自定义的key名）

它的有效期还有9秒，我们再来看里们的key1值为`078e44a3-5f95-4e24-b6aa-80684655a15a:45`

它的组成是：guid + 当前线程的ID。后面的value是就和可重入加锁有关。

相当于上面redis分布式锁的UUID进行验证是该线程的锁一样

**举图说明**

![img](https://gitee.com/zero049/MyNoteImages/raw/master/1090617-20190618183046827-1994396879.png)

上面这图的意思就是可重入锁的机制，它最大的优点就是相同线程不需要在等待锁，而是可以直接进行相应操作。

- **5、Redis分布式锁的缺点**

Redis分布式锁会有个缺陷，就是在**Redis哨兵模式**下:

客户端1 对某个 master节点 写入了redisson锁，此时会异步复制给对应的 slave节点。但是这个过程中一旦**发生 master节点宕机**，主备切换，slave节点从变为了 master节点。

这时客户端2 来尝试加锁的时候，在新的master节点上也能加锁，此时就会导致多个客户端对同一个分布式锁完成了加锁。

这时系统在业务语义上一定会出现问题，即**可能会有超卖现象**。

即在哨兵模式或者主从模式下，如果 master实例宕机的时候，可能导致多个线程同时完成加锁，导致超卖，也就是说并不保证完全的分布式安全的生产环境，而zoo

其实还有个RedLock，但是没被业界认可，因为底层有bug，不推荐使用

- **6、提高性能（TODO）**

我们可以通过分段锁的思想进一步提高性能，比如库存为100，分段的思想将其分为10个key，每个key操作上限为10，提高并发效率

更多的提高性能的方案会慢慢完善



**3、zookeeper的临时节点**

curator是Zookeeper开源的框架，这里简单提及，在代码上使用方面也比较简单，具体Zookeeper实现分布式锁的原理和使用，放到Zookeeper模块里讲解。



**Redis和Zookeeper分布式锁的区别**

redis和zk分布式锁的区别，关键就在于高可用性和强一致性的选择，redis的性能高于zk太多了，但在可靠性上又远远不如zk

- **技术上**

Redis 是nosql数据，主要特点缓存

Zookeeper是分布式协调工具，主要用于分布式解决方案

- **实现上**

区别在获取锁、释放锁、死锁问题上

- - **获取锁**

  **Zookeeper：**多个客户端（jvm），会在Zookeeper上**创建同一个临时节点**，因为Zookeeper节点命名路径保证唯一，不允许出现重复，只要谁能够先创建成功，谁能够获取到锁。当获取不到锁时，可以根据业务需求是否选择不断去尝试获取锁，但比较消耗性能

  **Redis：**多个客户端（jvm），会在Redis使用setnx命令创建**相同的一个key**，因为Redis的key保证唯一，不允许出现重复，只要谁能够先创建成功，谁能够获取到锁。当获取不到锁时，注册个监听器即可，不需要不断主动尝试获取锁，性能开销较小，

- - **释放锁**

  **Zookeeper：**使用直接关闭临时节点session会话连接，因为临时节点生命周期与session会话绑定在一块，如果session会话连接关闭的话，该临时节点也会被删除。

  这时候客户端使用事件监听，如果该临时节点被删除的话，重新进入到获取锁的步骤。对于释放锁的特殊情况，比如持有锁的客户端挂了，因为创建的是临时znode，只要客户端挂了，znode就没了，此时就自动释放锁。

  **Redis：**在释放锁的时候，为了确保是锁的一致性问题，在删除的redis 的key时候，需要判断同一个锁的id，才可以删除。对于释放锁的特殊情况，比如持有锁的客户端挂了，那么只能等待超时时间之后才能释放锁。

- - **共同特征：如何解决死锁现象问题**

  Zookeeper使用会话有效期方式解决死锁现象。

  Redis 是对key设置有效期解决死锁现象

-  **性能角度考虑**

因为Redis是NoSQL数据库，相对比来说Redis比Zookeeper性能要好。

- **可靠性**

从可靠性角度分析，Zookeeper可靠性比Redis更好。

因为Redis有效期不是很好控制，可能会产生有效期延迟，Zookeeper就不一样，因为Zookeeper临时节点先天性可控的有效期，所以相对来说Zookeeper比Redis更好。还有主从复制或哨兵模式下redis会出现一定概率的超卖



## 缓存雪崩（redis缓存大量过期导致没有，数据库有）

缓存雪崩，是指在某一个时间段，高峰期缓存局部失效，或热点缓存集中过期失效，或者缓存层失效（Redis集群宕机），所有请求都会达到存储层。（相当于击穿的升级版）

![image-20200530190748375](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530190748375.png)

产生雪崩的原因之一，比如双十二，很快就会迎来一波抢购，这波商品时间比较集中的放入了缓存，假设缓存一个小时。那么到了凌晨一点钟的时候，这批商品的缓存就都过期了。而对这批商品的访问查询，都落到了数据库上，对于数据库而言，就会产生周期性的压力波峰。于是所有的请求都会达到存储层，存储层的调用量会暴増，造成存储层也会挂掉的情况。

其实集中过期，倒不是非常致命，比较致命的缓存雪崩，是缓存服务器某个节点宕机或断网。因为自然形成的缓存雪崩，一定是在某个时间段集中创建缓存，这个时候，数据库也是可以顶住压力的。无非就是对数据库产生周期性的压力而已。而缓存服务节点的宕机，对数据库服务器造成的压力是不可预知的，很有可能瞬间就把数据库压垮





### 解决方案

#### 1、redis高可用

这个思想的含义是，既然redis有可能挂掉，那我多增设几台redis，这样一台挂掉之后其他的还可以继续工作，其实就是搭建的集群。

为了防止redis挂掉，有三种策略

**（1）熔断模式**

这种模式主要是参考电路熔断，如果一条线路电压过高，保险丝会熔断，防止火灾。放到我们的系统中，如果某个目标服务调用慢或者有大量超时，此时，熔断该服务的调用，对于后续调用请求，不在继续调用目标服务，直接返回，快速释放资源。如果目标服务情况好转则恢复调用。

| 重点监控的机器性能指标                                       |
| ------------------------------------------------------------ |
| cpu(Load)：cpu使用率/负载                                    |
| memory：内存                                                 |
| mysql监控长事务(这里与sql查询超时是紧密结合的，需要重点监控) |
| sql超时                                                      |
| 线程数等                                                     |

总之，除了cpu、内存、线程数外，重点监控数据库端的长事务、sql超时等，绝大多数应用服务器发生的雪崩场景，都是来源于数据库端的性能瓶颈，从而先引起数据库端大量瓶颈，最终拖累应用服务器也发生雪崩，最后就是大面积的雪崩。

**（2）隔离模式**

这种模式就像对系统请求按类型划分成一个个小岛的一样，当某个小岛被烧光了，不会影响到其他的小岛。

例如可以对不同类型的请求使用线程池来资源隔离，每种类型的请求互不影响，如果一种类型的请求线程资源耗尽，则对后续的该类型请求直接返回，不再调用后续资源。这种模式使用场景非常多，例如将一个**服务拆开**，对于重要的服务使用单独服务器来部署，再或者公司最近推广的多中心。

**（3）限流模式**

上述的熔断模式和隔离模式都属于出错后的容错处理机制，而限流模式则可以称为预防模式。限流模式主要是提前对各个类型的请求设置最高的QPS阈值（峰值时间每秒请求数），若高于设置的阈值则对该请求直接返回，不再调用后续资源。这种模式不能解决服务依赖的问题，只能解决系统整体资源分配问题，因为没有被限流的请求依然有可能造成雪崩效应。

**熔断设计**

在熔断的设计主要参考了hystrix的做法。其中最重要的是三个模块：熔断请求判断算法、熔断恢复机制、熔断报警

（1）熔断请求判断机制算法：使用无锁循环队列计数，每个熔断器默认维护10个bucket，每1秒一个bucket，每个blucket记录请求的成功、失败、超时、拒绝的状态，默认错误超过50%且10秒内超过20个请求进行中断拦截。

（2）熔断恢复：对于被熔断的请求，每隔5s允许部分请求通过，若请求都是健康的（RT<250ms）则对请求健康恢复。

（3）熔断报警：对于熔断的请求打日志，异常请求超过某些设定则报警。

**隔离设计**

隔离的方式一般使用两种

（1）线程池隔离模式：使用一个线程池来存储当前的请求，线程池对请求作处理，设置任务返回处理超时时间，堆积的请求堆积入线程池队列。这种方式需要为每个依赖的服务申请线程池，有一定的资源消耗，好处是可以应对突发流量（流量洪峰来临时，处理不完可将数据存储到线程池队里慢慢处理）

（2）信号量隔离模式：使用一个原子计数器（或信号量）来记录当前有多少个线程在运行，请求来先判断计数器的数值，若超过设置的最大线程个数则丢弃改类型的新请求，若不超过则执行计数操作请求来计数器+1，请求返回计数器-1。这种方式是严格的控制线程且立即返回模式，无法应对突发流量（流量洪峰来临时，处理的线程超过数量，其他的请求会直接返回，不继续去请求依赖的服务）

**超时机制设计**

超时分两种，一种是请求的等待超时，一种是请求运行超时。

（1）等待超时：在任务入队列时设置任务入队列时间，并判断队头的任务入队列时间是否大于超时时间，超过则丢弃任务。

（2）运行超时：直接可使用线程池提供的get方法。

#### 2、限流降级

**限流：分布式锁**

这个解决方案的思想是，在缓存失效后，通过加锁或者队列来控制读数据库写缓存的线程数量，比如对某个key只允许一个线程查询数据和写缓存，其他线程等待

**降级：停掉一些非核心业务**

这个解决方案的思想是，停掉一些非核心的业务（比如双十一退货退款的服务是关闭的），提高我们缓存和存储层的性能。

#### 3、数据预热

据加热的含义就是在正式部署之前，我先把可能的数据先预先访问一遍，这样部分可能大量访问的数据就会记载到缓存中。在即将发生大并发访问前手动触发加载缓存不同的key，设置不同的过期时间，让缓存失效的时间点尽量均匀。（比如双十一的0点到1点是数据访问的高发期，对于热门商品，我们提前把缓存数据存货时间设置到凌晨3点）