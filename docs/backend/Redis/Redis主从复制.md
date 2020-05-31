# Redis主从复制

## 概念

主从复制，是指将一台 Redis服务器的数据，复制到其他的Reds服务器。前者称为主节点 （master/leader），后者称为从节点
（slave/follower）**数据的复制是单向的，只能由主节点到从节点。Master以写为主，Slave以读为主**

**默认情况下，每台 Redis服务器都是主节点**；且一个主节点可以有多个从节点（或没有从节点），但一个从节点只能有一个主节点。

![image-20200530010748469](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530010748469.png)

主从复制，读写分离！80%的情况下都是在进行读操作！减缓服务器的压力！架构中经常使用！一主二从是最基本的



**主从复制的作用：**

**1、数据冗余：**主从复制实现了数据的**热备份**，是持久化之外的一种数据冗余方式。

**2、故障恢复：**当主节点岀现问题时，可以由从节点提供服务，实现快速的故障恢复；实际上是一种服务的冗余。

**3、负载均衡：**在主从复制的基础上，配合读写分离，可以由主节点提供写服务，由从节点提供读服务（即写 Redis数据时应用连接主节点，读 Redis数据时应用连接从节点），分担服务器负载；尤其是在写少读多的场景下，通过多个从节点分担读负载，可以大大提高 Redis服务器的并发量（读写分离）

**4、高可用（集群）基石：**除了上述作用以外，**主从复制还是哨兵和集群能够实施的基础**，因此说主从复制是 Redis高可用的基础。



一般来说，要将Redis运用于工程项目中，只使用一台Redis是万万不能的（宕机，一主二从），原因如下

1、从结构上，单个 Redis服务器会发生单点故障，并且一台服务器需要处理所有的请求负载，压力较大；

2、从容量上，单个 Redis服务器内存容量有限，就算一台 Redis服务器内存容量为256G，也不能将所有内存用作 Redis存储内存，一般来说，**单台Redis服务器最大使用内存不应该超过20G**。

电商网站上的商品，一般都是一次上传，无数次浏览的，说专业点也就是"多读少写"。



## 一主二从配置

只配置从库，不用配置主库（主库默认自己是主库）

现在配置两个从机

1、可以用**info replication**查看当前服务器主从关系

```bash
127.0.0.1:6379> info replication			# 查看当前库信息
# Replication
role:master
connected_slaves:0
master_replid:b1f5e7d6f5107cc68ceafb8780039003491c6cb8
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:0
second_repl_offset:-1
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0

```

2、复制3个配置文件，然后修改对应的信息，主机不需要修改，修改两个从机

​	1、端口

![image-20200530012618805](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530012618805.png)

​	2、pid

![image-20200530012659923](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530012659923.png)

​	3、log名

![image-20200530012733659](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530012733659.png)

​	4、dump文件名

![image-20200530012816798](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530012816798.png)

​	5、由于设置了密码，从机配置文件还需要获得materauth

![image-20200530020130514](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530020130514.png)

​	6、修改bind为0.0.0.0，设置防火墙端口（主从俩台服务器都要设置）

```bash
firewall-cmd --zone=public --add-port=6379/tcp --permanent
```

​	7、启动三台服务器，ps查看是否启动成功

```bash
[root@VM_0_10_centos bin]# ps -ef|grep redis
root     10368     1  0 01:29 ?        00:00:00 redis-server *:6379
root     10557     1  0 01:30 ?        00:00:00 redis-server *:6380
root     10648     1  0 01:31 ?        00:00:00 redis-server *:6381
```



### 从机配置

就一个**slaveof命令**

```bash
127.0.0.1:6380> slaveof 127.0.0.1 6379		# 配置从机，找谁当自己老大
OK
127.0.0.1:6380> info replication		# 查看主从关系
# Replication
role:slave				# 当前角色
master_host:127.0.0.1	# 主机ip
master_port:6379
master_link_status:down
master_last_io_seconds_ago:-1
master_sync_in_progress:0
slave_repl_offset:1
master_link_down_since_seconds:1590773774
slave_priority:100
slave_read_only:1
connected_slaves:0
master_replid:f8aa11ad027507cf76c7bc7787d75d507cfc7679
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:0
second_repl_offset:-1
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0


# 主机信息
127.0.0.1:6379> info replication
# Replication
role:master
connected_slaves:2									# 两个从机信息
slave0:ip=127.0.0.1,port=6380,state=online,offset=98,lag=1
slave1:ip=127.0.0.1,port=6381,state=online,offset=98,lag=0
master_replid:6db172c9b3fd2f1289bfec9561c03e14e2ecda74
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:98
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:98

```

真实的从主配置应该在配置文件中配置，这样的话是永久的，我们这里使用的是**命令配置**，是暂时的，**当从机重启时，自动变为独立的主机**

