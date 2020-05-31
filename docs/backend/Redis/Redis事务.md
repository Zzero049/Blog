# Redis事务

Mysql数据库的事务保证ACID，而**Redis**单条命令式保证原子性的，但是**事务不保证原子性**！

Redis 本身提供的所有 API 都是原子操作，那么 Redis 事务其实是要保证批量操作的原子性，但 Redis 在事务执行过程的错误情况做出了权衡取舍，那就是**放弃了回滚**。Redis 官方文档对此给出的解释是：

1. Redis 操作失败的原因只可能是语法错误或者错误的数据库类型操作，这些都是在开发层面能发现的问题不会进入到生产环境，因此不需要回滚。
2. Redis 内部设计推崇简单和高性能，因此不需要回滚能力。

Redis事务本质：一组命令的集合！一个事务中的所有命令都会被序列化，在事务执行过程的中，会按照顺序执行。事务在执行的过程中，不会被其他客户端发送来的命令请求所打断。

![image-20200529001915391](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529001915391.png)

**Redis事务没有隔离级别的概念**

所有的命令在事务中，并没有直接被执行！**只有发起执行命令的时候才会执行**！Exec



## 事务发展阶段

一个事务从开始到执行会经历以下**三个阶段**：

- **开始事务（multi）**
- **命令入队（。。。）**
- **执行事务（exec）**

```bash
127.0.0.1:6379> multi			# 开始事务
OK
127.0.0.1:6379> set k1 v1		# 命令入队
QUEUED							# QUEUED
127.0.0.1:6379> set k2 v2		# 命令入队
QUEUED
127.0.0.1:6379> set k3 v3		# 命令入队
QUEUED
127.0.0.1:6379> get k1			# 命令入队
QUEUED
127.0.0.1:6379> exec			# 执行事务
1) OK							# 顺序的执行
2) OK
3) OK
4) "v1"

```

也可以手动**取消事务：discard**，一旦取消事务，事务队列中所有命令不会执行

```bash
127.0.0.1:6379> multi
OK
127.0.0.1:6379> set k4 v4
QUEUED
127.0.0.1:6379> discard			# 取消事务
OK
127.0.0.1:6379> get k4
(nil)
```



## 事务中出现异常

**1、编译型异常**（代码有问题！命令写错）

**事务中所有命令都不会被执行**

```bash
127.0.0.1:6379> multi
OK
127.0.0.1:6379> set k1 v1
QUEUED
127.0.0.1:6379> set k2 v2
QUEUED
127.0.0.1:6379> set k3 v3
QUEUED
127.0.0.1:6379> getset k3					# 错误命令，没有value值
(error) ERR wrong number of arguments for 'getset' command
127.0.0.1:6379> set k4 v4
QUEUED
127.0.0.1:6379> set k5 v5
QUEUED
127.0.0.1:6379> exec						# 可以看到提示也说discarded了
(error) EXECABORT Transaction discarded because of previous errors.
127.0.0.1:6379> keys *						# 没有任何命令成功
(empty list or set)

```



**2、运行时异常**（比如java中1/0的操作）

如果事务队列中存在语法性，那么执行命令的时候，**其他命令是可以正常执行**的，错误命令抛出异常！

```bash
127.0.0.1:6379> multi
OK
127.0.0.1:6379> set k1 "v1"			# k1是字符串
QUEUED
127.0.0.1:6379> set k2 v2
QUEUED
127.0.0.1:6379> incr k1					# 对字符串自增1
QUEUED
127.0.0.1:6379> set k3 v3
QUEUED
127.0.0.1:6379> get k1
QUEUED
127.0.0.1:6379> exec				# 其他命令正常执行
1) OK
2) OK
3) (error) ERR value is not an integer or out of range		# 单条任务出错
4) OK
5) "v1"

```



## Redis中的乐观锁

**悲观锁：**

- 很悲观，认为什么时候都会出问题，无论做什么都会加锁

**乐观锁**

- 很乐观，认为什么时候都不会出问题，所以不会上锁！更新数据的时候去判断一下，在此期间是否有人修改过这个数据

- mysql版本号机制，获取version，更新的时候比较version

**WATCH命令（监视）**可以为 **Redis 事务**提供 check-and-set （CAS）行为。（不在事务Multi内，则无效）

WATCH使得EXEC 命令需要有条件地执行： **事务只能在所有被监视键都没有被修改的前提下执行， 如果这个前提不能满足的话，<font color="red">事务就不会被执行</font>。**

**当 EXEC 被调用时，** **不管事务是否成功执行， 对所有键的监视都会被取消。**

另外， 当客户端断开连接时， 该客户端对键的监视也会被取消。

![image-20200529084208433](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529084208433.png)

使用无参数的 UNWATCH 命令可以手动取消对所有键的监视。 对于一些需要改动多个键的事务， 有时候程序需要同时对多个键进行加锁， 然后检查这些键的当前值是否符合程序的要求。 当值达不到要求时， 就可以使用 UNWATCH  命令来取消目前对键的监视， 中途放弃这个事务， 并等待事务的下次尝试。

```bash
# 线程1调用客户端，执行事务
127.0.0.1:6379> watch money
OK
127.0.0.1:6379> multi
OK
127.0.0.1:6379> decrby money 10
QUEUED
127.0.0.1:6379> incrby out 10
QUEUED
127.0.0.1:6379> exec				# 线程2修改之后，提交
(nil)								# 事务执行失败
127.0.0.1:6379> get money
"10000"

# 线程2直接修改money
127.0.0.1:6379> get money
"80"
127.0.0.1:6379> set money 10000
OK

# 线程1 监视money后提交，再执行新的事务
127.0.0.1:6379> watch money
OK
127.0.0.1:6379> multi
OK
127.0.0.1:6379> set out 100
QUEUED
127.0.0.1:6379> exec		# 结束对money的监视
1) OK
127.0.0.1:6379> multi
OK
127.0.0.1:6379> set money 1000	# 可以提交成功
QUEUED
127.0.0.1:6379> exec

# 线程2修改 money
127.0.0.1:6379> set money 10
OK

```



## Jedis执行事务

```java
public class JedisDemo1 {
    public static void main(String[] args) {
        // 1、new Jedis
        Jedis jedis = new Jedis("106.55.3.34",6379);
        jedis.auth("123");
        System.out.println(jedis.ping());
        jedis.select(0);
        System.out.println(jedis.flushAll());

        JSONObject jsonObject = new JSONObject();
        jsonObject.put("hello","world");
        jsonObject.put("name","zhangsan");
        //开启事务
        Transaction multi = jedis.multi();
        String result = jsonObject.toJSONString();
		jedis.watch("money");       //进行监控
        try{

            System.out.println(multi.set("user1", result));
            System.out.println(multi.set("user2", result));
            // 模拟出错
            int i = 1/0;
            multi.exec();		// 执行命令
        }catch (Exception e){
            // 出错就放弃事务提交
            multi.discard();
            e.printStackTrace();
        }finally {
            // 释放连接
            System.out.println(jedis.get("user1"));
            System.out.println(jedis.get("user2"));
            jedis.close();
        }


    }
}

```

靠自己程序实现出错“回滚”

![image-20200529105736127](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529105736127.png)

正常执行

![image-20200529105834900](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529105834900.png)