# InnoDB 存储引擎

InnoDB存储引擎将数据放在一个逻辑的表空间中，这个表空间就像黑盒一样由 InnoDB自身进行管理。从 MySQL41（包括4.1）版本开始，**它可以将每个-Innodb存储引擎的表单独存放到一个独立的ibd文件中**。与 Oracle类似，InnodB存储引擎同样可以使用裸设备
（row disk）来建立其表空间。

InnoDB通过使用**多版本并发控制（MVCC）**来获得高并发性，并且实现了SQL标准的4种隔离级别，**默认为 REPEATABLE级别**。同时使用一种被称为 next-key locking的策略来避免幻读（phantom）现象的产生。除此之外，InnoDB储存引擎还提供了插入缓冲（insert buffer）、二次写（double write）、自适应哈希索引（adaptive hash index）、预读（read

对于**表中数据的存储，InnodB存储引擎采用了聚集（clustered）的方式**，这种方式类似于 Oracle的索引聚集表（index organized table，IOT）。每张表的存储都按主键的顺序存放，如果没有显式地在表定义时指定主键，**InnoDB存储引擎会为每一行生成一个6字节的ROWID，并以此作为主键。**

与其他存储引擎特性区别表如下：

![image-20201009154408685](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201009154408685.png)

## 1.1 连接

TCPP套接字方式是 MySQL在任何平台下都提供的连接方式，也是网络中使用得最多的一种方式。这种方式在TCP连接上建立一个基于网络的连接请求，一般情况下客户端在一台服务器上，而 MySQL实例在另一台服务器上，这两台机器通过一个TCP网络连接。例如，我可以在 Windows服务器下请求一台远程 Linux服务器下的 MySQL实例，如下所示。

![image-20201009154816464](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201009154816464.png)

这里的客户端是 Windows，它向一台 Host ip为192.168.0.101的 MySQL实例发起了TCPP连接请求，并且连接成功。之后，就可以对 MySQL数据库进行一些数据库操作，如DDL和DML等。

这里需要注意的是，在通过 TCP/IP连接到 MySQL实例时，**MySQL会先检查一张权限视图，用来判断发起请求的客户端IP是否允许连接到 MySQL实例。**该视图在mysq库下，表名为user，如下所示。

![image-20201009154938430](pictures/image-20201009154938430.png)

从这张权限表中可以看到，MySQL允许davi这个用户在任何P段下连接该实例，并且不需要密码。此外，还给出了root用户在多个网段下的访问控制权限



## 2.1 体系结构

InnoDB有多个内存块，你可以认为这些内存块组成了一个大的内存池，负责如下工作：

- 维护所有进程线程需要访问的多个内部数据结构
- 缓存磁盘上的数据，方便快速地读取，并且在对磁盘文件的数据进行修改之前在这里缓存。
- 重做日志（redo log）缓冲。
- ......

![image-20201009155535122](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201009155535122.png)

后台线程的主要作用是负责刷新内存池中的数据，保证缓冲池中的内存缓存的是最近的数据。此外，将巳修改的数据文件刷新到磁盘文件，同时保证在数据库发生异常情况下InnoDB能恢复到正常运行状态（日志）。



### 2.1.1 后台线程

由于 Oracle是多进程的架构（Windows下除外），因此可以通过一些很简单的命令来得知 Oracle当前运行的后台进程，如ipcs命令。一般来说，Oracle的核心后台进程有CKPT DBWn、LGWR、ARCn、PMON、SMON等。

 InnoDB并不是这样对数据库进程进行操作的。**InnoDB存储引擎是在一个被称做 master thread的线程上几乎实现了所有的功能。**

默认情况下，**InnoDB存储引擎的后台线程有7个——4个 IO thread，1个 master thread，1个锁（lock）监控线程，1个错误监控线程。**IO thread的数量由配置文件中的 innodb file io_threads参数控制，默认为4，如下所示。

![image-20201009195932197](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201009195932197.png)

![image-20201009195953859](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201009195953859.png)

可以看到，**4个IO线程分别是 insert buffer thread、log thread、read thread、write thread。**在 Linux平台下，IO thread的数量不能进行调整，但是在 Windows平台下可以通过参数innodb file io_threads来增大 IO thread。InnoDB Plugin版本开始增加了默认 lo thread的数量，默认的 read thread和 write thread分别增大到了4个，并且不再使用 innodb_file io threads参数，而是分别使用 innodb read_io threads和 innodb write_io threads参数。



### 2.1.2 内存