一般用配置文件配置，只需指定 **replicaof  masterip  masterport**即可

由于默认从机是只读的replica-read-only yes，从机进行写操作会报错

```bash
# 从机
127.0.0.1:6380> set k1 b2
(error) READONLY You can't write against a read only replica.

# 主机
127.0.0.1:6379> set name zhangsan
OK
```



### 模拟主机宕机

将主机shutdown，从机依然能读取到之前的数据

```bash
127.0.0.1:6380> get name
"zhangsan"
127.0.0.1:6380> info replication
# Replication
role:slave
master_host:127.0.0.1
master_port:6379				# 主机依旧没变
master_link_status:down
master_last_io_seconds_ago:-1
master_sync_in_progress:0
slave_repl_offset:1250
master_link_down_since_seconds:15
slave_priority:100
slave_read_only:1
connected_slaves:0
master_replid:6db172c9b3fd2f1289bfec9561c03e14e2ecda74
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:1250
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:1250
```

主机重新连接后，更新name值，从机能取到新值

```bash
# 主机
127.0.0.1:6379> set name lisi
OK

# 从机
127.0.0.1:6380> get name
"lisi"
```

测试：主机断开连接，从机依旧连接到主机的，但是没有写操作，这个时候，主机如果回来了，从机依旧可以直接获取到主机写的信息

如果是使用命令行，来配置的主从关系，这个时候从机如果重启了，就会变回主机！只要变为从机，立马就会从主机中获取值！



## 复制原理

Slave启动成功连接到 master后会发送一个**sync同步命令**

Master接到命令，启动后台的存盘进程，同时**收集**所有接收到的用于**修改数据集命令**，在后台进程执行完毕之后，master将**传送整个数据文件到slave，并完成一次完全同步（全量复制）**

- 全量复制：slave服务在接收到数据库文件数据后，将其存盘并加载到内存中。

- 增量复制：Master继续将新的所有收集到的修改命令依次传给save，完成同步（连上之后，主机修改，传送给从机命令）

但是**只要是重新连接 master，一次完全同步（全量复制）将被自动执行**



## 层层主从

现在我们把端口6381的从机，指向6380，那么从理论上，6380即是主机，又是从机（实际身份还是从机，无法进行写入）

此时master进行修改，slave1和slave2肯定是能进行读取的

![image-20200530023953807](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530023953807.png)

```bash
127.0.0.1:6380> info replication
# Replication
role:slave					# 从机
master_host:127.0.0.1
master_port:6379
master_link_status:up
master_last_io_seconds_ago:10
master_sync_in_progress:0
slave_repl_offset:980
slave_priority:100
slave_read_only:1
connected_slaves:1
slave0:ip=127.0.0.1,port=6381,state=online,offset=980,lag=0
master_replid:0ca6a3939929abae29d6f964cc09c604a1902b7d
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:980
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:980

```

那么问题来了

1、如果中间的slave1宕机，slave2能进行主从复制吗？

答案是：不能

```bash
# master
127.0.0.1:6379> set heifei heifei
OK

# slave2
127.0.0.1:6381> get heifei
(nil)

# slave1连上之后
127.0.0.1:6381> get heifei
"heifei"
```



2、如果master宕机了，slave1如果想成为新的master，可行吗？（谋朝篡位）

可行，通过`slaveof no one`让自己变成主机！其他的节点就可以手动连接到最新的这个主节点（手动，哨兵是自动），而且原先的主节点回来之后，所有从机不再与之绑定（山中无老虎，猴子当霸王）

注意：命令slaveof no one 就是让自己变成主机，并断开与之前主机的链

```bash
# slave1
127.0.0.1:6380> slaveof no one		# 手动设置
OK
127.0.0.1:6380> set lalala heiheihei
OK

# slave2
127.0.0.1:6381> get lalala
"heiheihei"

# 当master连上之后，发现没有任何从机与他相连
127.0.0.1:6379> info replication
# Replication
role:master
connected_slaves:0
master_replid:a0ecdbac3b099e5690aacb814d3ade79fb313c73
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:0
second_repl_offset:-1
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0

```



## 哨兵模式Sentinel

主从切换技术的方法是：当主服务器宕机后，需要手动把一台从服务器切换为主服务器，这就需要人工干预，费事费力，还会造成一段时间内服务不可用。这不是一种推荐的方式，更多时候，我们优先考虑**哨兵模式**。Redis从2.8开始正式提供了 Sentinel（哨兵）架构来解决这个问题

谋朝篡位的自动版，能够后台监控主机是否故障，如果故障了根据投票数==自动将从库转换为主库==

哨兵模式是一种特殊的模式，首先 Redis提供了哨兵的命令，**哨兵是一个独立的进程**，作为进程，它会独立运行。其原理是**哨兵通过发送命令，等待 Redis服务器响应，从而监控运行的多个 Redis实例**

