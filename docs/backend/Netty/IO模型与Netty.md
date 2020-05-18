# IO模型与Netty

## BIO（Blocking I/O）

来看一个BIO的典型案例

服务器端

```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;


public class BIOServer {
    public static void main(String[] args) {    //注意网络程序的代码不可throws异常，会导致某些流不正常关闭
        try {
            ServerSocket serverSocket = new ServerSocket();
            serverSocket.bind(new InetSocketAddress("127.0.0.1",8888));//服务器绑定地址

            while(true){
                Socket socket = serverSocket.accept();//accept是阻塞方法，阻塞式监听，有socket连入，cpu才将其唤醒

                new Thread(()->{		//创建多个线程为多个客户端服务
                    handle(socket);
                }).start();       //run是单纯调用，而不是start是多线程
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static  void handle(Socket socket){
        //这个方法是把数据读过来再写回client
        try {
            byte[] bytes = new byte[1024];
            int len = socket.getInputStream().read(bytes);		//read是阻塞方法

            System.out.println(new String(bytes,0,len));
            
            socket.getOutputStream().write(bytes,0,len);		//write是阻塞方法
            socket.getOutputStream().flush();
            
        }catch (IOException e){
            e.printStackTrace();
        }
    }
}

```

客户端

```java
import java.io.IOException;
import java.net.Socket;

public class BIOClient {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("127.0.0.1",8888);
            socket.getOutputStream().write("Hello Server".getBytes());
            socket.getOutputStream().flush();
            System.out.println("write over, waiting for msg back...");
            
            byte[] bytes = new byte[1024];
            int len = socket.getInputStream().read(bytes);	
            System.out.println(new String(bytes,0,len));
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

```

本案例示意图

![image-20200513234605789](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513234605789.png)

在网络中示意图

![image-20200513234037076](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513234037076.png)



## NIO（Non Blocking I/O）无多路复用器的原始版



```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.LinkedList;

public class NioSocket {
    LinkedList<SocketChannel> clients = new LinkedList<>();
    
    ServerSocketChannel ssc;

    {
        try {
            //channel是双向通道，可读可写，基于Buffer
            ssc = ServerSocketChannel.open();
            ssc.bind(new InetSocketAddress(8888));
            ssc.configureBlocking(false);//重点，非阻塞配置
            
            while(true){
                
                Thread.sleep(1000);
                SocketChannel client = ssc.accept();		//boss
                
                if(client==null){
                    System.out.println("No client connect..");
                }else{
                    client.configureBlocking(false);
                    System.out.println("A client have connected, port is "+client.socket().getPort());
                    clients.add(client);
                }
                
                ByteBuffer buffer = ByteBuffer.allocateDirect(1024);
                
                for(SocketChannel c:clients){		//串行化读取，也可以多线程实现，后面所说的worker
                    int num = c.read(buffer);   //非阻塞
                    
                    if(num>0){              //读到了数据
                        buffer.flip();      //指针复位,并会记录limit位置
                        byte[] temp = new byte[buffer.limit()];
                        buffer.get(temp);
                        String tempStr = new String(temp);
                        
                        System.out.println("Client "+c.socket().getPort()+":"+tempStr);
                        buffer.clear();     //  清空缓存，下次读取
                    } 
                }
            }
            
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    
}

```

c10K问题下，客户端遍历过程都得调用一次read，即便没有数据传过来，很大的资源浪费，即有n个客户端，就有O（n）次调用read。而read涉及用户态和核心态状态切换的问题，大大加大了系统开销。

注：c10k问题是同时处理大量客户端请求的网络sockets优化问题。c10k用来命名并发处理10k连接的问题。



## NIO（New I/O）-Selector&single Thread

Selector是基于**多路复用器**的模型，多路复用底层在linux操作系统是调用select、poll、epoll

New I/O：channel、ByteBuffer、selector 

#### 同步

使用多路复用器可以监听I/O状态，但是读写操作依旧是用户自己触发，因此是同步的

**1、select**

这种多路复用下，只需要O(1)次调用select去监听accept事件和 I/O状态，知道了有I/O事件发生了，却并不知道是哪那些个文件描述符，我们只能无差别轮询所有文件描述符fd，找出能读出数据，或者写入数据的文件描述符fd，对他们进行操作。所以select具有O(n)的无差别轮询复杂度，同时处理的文件描述符fd越多，无差别轮询时间就越长