InnodB存储引擎内存由以下几个部分组成：**缓冲池（buffer pool）、重做日志缓冲池（redo log buffer）以及额外的内存池（additional memory pool）**，分别由配置文件中的参数innodb_buffer_pool_size和 innodb_log_buffer-size的大小决定。以下显示了一台 MySQL数据库服务器，它将 InnoDB存储引擎的缓冲池、重做日志缓冲池以及额外的内存池分别设置为25G、8M和8M（分别以字节显示）。

![image-20201009201657138](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201009201657138.png)

缓冲池是占最大块内存的部分，用来存放各种数据的缓存。因为 InnoDB的存储引擎的工作方式总是**将数据库文件按页（每页16K）读取到缓冲池**，然后按**最近最少使用（LRU）的算法**来保留在缓冲池中的缓存数据。**如果数据库文件需要修改，总是首先修改在缓存池中的页**（发生修改后，该页即为脏页），然后再按照一定的频率将缓冲池的脏页刷新（flush）到文件。可以通过命令 SHOW ENGINE INNODB STATUS来查看 innodb_buffer_pool的具体使用情况，如下所示

![image-20201009202725556](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201009202725556.png)

在 BUFFER POOL AND MEMORY里可以看到 InnodB存储引擎缓冲池的使用情况，**buffer_pool_size表明了一共有多少个缓冲帧（buffer frame），每个 buffer frame为16K，所以这里一共分配了65536*16/1024=1G内存的缓冲池。Free buffers表示当前空闲的缓冲帧，Database pages表示已经使用的缓冲帧，Modified db pages表示脏页的数量。**就当前状态看来，这台数据库的压力并不大，因为在缓冲池中有大量的空闲页可供数据库进一步使用。(注意：**show engine innodb status的命令显示的不是当前的状态，而是过去某个时间范围内 InnoDB存储引擎的状态**，从上面的示例中我们可以看到，Per second averages calculated from the last24 seconds表示的信息是过去24秒内的数据库状态)。

具体来看，缓冲池中缓存的数据页类型有：**索引页、数据页、undo页、插入缓冲（insert buffer）、自适应哈希索引（adaptive hash index）、InnoDB存储的锁信息（lock info）、数据字典信息（data dictionary）**等。不能简单地认为，缓冲池只是缓存索引页和数据页，它们只是占缓冲池很大的一部分而已。下图很好地显示了 InnoDB存储引擎中内存的结构情况。

![image-20201009203350121](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201009203350121.png)

**日志缓冲将重做日志信息先放入这个缓冲区**，然后按一定频率将其刷新到重做日志文件。该值**一般不需要设置为很大**，因为一般情况下**毎一秒钟就会将重做日志缓冲刷新到日志文件**，因此我们只需要保证每秒产生的事务量在这个缓冲大小之内即可。

额外的内存池通常被DBA忽略，认为该值并不是十分重要，但恰恰相反的是，该值其实同样十分重要。在 InnodB存储引擎中，对内存的管理是通过一种称为内存堆（heap）的方式进行的。**在对一些数据结构本身分配内存时，需要从额外的内存池中申请，当该区域的内存不够时，会从缓冲池中申请。**InnoDB实例会申请缓冲池（innodb buffer_pool）的空间，但是每个缓冲池中的帧缓冲（frame buffer）还有对应的缓冲控制对象（buffer control block），而且这些对象记录了诸如LRU、锁、等待等方面的信息，而这个对象的内存需要从额外内存池中申请。因此，当你申请了很大的 INnodB缓冲池时，这个值也应该相应增加。



## 2.2 master thread

通过对前一小节的学习我们已经知道，**InnoDB存储引擎的主要工作都是在一个单独的后台线程 master thread中完成的。**

master thread的线程优先级别最高。其内部由几个循环（loop）组成：**主循环（loop）、后台循环（background loop）、刷新循环（flush loop）、暂停循环（suspend loop）**。master thread会根据数据库运行的状态在loop、background loop、flush loop和 suspend loop中进行切换。

loop称为主循环，因为大多数的操作都在这个循环中，其中有两大部分操作：每秒钟的操作和每10秒的操作。伪代码如下：

```c
void master thread(){
    loop;
    for〔int i=0; i < 10; i++）{
		do thing once per second 
        sleep 1 second if necessary 
	}
    do things once per ten seconds
    goto loop;
}
```

可以看到，**loop循环通过 thread sleep来实现**，这意味着所谓的毎秒一次或每10秒一次的操作是不精确的。在负载很大的情况下可能会有延迟（delay），只能说大概在这个频率下。当然，InnodB源代码中还采用了其他的方法来尽量保证这个频率。

**每秒一次的操作包括：**

