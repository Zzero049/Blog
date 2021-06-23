# Redis

Reds（Remote Dictionary Server），即远程字典服务。redis是一个免费开源的使用ANSI语言编写、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库，并提供多种语言的API的NOSQL系列的非关系型数据库（5.x之前单线程），官方提供测试数据，50个并发执行100000个请求，读的速度是11万次/s，写的速度是8.1万次/s，且Redis通过提供多种键值数据类型来适应不同场景下的存储需求，许多语言都包含Redis支持，包括：

![image-20200528005424227](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200528005424227.png)

目前为止Redis支持的键值数据类型如下：

​	1）字符串类型 string
​	2）哈希类型hash
​	3）列表类型list
​	4）集合类型 set
​	5）有序集合类型 sortedset

官网：https://redis.io/

中文网：http://www.redis.cn/

官网下载即可

注意：Winow在 Github上下载（停更很久了！）Redis推荐都是在 Linux服务器上搭建的

## Redis功能

1、内存存储、持久化，内存中是断电即失、所以说持久化很重要（rdb、aof）

2、效率高，可以用于高速缓存

3、发布订阅系统

4、地图信息分析

5、计时器、计数器（浏览量！）

### 特性

1、多样的数据类型

2、持久化

3、集群

4、事务

```
export JAVA_HOME=/usr/tool/jdk8/jdk1.8.0_251
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
ln -s /usr/tool/jdk8/jdk1.8.0_251/bin/java /usr/bin/java
检查
```

## 下载安装

### linux