![image-20200530135643581](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530135643581.png)



这里里的哨兵有两个作用

- 通过发送命令，让Redis服务器返回监控其运行状态，包括主服务器和从服务器。

- 当哨兵监测到 master宕机，会自动将 slave切换成 master，然后通过**发布订阅模式**通知其他的从服务器，修改配置文件，让它们切换主机。

然而一个哨兵进程对 Redis服务器进行监控，可能会岀现问题，为此，我们可以使用多个哨兵进行监控。各个哨兵之间还会进行监控，这样就形成了多哨兵模式

![image-20200530135722357](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530135722357.png)

假设主服务器宕机，哨兵1先检测到个结果，系统并不会马上进行 failover过程，仅仅是哨兵1主观的认为主服务器不可用，这个现象成为**主观下线**。当后面的哨兵也检测到主服务器不可用，并且数量达到一定值时，那么哨兵之间就会进行一次投票，投票的结果由一个哨兵发起，进行 **failover故障转移**操作。切换成功后，就会通过发布订阅模式，让各个哨兵把自己监控的从服务器实现切换主机，这个过程称为**客观下线**



### 测试：

我们目前的状态是一主二从！

1、创建哨兵配置文件（sentinel.conf名字不能错）

```bash
vim sentinel.conf
```

```bash
# sentinel monitor 被监控的名称 host post 数字1，指明当有多少个sentinel认为一个master失效时，master才算真正失效
sentinel monitor myredis 127.0.0.1 6379 1
sentinel auth-pass myredis 123		# 有密码的
```



常用的配置：

```bash
port 26379
# sentinel announce-ip <ip>
# sentinel announce-port <port>
dir /tmp

################################# myreids #################################
sentinel monitor myredis 127.0.0.1 6379 2
# sentinel auth-pass <master-name> <password>
sentinel down-after-milliseconds myredis 30000
sentinel parallel-syncs myredis 1
sentinel failover-timeout myredis 180000
# sentinel notification-script <master-name> <script-path>
# sentinel client-reconfig-script <master-name> <script-path>

# 可以配置多个master节点
################################# master02 #################################
```

**1. port** :当前Sentinel服务运行的端口

**2. dir** : Sentinel服务运行时使用的临时文件夹

**3.sentinel monitor myreids 127.0.0.1 2**:Sentinel去监视一个名为myreids的主redis实例，这个主实例的IP地址为本机地址192.168.110.101，端口号为6379，而将这个主实例判断为失效至少需要2个 Sentinel进程的同意，只要同意Sentinel的数量不达标，自动failover就不会执行

**4.sentinel down-after-milliseconds myreids 30000**:指定了Sentinel认为Redis实例已经失效所需的毫秒数。当实例超过该时间没有返回PING，或者直接返回错误，那么Sentinel将这个实例标记为主观下线。只有一个 Sentinel进程将实例标记为主观下线并不一定会引起实例的自动故障迁移：只有在足够数量的Sentinel都将一个实例标记为主观下线之后，实例才会被标记为客观下线，这时自动故障迁移才会执行

**5.sentinel parallel-syncs myreids 1**：指定了在执行故障转移时，最多可以有多少个从Redis实例在同步新的主实例，在从Redis实例较多的情况下这个数字越小，同步的时间越长，完成故障转移所需的时间就越长

**6.sentinel failover-timeout myreids 180000**：如果在该时间（ms）内未能完成failover操作，则认为该failover失败

**7.sentinel notification-script <master-name> <script-path>**：指定sentinel检测到该监控的redis实例指向的实例异常时，调用的报警脚本。该配置项可选，但是很常用



2、 启动哨兵

```bash
[root@VM_0_10_centos bin]# redis-sentinel redisConfig/sentinel.conf 
```

可以看到两个从机

```
1419:X 30 May 2020 14:27:13.893 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1419:X 30 May 2020 14:27:13.893 # Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=1419, just started
1419:X 30 May 2020 14:27:13.893 # Configuration loaded
                _._                                                  
           _.-``__ ''-._                                             
      _.-``    `.  `_.  ''-._           Redis 5.0.5 (00000000/0) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._                                   
 (    '      ,       .-`  | `,    )     Running in sentinel mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 26379
 |    `-._   `._    /     _.-'    |     PID: 1419
  `-._    `-._  `-./  _.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |           http://redis.io        
  `-._    `-._`-.__.-'_.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |                                  
  `-._    `-._`-.__.-'_.-'    _.-'                                   
      `-._    `-.__.-'    _.-'                                       
          `-._        _.-'                                           
              `-.__.-'                                               