![image-20200514122421744](H:\Desktop\新建文件夹\Blog\docs\backend\Netty\pictures\image-20200514122421744.png)

缺点：

（1）每次调用select，都需要把fd集合从用户态拷贝到内核态，这个开销在fd很多时会很大

（2）同时每次调用select都需要在内核遍历传递进来的所有fd，这个开销在fd很多时也很大

（3）select支持的文件描述符数量太小了，32位机默认是1024个，64位机默认是2048。

**2、poll**

 调用过程和select类似，采用**链表**pollfd结构的方式替换原有fd_set数据结构,而使其**没有连接数的限制**，缺点为select前两条

**3、epoll**

epoll提供了三个函数解决poll和select的三个缺点，epoll_create,epoll_ctl和epoll_wait，epoll_create是创建一个epoll句柄；epoll_ctl是注册要监听的事件类型；epoll_wait则是等待事件的产生。

![image-20200514122738709](H:\Desktop\新建文件夹\Blog\docs\backend\Netty\pictures\image-20200514122738709.png)

对于第一个缺点，epoll的解决方案在epoll_ctl函数中。每次注册新的事件到epoll句柄中时（在epoll_ctl中指定EPOLL_CTL_ADD），会把所有的fd拷贝进内核，而不是在epoll_wait的时候重复拷贝。epoll保证了每个fd在整个过程中只会拷贝一次。

　　对于第二个缺点，epoll的解决方案不像select或poll一样每次都把current轮流加入fd对应的设备等待队列中，而只在epoll_ctl时把current挂一遍（这一遍必不可少）并为每个fd指定一个回调函数，当设备就绪，唤醒等待队列上的等待者时，就会调用这个回调函数，而这个回调函数会把就绪的fd加入一个就绪链表）。epoll_wait的工作实际上就是在这个就绪链表中查看有没有就绪的fd（利用schedule_timeout()实现睡一会，判断一会的效果，和select实现中的第7步是类似的）。

　　对于第三个缺点，epoll没有这个限制，它所支持的FD上限是最大可以打开文件的数目，这个数字一般远大于2048,举个例子,在1GB内存的机器上大约是10万左右，具体数目可以cat /proc/sys/fs/file-max察看,一般来说这个数目和系统内存关系很大。



NIO单线程模型

```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Iterator;
import java.util.Set;

public class NIOServer {
    public static void main(String[] args) {
        try {
            //NIO用的是java.nio.channels.ServerSocketChannel，双向通道
            ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();   //不是new方法
            serverSocketChannel.bind(new InetSocketAddress("127.0.0.1", 8888));

            serverSocketChannel.configureBlocking(false);      //设定阻塞为false

            System.out.println("server started, listening on :" + serverSocketChannel.getLocalAddress());
            Selector selector = Selector.open();        //不是new方法
            serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT); //注册轮询accept事件,返回值实际上是SelectionKey

            while (true) {    //轮询
                selector.select();  //阻塞,等待事件发生,相当于select（0）
                Set<SelectionKey> keys = selector.selectedKeys();   //以从多路复用器。取出有效的key
                Iterator<SelectionKey> iterator = keys.iterator();
                while (iterator.hasNext()) {              //处理该selector的所有事件
                    SelectionKey key = iterator.next();
                    iterator.remove();
                    handle(key);
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public static void handle(SelectionKey key) {
        if (key.isAcceptable()) {  
            try {
                ServerSocketChannel serverSocketChannel = (ServerSocketChannel) key.channel();	//serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);把server
                //注册进key里面了，可以从key拿出channel
                //SocketChannel
                SocketChannel socketChannel = serverSocketChannel.accept();
                socketChannel.configureBlocking(false);
                socketChannel.register(key.selector(), SelectionKey.OP_READ);  //注册client的channel 的read事件，绑定key和channel，到时可以从这个key里得到channel，也可以连ByteBuffer一起注册
                //通过key.attachment();取出buffer 
            } catch (IOException e) {
                e.printStackTrace();
            }

        } else if (key.isReadable()) { //读事件
            SocketChannel socketChannel = null;
            try {

                socketChannel = (SocketChannel) key.channel();	//取出client的channel
                ByteBuffer buffer = ByteBuffer.allocate(512);       //从字节数组读取，flip复位操作
                buffer.clear();

                int len = socketChannel.read(buffer);

                if(len!=-1){		//读到东西了，len=0发送的消息为空,len=-1没发送
                    System.out.println(new String(buffer.array(),0,len));
                }

                ByteBuffer bufferToWrite = ByteBuffer.wrap("HelloClient".getBytes());//模拟写事件
                socketChannel.write(bufferToWrite);
            } catch (IOException e) {
                e.printStackTrace();
            }finally {
                if(socketChannel!=null){
                    try {
                        socketChannel.close();//关闭该channel
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }
}

```