[Redis中文网](https://www.redis.net.cn/)  linux版

![](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200422130244686.png)

1、下载之后通过xftp或者rz命令上传到服务器

2、解压Redis的安装包！程序一般放/opt里

```shell
mv redis-5.0.5.tar.gz /opt
tar -zxvf redis-5.0.5.tar.gz 
```

![image-20200528132747150](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200528132747150.png)

3、基本的环境安装

```bash
yum install gcc-c++
```

4、make编译并安装

```bash
make
make install
```

5、安装默认会放到`/usr/local/bin`目录下

![image-20200528133317367](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200528133317367.png)

6、将redis配置文件复制到安装目录下,之后就使用这个配置文件，能保证原生配置文件安全和回滚

```bash
mkdir redisConfig
cp /opt/redis-5.0.5/redis.conf redisConfig/
```

7、redis默认不是后台启动的，修改，设置默认后台启动，守护进程

![image-20200528133838876](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200528133838876.png)

8、通过指定的配置文件启动

```bash
redis-server redisConfig/redis.conf 
```

9、测试连通

```
redis-cli -p 6379
ping
set name zero
get name
```

![image-20200528134414173](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200528134414173.png)

10、查看进程

```bash
ps -ef|grep redis
```

![image-20200528134625827](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200528134625827.png)

11、如何关闭redis服务:在客户端执行shutdown和exit

```bash
127.0.0.1:6379> shutdown
not connected> exit
```

![image-20200528134846086](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200528134846086.png)

12、开启远程 登录，详见Redis开启远程连接

13、后面我们会使用单机多 Redis启动集群测试！（多个conf）

### windows

win版 https://github.com/microsoftarchive/redis/releases/tag/win-3.2.100

![image-20200422131108759](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200422131108759.png)

win端解压直接可以使用：

​	redis.windows.conf：    配置文件

​	redis-cli.exe:                  redis的客户端

​	redis-server.exe:           redis服务器端



## 性能测试

redis-benchmark是一个压力测试工具！

官方自带的性能测试工具！

reds-benchmark命令参数：

| 序号 | 选项      | 描述                                       | 默认值    |
| :--- | :-------- | :----------------------------------------- | :-------- |
| 1    | **-h**    | 指定服务器主机名                           | 127.0.0.1 |
| 2    | **-p**    | 指定服务器端口                             | 6379      |
| 3    | **-s**    | 指定服务器 socket                          |           |
| 4    | **-c**    | 指定并发连接数                             | 50        |
| 5    | **-n**    | 指定请求数                                 | 10000     |
| 6    | **-d**    | 以字节的形式指定 SET/GET 值的数据大小      | 2         |
| 7    | **-k**    | 1=keep alive 0=reconnect                   | 1         |
| 8    | **-r**    | SET/GET/INCR 使用随机 key, SADD 使用随机值 |           |
| 9    | **-P**    | 通过管道传输 <numreq> 请求                 | 1         |
| 10   | **-q**    | 强制退出 redis。仅显示 query/sec 值        |           |
| 11   | **--csv** | 以 CSV 格式输出                            |           |
| 12   | **-l**    | 生成循环，永久执行测试                     |           |
| 13   | **-t**    | 仅运行以逗号分隔的测试命令列表。           |           |
| 14   | **-I**    | Idle 模式。仅打开 N 个 idle 连接并等待。   |           |

我们来简单测试一下：

```bash
# 测试：100个并发连接100000请求

# 先打开redis
redis-server redisConfig/redis.conf 
redis-benchmark -h localhost -p 6379 -c 100 -n 100000
```

![image-20200528140327491](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200528140327491.png)





## 基础知识

Redis一共有16个数据库

![image-20200528144254532](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200528144254532.png)

默认使用的是第0个

可以在客户端使用 select迸行切换数据库！

```bash
[root@VM_0_10_centos bin]# redis-cli -p 6379
127.0.0.1:6379> select 3		# 选择3号数据库
OK
127.0.0.1:6379[3]> DBSIZE		# 查看数据库大小
(integer) 0
127.0.0.1:6379[3]> set name zhangsan
OK
127.0.0.1:6379[3]> DBSIZE
(integer) 1
```

清除当前数据库`flushdb`，清除全部数据库`flushall`

```bash
127.0.0.1:6379[3]> flushdb
OK 
127.0.0.1:6379[3]> keys *
(empty list or set)
127.0.0.1:6379> FLUSHALL
OK
127.0.0.1:6379> keys *
(empty list or set)
```

### 为什么Redis用单线程

明白 Redis是很快的，官方表示，Redis是基于内存操作，**CPU不是 Redis性能瓶颈**，**Redis的瓶颈是根据机器的内存和网络带宽**，既然可以使用单线程来实现，就使用单线程了。

Reds是C语言写的，官方提供的数据为100000+的QPs，完全不比同样是使用 key-value的 Memcache差

**1、为什么单线程还这么快？**

1、误区1：高性能的服务器一定是多线程的？

2、误区2：多线程（CPU上下文会切换！）一定比单线程效率高！（与CPU核数有关）

redis 核心就是 如果我的数据全都在内存里，我单线程的去操作 就是效率最高的，为什么呢，因为多线程的本质就是 CPU 模拟出来多个线程的情况，这种模拟出来的情况就有一个代价，就是上下文的切换，对于一个内存的系统来说，它**没有上下文的切换（一次CPU上下文的切换大概在 1500ns 左右。）**就是效率最高的。redis 用 单个CPU 绑定一块内存的数据，然后针对这块内存的数据进行多次读写的时候，都是在一个CPU上完成的，所以它是单线程处理这个事。在内存的情况下，这个方案就是最佳方案

单核环境下，从内存中读取 1MB 的连续数据，耗时大约为 250us，假设1MB的数据由多个线程读取了1000次，那么就有1000次时间上下文的切换，那么就有1500ns * 1000 = 1500us 。

我单线程的读完1MB数据才250us ,你光时间上下文的切换就用了1500us了，我还不算你每次读一点数据 的时间。

**2、那什么时候用多线程的方案呢？**

【**IOPS**（Input/Output Operations Per Second）是一个用于计算机存储设备（如硬盘（HDD）、固态硬盘（SSD）或存储区域网络（SAN））**性能测试的量测方式**】

【**吞吐量**是指对网络、设备、端口、虚电路或其他设施，**单位时间内成功地传送数据的数量**（以比特、字节、分组等测量）】

**答案是：下层的存储等慢速的情况。比如磁盘**

内存是一个 **IOPS 非常高**的系统，因为我想申请一块内存就申请一块内存，销毁一块内存我就销毁一块内存，内存的申请和销毁是很容易的。而且内存是可以动态的申请大小的。

磁盘的特性是：**IOPS很低很低，但吞吐量很高**。这就意味着，**大量的读写操作都必须攒到一起，再提交到磁盘**的时候，**性能最高**。为什么呢？

如果我有一个事务组的操作（就是几个已经分开了的事务请求，比如写读写读写，这么五个操作在一起），在内存中，因为IOPS非常高，我可以一个一个的完成。

但是如果在磁盘中也有这种请求方式的话，我第一个写操作是这样完成的：我先在硬盘中寻址，大概花费10ms，然后我读一个数据可能花费1ms然后我再运算（忽略不计），再写回硬盘又是10ms ，总共21ms

第二个操作去读花了10ms, 第三个又是写花费了21ms ,然后我再读10ms, 写21ms ，**五个请求总共花费83ms，这还是最理想的情况下，这如果在内存中，大概1ms不到。**

所以对于磁盘来说，它吞吐量这么大，那最好的方案肯定是我将**N个请求一起放在一个buff里，然后一起去提交**。

方法就是用异步：将**请求和处理的线程不绑定**，**请求的线程将请求放在一个buff里，然后等buff快满了，处理的线程再去处理这个buff**。然后由**这个buff 统一的去写入磁盘，或者读磁盘，**这样效率就是最高。java里的 IO不就是这么干的么~

对于慢速设备，这种处理方式就是最佳的，**慢速设备有磁盘，网络 ，SSD** 等等，

多线程 ，异步的方式处理这些问题非常常见，大名鼎鼎的netty 就是这么干的。

终于把 redis 为什么是单线程说清楚了，把什么时候用单线程跟多线程也说清楚了。

**3、为何单核cpu绑定一块内存效率最高**

“我们不能任由操作系统负载均衡，因为我们自己更了解自己的程序，所以我们可以手动地为其分配CPU核，而不会过多地占用CPU”，默认情况下**单线程在进行系统调用的时候会随机使用CPU内核**，为了优化Redis，我们可以使用工具为单线程绑定固定的CPU内核，减少不必要的性能损耗！(轮流使用多个CPU执行的弊端：1、CPU切换时损耗的性能（长时间用一个就不用切换了） 2、降频技术导致性能下降)

**redis作为单进程模型的程序，为了充分利用多核CPU，常常在一台server上会启动多个实例。而为了减少切换的开销，有必要为每个实例指定其所运行的CPU。**

Linux 上 **taskset 可以将某个进程绑定到一个特定的CPU**。你比操作系统更了解自己的程序，为了避免调度器愚蠢的调度你的程序，或是为了在多线程程序中避免缓存失效造成的开销。



## 拓展：Object命令

能看到redis里面真正的数据存储结构

```bash
127.0.0.1:6381> Object help
1) OBJECT <subcommand> arg arg ... arg. Subcommands are:
2) ENCODING <key> -- Return the kind of internal representation used in order to store the value associated with a key.
3) FREQ <key> -- Return the access frequency index of the key. The returned integer is proportional to the logarithm of the recent access frequency of the key.
4) IDLETIME <key> -- Return the idle time of the key, that is the approximated number of seconds elapsed since the last access to the key.
5) REFCOUNT <key> -- Return the number of references of the value associated with the specified key.

127.0.0.1:6381> zadd myZset 10 v1
(integer) 1
127.0.0.1:6381> type myZset
zset
127.0.0.1:6381> Object encoding myZset
"ziplist"

```





## Redis的5大数据类型

Redis是一个开源（BSD许可）的，内存中的数据结构存储系统，它可以用作**数据库**、**缓存**和**消息中间件**MQ。它支持多种类型的数据结构，如字符串（strings），散列（hashes），列表（ists），集合（sets），有序集合（sorted sets）与范围查询，bitmaps，hyperloglogs和地理空间（geospatial）索引半径查询。Reds内置了复制（replication），LUA脚本（Lua scripting），LRU驱动事件（LRU eviction），事务（transactions）和不同级别的磁盘持久化（persistence），并通过Reds哨兵（Dentine）和自动分区（Cluster）提供高可用性（high availability）

redis存储的是：key，value格式的数据，其中key都是字符串，value有5种不同的数据结构	

​	1）字符串类型 string

​	2）哈希类型hash                类似map

​	3）列表类型list                    类似LinkedList

​	4）集合类型 set

​	5）有序集合类型 sortedset



本质基本元素都是字符串

redis是保证**二进制安全**的，即各种操作输入的字节流都是原始的，不会特殊格式意义的数据流（如C语言里面'\0'代表字符串结束，而这里'\0'就是'\0'没有任何转换，写入是这样，读取时也是这样），因此想要读取正确的中文字符，必须指定相同的编码语言（GBK、UTF-8）才能正确编码

![image-20200422134807123](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200422134807123.png)

博客只记录常用的命令，命令都是不区分大小写的，但是字符串是区分大小写的，不常用的可见官网Redis命令:http://www.redis.cn/commands.html







### 对key的操作

**1、查看所有key**

```bash
127.0.0.1:6379> keys *
1) "age"
2) "name"
```

**2、exists-判断当前的key是否存在**

```bash
127.0.0.1:6379> exists name
(integer) 1
127.0.0.1:6379> exists name1
(integer) 0
```

**3、move-移除key到另一个库**

```bash
127.0.0.1:6379> move name 1
(integer) 1
127.0.0.1:6379> keys *
1) "age"
127.0.0.1:6379> select 1
OK
127.0.0.1:6379[1]> keys *
1) "name"
127.0.0.1:6379[1]> get name
"zzzz"
```

**4、del-移除key**

```bash
127.0.0.1:6379[1]> del name
(integer) 1
127.0.0.1:6379[1]> keys *
(empty list or set)
```

**5、expire-设置key过期时间，ttl查看剩余存活时间，单位为秒**

```bash
127.0.0.1:6379> expire name 10
(integer) 1
127.0.0.1:6379> ttl name
(integer) 5
127.0.0.1:6379> ttl name
(integer) 3
127.0.0.1:6379> ttl name
(integer) 1
127.0.0.1:6379> ttl name
(integer) -2
```

**6、type-查看类型**

```bash
127.0.0.1:6379> type age
string
```



### 字符串类型 String 

除了set返回值是，基本是字符串内容、长度或者操作字符串数量

**1、创建：set key value**

```bash
127.0.0.1:6379> set hello hello
OK
127.0.0.1:6379> set hello ssss	# 若key存在，则覆盖
OK
127.0.0.1:6379> get hello 
"ssss"
```

**2、获取：get key**

**3、删除：del key**

**4、追加/ 创建：append**

```bash
127.0.0.1:6379> set hello hello
OK
127.0.0.1:6379> append hello " redis"		# 不用"" 也可以插入字符串，但无法加入空格
(integer) 11
127.0.0.1:6379> get hello
"hello redis"
127.0.0.1:6379> append zhangsan zhangsan	# 如果当前key不存在
(integer) 8
```

**5、获取字符串长度：strlen**

```bash
127.0.0.1:6379> strlen zhangsan
(integer) 8
```

**6、自增/自减：incr/decr &emsp;设置步长incrby/decrby**

```bash
127.0.0.1:6379> set view 0	# 初始浏览量0
OK
127.0.0.1:6379> incr views	# 自增1
(integer) 1
127.0.0.1:6379> incr views
(integer) 2
127.0.0.1:6379> decr views	# 自减1
(integer) 1

# 增长一次，步长为10
127.0.0.1:6379> incrby views 10
(integer) 11
127.0.0.1:6379> decrby views 10
(integer) 1
```

**7、范围：getrange**

```bash
127.0.0.1:6379> set hello "hello redis"
OK
127.0.0.1:6379> getrange hello 1 3		# [1，3]右边闭合，和subString还是不同的
"ell"
127.0.0.1:6379> getrange hello 0 -1		# -1 表示到末尾
"hello redis"
```

**8、范围替换：setrange**

```bash
127.0.0.1:6379> setrange hello 6 java
(integer) 11
127.0.0.1:6379> get hello		# 只替换对应长度，超过部分原字符串保留
"hello javas"
```

**9、setex（set with expire）创建/覆盖，并设置过期时间**

```bash
127.0.0.1:6379> setex hello 5 hehe	# 5秒存活时间，覆盖了hello
OK
127.0.0.1:6379> get hello
"hehe"
127.0.0.1:6379> ttl hello
(integer) -2
127.0.0.1:6379> get hello
(nil)
```

**10、setnx（set if not exists）创建，如果不存在**

可以用于版本号，存在+1，不存在创建

```bash
127.0.0.1:6379> set name zhangsan
OK
127.0.0.1:6379> setnx name lisi		# 存在，创建失败，返回0
(integer) 0
127.0.0.1:6379> setnx lisi lisi		# 不存在，创建成功，返回1
(integer) 1
```

**11、批量操作：m，注意整条语句是原子操作**

```bash
127.0.0.1:6379> mset k1 v1 k2 v2 k3 v3	# 批量设置
OK
127.0.0.1:6379> keys *
1) "k3"
2) "k2"
3) "k1"
127.0.0.1:6379> msetnx k1 xxx k4 v4		# 由于k1存在，此次批量setnx失败
(integer) 0
127.0.0.1:6379> keys *
1) "k3"
2) "k2"
3) "k1"
127.0.0.1:6379> mget k1 k2 k3
1) "v1"
2) "v2"
3) "v3"

# 通过批处理，实际上可以模拟json字符保存一个对象
# 下面的key是一个巧妙的设计： user:{id}:{filed}
127.0.0.1:6379> mset user:1:name zhangsan user:1:age 18	# 1号用户
OK
127.0.0.1:6379> mget user:1:name user:1:age
1) "zhangsan"
2) "18"
```

**12、组合命令：获取后设置 getset**

不存在时返回nil，存在时，获取原来值，并设置新的值

```bash
127.0.0.1:6379> getset db redis # 获取时不存在
(nil)
127.0.0.1:6379> get db
"redis"
127.0.0.1:6379> getset db mongoDB
"redis"
127.0.0.1:6379> get db
"mongoDB"
```

String类似的使用场景：value除了是我们的字符串还可以是我们的数字！

**String作为字符串使用：**

- 对象缓存存储（json）
- UUID
- 小文件转储（转成字节）
- 共享session

**String作为数值使用：**

- 计数器（点击率、限流、统计）





###  哈希类型：Hash

Map集合，key-Map（Map：key-value）集合，方法和 String类型没有太大区别，仅仅多了一个h，还是一个简单的 key-vlaue

key代表hash变量名，field表示存的键值对的key（字段名）

**1、存储：hset key  field value**

**2、获取：hget field  key** 

​		hgetall key:获取所有的field和value

**3、删除：hdel  key  field**

**4、不存在时创建：hsetnx key field value**

```bash
127.0.0.1:6379> hset myhash field1 zero
(integer) 1
127.0.0.1:6379> hget myhash field1
"zero"
127.0.0.1:6379> hdel myhash field1
(integer) 1
127.0.0.1:6379> hsetnx myhash field1 zero		# 存在时不创建
(integer) 0
127.0.0.1:6379> hsetnx myhash field2 zhangsan
(integer) 1
```

**4、批处理：hmset、hmget**

```bash
127.0.0.1:6379> hmset myhash field1 zhangsan field2 lisi field3 wangwu
OK
127.0.0.1:6379> hgetall myhash
1) "field1"
2) "zhangsan"
3) "field2"
4) "lisi"
5) "field3"
6) "wangwu"

127.0.0.1:6379> hmget myhash field1 field2 field3
1) "zhangsan"
2) "lisi"
3) "wangwu"

```

**5、hash的长度：hlen**

```bash
127.0.0.1:6379> hlen myhash
(integer) 3
```

**6、判断hash中某个field是否存在：hexists**

```bash
127.0.0.1:6379> HEXISTS myhash field3
(integer) 1
127.0.0.1:6379> HEXISTS myhash field4
(integer) 0
```

**7、只获得所有key：hkeys；只获得所有val：hvals**

```bash
127.0.0.1:6379> hkeys myhash
1) "field1"
2) "field2"
3) "field3"
127.0.0.1:6379> hvals myhash
1) "zhangsan"
2) "lisi"
3) "wangwu"
```

**8、指定增量增加：hincrby，hash没有自减和自增1**

```bash
127.0.0.1:6379> flushdb
OK
127.0.0.1:6379> hset myhash field1 1			# 增1
(integer) 1
127.0.0.1:6379> hincrby myhash field1 10		# 加10
(integer) 11
127.0.0.1:6379> hincrby myhash field1 -1		# 相当于自减1
(integer) 10

```

hash变更的数据 user：name、age，尤其是是用户信息之类的，经常变动的信息！hash更适合对象的存储，String更适合字符串存储

```bash
127.0.0.1:6379> hmset user:1 name zhangsan age 18
OK
```

**应用场景**

hash特别适合用于存储对象

1、商品的所有信息（详情页），可以放到value里面

2、用户信息



### 列表类型List

在 redis里面，我们可以把list玩成，栈、队列、阻塞队列

可以添加一个元素到列表的头部（左边）或者尾部（右边），可以一次性将多个元素加入，**除了push和pop，其他操作基本都是从左边进行操作的**

![image-20200528173906234](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200528173906234.png)

**1、添加：push**

​		1.lpush key value：捋元素加入列表左表

​		2.rpush key value：捋元素加入列表右边

**2、获取（只能从左往右获取）：lrange**

​		lrange key start end：范围获取 如lrange myList 0 -1（获取全部）

**3、删除：pop**

​		1.lpop key：删除列表最左边的元素，并将元素返回

​		2.rpop key：删除列表最君边的元素，并将元素返回

```bash
127.0.0.1:6379> lpush mylist zhangsan		# 将一个值或者多个，从左边插入列表
(integer) 1
127.0.0.1:6379> lpush mylist lisi
(integer) 2
127.0.0.1:6379> lpush mylist wangwu
(integer) 3
127.0.0.1:6379> lrange mylist 0 -1
1) "wangwu"
2) "lisi"
3) "zhangsan"
127.0.0.1:6379> rpush mylist zzzznn
(integer) 4
127.0.0.1:6379> lrange mylist 0 -1
1) "wangwu"
2) "lisi"
3) "zhangsan"
4) "zzzznn"
127.0.0.1:6379> rrange mylist 0 -1			# 没有rrange命令
(error) ERR unknown command `rrange`, with args beginning with: `mylist`, `0`, `-1`,

127.0.0.1:6379> lpush mylist zzz nnn kkk eee	# 插入多个value
(integer) 8
127.0.0.1:6379> lrange mylist 0 -1
1) "eee"
2) "kkk"
3) "nnn"
4) "zzz"
5) "wangwu"
6) "lisi"
7) "zhangsan"
8) "zzzznn"
127.0.0.1:6379> rpop mylist			# 右边元素弹出
"zzzznn"
127.0.0.1:6379> lpop mylist			# 左边元素弹出
"eee"
```

**4、通过下标获得值：lindex**

​		lindex命令，根据从左往右的索引取值

```bash
127.0.0.1:6379> lrange mylist 0 -1		# 查看列表元素
1) "kkk"
2) "nnn"
3) "zzz"
4) "wangwu"
5) "lisi"
6) "zhangsan"
127.0.0.1:6379> lindex mylist 2		# 获取下表为2的value， 从0开始
"zzz"
127.0.0.1:6379> lindex mylist 10	# 下标超过长度返回nil
(nil)
127.0.0.1:6379> rindex mylist 2		# 没有rindex
(error) ERR unknown command `rindex`, with args beginning with: `mylist`, `2`, 

```

**5、获取长度：llen**

```bash
127.0.0.1:6379> llen mulist		# 不存在该表，返回0
(integer) 0
127.0.0.1:6379> llen mylist
(integer) 6
```

**6、移除指定值：lrem**

```bash
127.0.0.1:6379> flushdb		# 清空一下数据库
OK
127.0.0.1:6379> lpush mylist one two three one two zero zero zero
(integer) 8
127.0.0.1:6379> lrem mylist 1 two	# 从左边移除一个two
(integer) 1
127.0.0.1:6379> lrange mylist 0 -1
1) "zero"
2) "zero"
3) "zero"
4) "one"
5) "three"
6) "two"
7) "one"
127.0.0.1:6379> lrem mylist 3 zero	# 从左边移除3个zero
(integer) 3
127.0.0.1:6379> lrange mylist 0 -1
1) "one"
2) "three"
3) "two"
4) "one"
127.0.0.1:6379> lrem mylist 3 one 	# 删除数量超过列表one的数量时，删除全部，返回删除数量
(integer) 2
```

**7、截断：ltrim**

通过下标截取指定长度

```bash
127.0.0.1:6379> flushdb
OK
127.0.0.1:6379> rpush mylist hello0 hello1 hello2 hello3
(integer) 4
127.0.0.1:6379> ltrim mylist 1 2		# [1,2] 通过下标截取指定长度
OK
127.0.0.1:6379> lrange mylist 0 -1
1) "hello1"
2) "hello2"
```

**8、组合命令:rpoplpush（只有这一个）**

将一个元素从一个列表右边弹出，在另一个列表左边插入

```bash
127.0.0.1:6379> rpush mylist hello0 hello1 hello2 hello3
(integer) 4
127.0.0.1:6379> rpoplpush mylist myotherlist
"hello3"
127.0.0.1:6379> lrange mylist 0 -1
1) "hello0"
2) "hello1"
3) "hello2"
127.0.0.1:6379> lrange myotherlist 0 -1
1) "hello3"
```

**9、修改存在的指定下标值：lset**

如果列表不存在，则会报错，下标值不存在也会报错

```bash
127.0.0.1:6379> rpush mylist hello0 hello1 hello2 hello3
(integer) 4
127.0.0.1:6379> lset mylist 0 item			# 替换0号的下标元素值
OK
127.0.0.1:6379> lrange 0 -1
(error) ERR wrong number of arguments for 'lrange' command
127.0.0.1:6379> lrange mylist 0 -1
1) "item"
2) "hello1"
3) "hello2"
4) "hello3"
```

**10、指定位置插入：linsert**

通过before和after可以完成在指定元素值，前面或后面插入

```bash
127.0.0.1:6379> rpush mylist hello0 hello1 hello2 hello3
(integer) 4
127.0.0.1:6379> LINSERT mylist before hello1 zhangsan
(integer) 5
127.0.0.1:6379> lrange mylist 0 -1
1) "hello0"
2) "zhangsan"
3) "hello1"
4) "hello2"
5) "hello3"
127.0.0.1:6379> LINSERT mylist after hello1 lisi
(integer) 6
127.0.0.1:6379> lrange mylist 0 -1
1) "hello0"
2) "zhangsan"
3) "hello1"
4) "lisi"
5) "hello2"
6) "hello3"

127.0.0.1:6379> LINSERT mylist after hello5 zhangfei # value不存在，则不会进行插入
(integer) -1
127.0.0.1:6379> lrange mylist 0 -1
1) "hello0"
2) "zhangsan"
3) "hello1"
4) "lisi"
5) "hello2"
6) "hello3"
```

**应用场景：**

 1、按评论时间入栈

2、最新消息排行

3、消息队列（将任务存在List中，然后工作线程再用POP操作将任务取出进行执行）

### 集合Set

不允许重复元素

**1、存储：sadd key value****

**2、获取：smembers key**   获取set集合中所有元素

**3、删除：srem key value**  删除set集合中的某个元素

```bash
127.0.0.1:6379> sadd myset zhangsan lisi wangwu		# 添加元素
(integer) 3
127.0.0.1:6379> SMEMBERS myset						# 获取所有元素
1) "lisi"
2) "wangwu"
3) "zhangsan"
127.0.0.1:6379> srem myset zhangsan				 # 删除zhangsan
(integer) 1
127.0.0.1:6379> SMEMBERS myset
1) "lisi"
2) "wangwu"
127.0.0.1:6379> sadd myset lisi					# 重复值插入无效
(integer) 0
```

**4、获取set长度：scard**

```bash
127.0.0.1:6379> scard myset
(integer) 2
```

**5、随机取指定数量的set元素：srandmember**

```bash
127.0.0.1:6379> flushdb
OK
127.0.0.1:6379> sadd myset zhangsan lisi wangwu
(integer) 3
127.0.0.1:6379> SRANDMEMBER myset 
"wangwu"
127.0.0.1:6379> SRANDMEMBER myset 
"lisi"
127.0.0.1:6379> SRANDMEMBER myset 2		# 取两个
1) "wangwu"
2) "zhangsan"

```

**6、随机删除set元素：spop**

```bash
127.0.0.1:6379> SMEMBERS myset
1) "wangwu"
2) "xiaohei"
3) "zhangsan"
4) "wanglaowu"
5) "lisi"
6) "dabai"
127.0.0.1:6379> spop myset
"wangwu"
127.0.0.1:6379> spop myset
"zhangsan"
```

**7、移动自定元素到另一个Set：smove**

```bash
127.0.0.1:6379> sadd myset zhangsan lisi wangwu xiaohei dabai wanglaowu
(integer) 6
127.0.0.1:6379> sadd myNewSet zz
(integer) 1
127.0.0.1:6379> smove myset myNewSet zhangsan
(integer) 1
127.0.0.1:6379> SMEMBERS myset
1) "xiaohei"
2) "wangwu"
3) "wanglaowu"
4) "lisi"
5) "dabai"
127.0.0.1:6379> SMEMBERS myNewSet
1) "zhangsan"
2) "zz"
```

**8、差集：sdiff  ；交集：sinter；并集：sunion **

sdiff A B 存在A中而不存在B的元素

```bash
127.0.0.1:6379> sadd key1 a
(integer) 1
127.0.0.1:6379> sadd key1 b
(integer) 1
127.0.0.1:6379> sadd key1 c
(integer) 1
127.0.0.1:6379> sadd key2 c
(integer) 1
127.0.0.1:6379> sadd key2 d
(integer) 1
127.0.0.1:6379> sadd key2 e
(integer) 1
127.0.0.1:6379> sdiff key1 key2			# 差集，key1中有，key2没有的元素
1) "a"
2) "b"
127.0.0.1:6379> sinter key1 key2		# 交集
1) "c"
127.0.0.1:6379> sunion key1 key2		# 并集，共同好友就可以这样实现
1) "a"
2) "b"
3) "c"
4) "e"
5) "d"

```

微博，A用户将所有关注的人放在一个set集合中！将它的粉丝也放在一个集合中！取交集，就能看到相互关注，共同话题等等。

**应用场景**

1、共同好友（交集）

2、推荐好友（差集）



### 有序集合Zset

在set基础上，增加了一个值 **score**，总体上和set差不多

**1、存储：zadd key score value：**

**2、获取：zrange key start end（获取上与set有很大区别smembers）**

**3、删除：zrem key value**

```bash
127.0.0.1:6379> zadd myzset 1 one
(integer) 1
127.0.0.1:6379> zadd myzset 2 two 3 three
(integer) 2
127.0.0.1:6379> zrange myzset 0 -1
1) "one"
2) "two"
3) "three"	
127.0.0.1:6379> zrem myzset two				# 删掉2
(integer) 1
127.0.0.1:6379> zrange myzset 0 -1
1) "one"
2) "three"
```

**4、按照分数展示：zrangebyscore，降序：zrevrange**

```bash
127.0.0.1:6379> zadd salary 2500 lin
(integer) 1
127.0.0.1:6379> zadd salary 5000 li
(integer) 1
127.0.0.1:6379> zadd salary 7000 zhang
(integer) 1
127.0.0.1:6379> zrangebyscore salary -inf +inf			# 负无穷到正无穷，升序
1) "lin"
2) "li"
3) "zhang"
127.0.0.1:6379> zrangebyscore salary -inf +inf withscores	# 带上分数展示
1) "lin"
2) "2500"
3) "li"
4) "5000"
5) "zhang"
6) "7000"
127.0.0.1:6379> zrangebyscore salary -inf 5500 withscores	# 限制展示分数上限为5500
1) "lin"
2) "2500"
3) "li"
127.0.0.1:6379> zrevrange salary 0 -1 withscores			# 降序，参数不再是分数，而是下标
1) "zhang"
2) "7000"
3) "li"
4) "5000"
5) "lin"
6) "2500"
```

**5、查看zset长度：zcard**

```bash
127.0.0.1:6379> zcard salary
(integer) 3
```

**6、获取score属于某区间的元素数量：zcount**

```bash
127.0.0.1:6379> zcount salary 2500 5500
(integer) 2
127.0.0.1:6379> zcount salary 2500 4000
(integer) 1
```

案例思路：zset排序，存储班级成绩表，工资表排序，排行榜应用！

普通消息，1、重要消息 2、带权重进行判断

**具体使用**

1、排行榜

2、有序事件，带权重的队列

3、评论+动态分页（按照时间或者点赞，由于score动态变化，就可以做动态分页）



## Redis的3种特殊数据类型

### geospatial地理空间

朋友的定位，附近的人，打车距离计算

Redis的Geo在Redis3.2版本就推出了！

可以从下面的网站拿到城市的经度纬度作为测试数据：http://www.jsons.cn/lngcode/



相关命令（官网纬度经度顺序搞反了）

![image-20200528213345776](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200528213345776.png)



**1、GEOADD添加地理位置**

geoadd key 经度 纬度 名称

```bash
# 添加6个城市
# 规则：两级无法直接添加，我们一般会下载城市数据，直接通过java程序一次性导入！
127.0.0.1:6379> geoadd china:city 114.09 22.55 shenzhen
(integer) 1
127.0.0.1:6379> geoadd china:city 121.47 31.23 shanghai
(integer) 1
127.0.0.1:6379> geoadd china:city 106.50 29.53 chongqing
(integer) 1
127.0.0.1:6379> geoadd china:city 116.41 39.90 beijing
(integer) 1
127.0.0.1:6379> geoadd china:city 120.15 30.29 hangzhou
(integer) 1
127.0.0.1:6379> geoadd china:city 125.15 42.93 xian
(integer) 1

```

**2、GEOPOS获取给定元素位置** 

从`key`里返回所有给定位置元素的位置（经度和纬度）。

```bash
127.0.0.1:6379> geopos china:city shanghai
1) 1) "121.47000163793563843"
   2) "31.22999903975783553"
127.0.0.1:6379> geopos china:city shenzhen
1) 1) "114.09000009298324585"
   2) "22.5500010475923105"
```

**3、GEODIST返回两个给定位置之间的距离**

返回两个给定位置之间的距离。

如果两个位置之间的其中一个不存在， 那么命令返回空值。

指定单位的参数 unit 必须是以下单位的其中一个：

- **m** 表示单位为米。
- **km** 表示单位为千米。
- **mi** 表示单位为英里。
- **ft** 表示单位为英尺。

```bash
127.0.0.1:6379> geodist china:city beijing shenzhen km
"1942.1485"
127.0.0.1:6379> geodist china:city shanghai chongqing km
"1447.6737"
```



**4、GEORADIUS以给定的经纬度为中心，找出半径内的元素**

以给定的经纬度为中心， 返回键包含的位置元素当中， 与中心的距离不超过给定最大距离的所有位置元素。

范围可以使用以下其中一个单位：

- **m** 表示单位为米。
- **km** 表示单位为千米。
- **mi** 表示单位为英里。
- **ft** 表示单位为英尺。
- 命令默认返回未排序的位置元素。 通过以下两个参数， 用户可以指定被返回位置元素的排序方式：
  - `ASC`: 根据中心的位置， 按照从近到远的方式返回位置元素。
  - `DESC`: 根据中心的位置， 按照从远到近的方式返回位置元素。

所有数据应该都录入：china:city，才会让结果更加精确！

```bash

127.0.0.1:6379> GEORADIUS china:city 110 30 1000 km # 以110，30这个经纬度为中心，寻找方圆1000km内的城市
1) "chongqing"
2) "shenzhen"
3) "hangzhou"
127.0.0.1:6379> GEORADIUS china:city 110 30 1000 km withcoord withdist asc	# 显示距离和经纬度
1) 1) "chongqing"
   2) "341.9374"
   3) 1) "106.49999767541885376"
      2) "29.52999957900659211"
2) 1) "shenzhen"
   2) "923.3692"
   3) 1) "114.09000009298324585"
      2) "22.5500010475923105"
3) 1) "hangzhou"
   2) "976.4733"
   3) 1) "120.15000075101852417"
      2) "30.29000023253814078"
127.0.0.1:6379> GEORADIUS china:city 110 30 1000 km withcoord withdist asc count 2 # 限定2个
1) 1) "chongqing"
   2) "341.9374"
   3) 1) "106.49999767541885376"
      2) "29.52999957900659211"
2) 1) "shenzhen"
   2) "923.3692"
   3) 1) "114.09000009298324585"
      2) "22.5500010475923105"

```

即附近的人的功能（获得所有附近的人的地址，定位！）通过半径来查询！

还可以获得指定数量的人



**5、GEORADIUSBYMEMBER：以某个成员为中心，找出半径内的元素**

基本和经纬度为中心一样

```bash
127.0.0.1:6379> GEORADIUSBYMEMBER china:city shenzhen 1000 km withdist withcoord
1) 1) "shenzhen"
   2) "0.0000"
   3) 1) "114.09000009298324585"
      2) "22.5500010475923105"
      
127.0.0.1:6379> GEORADIUSBYMEMBER china:city shenzhen 1500 km 
1) "chongqing"
2) "shenzhen"
3) "hangzhou"
4) "shanghai"
```



**6、GEOHASH返回一个或多个位置元素的HASH表示。**

了解即可，将经纬度转换成11个字符的Geohash字符串

```bash
127.0.0.1:6379> geohash china:city beijing shenzhen
1) "wx4fbzx4me0"
2) "ws10k1jg380"
```



**GEO底层的实现原理其实就是zset！我们可以使用Zset命令来操作geo！**

```bash
127.0.0.1:6379> zrange china:city 0 -1	# 查看地图中全部元素
1) "chongqing"
2) "shenzhen"
3) "hangzhou"
4) "shanghai"
5) "beijing"
6) "xian"
127.0.0.1:6379> zrem china:city chongqing
(integer) 1
127.0.0.1:6379> zrange china:city 0 -1
1) "shenzhen"
2) "hangzhou"
3) "shanghai"
4) "beijing"
5) "xian"

```



### Hyperloglog基数统计

什么是基数====》不重复的元素

{1,3,5,7,8,7}====》{1,3,5,7,8} 

基数（不重复的元素）= 5 ，可以接受误差 

Reds2.89版本就更新了 Hyperloglog数据结构！Redis Hyperloglog基数统计的算法！

优点：占用的内存是固定，2^64不同的元素的基数，**只需要废12KB内存**，如果要从内存角度来比较的话 Hyperloglog首选！是有容错的，0.81%错误率！统计UV任务，可以忽略不计的

**网页的UV访客数（一个人访问一个网站多次，但是还是算作一个人）**

传统的方式，set保存用户的id，然后就可以统计set中的元素数量作为标准判断！

这个方式如果保存大量的用户id，就会比较麻烦！我们的目的是为了计数，而不是保存用户id；

```bash
# 比如 有两个网站，现在要统计总的访客数量
# userTable1是一个网站的访客名，userTable2 是另一个网站的访客名，由于相同访客名要算作一个，进行合并
127.0.0.1:6379> PFadd userTable1 a b c d e f g h i j # 创建第一组
(integer) 1
127.0.0.1:6379> PFcount userTable1
(integer) 10
127.0.0.1:6379> PFadd userTable2 i j z x c v b n m	# 创建第二组
(integer) 1
127.0.0.1:6379> PFcount userTable2
(integer) 9
127.0.0.1:6379> PFMerge userTableTotal userTable1 userTable2	# 合并
OK
127.0.0.1:6379> PFcount userTableTotal
(integer) 15

```



### Bitmaps位图

位存储，两个状态的，都可以使用 Bitmaps！

统计用户信息，活跃，不活跃；登录、未登录；365天打卡，365天=365bit  1字节=8bit  46个字节左右！

统计疫情感染人数： 0 1 0 1 0 0 0



**setbit设置，getbit查看**

实际上，setbit k2 1 1意思是申请一个Byte的空间，偏移量为1，设置为1，如果偏移量很大，就会申请一个很长的字节数组

![image-20200601201714015](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200601201714015.png)

注意如果用get key的方式去读，如果第一位是0，代表是ASCII码的一个形式

```bash
127.0.0.1:6381> setbit k2 1 1
(integer) 0
127.0.0.1:6381> setbit k2 7 1
(integer) 0
127.0.0.1:6381> get k2
"A"				# 65

```

**bitop可以进行与或运算**

```bash
127.0.0.1:6381> setbit k1 1 1
(integer) 0
127.0.0.1:6381> setbit k1 7 1
(integer) 0
127.0.0.1:6381> get k1
"A"
127.0.0.1:6381> setbit k2 1 1
(integer) 0
127.0.0.1:6381> setbit k2 6 1
(integer) 0
127.0.0.1:6381> get k2
"B"
127.0.0.1:6381> bitop and andKey k1 k2		# 与运算得到的值放到andKey
(integer) 1
127.0.0.1:6381> get andKey
"@"
127.0.0.1:6381> bitop or orKey k1 k2		# 或运算得到的值放到orKey
(integer) 1
127.0.0.1:6381> get orKey
"C"

```

使用 bitmaps来记录周一到周日的打卡！

```bash
# 模拟一周7天打卡
127.0.0.1:6379> setbit sign 0 1	# 周一，打卡了
(integer) 0
127.0.0.1:6379> setbit sign 1 1	# 周二，打卡了
(integer) 0
127.0.0.1:6379> setbit sign 2 1	# 周三，打卡了
(integer) 0
127.0.0.1:6379> setbit sign 3 0	# 周四，没打卡
(integer) 0
127.0.0.1:6379> setbit sign 4 1	# 周五，打卡了
(integer) 0
127.0.0.1:6379> setbit sign 5 1	# 周六，打卡了
(integer) 0
127.0.0.1:6379> setbit sign 6 0	# 周日，没打卡
(integer) 0
# 查看打卡情况
127.0.0.1:6379> getbit sign 2	# 查看周三打卡情况
(integer) 1
127.0.0.1:6379> getbit sign 3	# 查看周四打卡情况
(integer) 0

```

到时要统计一周打卡情况，bitcount统计一下就可以了

```bash
127.0.0.1:6379> bitcount sign
(integer) 5
```

实际业务场景：

1、上述的登录或活跃天数

2、比如618前的活动，对每个活跃用户发放礼物，那么我们可以做的是，按日期生成key，用户id登录之后设成1，最后进行一个或运算就可以了

3、12306 统计区间，假如c1用户要买A-C区间，那么把ABC三个key中的该座位设置成1，然后C2用户如果想买B-D区间，那么需要对key BCD的该位置做一个或运算，如果为1，则买不了

![image-20200602004133148](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200602004133148.png)

4、还有权限，每一项权限代表一个位即可

## Jedis

一款java操作redis数据库的工具,类似 JDBC，是 Redis官方推荐的java连接开发工具！使用 java操作 Redis中间件

依赖：

```xml
<dependency>
      <groupId>redis.clients</groupId>
      <artifactId>jedis</artifactId>
      <version>3.2.0</version><!--尽量安装适配的新版本，低了一些功能不支持-->
    </dependency>
    <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-lang3</artifactId>
      <version>3.3.2</version>
    </dependency>
    <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-pool2</artifactId>
      <version>2.3</version>
    </dependency>
```

1、new 一个Jedis对象、进行连接

2、进行操作，所有方法都和上面的api名字相同

3、关闭连接

```java
public void test1(){
        //1.获取连接
        Jedis jedis = new Jedis("localhost",6379);///如果使用空参构造，默认值“1ocalhost"，6379端口
        //2.操作，
        jedis.set("username","张三");
        jedis.geoadd("china:city",114.09,22.55,"shenzhen");
        jedis.geoadd("china:city",121.47,31.23,"shanghai");

        System.out.println(jedis.geodist("china:city", "shenzhen", "shanghai", GeoUnit.KM));
        //3.关闭连接
        jedis.close();
    }
```

jedis里的方法基本与redis操作数据库的方法名字相同

值得注意的有

1. 可以使用setex（）方法存储可以指定过期时间的 key value

```java
//将activecode:11111键值对存入redis，并且20秒后自动删除该键值对
jedis.setex("activecode",20,"11111");
```



### Jedis连接池

1.创建JedisPool连接池对象

2.调用方法getResource()方法获取]edis连接

