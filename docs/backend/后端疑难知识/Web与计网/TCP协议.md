# TCP协议

TCP报文结构

![image-20200920084448051](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200920084448051.png)

## 可靠传输

TCP的可靠传输基本上都可以在TCP 20B的头部体现

1、确认和超时重传：接收方收到报文就会确认，发送方发送一段时间后没有收到确认就超时重传，这个是依赖序号和确认号实现的。

2、数据校验：校验和

3、连接管理：三次握手和四次挥手

4、流量控制：通过滑动窗口机制，当接收方来不及处理发送方的数据，能提示发送方降低发送的速率，防止包丢失。

5、拥塞控制：通过拥塞窗口机制，当网络拥塞时，减少数据的发送。慢开始+拥塞避免，快恢复+快重传





## 三次握手

![image-20200919235745825](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200919235745825.png)

### 三次握手改成两次会怎么样

1、如果客户端一开始发送的SYN报文在网络阻塞，而又发生超时重传，并完成了一次通信，后面这个阻塞的报文又重新到了服务器端，服务器又打开了连接，浪费资源

2、通过序号和确认号能保证旧链接和新链接在服务器看来尽可能不同，为了确认序号，证明这个包是新的，而不是在链路中delay的

### **如果已经建立了连接，但是客户端突然出现故障了怎么办？**

TCP设有一个**保活计时器，客户端如果出现故障，服务器不能一直等下去**，白白浪费资源。服务器每收到一次客户端的请求后都会重新**复位这个计时器**，时间通常是设置为2小时，若两小时还没有收到客户端的任何数据，服务器就会发送一个探测报文段，以后每**隔75秒钟发送一次。若一连发送10个探测报文仍然没反应**，服务器就认为客户端出了故障，接着就关闭连接。

### 什么是半连接队列

   服务器第一次收到客户端的 SYN 之后，就会处于 SYN_RCVD 状态，此时双方还没有完全建立其连接，服务器会把此种状态下请求连接放在一个队列里，我们把这种队列称之为半连接队列。当然还有一个全连接队列，就是已经完成三次握手，建立起连接的就会放在全连接队列中。如果队列满了就有可能会出现丢包现象。





## 四次挥手

![image-20200920084320834](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200920084320834.png)



### **为什么TCP连接的时候是3次，关闭的时候却是4次？**

**因为只有在客户端和服务端都没有数据要发送的时候才能断开TCP（相当于需要断开双向连接）**。而客户端发出FIN报文时只能保证客户端没有数据发了，服务端还有没有数据发客户端是不知道的。而服务端收到客户端的FIN报文后只能先回复客户端一个确认报文来告诉客户端我服务端已经收到你的FIN报文了，但我服务端还有一些数据没发完，等这些数据发完了服务端才能给客户端发FIN报文(**所以不能一次性将确认报文和FIN报文发给客户端，就是这里多出来了一次)。**



### TIME_WAIT（等待2MSL）的作用

1、防止客户端最后一次发给服务器的确认在网络中丢失以至于客户端关闭，而服务端并未关闭，导致资源的浪费。如果有TIME_WAIT等待2MSL则服务器最后一个FIN报文会超时重传

2、等待最大的2MSL可以让本次连接的所有的网络包在链路上消失，以防造成不必要的干扰。比如新的连接端口号还是一样的，用的初始序号和上一次连接差不多，那网络中滞留的包被服务器接收，返回的数据全部被新连接接收，造成客户端的数据错误。



### 网络中（服务器端）大量的TIME_WAIT

首先time_wait出现在**主动关闭连接的一方**

**1、服务器大量的TIME_WAIT**

这种情况比较常见，一些**爬虫服务器**或者WEB服务器（如果网管在安装的时候没有做内核参数优化的话）上经常会遇到这个问题，这个问题是怎么产生的呢？

TIME_WAIT是主动关闭连接的一方保持的状态。

1. 对于爬虫服务器来说他本身就是“客户端”，在完成一个爬取任务之后，他就会发起主动关闭连接。

2. 在**高并发短连接**的TCP服务器上，当服务器处理完请求后立刻主动正常关闭连接。这个场景下会出现大量socket处于TIME_WAIT状态。

解决思路很简单，就是**让服务器能够快速回收和重用那些TIME_WAIT的资源。**修改TCP内核参数配置文件,**TIME_WAIT的快速回收**

第二个解决方案是改为长连接，显著减少连接量，但是并发量减少很多

**2、大量客户端TIME_WAIT**

大量客户端在TIME_WAIT的状态说明有很多请求（比如HTTP）

1. CC攻击等网络攻击，有大量的请求进来

**如何尽量处理TIMEWAIT过多?**

编辑内核文件/etc/sysctl.conf，加入以下内容：

```
net.ipv4.tcp_syncookies = 1 表示开启SYN Cookies。当出现SYN等待队列溢出时，启用cookies来处理，可防范少量SYN攻击，默认为0，表示关闭；
net.ipv4.tcp_tw_reuse = 1 表示开启重用。允许将TIME-WAIT sockets重新用于新的TCP连接，默认为0，表示关闭；
net.ipv4.tcp_tw_recycle = 1 表示开启TCP连接中TIME-WAIT sockets的快速回收，默认为0，表示关闭。
net.ipv4.tcp_fin_timeout 修改系默认的 TIMEOUT 时间
```

然后执行 /sbin/sysctl -p 让参数生效.

```
/etc/sysctl.conf是一个允许改变正在运行中的Linux系统的接口，它包含一些TCP/IP堆栈和虚拟内存系统的高级选项，修改内核参数永久生效。
```

## 心跳包

心跳检测机制一般有两个作用：

1. 保活
2. 检测死链

**1）针对情形一：**此应用场景要求必须保持客户端与服务器之间的连接正常，就是我们通常所说的“保活“。如上所述，当服务器与客户端一定时间内没有有效业务数据来往时，我们只需要给对端发送心跳包即可实现保活。

**2）针对情形二：**要解决死链问题，只要我们此时任意一端给对端发送一个数据包即可检测链路是否正常，这类数据包我们也称之为”心跳包”，这种操作我们称之为“心跳检测”。顾名思义，如果一个人没有心跳了，可能已经死亡了；一个连接长时间没有正常数据来往，也没有心跳包来往，就可以认为这个连接已经不存在，为了节约服务器连接资源，我们可以通过关闭 socket，回收连接资源。



在TCP协议的机制里面，本身是存在有心跳包机制的，也就是TCP协议中的 SO_KEEPALIVE，系统默认是设置2小时的心跳频率。需要用要用 setsockopt将 SOL SOCKET.SO KEEPALIVE设置为1才是打开，并且可以设置三个参数:

**tcp_keepalive_time/tcp_keepalive_probes/tcp_keepalive_intv，分别表示连接闲置多久开始发 keepalive的ACK包、发几个ACK包不回复才当对方死了、两个ACK包之间间隔多长TCP协议会向对方发一个带有ACK标志的空数据包**（KeepAlive探针），对方在收到ACK包以后，如果连接—切正常，应该回复一个ACK；如果连接出现错误了（例如对方重启了，连接状态丢失），则应当回复一个RST；如果对方没有回复，服务器每隔多少时间再发ACK，如果连续多个包都被无视了，说明连接被断开了。

心跳检测包”是属于TCP协议底层的检测机制，上位机软件只是解析显示网口的有用数据包，收到心跳包报文属于TCP协议层的数据，一般软件不会将它直接在应用层显示出来，所以看不到。以太网中的“心跳包”可以通过“以太网抓包软件”分析ICP/P协议层的数据流看到。报文名称"TCP Keep-Aive"