- 日志缓冲刷新到磁盘（重做日志），即使这个事务还没有提交（总是）有redo log。
- 合并插入缓冲（可能）。
- 至多刷新100个 InnodB的缓冲池中的脏页到磁盘（可能）。
- 如果当前没有用户活动，切换到 background loop（可能）。

**即使某个事务还没有提交，InnoDB存储引擎仍然会每秒将重做日志缓冲中的内容刷新到重做日志文件。**这一点是必须知道的，这可以很好地解释为什么再大的事务 commit的时间也是很快的。

合并插入缓冲（insert buffer）并不是每秒都发生。InnoDB存储引擎会判断**当前一秒内发生的 IO次数是否小于5次**，如果小于5次，InnodB认为当前的IO压力很小，可以执行合并插入缓冲的操作。

同样，刷新100个脏页也不是每秒都在发生。InnoDB存储引擎通过判断**当前缓冲池中脏页的比例（buf_get_modified_ratio_pct）是否超过了配置文件中 innodb max dirty_pages_pct这个参数（默认为90，代表90%）**，如果超过了这个阈值，IoDB存储引擎认为需要做磁盘同步操作，将100个脏页写入磁盘。

总结上述3个操作，伪代码可以进一步具体化，如下所示

```c
void master thread(){
    loop:
    for〔int i=0; i < 10; i++）{
        thread_sleep(1); 			// 睡一秒,等于每秒做以下的事情
        do log buffer flush to disk; 	// 总是将日志写入磁盘
        if (last_one_second_ios < 5)						// 如果最近一秒io次数小于5
			do merge at most 5 insert buffer				// 合并插入缓存，最多5个
		if (buf get modified ratio _ pct> innodb_max_dirty_pages_pct)		// 缓冲池脏页比例超过预设值
			do buffer pool flush 100 dirty page				// 将缓冲池中100个脏页写入磁盘
		if(no user activity)				// 空闲
			goto backgroud loop    
	}
    do things once per ten seconds;			// 10s后要做的事情
    background loop:						// 后台循环
    	do something;
    	goto loop;
}
```

**接着来看每10秒的操作，包括如下内容：**

- 刷新100个脏页或者10个到磁盘（可能）。
- 合并至多5个插入缓冲（总是）。
- **将日志缓冲刷新到磁盘（总是）。1秒和10秒都必做的事情**
- 删除无用的Undo页（总是）。
- 产生一个检查点（总是）。

**基本上除判断标准升级以外，做的事比1s多了删除undo页和产生检查点**

在以上的过程中，InnoDB存储引擎会先判断过去10秒之内磁盘的**IO操作是否小于200次**。如果是，InnoDB存储引擎认为当前有足够的磁盘 IO 操作能力，因此**将100个脏页刷新到磁盘**。接着，InnoDB存储引擎会合并插入缓冲。不同于每1秒操作时可能发生的合并插入缓冲操作，**这次的合并插入缓冲操作总会在这个阶段进行。**之后，InnoDB存储引擎会再执行一次将日志缓冲刷新到磁盘的操作，这与每秒发生的操作是一样的。

接着 InnoDB存储引擎会执行一步 full purge操作，即**删除无用的Undo页**。**对表执行update、delete这类操作时，原先的行被标记为删除，但是因为一致性读（consistent read）的关系，需要保留这些行版本的信息。**但是在 full purge过程中，InnoDB存储引擎会判断当前事务系统中已被删除的行**是否可以删除，比如有时候可能还有查询操作需要读取之前版本的Undo信息**，如果可以，InnoDB会立即将其删除。从源代码中可以发现，InnoDB存储引擎在操作 full purge时，每次最多删除20个Undo页。

然后，InnodB存储引擎会**判断缓冲池中脏页的比例**（buf_get_modified_ratio_pct），**如果有超过70%的脏页，则刷新100个脏页到磁盘；如果脏页的比例小于70%，则只需刷新10%的脏页到磁盘。**

最后，InnoDB存储引擎会产生一个**检查点**（checkpoint），InnoDB存储引擎的检查点也称为模糊检査点（fuzzy checkpoint）。InnodB存储引擎在 checkpoint时**并不会把所有缓冲池中的脏页都写入磁盘，因为这样可能会对性能产生影响，而只是将最老日志序列号**
**（oldest LSN）的页写入磁盘。**

现在，我们可以完整地把主循环（main loop）的伪代码写出来了，内容如下：