```java
public void test2(){
        //0.创建一个配置对象
        JedisPoolConfig config = new JedisPoolConfig();
        config.setMaxTotal(50);
        config.setMinIdle(10);
        //1.创建JedisPool连接池对象
        JedisPool jedisPool = new JedisPool();
        //2.获取连接
        Jedis jedis = jedisPool.getResource();
        //3.操作
        jedis.set("username","hehe");
        //4.归还连接
        jedis.close();
    }
```



## SpringBoot整合redis

SpringBoot：操作数据依靠SpringData ：jpa jdbc mongodb redis都可以进行整合

Spring Data也是和 SpringBoot齐名的项目

说明：**在 Spring Boot2.x之后，原来使用的 jedis被替换为了 lettuce**

Jedis是直接连接Redis，**非线程安全**，在性能上，每个线程都去拿自己的 Jedis 实例，当连接数量增多时，资源消耗阶梯式增大，连接成本就较高了。

Lettuce的连接是**基于Netty**的，Netty 是一个多线程、事件驱动的 I/O 框架。连接实例可以在多个线程间共享，当多线程使用同一连接实例时，是**线程安全**的。

![image-20200529152232727](H:\Desktop\新建文件夹\Blog\docs\backend\Redis\pictures\image-20200529152232727.png)

