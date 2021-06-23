# Redis 发布订阅

Redis发布订阅（pub/sub）是一种==消息通信模式==：发送者（pub）发送消息，订阅者（sub）接收消息。如微信、微博、B站的关注系统。

redis不是专门做消息队列的，但是也可以实现，由于自身发布订阅的api太过于鸡肋，只能客户端单纯做一个阻塞监听，而要退出客户端才能退出监听。这就导致在linux下一次连接上来的客户端可能不是前面那个。

Reds客户端可以订阅任意数量的频道

订阅/发布消息图：

三个角色

第一个：消息发送者

第二个：频道

第三个：消息订阅者

![image-20200529235041650](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529235041650.png)

下图展示了频道 channel1 ， 以及订阅这个频道的三个客户端 —— client2 、 client5 和 client1 之间的关系：

![img](https://gitee.com/zero049/MyNoteImages/raw/master/pubsub1.png)

当有新消息通过 PUBLISH 命令发送给频道 channel1 时， 这个消息就会被发送给订阅它的三个客户端：

![img](https://gitee.com/zero049/MyNoteImages/raw/master/pubsub2.png)



## Redis 发布订阅命令

命令中，字段建议都用双引号

下面列出了 redis 发布订阅常用命令：主要用前三个，由于订阅会阻塞，导致退订功能好像没什么用。。。

这些命令被广泛用于构建即时通信应用，比如网络聊天室（chatroom）和实时广播、实时提醒等。

**1、SUBSCRIBE：订阅给定的一个或多个频道的信息**、

SUBSCRIBE channel1 channel2 ... 

一旦订阅，阻塞监听，只能Ctrl+c 退出客户端

```bash
# 该客户端订阅kuangshenshuo和zhuge
127.0.0.1:6379> SUBSCRIBE kuangshenshuo zhuge
Reading messages... (press Ctrl-C to quit)		# 监听频道，等待推送信息
1) "subscribe"
2) "kuangshenshuo"
3) (integer) 1
1) "subscribe"
2) "zhuge"
3) (integer) 2

```

**2、PUBLISH：将信息发送到指定的频道**

PUBLISH channel message

```bash
# 该客户端是发布者
127.0.0.1:6379> publish kuangshenshuo helloworld
(integer) 3
```

```bash
# 订阅端收到消息
1) "message"
2) "kuangshenshuo"		# 频道
3) "helloworld"			# 消息具体内容
```

**3、PSUBSCRIBE：订阅符合规则（类似正则）的频道**

PSUBSCRIBE pattern1 pattern2 

kuang* 就是以kuang开头的频道

```bash
# 订阅端
127.0.0.1:6379> PSUBSCRIBE zhu* kuang*
Reading messages... (press Ctrl-C to quit)
1) "psubscribe"
2) "zhu*"
3) (integer) 1
1) "psubscribe"
2) "kuang*"
3) (integer) 2
1) "pmessage"				# pmessage
2) "kuang*"
3) "kuangshenshuo"			# 频道全名
4) "zaima"					# 消息
1) "pmessage"
2) "zhu*"
3) "zhuge"
4) "xuejava"

```

```bash
# 发布端
127.0.0.1:6379> publish kuangshenshuo zaima 
(integer) 3
127.0.0.1:6379> publish zhuge xuejava
(integer) 1

```

**4、PUBSUB：查看订阅与发布系统状态**

PUBSUB channels 查看 有哪些频道

```bash
# 查看有哪些精确名字的频道
127.0.0.1:6379> PUBSUB channels
1) "zhangfei"
2) "Bzhan"
3) "kuangshenshuo"
```

**5、UNSUBSCRIBE/PUNSUBSCRIBE：精确退订/模糊退订**

没什么用，ctrl+c再连上的客户端不是同一个了

```bash
# 订阅
127.0.0.1:6379> SUBSCRIBE kuangshen 
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "kuangshen"
3) (integer) 1
quit
^C
# 
127.0.0.1:6379> UNSUBSCRIBE kuangshen
1) "unsubscribe"
2) "kuangshen"
3) (integer) 0


```





# Redis 频道的订阅与退订原理

**实际是维护了一个字典**

当一个客户端执行 SUBSCRIBE 命令， 订阅某个或某些频道的时候， 这个客户端与被订阅频道之间就建立起了一种订阅关系。

Redis 将所有频道的订阅关系都保存在服务器状态的 `pubsub_channels` 字典里面， 这个字典的键是某个被订阅的频道， 而键的值则是一个链表， 链表里面记录了所有订阅这个频道的客户端：

```
struct redisServer {

    // ...

    // 保存所有频道的订阅关系
    dict *pubsub_channels;

    // ...

};
```

比如说， 图 IMAGE_PUBSUB_CHANNELS 就展示了一个 `pubsub_channels` 字典示例， 这个字典记录了以下信息：

- `client-1` 、 `client-2` 、 `client-3` 三个客户端正在订阅 `"news.it"` 频道。
- 客户端 `client-4` 正在订阅 `"news.sport"` 频道。
- `client-5` 和 `client-6` 两个客户端正在订阅 `"news.business"` 频道。

![img](https://gitee.com/zero049/MyNoteImages/raw/master/2015-09-13_55f5290278113.png)

## 订阅频道

每当客户端执行 SUBSCRIBE 命令， 订阅某个或某些频道的时候， 服务器都会将客户端与被订阅的频道在 `pubsub_channels` 字典中进行关联。

根据频道是否已经有其他订阅者， 关联操作分为两种情况执行：

- 如果频道已经有其他订阅者， 那么它在 `pubsub_channels` 字典中必然有相应的订阅者链表， 程序唯一要做的就是将客户端添加到订阅者链表的末尾。
- 如果频道还未有任何订阅者， 那么它必然不存在于 `pubsub_channels` 字典， 程序首先要在 `pubsub_channels` 字典中为频道创建一个键， 并将这个键的值设置为空链表， 然后再将客户端添加到链表， 成为链表的第一个元素。

举个例子， 假设服务器 `pubsub_channels` 字典的当前状态如图 IMAGE_PUBSUB_CHANNELS 所示， 那么当客户端 `client-10086` 执行命令：

```
SUBSCRIBE "news.sport" "news.movie"
```

之后， `pubsub_channels` 字典将更新至图 IMAGE_AFTER_SUBSCRIBE 所示的状态， 其中用虚线包围的是新添加的节点：

- 更新后的 `pubsub_channels` 字典新增了 `"news.movie"` 键， 该键对应的链表值只包含一个 `client-10086` 节点， 表示目前只有 `client-10086`一个客户端在订阅 `"news.movie"` 频道。
- 至于原本就已经有客户端在订阅的 `"news.sport"` 频道， `client-10086` 的节点放在了频道对应链表的末尾， 排在 `client-4` 节点的后面。

![img](https://gitee.com/zero049/MyNoteImages/raw/master/2015-09-13_55f529039b077.png)

SUBSCRIBE 命令的实现可以用以下伪代码来描述：

```
def subscribe(*all_input_channels):

    # 遍历输入的所有频道
    for channel in all_input_channels:

        # 如果 channel 不存在于 pubsub_channels 字典（没有任何订阅者）
        # 那么在字典中添加 channel 键，并设置它的值为空链表
        if channel not in server.pubsub_channels:
            server.pubsub_channels[channel] = []

        # 将订阅者添加到频道所对应的链表的末尾
        server.pubsub_channels[channel].append(client)
```

## 退订频道

UNSUBSCRIBE 命令的行为和 SUBSCRIBE 命令的行为正好相反 —— 当一个客户端退订某个或某些频道的时候， 服务器将从 `pubsub_channels` 中解除客户端与被退订频道之间的关联：

- 程序会根据被退订频道的名字， 在 `pubsub_channels` 字典中找到频道对应的订阅者链表， 然后从订阅者链表中删除退订客户端的信息。
- 如果删除退订客户端之后， 频道的订阅者链表变成了空链表， 那么说明这个频道已经没有任何订阅者了， 程序将从 `pubsub_channels` 字典中删除频道对应的键。

举个例子， 假设 `pubsub_channels` 的当前状态如图 IMAGE_BEFORE_UNSUBSCRIBE 所示， 那么当客户端 `client-10086` 执行命令：

```
UNSUBSCRIBE "news.sport" "news.movie"
```

之后， 图中用虚线包围的两个节点将被删除， 如图 IMAGE_AFTER_UNSUBSCRIBE 所示：

- 在 `pubsub_channels` 字典更新之后， `client-10086` 的信息已经从 `"news.sport"` 频道和 `"news.movie"` 频道的订阅者链表中被删除了。
- 另外， 因为删除 `client-10086` 之后， 频道 `"news.movie"` 已经没有任何订阅者， 因此键 `"news.movie"` 也从字典中被删除了。

![img](https://gitee.com/zero049/MyNoteImages/raw/master/2015-09-13_55f529053e290.png)

![img](https://gitee.com/zero049/MyNoteImages/raw/master/2015-09-13_55f5290654c19.png)