```c
void master thread(){
    loop:
    for〔int i=0; i < 10; i++）{
        thread_sleep(1); 			// 睡一秒,等于每秒做以下的事情
        do log buffer flush to disk; 	// 总是将日志写入磁盘
        if (last_one_second_ios < 5)						// 如果最近一秒io次数小于5
			do merge at most 5 insert buffer				// 合并插入缓存，最多5个
		if (buf get modified ratio _ pct> innodb_max_dirty_pages_pct)		// 缓冲池脏页比例超过预设值
			do buffer pool flush 100 dirty page				// 将缓冲池中100个脏页写入磁盘
		if(no user activity)				// 空闲
			goto backgroud loop    
	}
    if (last_ten_second_ios < 200)
		do buffer pool flush 100 dirty page;		// 10s内io总数小于200，脏页刷入磁盘
	
    do merge at most 5 insert buffer;				// 插入缓存合并，最多五条
	do log buffer flush to disk;					// redo log写入磁盘
    
    do full purge;									// 删除可以删的undo log页
	if (buf get modified ratio pct >70%)			
		do buffer pool flush 100 dirty page;		// 脏页比例大于70%，100个脏页刷盘
	else
		buffer pool flush 10 dirty page				// 否则10个脏页刷盘，总是要刷盘
	do fuzzy checkpoint;							// 产生一个检查点	
	goto loop;										// 主线程继续循环
    
    background loop:						// 后台循环
    	do something;
    	goto loop;
}
```



接着来看 background loop，若当前没有用户活动（数据库空闲时）或者数据库关闭时，就会切换到这个循环。这个循环会执行以下操作：

- 删除无用的Undo页（总是）。
- 合并20个插入缓冲（总是）。
- 跳回到主循环（总是）。
- 不断刷新100个页，直到符合条件（可能，跳转到 flush loop中完成）。

如果 flush loop中也没有什么事情可以做了，InnoDB存储引擎会切换到 suspend_loop，将 master thread挂起，等待事件的发生。若启用了 InnoDB存储引擎，却没有使用任何InnoDB存储引擎的表，那么 master thread总是处于挂起状态。

最后，master thread完整的伪代码如下；

```c
void master thread(){
    loop:
    for〔int i=0; i < 10; i++）{
        thread_sleep(1); 			// 睡一秒,等于每秒做以下的事情
        do log buffer flush to disk; 	// 总是将日志写入磁盘
        if (last_one_second_ios < 5)						// 如果最近一秒io次数小于5
			do merge at most 5 insert buffer				// 合并插入缓存，最多5个
		if (buf get modified ratio _ pct> innodb_max_dirty_pages_pct)		// 缓冲池脏页比例超过预设值
			do buffer pool flush 100 dirty page				// 将缓冲池中100个脏页写入磁盘
		if(no user activity)				// 空闲
			goto backgroud loop    
	}
    if (last_ten_second_ios < 200)
		do buffer pool flush 100 dirty page;		// 10s内io总数小于200，脏页刷入磁盘
	
    do merge at most 5 insert buffer;				// 插入缓存合并，最多五条
	do log buffer flush to disk;					// redo log写入磁盘
    
    do full purge;									// 删除可以删的undo log页
	if (buf get modified ratio pct >70%)			
		do buffer pool flush 100 dirty page;		// 脏页比例大于70%，100个脏页刷盘
	else
		buffer pool flush 10 dirty page				// 否则10个脏页刷盘，总是要刷盘
	do fuzzy checkpoint;							// 产生一个检查点	
	goto loop;										// 主线程继续循环
    
    background loop:								// 后台循环
    	do full purge; 								// 删undo 页
    	do merge 20 insert buffer; 					// 合并插入缓存
    	if not idle: 
    		goto loop;								// 不空闲，继续主循环
    	else: 
    		goto f1ush 1oop;						// 空闲，执行flush循环
    
    flush loop: 		
    do buffer pool flush 100 dirty page;		// 不断写把100个脏页写入磁盘，直到缓存脏页低于比例
    if (buf_get_modified_ratio_pct> innodb max dirty pages_pct) 
        goto flush loop 
    goto suspend loop;								// 挂起线程，等待事件
    
    suspend loop: 
    suspend_thread();		// 等待事件
	waiting event;
    goto loop;
}
```

**潜在问题**

在了解了 master thread的具体实现过程后，我们会发现 **InnoDB存储引擎对于IO其实是有限制的**，在缓冲池向磁盘刷新时其实都做了一定的硬性规定（hard coding）。在磁盘技术飞速发展的今天，**当固态磁盘出现时，这种规定在很大程度上限制了 InnoDB存储引擎对磁盘IO的性能，尤其是写入性能。**