注意SpringBoot2.x版本JedisConnectionFactory很多类不生效



1、创建spring项目

![image-20200529115023712](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529115023712.png)

2、勾选需要的开发工具

![image-20200529115106207](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529115106207.png)

3、第一次安装需要的依赖要等很久，要耐心

![image-20200529115924019](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529115924019.png)



源码分析：

```java
@Configuration(
    proxyBeanMethods = false
)
@ConditionalOnClass({RedisOperations.class})
@EnableConfigurationProperties({RedisProperties.class})
@Import({LettuceConnectionConfiguration.class, JedisConnectionConfiguration.class})
public class RedisAutoConfiguration {
    public RedisAutoConfiguration() {
    }

    @Bean
    @ConditionalOnMissingBean(
        name = {"redisTemplate"}		//我们可以自己定义一个 redisTemplate来替换这个默认的！
    )
    public RedisTemplate<Object, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory) throws UnknownHostException {
        // 默认的 RedisTemplate 没有过多的设置，redis对象是需要序列化的
        // 两个泛型都是Object，需要强制转换
        RedisTemplate<Object, Object> template = new RedisTemplate();
        template.setConnectionFactory(redisConnectionFactory);
        return template;
    }

    @Bean
    @ConditionalOnMissingBean	//由于 string是 redis中最常使用的类型，所以说单独提出来了一个bean！
    public StringRedisTemplate stringRedisTemplate(RedisConnectionFactory redisConnectionFactory) throws UnknownHostException {
        StringRedisTemplate template = new StringRedisTemplate();
        template.setConnectionFactory(redisConnectionFactory);
        return template;
    }
}

```

