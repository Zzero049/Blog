# 多路 I/O 转接服务器

​	在BIO的架构里，在accept和read的过程中，服务器都是处于阻塞的，这样不利于多任务的场景（如果想完成多任务需要很多线程，但是一般不可能做到开那么多线程）。

​	多路IO转接服务器也叫做多任务IO服务器。该类服务器实现的主旨思想是，**不再由应用程序自己监视客户端连接**，取而代之由**内核**替应用程序**监视文件**。（**事件驱动**）

​	主要使用的方法有三种 select、poll、epoll

![image-20200919202134113](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200919202134113.png)

​	

### select（198x年的api，阻塞函数）

客户端socket连接进来，对于个这个连接，操作系统内核实际上还是在文件描述符上进行操作

![image-20200919203435345](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200919203435345.png)

![image-20200919203617331](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200919203617331.png)

```
　　FD_ZERO(&set); /*将set清零使集合中不含任何fd*/
　　FD_SET(fd, &set); /*将fd加入set集合*/ 
　　FD_CLR(fd, &set); /*将fd从set集合中清除*/ 
　　FD_ISSET(fd, &set); /*测试fd是否在set集合中*/
```

select()返回值：所监听的所有的监听集合（读、写、异常集合）中，满足条件的**总数**。



 下面来看一下使用select的代码

由于我们的代码是跑在用户态的，如果用户态去轮询每个文件描述符，开销很大，因为每个文件描述符都涉及一次用户态和内核态的切换，因此**我们需要调用FD_ZERO和FD_SET把文件描述符先加到set集合中（至于为什么不能读出后对应位就改成0，不知道，可能和用户态有关）**

**调用select会阻塞，直到监听到事件**

![image-20200919214111887](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200919214111887.png)

 这种多路复用下，只**需要O(1)次调用select去监听accept事件和 I/O状态，知道了有I/O事件发生了，却并不知道是哪那些个文件描述符**，我们只能无差别轮询所有文件描述符fd，找出能读出数据，或者写入数据的文件描述符fd，对他们进行操作。所以**select具有O(n)的无差别轮询复杂度**，同时处理的文件描述符fd越多，无差别轮询时间就越长

**缺点：**

1. fd_set（即bitMap）只能支持1024个文件描述符
2. 每次调用select前，需要把fd_set从用户态拷贝到内核态
3. 调用完select之后，知道有事件发生了，需要O(n)的时间复杂度去遍历fd_set的所有文件描述符，读取有事件的fd的数据
4. 有用户态到内核态拷贝数据的开销



### poll（同样是阻塞函数）

poll的逻辑和select是一致的，但是不再用bitmap了，而是改用链表，使用的结构体如下

```c
struct pollfd{
  	int fd;						// 文件描述符，对应select的fd_set下标
    short events;				// 需要监听的事件，读POLLIN/写POLLOUT
    short revents;				// 反馈，也就是有这个事件，则记录为对应事件标志，如读事件发生，则赋值为POLLIN
};
```

继续来看一段使用poll的代码

![image-20200919231133595](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200919231133595.png)

那么很明显，**每次调用poll之前不需要像select一样需要将fd_set每次都拷到内核，而且也没有bitmap 1024大小的限制**

**缺点**

1. 依然要轮询所有链节点才能知道谁被修改了，再从对应fd中读出数据，这个过程需要O(n)的时间复杂度
2. 有用户态到内核态拷贝数据的开销



### epoll（可以非阻塞，linux特有）

**epoll首先是用内核态和用户态的共享内存的，因此不存在数据拷贝的开销**

epoll有三个关键函数，如下

- `epoll_create`:内核在epoll文件系统中创建结点epfd，还会在内核缓存中建立一棵红黑树， 用来存储以后epoll_ctl传来的epoll_fd，将后面的fd加到缓存
- `epoll_ctl`：将fd和对应的事件加入到内核缓存
- `epoll_wait` ：如果有事件来了，就返回  触发事件的个数

![image-20200514122738709](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200514122738709.png)



`epoll_wait`两种触发模式：

- **LT:水平触发**
  - 当 epoll_wait() 检测到描述符事件到达时，将此事件通知进程，**进程可以不立即处理该事件**，下次调用 epoll_wait() 会再次通知进程。是默认的一种模式，并且同时支持 Blocking 和 No-Blocking。		
- **ET:边缘触发**
  - 和 LT 模式不同的是，通知之后进程必须立即处理事件，**比如读事件必须把buffer读光**。			
  - 下次再调用 epoll_wait() 时不会再得到事件到达的通知。很大程度上**减少了 epoll 事件被重复触发的次数，**因此效率要比 LT 模式高。只支持 No-Blocking，以避免由于一个文件句柄的阻塞读/阻塞写操作把处理多个文件描述符的任务饿死。

继续来看一段使用epoll的代码

![image-20200919233756206](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200919233756206.png)

可以看到epoll解决了poll剩下的缺点，即拷贝和O(n)遍历的问题

epoll优化总结如下

- 对于第一个缺点，epoll的解决方案在epoll_ctl函数中。每次注册新的事件到epoll句柄中时（在epoll_ctl中指定EPOLL_CTL_ADD），会把所有的fd拷贝进内核，而不是在epoll_wait的时候重复拷贝。epoll保证了每个fd在整个过程中只会拷贝一次。
- 对于第二个缺点，epoll的解决方案不像select或poll一样每次都把current轮流加入fd对应的设备等待队列中，而只在epoll_ctl时把current挂一遍（这一遍必不可少）并为每个fd指定一个**回调函数**，当设备就绪，唤醒等待队列上的等待者时，就会调用这个回调函数，而这个回调函数会把就绪的fd加入一个就绪链表）。epoll_wait的工作实际上就是在这个就绪链表中查看有没有就绪的fd（利用schedule_timeout()实现睡一会，判断一会的效果，和select实现中的第7步是类似的）。

- 对于第三个缺点，epoll没有这个限制，它所支持的FD上限是最大可以打开文件的数目，这个数字一般远大于2048,举个例子,在1GB内存的机器上大约是10万左右，具体数目可以cat /proc/sys/fs/file-max察看,一般来说这个数目和系统内存关系很大。
- 第四个缺点，通过共享内存去解决