从前面的伪代码来看，无论何时，InnodB存储引擎最多都只会刷新100个脏页到磁盘，合并20个插入缓冲。如果是在密集写的应用程序中，**每秒中可能会产生大于100个的脏页，或是产生大于20个插入缓冲，此时 master thread似乎会“忙不过来”**，或者说它总是做得很慢。即使磁盘能在1秒内处理多于100个页的写入和20个插入缓冲的合并，由于 hard coding，master thread也只会选择刷新100个脏页和合并20个插入缓冲。同时，当发生宕机需要恢复时，由于很多数据还没有刷新回磁盘，所以可能会导致恢复需要很快的时间（内存中的脏页丢失，要从日志恢复，此时数据还没更新的所以恢复快，但是要到一致性状态还有一段时间），尤其是对于insert buffer

这个问题最初是由 Google的工程师 Mark Callaghan提出的，之后 InnodB对其进行了修正并发布了补丁。InnoDB存储引擎的开发团队参考了 Google的 patch，提供了类似的方法来修正该问题。因此 InnoDB Plugin开始提供了一个参数，用来表示磁盘I的吞吐量，参数为 innodb_io_capacity，默认值为200（SSD或RAID可以更高些）。对于刷新到磁盘的数量，会按照 innodb_io_capacity的百分比来刷新相对数量的页。规则如下：

- 在合并插入缓冲时，合并插入缓冲的数量为 innodb_io_capacity数值的5%。
- 在从缓冲区刷新脏页时，刷新脏页的数量为 innodb_io_capacity。

另一个问题是参数 innodb_max_dirty_pages_pct的默认值，在 MySQL5.1版本之前（包括5.1），该值的默认值为90，意味着**脏页占缓冲池的90%。但是该值“太大”了**，因为你会发现，InnoDB存储引擎在每1秒刷新缓冲池和 flush loop时，会判断这个值，如果大于innodb_max_dirty_pages_pct，才刷新100个脏页。因此，**如果你有很大的内存或你的数据库服务器的压力很大，这时刷新脏页的速度反而可能会降低。**同样，在数据库的恢复阶段可能需要更多的时间。 从 InnoDB Plugin开始，**innodb max_dirty_pages_pc默认值变为了75，和 Google测试的80比较接近。**这样既可以**加快刷新脏页的频率**，也能保证磁盘IO的负载。

还有一个**自适应刷新参数（innodb adaptive flushing）**，该值影响每1秒刷新脏页的数量，即即使脏页比比例小，也会自适应的更新一部分。



## 2.3 关键特性

InnoDB存储引擎的关键特性包括**插入缓冲、两次写（double write）、自适应哈希索引（adaptive hash index）**。这些特性为 InnoDB存储引擎带来了更好的性能和更高的可靠性。

### 2.3.1 插入缓冲

我们知道，主键是行唯一的标识符，在应用程序中行记录的插入顺序是按照主键递增的顺序进行插入的。因此，插入聚集索引一般是顺序的，不需要磁盘的随机读取。比如说我们按下列SQL定义的表。

```sql
create table t( 
    id int auto increment, 
    name varchar (30),
    primary key (id)
);
```

id列是自增长的，这意味着当执行插入操作时，id列会自动增长，页中的行记录按id执行顺序存放。一般情况下，不需要随机读取另一页执行记录的存放。因此，在这样的情况下，插入操作一般很快就能完成。但是，不可能每张表上只有一个聚集索引，在更多的情况下，一张表上有多个非聚集的辅助索引（secondary index）。比如，我们还需要按照name这个字段进行查找，并且name这个字段不是唯一的。即，表是按如下的SQL语句定义的：即对name创建我们说的普通索引

```sql
create table t( 
    id int auto increment, 
    name varchar (30),
    primary key (id),
    key(name)
);
```

这样的情况下产生了**一个非聚集的并且不是唯一的索引。**在进行插入操作时，**数据页的存放还是按主键id的执行顺序存放**，**但是对于非聚集索引页，叶子节点的插入不再是顺序的了。**这时就需要离散地访问非聚集索引页，插入性能在这里变低了。然而这并不是这个name字段上索引的错误，因为B+树的特性决定了非聚集索引插入的离散性

InnoDB存储引擎开创性地设计了插入缓冲，**对于非聚集索引的插入或更新操作**，不是每一次直接插入索引页中。而是**先判断插入的非聚集索引页是否在缓冲池中**。**如果在，则直接插入；如果不在，则先放入一个插入缓冲区中**，好似欺骗数据库这个非聚集的索引已经插到叶子节点了，**然后再以一定的频率执行插入缓冲和非聚集索引页子节点的合并操作，这时通常能将多个插入合并到一个操作中（因为在一个索引页中），这就大大提高了对非聚集索引执行插入和修改操作的性能。**