1、实际依赖

```xml
		<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>
```

2、application.properties配置连接

```properties
# 配置redis
spring.redis.host=106.55.3.34
spring.redis.port=6379
spring.redis.password=123

```

3、测试

与jedis不同redisTemplate不再是单纯的redis里面的api，对于redis不同的类型，再一次进行划分，一些方法上还是与原生api不同的

![image-20200529153056309](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529153056309.png)

```java
@SpringBootTest
class Redis02SpringbootApplicationTests {

    @Autowired
    private RedisTemplate redisTemplate;
    @Test
    void contextLoads() {
        //获取连接，某些操作通过连接去操作
        RedisConnection connection = redisTemplate.getConnectionFactory().getConnection();
//        connection.select(0);
        //　注意: spring boot 2.0 默认使用lettuce连接, 在共享连接状态下不能进行select(dbIndex)操作
        // 实例化RedisTemplate时，不再注入RedisConnectionFactory而是注入LettuceConnectionFactory, 再设置非共享连接
        connection.flushDb();
        //redisTemplate opsForValue 操作字符串 类似string
        redisTemplate.opsForValue().set("k1","v1");

        //redisTemplate opsForList 操作列表
        redisTemplate.opsForList().leftPushAll("name","zhangsan","lisi","wangwu","xiaoliu");

        System.out.println(redisTemplate.keys("*"));
        System.out.println(redisTemplate.opsForValue().get("k1"));
        System.out.println(redisTemplate.opsForList().range("name", 0, -1));

    }

}

```

