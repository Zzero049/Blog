# Redis.conf 配置文件

redis启动的时候，要根据配置内容启动

**1、占用大小单位，配置文件unit单位对大小写不敏感**

![image-20200529195915622](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529195915622.png)

**2、可以包含别的配置文件（类似import）**

![image-20200529200100938](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529200100938.png)



**3、网络NETWORK**

```bash
# 指定 redis 只接收来自于该IP地址的请求，如果不进行设置，那么将处理所有请求
bind 127.0.0.1

# 是否开启保护模式，默认开启。要是配置里没有指定bind和密码。开启该参数后，redis只会本地进行访问，
# 拒绝外部访问。要是开启了密码和bind，可以开启。否则最好关闭，设置为no
protected-mode no

# 端口设置
port 6379

#此参数为设置客户端空闲超过timeout，服务端会断开连接，为0则服务端不会主动断开连接，不能小于0
timeout 0

# 在Linux内核中，设置了keepalive，redis会定时给对端发送ack，检测挂掉的对端。检测到对端关闭需要两倍的设置值
tcp-keepalive 300
```



**4、通用GENERAL**

```bash
# 是否在后台执行(守护线程执行)，yes：后台运行；no：不是后台运行
daemonize yes

# 如果以后台方式执行。需要指定一个pid文件
pidfile /var/run/redis_6379.pid

# 指定了服务端日志的级别。级别包括：
# debug（很多信息，方便开发、测试）
# verbose（许多有用的信息，但是没有debug级别信息多）
# notice（适当的日志级别，适合生产环境）
# warn（只有非常重要的信息）
loglevel notice
logfile ""			# 指定了记录日志的文件。空字符串，日志会打印到标准输出设备。后台运行的redis标准输出是/dev/null

# 数据库数量
databases 16

always-show-logo yes # 是否显示logo

```



**5、快照SNAPSHOTTING**

```bash
# 持久化规则，执行了多少次操作，则会持久化到文件 .rdb / .aof
# redis是内存数据库，如果没有持久化，那么数据断电即失！
save 900 1			# 如果900秒内，如果至少有一个key进行修改，我们就进行持久化操作
save 300 10			# 如果300秒内，如果至少有十个key进行修改，我们就进行持久化操作
save 60 10000		# 如果60秒被，如果至少有10000个key进行修改，我们就进行持久化操作

# 持久化出错，是否继续工作，一般为是
stop-writes-on-bgsave-error yes

# 是否压缩rdb文件，需要耗费一定的cpu资源
rdbcompression yes
# 保存rdb文件的时候，进行错误检查
rdbchecksum yes
# 数据目录，数据库的写入会在这个目录。
dir ./

```



**6、主从复制REPLICATION**

```bash
# 复制选项，slave复制对应的master。
replicaof 127.0.0.1 6379

#如果master设置了requirepass，那么slave要连上master，需要有master的密码才行
masterauth 123

# 当从库同主机失去连接或者复制正在进行，从机库有两种运行方式：
# 1) 如果slave-serve-stale-data设置为yes(默认设置)，从库会继续响应客户端的请求。
# 2) 如果slave-serve-stale-data设置为no，
# INFO,replicaOF, AUTH, PING, SHUTDOWN, REPLCONF, ROLE, CONFIG,SUBSCRIBE, UNSUBSCRIBE,
# PSUBSCRIBE, PUNSUBSCRIBE, PUBLISH, PUBSUB,COMMAND, POST, HOST: and LATENCY命令之外
# 的任何请求都会返回一个错误”SYNC with master in progress”。
replica-serve-stale-data yes

#作为从服务器，默认情况下是只读的（yes），可以修改成NO，用于写（不建议）
#replica-read-only yes

# 复制缓冲区大小，这是一个环形复制缓冲区，用来保存最新复制的命令。这样在slave离线的时候，不需要完
# 全复制master的数据，如果可以执行部分同步，只需要把缓冲区的部分数据复制给slave，就能恢复正常复制状
# 态。缓冲区的大小越大，slave离线的时间可以更长，复制缓冲区只有在有slave连接的时候才分配内存。没有
# slave的一段时间，内存会被释放出来，默认1MB
# repl-backlog-size 1mb
 
# master没有slave一段时间会释放复制缓冲区的内存，repl-backlog-ttl用来设置该时间长度。单位为秒。
# repl-backlog-ttl 3600


```



**7、安全SECURITY**

```bash
# 默认不开启密码
# 注意，因为redis太快了，每秒可以认证15w次密码，简单的密码很容易被攻破，所以最好使用一个更复杂的密码
# 客户端认证auth xxx通过后，可以通过config get/set requirepass查看/修改密码
# requirepass foobared
requirepass 123		# 设置密码

```



**8、客户端CLIENTS**

```bash
# 设置能连上客户端的最大数量，默认一万，建议32以上
# maxclients 10000

```



**9、内存管理MEMORY MANAGEMENT**

```bash
# redis配置的最大内存容量。当内存满了，需要配合maxmemory-policy策略进行处理。
# 注意slave的输出缓冲区是不计算在maxmemory内的。所以为了防止主机内存使用完，建议设置的maxmemory需要更小一些
# maxmemory <bytes>
maxmemory 122000000		# 进行设置


# 内存达到上限后的key处理策略（6种）
# volatile-lru:从已设置过期时间的内存数据集中挑选最近最少使用的数据 淘汰；
# volatile-ttl: 从已设置过期时间的内存数据集中挑选即将过期的数据 淘汰；
# volatile-random:从已设置过期时间的内存数据集中任意挑选数据 淘汰；
# allkeys-lru:从内存数据集中挑选最近最少使用的数据 淘汰；
# allkeys-random:从数据集中任意挑选数据 淘汰；
# noenviction(驱逐)：禁止驱逐数据。（默认淘汰策略。当redis内存数据达到maxmemory，在该策略下，直接返回OOM错误）；

# maxmemory-policy noeviction

```



**10、AOF机制APPEND ONLY MODE**

Redis 默认不开启。它的出现是为了弥补RDB的不足（数据的不一致性），所以它采用日志的形式来**记录每个写操作，并追加到文件中**。Redis 重启的会根据日志文件的内容将写指令从前到后执行一次以完成数据的恢复工作默认redis使用的是rdb方式持久化，这种方式在许多应用中已经足够用了。但是redis如果中途宕机，会导致可能有几分钟的数据丢失，根据save来策略进行持久化，Append Only File是另一种持久化方式，可以提供更好的持久化特性。Redis会把**每次写入的数据在接收后都写入 appendonly.aof 文件**，每次启动时Redis都会先把这个文件的数据读入内存里，先忽略RDB文件。

```bash
# 默认是不开启aof模式的，默认是使用rdb方式持久化的，在大部分所有的情况下，rgb完全够用
appendonly no

# 持久化文件名字
appendfilename "appendonly.aof"

# appendfsync always		# 每次修改都会sync。消耗性能
appendfsync everysec		# 每秒执行一次sync（同步），可能会丢失这1s的数据！
# appendfsync no			# 不执行sync，这个时候操作系统自己同步数据，速度最快！


```

具体的配置，在Reds持久化中详细讲解！