插入缓冲的使用需要满足以下两个条件：

- 索引是辅助索引。
- 索引不是唯一的。

当满足以上两个条件时，InnoDB存储引擎会使用插入缓冲，这样就能提高性能了。不过考虑一种情况，应用程序执行大量的插入和更新操作，这些操作都涉及了不唯一的非聚集索引，**如果在这个过程中数据库发生了宕机，这时候会有大量的插入缓冲并没有合并到实际的非聚集索引中。**如果是这样，**恢复可能需要很长的时间**，极端情况下甚至需要几个小时来执行合并恢复操作。

辅助索引不能是唯一的，因为在把它插入到插入缓冲时，我们并不去查找索引页的情况。如果去查找肯定又会出现离散读的情况，插入缓冲就失去了意义。



上面描述有些抽象，对于**为什么会有insert buffer,insert buffer能帮我们解决什么这个问题**，我们可以用下面例子说明

我们去图书馆还书，对应图书馆来说，他是做了insert(增加)操作，管理员在1小时内接受了100本书，这时候他有2种做法把还回来的书归位到书架上

1）每还回来一本书，根据这本书的编码（书柜区-排-号）把书送回架上

2）暂时不做归位操作，先放到前台上，等不忙的时候，再把这些书按照书柜区-排-号先排好，然后一次性归位

用方法1，管理员需要进出（IO）藏书区100次，不停的登高爬低完成图书归位操作，累死累活，效率很差。

用方法2，管理员只需要进出（IO）藏书区1次，对同一个位置的书，不管多少，都只要爬一次楼梯，大大减轻了管理员的工作量。

所以图书馆都是按照方法2来做还书动作的。但是你要说，我的图书馆就20本书，1个0.5米的架子，方法2和1管理起来都很方便，这种情况不在我们讨论的范围。当数据量非常小的时候，就不存在效率问题了。

 

再说第二个问题，**有什么限制：“只对于非聚集索引（非唯一）的插入和更新有效”**

还是用还书的例子来说，还一本书A到图书馆，假设这个图书馆非常个性，每种书只有一本，那么这个时候，管理员要判断一下这本书是不是唯一的，他在柜台上是看不到的，必须爬到指定位置去确认，这个过程其实已经产生了一次IO操作，相当于没有节省任何操作。

**所以这个buffer只能处理非唯一的插入，不要求判断是否唯一。**聚集索引就不用说了，它肯定是唯一的，mysql现在还只能通过主键聚集。

 

目前插入缓冲存在一个问题是，在**写密集的情况下，插入缓冲会占用过多的缓冲池内存，默认情况下最大可以占用 *1/2* 的缓冲池内存**。以下是 InnoDB存储引擎源代码中对 Insert buffer的初始化操作：

![image-20201010001046718](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201010001046718.png)

其实插入缓冲占用太多空间了，会有一定问题，简单来说，可以修改IBUF_POOL SIZE PER MAX SIZE就可以对插入缓冲的大小进行控制，例如，将 IBUF POOL SIZE PER MAX_SIZE改为3，则最大只能使用1/3的缓冲池内存。



### 2.3.2 两次写

如果说**插入缓冲带给 InnodB存储引擎的是性能，那么两次写带给 InnoDB存储引擎的是数据的可靠性。**当数据库宕机时，可能发生数据库正在写一个页面，而这个页只写了部分（比如16K的页，只写前4K的页）的情况，我们称之为**部分写失效（partial page write）**
在 InnoDB存储引擎未使用 double write技术前，曾出现过因为部分写失效而导致数据丢失的情况。

有人也许会想，如果发生写失效，可以通过重做日志进行恢复。这是一个办法。但是必须凊楚的是，重做日志中记录的是对页的物理操作，如偏移量800，写'aaaa'记录。**如果这个页本身已经损坏，再对其进行重做是没有意义的。（该页或者说文件损坏，不能存储数据，也就重做没有意义）**这就是说，在应用（apply）重做日志前，我们需要一个页的副本，当写入失效发生时，先通过页的副本来还原该页，再进行重做，这就是 doublewrite。InnoDB存储引擎 doublewrite的体系架构如下图所示

![image-20201010002213788](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201010002213788.png)

doublewrite由两部分组成：一部分是内存中的 doublewrite buffer，大小为2MB；另部分是物理磁盘上共享表空间中连续的128个页，即两个区（extent），大小同样为2MB。