![image-20200529155256331](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529155256331.png)

```bash
127.0.0.1:6379> keys *
1) "\xac\xed\x00\x05t\x00\x02k1"
2) "\xac\xed\x00\x05t\x00\x04name"
```

由于此时，使用JDK自带的序列化，因此是有问题的

![image-20200529161341942](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529161341942.png)

再来看看不序列化，会发生什么

```java
@Component
@AllArgsConstructor
@NoArgsConstructor
@Data
public class User {	//定义一个User类

    private String name;
    private int age;
}

```

对象不进行序列化，传入redis会报错

```java
//测试
@SpringBootTest
class Redis02SpringbootApplicationTests {

    @Autowired
    private RedisTemplate redisTemplate;
    @Test
    void contextLoads() {
        //获取连接，某些操作通过连接和工厂去操作
        RedisConnection connection = redisTemplate.getConnectionFactory().getConnection();

        connection.flushDb();
        //redisTemplate opsForValue 操作字符串 类似string
        redisTemplate.opsForValue().set("k1","v1");

        //redisTemplate opsForList 操作列表
        redisTemplate.opsForList().leftPushAll("name","zhangsan","lisi","wangwu","xiaoliu");

        System.out.println(redisTemplate.keys("*"));
        System.out.println(redisTemplate.opsForValue().get("k1"));
        System.out.println(redisTemplate.opsForList().range("name", 0, -1));

        // 常用的操作可以直接通过redisTemplate操作
//        redisTemplate.multi();
//        redisTemplate.opsForValue().set("k2","v2");
//        redisTemplate.exec();
    }


    @Test
    public void test() throws JsonProcessingException {
        //真实的开发一般都用Json传递对象
        User zero = new User("zero", 3);
        String jsonUser = new ObjectMapper().writeValueAsString(zero);
        // 传一个json字符串
        redisTemplate.opsForValue().set("user",jsonUser);
        System.out.println(redisTemplate.opsForValue().get("user"));    //{"name":"zero","age":3}


        // 直接传User对象
        redisTemplate.opsForValue().set("user1", zero);
        System.out.println(redisTemplate.opsForValue().get("user1"));   //SerializationException: Cannot serialize;
    }
}

```

