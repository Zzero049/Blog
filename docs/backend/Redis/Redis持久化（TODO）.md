# Redis持久化（todo）

redis是一个内存数据库，如果不将内存中的数据库状态保存到磁盘，那么一旦服务器进程退出，服务器中的数据库状态也会消失。所以 Redis提供了持久化功能！



## RDB：默认方式

**在指定的时间间隔内将内存中的数据集快照写入磁盘**，也就是行话讲的Snapshot快照，它**恢复时是将快照文件直接读到内存**里。

![image-20200529223614967](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529223614967.png)



Redis会单独创建（fork）一个子进程来进行持久化，会先将数据写入到一个临时文件中，待持久化过程都结束了，再用这个临时文件替换上次持久化好的文件。整个过程中，**主进程是不进行任何IO操作的**。这就确保了极高的性能。如果需要进行大规模数据的恢复，且对于数据恢复的完整性不是非常敏感，那RDB方式要比AOF方式更加的高效。RDB的缺点是最后一次持久化后的数据可能丢失。我们默认的就是RDB，一般情况下不需要修改这个配置！

==rdb保存的文件是dump.rdb==，都是在我们的配置文件中快照中进行配置的！

![image-20200529212923825](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529212923825.png)



进行测试，注意是是60秒对5个key执行修改触发rdb，而对同一个key的修改行为，也只算作一个key，而且**这个备份不是立刻的，即使在50秒达到了5次，也需要等到60秒才会生成dump.rdb文件**

![image-20200529214332730](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529214332730.png)

先删除原来的dump.rdb

```bash
[root@VM_0_10_centos bin]# ls
dump.rdb  redis-benchmark  redis-check-aof  redis-check-rdb  redis-cli  redisConfig  redis-sentinel  redis-server
[root@VM_0_10_centos bin]# rm -rf dump.rdb 
```

进行测试，同一个key多次操作只算一次key修改事件

```
127.0.0.1:6379> flushdb
OK
127.0.0.1:6379> set k2 v2
OK
127.0.0.1:6379> set k3 v3
OK
127.0.0.1:6379> set k2 v2
OK
127.0.0.1:6379> set k3 v3
OK
127.0.0.1:6379> set k2 v2
OK
127.0.0.1:6379> set k1 v1
OK
127.0.0.1:6379> set k4 v4
OK
127.0.0.1:6379> set k5 v5
OK
```

可以看到一分钟后，成功写入

![image-20200529214614945](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529214614945.png)

将服务器关掉后，再开启，客户端连接进来后，发现数据依然存在

```bash
127.0.0.1:6379> keys *
1) "k4"
2) "k3"
3) "k2"
4) "k5"
5) "k1"
```

不止是save规则满足会触发rdb事件

**触发机制：**

1、save的规则满足的情况下，会等待规定时间触发rdb文件

2、flushAll会默认立即产生dump.rdb文件

3、退出redis服务器，也会产生rdb文件

**redis如何恢复rdb文件的数据：**

1、只需要将rdb文件放在bin目录就可以，redis启动的时候会自动检查 dump.rdb恢复其中的数据！

2、查看rdb自动存储和读取的位置

```bash
127.0.0.1:6379> config get dir
1) "dir"
2) "/usr/local/bin"
```



**优点：**

1、使用单独**子进程**来进行持久化，**主进程不会进行任何IO操作**，保证了redis的高性能 （对数据完整性不高时，使用）



**缺点：**

1、RDB是间隔一段时间进行持久化，如果持久化之间redis发生故障，会发生数据丢失。所以这种方式更适合数据要求不严谨的时候

2、fork进程的时候，子进程会复制父进程的缓存空间，所以需要一定的内存空间



有时候我们会将dump.rdb再进行备份（生产环境中一旦丢失损坏，后果不堪设想）



### SAVE和BGSAVE

除了 Redis 的配置文件可以对快照的间隔进行设置之外，Redis 客户端还同时提供两个命令来生成 RDB 存储文件，也就是 `SAVE` 和 `BGSAVE`，通过命令的名字我们就能猜出这两个命令的区别。