1419:X 30 May 2020 14:27:13.894 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
1419:X 30 May 2020 14:27:13.899 # Sentinel ID is 0b55763a766205ed15d4a4ed30223ae99905eb77
1419:X 30 May 2020 14:27:13.899 # +monitor master myredis 127.0.0.1 6379 quorum 1
1419:X 30 May 2020 14:27:13.899 * +slave slave 127.0.0.1:6380 127.0.0.1 6380 @ myredis 127.0.0.1 6379
1419:X 30 May 2020 14:27:13.908 * +slave slave 127.0.0.1:6381 127.0.0.1 6381 @ myredis 127.0.0.1 6379
```

让主机挂掉，发生故障转移

![image-20200530143435303](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530143435303.png)

可以看到6381成为了新的主机，通过投票算法选出

而当6379回来之后，哨兵自动将6379作为从机加入主机6381

![image-20200530143716751](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530143716751.png)



###  优缺点

**优点：**

1、哨兵集群，基于主从复制模式，所有的主从配置优点，它全有

2、主从可以切换，故障可以转移，系统的可用性就会更好

3、哨兵模式就是主从模式的升级，手动到自动，更加健壮！

**缺点：**

1、Redis不好在线扩容的，集群容量一旦到达上限，在线扩容就十分麻烦

2、实现哨兵模式的配置其实是很麻烦的，里面有很多选择！

官网完整配置

```bash
# Example sentinel.conf

# 哨兵 sentinel实例运行的端口默认26379
port 26379

# 哨兵sentinel的工作目录
dir /tmp


# 哨兵 sentinel监视的 redis主节点的 ip port 
# master-name可以自己命名的主节点名字只能由字母A-z、数字0-9、这三个字符”，-"组成
# quorum配置多少个 dentine1哨兵统一认为 master主节点失联那么这时客观上认为主节点失联了
# sentinel monitor <master-name> <ip> <redis-port> <quorum>
sentinel monitor mymaster 127.0.0.1 6379 2

# 当在 Redis实例中开启了 requi repass foobared授权密码这样所有连接 Redis实例的客户端都要提供密码
# 设置哨兵 sentinel连接主从的密码注意必须为主从设置一样的验证密码
# sentinel auth-pass <master-name> <password>
sentinel auth-pass mymaster 123

# 指定多少毫秒之后主节点没有应答哨兵 dentine1此时哨兵主观上认为主节点下线默认30秒
sentinel down-after-milliseconds mymaster 30000



# 选项指定了在执行故障转移时， 最多可以有多少个从Redis实例在同步新的主实例，
# 在从Redis实例较多的情况下这个数字越小，同步的时间越长，完成故障转移所需的时间就越长。
# sentinel parallel-syncs <master-name> <numslaves>
sentinel parallel-syncs mymaster 1



# 如果在该时间（ms）内未能完成failover操作，则认为该failover失败，默认3分钟
# sentinel failover-timeout <master-name> <milliseconds>
sentinel failover-timeout mymaster 180000

# SCRIPTS EXECUTION

# 配置当某一事件发生时所需要执行的脚本，可以通过脚本来通知管理员，例如当系统运行不正常时发邮件通知相关人员。
# 对于脚本的运行结果有以下规则
# 若脚本执行后返回1，那么该脚本稍后将会被再次执行，重复次数目前默认为10
# 若脚本执行后返回2，或者比2更高的一个返回值，脚本将不会重复执行。
# 如果脚本在执行过程中由于收到系统中断信号被终止了，则同返回值为1时的行为相同
# 一个脚本的最大执行时间为60s，如果超过这个时间，脚本将会被一个SIGKILL信号终止，之后重新执行
# 通知型脚本：当 sentinel有任何警告级别的事件发生时（比如说 redis实例的主观失效和客观失效等等），将会去调用这个脚本，这时这个脚本应该通过邮件，SMS等方式去通知系统管理员关于系统不正常运行的信息。调用该脚本时，将传给脚本两个参数，一个是事件的类型是事件的描述。如果 sentinel.conf配置文件中配置了这个脚本路径，那么必须保证这个脚本存在于这个路径，并且是可执行的，否则sentinel无法正常启动成功

# 通知脚本,shell编程
sentinel notification-script mymaster /var/redis/notify.sh


# 客户端重新配置主节点参数脚本
# 当一个 master由年fai1over而发生改变时，这个脚本将会被调用，通知相关的客户端关于 master地址已经发生改变的信息。
# 以下参数将会在调用脚本时传给脚本
# <master-name> <role> <state> <from-ip> <from-port> <to-ip><to-port>
# 目前<state>总是"failover"
# <role>是“leader"或者“observer”中的一个。
# 参数from-ip，from-port，to-ip，to-port是用来和旧的 master和新的 master即旧的s1ave通信的
# 这个脚本应该是通用的，能被多次调用，不是针对性的
# sentinel client-reconfig-script <master-name> <script-path>
sentinel client-reconfig-script mymaster /var/redis/reconfig.sh

```