![image-20200529165523579](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529165523579.png)

对象进行序列化，再看看结果

```java
@Component
@AllArgsConstructor
@NoArgsConstructor
@Data
public class User implements Serializable {

    private String name;
    private int age;
}

```

![image-20200529171134596](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529171134596.png)

然而，在redis客户端存的是带转义字符的

```bash
127.0.0.1:6379> keys *
1) "\xac\xed\x00\x05t\x00\x04user"
2) "\xac\xed\x00\x05t\x00\x05user1"
```





编写我们自己的redisTemplate思路：

```java
@Configuration
public class MyRedisConfig {

    // 编写我们自己的redisTemplate,从RedisAutoConfiguration复制过来，修改
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory) throws UnknownHostException {
        RedisTemplate<String, Object> template = new RedisTemplate();
        // 生成序列化方式
        Jackson2JsonRedisSerializer<Object> objectJackson2JsonRedisSerializer = new Jackson2JsonRedisSerializer<Object>(Object.class);
        // 配置具体的序列化方式,key采用String的序列化方式
        template.setKeySerializer(objectJackson2JsonRedisSerializer);

        template.setConnectionFactory(redisConnectionFactory);
        return template;
    }
}
```

RedisSerializer接口的实现类

![image-20200529171505708](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529171505708.png)

编写我们自己的redisTemplate实现

```java
@Configuration
public class MyRedisConfig {

    // 编写我们自己的redisTemplate,从RedisAutoConfiguration复制过来，修改
    // 写好的一个固定模板
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory) throws UnknownHostException {
        //  我们为了自己开发方便，一般直接使用String,Object
        RedisTemplate<String, Object> template = new RedisTemplate();
        template.setConnectionFactory(redisConnectionFactory);

        // json序列化方式
        // 解析任意Object对象
        Jackson2JsonRedisSerializer<Object> jsonSerializer = new Jackson2JsonRedisSerializer<Object>(Object.class);
        ObjectMapper om = new ObjectMapper();       // 转义
        om.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
        om.activateDefaultTyping(LaissezFaireSubTypeValidator.instance,ObjectMapper.DefaultTyping.NON_FINAL);
        jsonSerializer.setObjectMapper(om);
        // string序列化
        StringRedisSerializer stringRedisSerializer = new StringRedisSerializer();

        //key采用String的序列化方式
        template.setKeySerializer(stringRedisSerializer);
        //hash的key 也采用String的序列化方式
        template.setHashKeySerializer(stringRedisSerializer);
        // value序列化采用json
        template.setValueSerializer(jsonSerializer);
        // hash的value也采用json
        template.setValueSerializer(jsonSerializer);

        template.afterPropertiesSet();

        return template;
    }
}
```

修改导入的RedisTemplate

```java
	@Autowired
    @Qualifier("redisTemplate")
    private RedisTemplate redisTemplate;
```

查看结果

```bash
127.0.0.1:6379> keys *
1) "user1"
2) "user"
```



在企业开发中，我们80%的情况下，都不会使用这个原生的方式去编写代码！我们应该像操作JDBCTemplate一样，自己写一个Utils工具类，把一些自己常用的命令，再从resdisTemplate.xxxxx.xxx里面提取出来 ，底层虽然还是resdisTemplate.xxxxx.xxx去实现的，还可以定义某些没有的方法，如hash不支持的decr

比如