**当缓冲池的脏页刷新时，并不直接写磁盘，而是会通过 memcpy函数将脏页先拷贝到内存中的 doublewrite buffer，之后通过 doublewrite buffer再分两次，每次写入1MB到共享表空间的物理磁盘上，然后马上调用sync函数，同步磁盘，避免缓冲写带来的问题。**在这个过程中，因为 doublewrite页是连续的，因此这个过程是顺序写的，开销并不是很大。在完成doublewrite页的写入后，再将 doublewrite buffer中的页写入各个表空间文件中，此时的写入则是离散的。可以通过以下命令观察到 doublewrite运行的情况

![image-20201010004328762](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201010004328762.png)

可以看到，doublewrite一共写了6325194个页，但实际的写入次数为100399，基本上符合64：1（2份，128页）。如果发现你的系统在高峰时 Innodb_dblwr_pages_written：Innodb_dblwr writes远小于64：1，那么说明你的系统写入压力并不是很高。

如果操作系统在将页写入磁盘的过程中崩溃了，在恢复过程中，InnoDe存储引擎可以从共享表空间中的 doublewrite中找到该页的一个副本，将其拷贝到表空间文件，再应用重做日志。下面显示了由 doublewrite进行恢复的一种情况：

![image-20201010005300660](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201010005300660.png)

参数 skip_innodb_doublewrite可以棼止使用两次写功能，这时可能会发生前面提及的写失效问题。不过，如果你有多台从服务器（slave server），需要提供较快的性能（如slave上做的是RAID0），也许启用这个参数是一个办法。不过，在需要提供数据高可靠性的主服务器（master server）上，任何时候我们都应确保开启两次写功能。



### 2.3.3 自适应哈希

哈希（hash）是一种非常快的查找方法，**一般情况下查找的时间复杂度为O（1）**。常用于连接（join）操作，如 SQL Server和 Oracle中的哈希连接（hash join）。但是SQL Server和 Oracle等**常见的数据库并不支持哈希索引（hash index）**。MySQLI的Heap存储引擎默认的索引类型为哈希，而 **InnoDB存储引擎提出了另一种实现方法，自适应哈希索引（adaptive hash index）。**

InnoDB存储引擎会监控对表上索引的查找，如果观察到建立哈希索引可以带来速度的提升，则建立哈希索引，所以称之为自适应（adaptive）的。**自适应哈希索引通过缓冲池的B+树构造而来，因此建立的速度很快。而且不需要将整个表都建哈希索引，InnoDB存储引擎会自动根据访问的频率和模式来为某些页建立哈希索引。**

根据 InnoDB的官方文档显示，启用自适应哈希索引后，读取和写入速度可以提高2倍；对于辅助索引的连接操作，性能可以提高5倍。在我看来，自适应哈希索引是非常好的优化模式，其设计思想是数据库自优化（self-tuning），即无需DBA对数据库进行调整。通过命令 SHOW ENGINE INNODB STATUS可以看到当前自适应哈希索引的使用状况，如下所示：

```sql
SHOW ENGINE INNODB STATUS
```

![image-20201010005732276](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201010005732276.png)

现在可以看到自适应哈希索引的使用信息了，包括自适应哈希索引的大小、使用情况每秒使用自适应哈希索引搜索的情况。值得注意的是，**哈希索引只能用来搜索等值的查询**，如 `select* from table where index col='xxx'`，而对于其他査找类型，**如范围查找，是不能使用的。**因此，这里出现了non-hash searches/s的情况。用 hash searches:non-hash searches命令可以大概了解使用哈希索引后的效率。

由于自适应哈希索引是由 InnoDB存储引擎控制的，所以这里的信息只供我们参考。不过我们可以通过参数innodb_adaptive_hash_index来禁用或启动此特性，默认为开启。



## 2.4 启动、关闭与恢复

InnodB存储引擎是 MySQL的存储引擎之一，因此 InnodB存储引擎的启动和关闭更准确地是指在 MySQL实例的启动过程中对 InnoDB表存储引擎的处理过程。

在关闭时，参数 **innodb_fast_shutdown**影响着表的存储引擎为 InnoDB的行为。该参数可取值为0、1、2。

- 0代表当 MySQL关闭时，InnoDB需要完成所有的 full purge和 merge insert buffer操作，这会需要一些时间，有时甚至需要几个小时来完成。如果在做 InnodB plugin升级，通常需要将这个参数调为0，然后再关闭数据库。
- 1是该参数的默认值，表示不需要完成上述的 full purge和 merge insert buffer操作，但是在缓冲池的一些数据脏页还是会刷新到磁盘。
- 2表示不完成 full purge和 merge insert buffer操作，也不将缓冲池中的数据脏页写回磁盘，而是将日志都写入日志文件。这样不会有任何事务会丢失，但是 MySQL数据库下次启动时，会执行恢复操作（recovery）。
  当正常关闭 My SQL数据库时，下一次启动应该会很正常。但是，如果没有正常地关闭数据库，如用kill令关闭数据库，在 MySQL数据库运行过程中重启了服务器，或者在关闭数据库时将参数 innodb fast shutdown设为了2，My SQL数据库下次启动时都会对InnoDB存储引擎的表执行恢复操作。