![image-20200513235151107](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200513235151107.png)

问题在于，如果select在读写事件发生阻塞，则新客户端无法连入server



## NIO-reactor模式

单线程+线程池

```java

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.util.Iterator;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class NIOReactor {

    ExecutorService pool = Executors.newFixedThreadPool(50);    //创建有50个线程的线程池

    private Selector selector;

    public static void main(String[] args) {
        NIOReactor server = new NIOReactor();
        server.initServer(8000);
        server.listen();
    }

    public void initServer(int port) {//初始化server
        try {
            ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
            serverSocketChannel.bind(new InetSocketAddress(port));
            serverSocketChannel.configureBlocking(false);

            this.selector = Selector.open();

            serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);
            System.out.println("server started, listening on :" + serverSocketChannel.getLocalAddress());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void listen() {//轮询访问selector
        while (true) {
            try {
                selector.select();
                Iterator iterator = selector.selectedKeys().iterator();
                while (iterator.hasNext()) {
                    SelectionKey key = (SelectionKey) iterator.next();
                    iterator.remove();

                    if (key.isAcceptable()) {
                        ServerSocketChannel serverSocketChannel = (ServerSocketChannel) key.channel();
                        SocketChannel channel = serverSocketChannel.accept();
                        channel.configureBlocking(false);
                        channel.register(this.selector, SelectionKey.OP_READ);


                        //前面基本与单线程一致
                    } else if (key.isReadable()) {
                        key.interestOps(key.interestOps() & (-SelectionKey.OP_READ));
                        //线程池拿出线程执行
                        pool.execute(new ThreadHandlerChannel(key));
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

        }
    }

}

class ThreadHandlerChannel extends Thread {
    private SelectionKey key;

    public ThreadHandlerChannel(SelectionKey key) {
        this.key = key;
    }

    @Override
    public void run() {
        SocketChannel socketChannel = (SocketChannel) key.channel();
        ByteBuffer buffer = ByteBuffer.allocate(1024);
        ByteArrayOutputStream baos = new ByteArrayOutputStream();


        try {
            int size = 0;
            while ((size = socketChannel.read(buffer)) > 0) {
                buffer.flip();
                baos.write(buffer.array(), 0, size);
                buffer.clear();
            }
            baos.close();

            byte[] content = baos.toByteArray();
            ByteBuffer writeBuf = ByteBuffer.allocate(content.length);
            writeBuf.put(content);
            writeBuf.flip();
            socketChannel.write(writeBuf);
            if (size == -1) {
                socketChannel.close();
            }else{
                key.interestOps(key.interestOps()|SelectionKey.OP_READ);
                key.selector().wakeup();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
```

![image-20200514010848631](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200514010848631.png)



### AIO（asynchronous）不再需要轮询

单线程

```java
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.AsynchronousServerSocketChannel;
import java.nio.channels.AsynchronousSocketChannel;
import java.nio.channels.CompletionHandler;

public class AIOSingleServe {

    public static void main(String[] args) {
        try {
            final AsynchronousServerSocketChannel serverChannel = AsynchronousServerSocketChannel.open();

            serverChannel.accept(null, new CompletionHandler<AsynchronousSocketChannel, Object>() {	//观察者模式，回调函数，当有连接时让操作系统通知执行该方法，相当于把该方法交给操作系统
                
                @Override
                public void completed(AsynchronousSocketChannel client, Object attachment) {
                    serverChannel.accept(null,this);

                    try {
                        System.out.println(client.getRemoteAddress());
                        ByteBuffer buffer = ByteBuffer.allocate(1024);
                        client.read(buffer, buffer, new CompletionHandler<Integer, ByteBuffer>() {	//回调函数，读完了就执行Handler的completed方法
                            @Override
                            public void completed(Integer result, ByteBuffer attachment) {
                                attachment.flip();
                                System.out.println(new String(attachment.array(),0,result));
                                client.write(ByteBuffer.wrap("HelloClient".getBytes()));
                            }

                            @Override
                            public void failed(Throwable exc, ByteBuffer attachment) {
                                    exc.printStackTrace();
                            }
                        });
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }

                @Override
                public void failed(Throwable exc, Object attachment) {
					exc.printStackTrace();
                }
            });
            
            while(true){
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

```