```java
import java.util.List;  
import java.util.Map;  
import java.util.Set;  
import java.util.concurrent.TimeUnit;  
  
  
import org.springframework.data.redis.core.RedisTemplate;  
import org.springframework.util.CollectionUtils;  
  
  
/** 
 * 基于spring和redis的redisTemplate工具类 
 * 针对所有的hash 都是以h开头的方法 
 * 针对所有的Set 都是以s开头的方法                    
 * 针对所有的List 都是以l开头的方法 
 */  
public class RedisUtils {  
  
  
    private RedisTemplate<String, Object> redisTemplate;  
      
    public void setRedisTemplate(RedisTemplate<String, Object> redisTemplate) {  
        this.redisTemplate = redisTemplate;  
    }  
    //=============================common============================  
    /** 
     * 指定缓存失效时间 
     * @param key 键 
     * @param time 时间(秒) 
     * @return 
     */  
    public boolean expire(String key,long time){  
        try {  
            if(time>0){  
                redisTemplate.expire(key, time, TimeUnit.SECONDS);  
            }  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
      
    /** 
     * 根据key 获取过期时间 
     * @param key 键 不能为null 
     * @return 时间(秒) 返回0代表为永久有效 
     */  
    public long getExpire(String key){  
        return redisTemplate.getExpire(key,TimeUnit.SECONDS);  
    }  
      
    /** 
     * 判断key是否存在 
     * @param key 键 
     * @return true 存在 false不存在 
     */  
    public boolean hasKey(String key){  
        try {  
            return redisTemplate.hasKey(key);  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
      
    /** 
     * 删除缓存 
     * @param key 可以传一个值 或多个 
     */  
    @SuppressWarnings("unchecked")  
    public void del(String ... key){  
        if(key!=null&&key.length>0){  
            if(key.length==1){  
                redisTemplate.delete(key[0]);  
            }else{  
                redisTemplate.delete(CollectionUtils.arrayToList(key));  
            }  
        }  
    }  
      
    //============================String=============================  
    /** 
     * 普通缓存获取 
     * @param key 键 
     * @return 值 
     */  
    public Object get(String key){  
        return key==null?null:redisTemplate.opsForValue().get(key);  
    }  
      
    /** 
     * 普通缓存放入 
     * @param key 键 
     * @param value 值 
     * @return true成功 false失败 
     */  
    public boolean set(String key,Object value) {  
         try {  
            redisTemplate.opsForValue().set(key, value);  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
          
    }  
      
    /** 
     * 普通缓存放入并设置时间 
     * @param key 键 
     * @param value 值 
     * @param time 时间(秒) time要大于0 如果time小于等于0 将设置无限期 
     * @return true成功 false 失败 
     */  
    public boolean set(String key,Object value,long time){  
        try {  
            if(time>0){  
                redisTemplate.opsForValue().set(key, value, time, TimeUnit.SECONDS);  
            }else{  
                set(key, value);  
            }  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
      
    /** 
     * 递增 
     * @param key 键 
     * @param by 要增加几(大于0) 
     * @return 
     */  
    public long incr(String key, long delta){    
        if(delta<0){  
            throw new RuntimeException("递增因子必须大于0");  
        }  
        return redisTemplate.opsForValue().increment(key, delta);  
    }  
      
    /** 
     * 递减 
     * @param key 键 
     * @param by 要减少几(小于0) 
     * @return 
     */  
    public long decr(String key, long delta){    
        if(delta<0){  
            throw new RuntimeException("递减因子必须大于0");  
        }  
        return redisTemplate.opsForValue().increment(key, -delta);    
    }    
      
    //================================Map=================================  
    /** 
     * HashGet 
     * @param key 键 不能为null 
     * @param item 项 不能为null 
     * @return 值 
     */  
    public Object hget(String key,String item){  
        return redisTemplate.opsForHash().get(key, item);  
    }  
      
    /** 
     * 获取hashKey对应的所有键值 
     * @param key 键 
     * @return 对应的多个键值 
     */  
    public Map<Object,Object> hmget(String key){  
        return redisTemplate.opsForHash().entries(key);  
    }  
      
    /** 
     * HashSet 
     * @param key 键 
     * @param map 对应多个键值 
     * @return true 成功 false 失败 
     */  
    public boolean hmset(String key, Map<String,Object> map){    
        try {  
            redisTemplate.opsForHash().putAll(key, map);  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
      
    /** 
     * HashSet 并设置时间 
     * @param key 键 
     * @param map 对应多个键值 
     * @param time 时间(秒) 
     * @return true成功 false失败 
     */  
    public boolean hmset(String key, Map<String,Object> map, long time){    
        try {  
            redisTemplate.opsForHash().putAll(key, map);  
            if(time>0){  
                expire(key, time);  
            }  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
      
    /** 
     * 向一张hash表中放入数据,如果不存在将创建 
     * @param key 键 
     * @param item 项 
     * @param value 值 
     * @return true 成功 false失败 
     */  
    public boolean hset(String key,String item,Object value) {  
         try {  
            redisTemplate.opsForHash().put(key, item, value);  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
      
    /** 
     * 向一张hash表中放入数据,如果不存在将创建 
     * @param key 键 
     * @param item 项 
     * @param value 值 
     * @param time 时间(秒)  注意:如果已存在的hash表有时间,这里将会替换原有的时间 
     * @return true 成功 false失败 
     */  
    public boolean hset(String key,String item,Object value,long time) {  
         try {  
            redisTemplate.opsForHash().put(key, item, value);  
            if(time>0){  
                expire(key, time);  
            }  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
      
    /** 
     * 删除hash表中的值 
     * @param key 键 不能为null 
     * @param item 项 可以使多个 不能为null 
     */  
    public void hdel(String key, Object... item){    
        redisTemplate.opsForHash().delete(key,item);  
    }   
      
    /** 
     * 判断hash表中是否有该项的值 
     * @param key 键 不能为null 
     * @param item 项 不能为null 
     * @return true 存在 false不存在 
     */  
    public boolean hHasKey(String key, String item){  
        return redisTemplate.opsForHash().hasKey(key, item);  
    }   
      
    /** 
     * hash递增 如果不存在,就会创建一个 并把新增后的值返回 
     * @param key 键 
     * @param item 项 
     * @param by 要增加几(大于0) 
     * @return 
     */  
    public double hincr(String key, String item,double by){    
        return redisTemplate.opsForHash().increment(key, item, by);  
    }  
      
    /** 
     * hash递减 
     * @param key 键 
     * @param item 项 
     * @param by 要减少记(小于0) 
     * @return 
     */  
    public double hdecr(String key, String item,double by){    
        return redisTemplate.opsForHash().increment(key, item,-by);    
    }    
      
    //============================set=============================  
    /** 
     * 根据key获取Set中的所有值 
     * @param key 键 
     * @return 
     */  
    public Set<Object> sGet(String key){  
        try {  
            return redisTemplate.opsForSet().members(key);  
        } catch (Exception e) {  
            e.printStackTrace();  
            return null;  
        }  
    }  
      
    /** 
     * 根据value从一个set中查询,是否存在 
     * @param key 键 
     * @param value 值 
     * @return true 存在 false不存在 
     */  
    public boolean sHasKey(String key,Object value){  
        try {  
            return redisTemplate.opsForSet().isMember(key, value);  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
      
    /** 
     * 将数据放入set缓存 
     * @param key 键 
     * @param values 值 可以是多个 
     * @return 成功个数 
     */  
    public long sSet(String key, Object...values) {  
        try {  
            return redisTemplate.opsForSet().add(key, values);  
        } catch (Exception e) {  
            e.printStackTrace();  
            return 0;  
        }  
    }  
      
    /** 
     * 将set数据放入缓存 
     * @param key 键 
     * @param time 时间(秒) 
     * @param values 值 可以是多个 
     * @return 成功个数 
     */  
    public long sSetAndTime(String key,long time,Object...values) {  
        try {  
            Long count = redisTemplate.opsForSet().add(key, values);  
            if(time>0) expire(key, time);  
            return count;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return 0;  
        }  
    }  
      
    /** 
     * 获取set缓存的长度 
     * @param key 键 
     * @return 
     */  
    public long sGetSetSize(String key){  
        try {  
            return redisTemplate.opsForSet().size(key);  
        } catch (Exception e) {  
            e.printStackTrace();  
            return 0;  
        }  
    }  
      
    /** 
     * 移除值为value的 
     * @param key 键 
     * @param values 值 可以是多个 
     * @return 移除的个数 
     */  
    public long setRemove(String key, Object ...values) {  
        try {  
            Long count = redisTemplate.opsForSet().remove(key, values);  
            return count;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return 0;  
        }  
    }  
    //===============================list=================================  
      
    /** 
     * 获取list缓存的内容 
     * @param key 键 
     * @param start 开始 
     * @param end 结束  0 到 -1代表所有值 
     * @return 
     */  
    public List<Object> lGet(String key,long start, long end){  
        try {  
            return redisTemplate.opsForList().range(key, start, end);  
        } catch (Exception e) {  
            e.printStackTrace();  
            return null;  
        }  
    }  
      
    /** 
     * 获取list缓存的长度 
     * @param key 键 
     * @return 
     */  
    public long lGetListSize(String key){  
        try {  
            return redisTemplate.opsForList().size(key);  
        } catch (Exception e) {  
            e.printStackTrace();  
            return 0;  
        }  
    }  
      
    /** 
     * 通过索引 获取list中的值 
     * @param key 键 
     * @param index 索引  index>=0时， 0 表头，1 第二个元素，依次类推；index<0时，-1，表尾，-2倒数第二个元素，依次类推 
     * @return 
     */  
    public Object lGetIndex(String key,long index){  
        try {  
            return redisTemplate.opsForList().index(key, index);  
        } catch (Exception e) {  
            e.printStackTrace();  
            return null;  
        }  
    }  
      
    /** 
     * 将list放入缓存 
     * @param key 键 
     * @param value 值 
     * @param time 时间(秒) 
     * @return 
     */  
    public boolean lSet(String key, Object value) {  
        try {  
            redisTemplate.opsForList().rightPush(key, value);  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
      
    /** 
     * 将list放入缓存 
     * @param key 键 
     * @param value 值 
     * @param time 时间(秒) 
     * @return 
     */  
    public boolean lSet(String key, Object value, long time) {  
        try {  
            redisTemplate.opsForList().rightPush(key, value);  
            if (time > 0) expire(key, time);  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
      
    /** 
     * 将list放入缓存 
     * @param key 键 
     * @param value 值 
     * @param time 时间(秒) 
     * @return 
     */  
    public boolean lSet(String key, List<Object> value) {  
        try {  
            redisTemplate.opsForList().rightPushAll(key, value);  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
      
    /** 
     * 将list放入缓存 
     * @param key 键 
     * @param value 值 
     * @param time 时间(秒) 
     * @return 
     */  
    public boolean lSet(String key, List<Object> value, long time) {  
        try {  
            redisTemplate.opsForList().rightPushAll(key, value);  
            if (time > 0) expire(key, time);  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
      
    /** 
     * 根据索引修改list中的某条数据 
     * @param key 键 
     * @param index 索引 
     * @param value 值 
     * @return 
     */  
    public boolean lUpdateIndex(String key, long index,Object value) {  
        try {  
            redisTemplate.opsForList().set(key, index, value);  
            return true;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }   
      
    /** 
     * 移除N个值为value  
     * @param key 键 
     * @param count 移除多少个 
     * @param value 值 
     * @return 移除的个数 
     */  
    public long lRemove(String key,long count,Object value) {  
        try {  
            Long remove = redisTemplate.opsForList().remove(key, count, value);  
            return remove;  
        } catch (Exception e) {  
            e.printStackTrace();  
            return 0;  
        }  
    }  
      
}  

```