![save-and-bgsave](https://gitee.com/zero049/MyNoteImages/raw/master/aHR0cHM6Ly9pbWcuZHJhdmVuZXNzLm1lL3NhdmUtYW5kLWJnc2F2ZS5wbmc)

其中 `SAVE` 命令在执行时会直接阻塞当前的线程，由于 Redis 是**单线程**的，所以 `SAVE` 命令会直接阻塞来自客户端的所有其他请求，这在很多时候对于需要提供较强可用性保证的 Redis 服务都是无法接受的。

我们往往需要 `BGSAVE` 命令在后台生成 Redis 全部数据对应的 RDB 文件，当我们使用 `BGSAVE` 命令时，Redis 会立刻 `fork` 出一个子进程，子进程会执行『将内存中的数据以 RDB 格式保存到磁盘中』这一过程，而 Redis 服务在 `BGSAVE` 工作期间仍然可以处理来自客户端的请求。



## AOF（Append Only File）：日志记录的方式

**将我们的所有命令都记录下来，恢复的时候就把这个文件全部在执行一遍**

![image-20200529225358020](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529225358020.png)

以日志的形式来记录每个写操作，将Reds执行过的所有指令记录下来（读操作不记录），**只许追加文件但不可以改写文件**，redis启动之初会读取该文件重新构建数据，换言之，redis重启的话就根据日志文件的内容将写指令从前到后执行一次以完成数据的恢复工作

AOF默认是关闭的

![image-20200529225554907](H:\Desktop\新建文件夹\Blog\docs\backend\Redis\pictures\image-20200529225554907.png)

==AOF保存的文件是appendonly.aof文件==

进行测试，

1、编辑redis.windwos.conf文件

```bash
appendonly yes

# 持久化策略默认每秒即可
# appendfsync always 				#每一次操作都进行持久化
appendfsync everysec			#每隔一秒进行一次持久化
# appendfsync no					#操作系统进行同步
```

2、重启服务器即生效

![image-20200529230819045](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529230819045.png)

3、进行插入数据测试

```bash
127.0.0.1:6379> flushdb
OK
127.0.0.1:6379> set k1 v1
OK
127.0.0.1:6379> set k2 v2
OK
127.0.0.1:6379> set k3 v3
OK
127.0.0.1:6379> get k1
"v1"
```

4、再查看appendonly.aof文件

```bash
[root@VM_0_10_centos bin]# vim appendonly.aof 

*2
$6
SELECT		# select 0
$1
0
*3
$3
set			# set k1 v1
$2
k1
$2
v1
*3
$3
set			# set k2 v2
$2
k2
$2
v2
*3
$3
set			# set k3 v3
$2
k3
$2
v3

```

5、测试破坏aof后，redis如何响应

![image-20200529231357487](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529231357487.png)

```bash
# 重启服务器后，连接，发现服务器根本没有启动
[root@VM_0_10_centos ~]# redis-cli -p 6379
Could not connect to Redis at 127.0.0.1:6379: Connection refused
[root@VM_0_10_centos ~]# ps -ef|grep redis
root     24958 11807  0 23:14 pts/2    00:00:00 grep --color=auto redis
```



如果这个aof文件有错，这时候reds是启动不起来的，我们需要修复这个aof文件

```bash
[root@VM_0_10_centos bin]# redis-check-aof --fix appendonly.aof 
```

![image-20200529231742945](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529231742945.png)

查看appendonly.aof 错误的命令被删了，redis服务器也可以正常启动了

```bash
# 可以看到set k3 v3被删除
[root@VM_0_10_centos bin]# vim appendonly.aof 

*2
$6
SELECT
$1
0
*3
$3
set
$2
k1
$2
v1
*3
$3
set
$2
k2
$2
v2
```



**优点：**

1、修改命令尽可能进行同步，尽可能保证数据完整性

**缺点：**

1、占空间大，相对于数据文件来说，aof远远大于rdb，修复的速度也比rdb慢！

2、耗费时间多，日志的记录维护也需要一定的时间

3、aof 默认就是文件的无限追加，文件会越来越大



**扩展：**

1、RDB持久化方式能够在指定的时间间隔内对你的**数据进行快照存储**

2、AOF持久化方式**记录每次对服务器写的操作**，当**服务器重启**的时候会**重新执行这些命令来恢复原始的数据**，AOF命令以 Redis协议追加保存每次写的操作到文件末尾，Redis还能对AOF文件进行后台重写，使得AOF文件的体积不至于过大。

3、只做缓存，如果你只希望你的数据在服务器运行的时候存在，你也可以不使用任何持久化

4、同时开启两种持久化方式

- 在这种情况下，当 redis重启的时候会优先载入AoF文件来恢复原始的数据，因为在通常情况下AOF文件保存的数据集要比RDB文件保存的数据集要完整。
- RDB的数据不实时，同时使用两者时服务器重启也只会找AOF文件，那要不要只使用AOF呢？作者建议不要，因为RDB更适合用于备份数据库（AOF在不断变化不好备份），快速重启，而且不会有AOF可能潜在的Bug，留着作为一个万一的手段。

5、性能建议

- 因为RDB文件只用作后备用途，建议**只在Slave上持久化RDB文件**，而且只要**15分钟备份一次**就够了，**只保留save 900 1**这条规则。
- 如果 Enable aof，好处是在最恶劣情况下也只会丢失不超过两秒数据，启动脚本较简单只load自己的AOF文件就可以了，代价一是带来了持续的IO，二是 AOF rewrite的最后将 rewrite过程中产生的新数据写到新文件造成的阻塞几乎是不可避免的。只要硬盘许可，应该尽量减少 AOF rewrite的频率，AOF重写的基础大小默认值64M太小了，可以设到5G以上，默认超过原大小100%大小重写可以改到适当的数值
- 如果不 Enable aof，仅靠 Master-Slave Replication实现高可用性也可以，能省掉-大笔lO，也减少了 rewrite时带来的系统波动。代价是如果 Master/Slave同时挂掉，会丢失十几分钟的数据，启动脚本也要比较两个 Master/Save中的RDB文件，载入较新的那个，微博就是这种架构。