即

```
0 ----->  删除undo页，合并插入缓存
1 ----->  缓冲池一些脏页刷入磁盘
2 ----->  写入日志，下次启动时再恢复
```

参数 **innodb_force_recovery**影响了整个 InnodB存储引擎的恢复状况。该值默认为0，表示当需要恢复时执行所有的恢复操作。当不能进行有效恢复时，如数据页发生了 corruption，MySQL数据库可能会宕机，并把错误写入错误日志中。

但是，在某些情况下，我们可能并不需要执行完整的恢复操作，我们自己知道如何进行恢复。比如正在对一个表执行 alter table操作，这时意外发生了，数据库重启时会对InnoDB表执行回滚操作。对于一个大表，这需要很长时间，甚至可能是几个小时。这时我们可以自行进行恢复，例如可以把表删除，从备份中重新将数据导入表中，这些操作的速度可能要远远快于回滚操作。

innodb_force_recovery还可以设置为6个非零值：1~6。大的数字包含了前面所有小数字的影响，具体情况如下。

- 1（SRV_FORCE_IGNORE_CORRUPT）：忽略检查到的 corrupt页。
- 2（SRV_FORCE_NO_BACKGROUND）：阻止主线程的运行，如主线程需要执行full purge操作，会导致 crash。
- 3（SRV_FORCE_NO_TRX_UNDO）：不执行事务回滚操作
- 4（SRV_FORCE_NO_IBUF_MERGE）：不执行插入缓冲的合并操作。
- 5（SRV_FORCE_NO_UNDO_LOG_SCAN）：不查看撤销日志（Undo log），InnoDB存储引擎会将未提交的事务视为已提交。
- 6（SRV_FORCE_NO_LOG_REDO）：不执行前滚的操作。

**需要注意的是，当设置参数 innodb_force_recovery大于0后，可以对表进行 selec create、drop操作，但 insert、update或者 delete这类操作是不允许的。**

我们来做个实验，模拟故障的发生。在第一会话中，对一张接近100W行的 InnodB存储引擎表执行更新操作，但是完成后不要马上提交：

![image-20201010132711495](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201010132711495.png)

start transaction语句开启了事务，同时防止了自动提交的发生，update操作则会产生大量的回滚日志。这时，我们人为地kill掉 My SQL数据库服务器。

![image-20201010132741291](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201010132741291.png)

通过kill命令，我们人为地模拟了一次数据库宕机故障，当 MySQL数据库下次启动时会对 update的这个事务执行回滚操作，而这些信息都会记录在错误日志文件中，默认后缀名为err。如果查看错误日志文件，可得到如下结果：

![image-20201010132831794](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201010132831794.png)

可以看到，如果采用默认的策略，即把 innodb_force_recovery设为0，InnoDB会在每次启动后对发生问题的表执行恢复操作，通过错误日志文件，可知这次回滚操作需要回滚8867280行记录，总共耗时约9分多钟。

我们做再做一次同样的测试，只不过在启动 MySQL数据库前将参数 innodb_force_recovery设为3，然后观察 InnoDB存储引擎是否还会执行回滚操作（应该不是update），査看错误日志文件可看到：

![image-20201010133109853](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201010133109853.png)

这里出现了“！！！”，InnoDB警告你已经将 innodb_force_recovery设置为3，不会进行undo的回滚操作了。因此数据库很快启动完成，但是你应该很小心当前数据库的状态，并仔细确认是否不需要回滚操作。





## 2.5  InnoDB Plugin=新版本的InnoDB存储引擎

MySQL5.1这个版本的一个很大的变动是采用了插件式的架构。通过分析源代码会发现，每毎个存储引擎是通过继承一个 handler的C++基类（之前的版本大多是通过函数指针来实现）。

这样设计的好处是，现在所有的存储引擎都是真正的插件式了。**在以前，如果发现一个 InnoDB存储引擎的Bug**，你能做的是**只能等待 MySQL新版本的发布**，InnoDB公司本身对此只能通过补丁的形式来解决，你还需要**重新编译一次 MySQL**才行。**现在**，你可以得到个新版本的 InnoDB存储引擎，用来替代有Bug的旧引擎。这样，当有重大问题时，不用等待 MySQL的新版本，**只要相应的存储引擎提供商发布新版本即可。**