使用线程池只需要把起始代码修改一下即可,回调不变

```java
ExecutorService executorService = Executors.newCachedThreadPool();
            AsynchronousChannelGroup threadGroup = AsynchronousChannelGroup.withCachedThreadPool(executorService,1);
            
            final AsynchronousServerSocketChannel serverChannel = AsynchronousServerSocketChannel.open(threadGroup);
```

![image-20200514014005069](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200514014005069.png)



## NIO、AIO操作系统实现

在linux上，NIO和AIO都是基于epoll轮询实现的，但是在windows下AIO是微软自己写的非轮询，效率高而windows的server少

因此在linux下AIO效率未必比NIO高，底层实现一样，AIO多一层封装



## Netty三种线程模型

1、单线程

```java
 		EventLoopGroup bossGroup = new NioEventLoopGroup(1);     //负责连接和读写线程组

        ServerBootstrap b = new ServerBootstrap();

        b.group(bossGroup, bossGroup)	
            ...
```

2、混合，有一个组即是boss也是worker

```java
 		EventLoopGroup bossGroup = new NioEventLoopGroup(4);     //负责连接和读写线程组

        ServerBootstrap b = new ServerBootstrap();

        b.group(bossGroup, bossGroup)	
            ...
```

3、主从

服务器端

```java
package com.zero;

import io.netty.bootstrap.ServerBootstrap;
import io.netty.buffer.ByteBuf;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.util.CharsetUtil;

public class NettyServer {
    int port = 8888;

    public NettyServer(int port) {
        this.port = port;
    }

    public void serverStart() {
        EventLoopGroup bossGroup = new NioEventLoopGroup();     //负责连接线程组
        EventLoopGroup workerGroup = new NioEventLoopGroup(2);   //负责读写线程组

        ServerBootstrap b = new ServerBootstrap();

        b.group(bossGroup, workerGroup)
                .channel(NioServerSocketChannel.class)
                .childHandler(new ChannelInitializer<SocketChannel>() { //处理器
                    @Override
                    protected void initChannel(SocketChannel socketChannel) throws Exception {	//通道初始化
                        socketChannel.pipeline().addLast(new Handler());
                    }
                });


        try {
            ChannelFuture f = b.bind(port).sync();

            f.channel().closeFuture().sync();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            workerGroup.shutdownGracefully();
            bossGroup.shutdownGracefully();
        }
    }
}

class Handler extends ChannelInboundHandlerAdapter{
    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        System.out.println("server: channel read");
        ByteBuf buf = (ByteBuf) msg;

        System.out.println(buf.toString(CharsetUtil.UTF_8));
        
        ctx.writeAndFlush(msg);
        ctx.close();
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
        cause.printStackTrace();
        ctx.close();
    }
}
```

客户端

```java
package com.zero;

import io.netty.bootstrap.Bootstrap;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioSocketChannel;
import io.netty.util.ReferenceCountUtil;

public class NettyClient {
    public static void main(String[] args) {
        new NettyClient().clientStart();
    }

    private void clientStart() {
        EventLoopGroup workers = new NioEventLoopGroup();
        Bootstrap b = new Bootstrap();
        b.group(workers)
                .channel(NioSocketChannel.class)
                .handler(new ChannelInitializer<SocketChannel>() {

                    @Override
                    protected void initChannel(SocketChannel socketChannel) throws Exception {
                        socketChannel.pipeline().addLast(new ClientHandler());
                    }
                });

        try {
            System.out.println("start to connect ...");
            ChannelFuture f =b.connect("127.0.0.1",8888).sync();
            f.channel().closeFuture().sync();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }finally {
            workers.shutdownGracefully();
        }

    }
}

class ClientHandler extends ChannelInboundHandlerAdapter {
    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        System.out.println("channel is activated");

        final ChannelFuture f = ctx.writeAndFlush(Unpooled.copiedBuffer("Hello Netty".getBytes()));
        f.addListener(new ChannelFutureListener(){

            @Override
            public void operationComplete(ChannelFuture channelFuture) throws Exception {
                System.out.println("msg send!");
            }
        });
    }

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        ByteBuf buf = (ByteBuf) msg;
        System.out.println(buf.toString());

        ReferenceCountUtil.release(msg);
    }

}
```

