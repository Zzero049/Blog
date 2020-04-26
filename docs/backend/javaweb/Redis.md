



# Redis

redis是一款高性能的NOSQL系列的非关系型数据库，是用c语言开发的一个开源的高性能键值对（key-value）数据库，官方提供测试数据，50个并发执行100000个请求，读的速度是110000次/s，写的速度是81000次/s，且Redis通过提供多种键值数据类型来适应不同场景下的存储需求，目前为止Redis支持的键值数据类型如下：

​	1）字符串类型 string
​	2）哈希类型hash
​	3）列表类型list
​	4）集合类型 set
​	5）有序集合类型 sortedset



关系型数据库和非关系型数据库区别：（关系型数据库存取慢）

![image-20200422125355785](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200422125355785.png)

优点：
1）成本：nosql数据库简单易部署，基本都是开源软件，不需要像使用oracle那样花费大量成本购买使用，相比关系型数据库价格便宜。
2）查询速度：nosql数据库将数据存储于缓存之中，关系型数据库将数据存储在硬盘中，自然查询速度远不及nosql数据库。
3）存储数据的格式：nosql的存储格式是key，value形式、文档形式、图片形式等等，所以可以存储基础类型以及对象或者是集合等各种格式，而数据库则只支持基础类型。
4）扩展性：关系型数据库有类似join这样的多表查询机制的限制导致扩展很艰难。

缺点：
1）维护的工具和资料有限，因为nosql是属于新的技术，不能和关系型数据库10几年的技术同日而语。
2）不提供对sql的支持，如果不支持sq1这样的工业标准，捋产生一定用户的学习和使用成本。
3）不提供关系型数据库对事务的处理。

非关系型数据库的优势：
1）性能NOSQL是基于键值对的，可以想象成表中的主键和值的对应关系，而且不需要经过SQL层的解析，所以性能非常高。
2）可扩展性同样也是因为基于键值对，数据之间没有耦合性，所以非常容易水平扩展。

关系型数据库的优势：
1）复杂查询可以用sQL语句方便的在一个表以及多个表之间做非常复杂的数据查询。
2）事务支持使得对于安全性能很高的数据访问要求得以实现。对于这两类数据库，对方的优势就是自己的弱势，反之亦然。

下载安装：

[Redis中文网](https://www.redis.net.cn/)  linux版

![](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200422130244686.png)

win版 https://github.com/microsoftarchive/redis/releases/tag/win-3.2.100

![image-20200422131108759](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200422131108759.png)

win端解压直接可以使用：
	redis.windows.conf：    配置文件
	redis-cli.exe:                  redis的客户端
	redis-server.exe:           redis服务器端

## 命令操作

### redis的数据结构：

redis存储的是：key，value格式的数据，其中key都是字符串，value有5种不同的数据结构	

​	1）字符串类型 string
​	2）哈希类型hash                类似map
​	3）列表类型list                    类似linkedlist
​	4）集合类型 set
​	5）有序集合类型 sortedset



本质基本元素都是字符串

![image-20200422134807123](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200422134807123.png)

#### 字符串类型 string 
1.存储：set key value
2.获取：get key
3.删除：del key

####  哈希类型：hash

key代表hash变量名，field表示存的键值对的key

1.存储：hset key  field value
2.获取：hget field  key 

​				hgetall key:获取所有的field和value

3.删除：hdel  key  field

#### 列表类型list

可以添加一个元素到列表的头部（左边）或者尾部（右边），可以一次性将多个元素加入

1.添加：
		1.lpush key value：捋元素加入列表左表
		2.rpush key value：捋元素加入列表右边
2.获取：
		lrange key start end：范围获取 如lrange myList 0 -1（获取全部）
3.删除：
		1.lpop key：删除列表最左边的元素，并将元素返回
		2.rpop key：删除列表最君边的元素，并将元素返回

#### 集合set

不允许重复元素

1.存储：sadd key value
2.获取：smembers key：获取set集合中所有元素
3.删除：srem key value：删除set集合中的某个元素

#### 有序集合sorted

不允许重复元素，且根据分数进行排序

1.存储：zadd key score value：
2.获取：zrange key start end
3.删除：zrem key value

### 通用命令

1.keys*：查询所有的键
2.type key：获取键对应的value的类型



## 持久化

redis是一个内存数据库，当redis服务器重后，获取电脑重后，数据会丢失，我们可以将redis内存中的数据持久化保存到硬盘的文件中。

### 持久化机制

#### RDB：默认方式

不需要进行配置，默认就使用这种机制

在一定的间隔时间中，检测key的变化情况，然后持久化数据

​		1.编辑redis.windwos.conf文件，默认如下	

```
save     900     1  		#after 9ee sec(15 min)if at least 1 key changed
save     300     10			# after 300 sec(5 min)if at least 10 keys changed
save      60     10000		#after 60 sec if at least 10000 keys changed
```

​		2.重新后动redis服务器，并指定配置文件名称

​		cmd 切到redis目录输入redis-server.exe redis.windows.conf

#### AOF：日志记录的方式

可以记录每一条命令的操作。可以每一次命令操作后，持久化数据

​		1.编辑redis.windwos.conf文件

​		appendonly no（关闭aof）-->appendonly yes（开启aof）

```
appendfsync always 				#每一次操作都进行持久化
appendfsync everysec			#每隔一秒进行一次持久化
appendfsync no					#不进行持久化
```

​		2.重新后动redis服务器，并指定配置文件名称

​		cmd 切到redis目录输入redis-server.exe redis.windows.conf



## Jedis

一款java操作redis数据库的工具,类似JDBC

依赖：

```xml
<dependency>
      <groupId>redis.clients</groupId>
      <artifactId>jedis</artifactId>
      <version>2.7.1</version><!--版本号可根据实际情况填写-->
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

入门demo

```java
public void test1(){
        //1.获取连接
        Jedis jedis = new Jedis("localhost",6379);///如果使用空参构造，默认值“1ocalhost"，6379端口
        //2.操作
        jedis.set("username","张三");
        //3.关闭连接
        jedis.close();
    }
```

jedis里的方法基本与redis操作数据库的方法名字相同

值得注意的有

1. 可以使用setex（）方法存储可以指定过期时间的 key value

```java
//将activecode:hehe键值对存入redis，并且2e秒后自动删除该键值对
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

