# ThreadLocal类的使用与问题

## ThreadLocal概述

从Java官方文档中的描述：ThreadLocal类用来提供线程内部的局部变量。这种变量在多线程环境下访问（通过get和set方法访问）时能保证各个线程的变量相对独立于其他线程内的变量。**Threadloca实例通常来说都是private static修饰的**，用于关联线程和线程上下文。

我们可以得知 ThreadLocal的作用是：提供线程内的局部变量，不同的线程之间不会相互干扰，这种变量在线程的生命周明内起作用，**减少同一个线程内多个函数或组件之间一些公共变量传递的复杂度。（比如Spring里面的事务控制）**

总结：主要是在**线程并发、传递数据、线程隔离**的场景使用

1、线程并发：在多线程并发的场景下

2、传递数据：我们可以通过ThreadLocal在同一线程，不同组件中传递公共变量（保存每个线程的数据在需要的地方可以直接获取，避免参数直接传递带来的代码耦合问题，类似 JavaWeb中的Session、Request等域对象）

3、线程隔离：每个线程的变量都是独立的，不会相互影响（各线程之间的数据相互隔离却又具备并发性，避免同步方式带来的性能损失）



## 基本使用

### 常用方法

在使用之前我们先来认识几个 ThreadLocal的常用方法

| 方法声明                 | 描述                       |
| ------------------------ | -------------------------- |
| ThreadLocal()            | 创建ThreadLocal对象        |
| public void set(T value) | 设置当前线程绑定的局部变量 |
| public T get()           | 取当前线程绑定的局部变量   |
| public void remove()     | 移除当前线程绑定的局部变量 |

我们来看下面这个案例，感受一下 ThreadLocal线程隔离的特点

```java
/**
 * @author Lin
 * @Description 需求：线程隔离
 * 在多线程并发的场景下，每个线程中的变量都是相互独立
 * 线程A：设置（变量1）获取（变量1）
 * 线程B：设置（变量2）获取（变量2）
 * @create 2020-06-12 18:49
 */
public class ThreadLocalDemo01 {
    // 变量
    private String content;
    ThreadLocal<String> tl = new ThreadLocal<>();

    public String getContent() {
//        return content;
        return tl.get();
    }

    public void setContent(String content) {
//        this.content = content;
        // 将传入的content绑定到当前线程
        tl.set(content);
    }

    public static void main(String[] args) {
        ThreadLocalDemo01 demo = new ThreadLocalDemo01();

        for (int i = 0; i < 5; i++) {
            new Thread(() -> {
                // 多线程下，存一个变量，再取出
                demo.setContent(Thread.currentThread().getName() + "的数据");
                System.out.println("--------------------------");
                System.out.println(Thread.currentThread().getName() + "------->" + demo.getContent());
            }, "线程" + i).start();
        }
    }
}

```

结果：拿出的数据都对应了当前线程的存入的数据，但是代码语句和线程切换依旧是不可控的执行的

![image-20200612203137524](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200612203137524.png)

事实上，就是将传入的字符串保存在了该ThreadLocal的对象中的map中，待会从源码说明get和set是怎么实现的。



### synchronized和ThreadLocal区别

虽然ThreadLocal模式与Synchronized关键字都用于**处理多线程并发访问变量的问题**, 不过两者处理问题的角度和思路不同，ThreadLocal相当于用空间换取时间，将线程-变量值作为key-value存入其map中，即放的是需要并发处理的变量的副本。

|        | synchronized                                       | ThreadLocal                                                  |
| ------ | -------------------------------------------------- | ------------------------------------------------------------ |
| 原理   | synchronized采用加锁机制实现共享变量的并发访问处理 | Threadlocal采用以**空间换时间**的方式，为每一个线程都提供了一份变量的副本，从而实现同访问而相不干扰 |
| 衡量点 | 多个线程之间访问资源的同步，性能不如ThreadLocal高  | 多线程中让每个线程之间的数据相互隔离，但代码并发执行，性能高 |

上述线程隔离的案例也可以用synchronized加锁进行同步实现

```java
public class ThreadLocalDemo01 {
    // 变量
    private String content;
//    ThreadLocal<String> tl = new ThreadLocal<>();

    public String getContent() {
        return content;
//        return tl.get();
    }

    public void setContent(String content) {
        this.content = content;
        // 将传入的content绑定到当前线程
//        tl.set(content);
    }

    public static void main(String[] args) {
        ThreadLocalDemo01 demo = new ThreadLocalDemo01();

        for (int i = 0; i < 5; i++) {
            new Thread(() -> {
                // 多线程下，存一个变量，再取出
                synchronized (demo){
                    demo.setContent(Thread.currentThread().getName() + "的数据");
                    System.out.println("--------------------------");
                    System.out.println(Thread.currentThread().getName() + "------->" + demo.getContent());
                }
            }, "线程" + i).start();
        }
    }
}
```

结果：可以看到打印分割线也是按严格同步进行的

![image-20200612205650654](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200612205650654.png)

总结：在刚刚的案例中，虽然使用 ThreadLocal和 synchronized都能解决问题，但是使用 ThreadLocal 更为合适，因为这样可以使程序拥有更高的并发性

## 运用场景

通过以上的介绍，我们已经基本了解 ThreadLocal的特点。但是它具体是运用在什么场景中呢？接下来让我们看一个案例：事务操作。

### 转账案例

这里我们先构建一个简单的转账场景：有一个数据表 account，里面有两个用户 Jack 和 Rose，用户 Jack 给用户 Rose 转账

![image-20200612214309721](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200612214309721.png)

案例的实现主要用mysql数据库，JDBC和C3P0框架。以下是详细代码

mysql语句

```mysql
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `money` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB CHARSET=utf8

INSERT INTO `account`(NAME,money) VALUES('Jack',1000);
INSERT INTO `account`(NAME,money) VALUES('Rose',0);
```

导入c3p0、mysql-connector-java、mchange-commons-java依赖

```xml
	<dependency>
      <groupId>c3p0</groupId>
      <artifactId>c3p0</artifactId>
      <version>0.9.1.2</version>
    </dependency>
    <dependency>
      <groupId>mysql</groupId>
      <artifactId>mysql-connector-java</artifactId>
      <version>5.1.8</version>
    </dependency>
	<dependency>
      <groupId>com.mchange</groupId>
      <artifactId>mchange-commons-java</artifactId>
      <version>0.2.12</version>
    </dependency>
```

仿造Controller-Service-Dao的三层架构模拟转账

1、Jdbc连接池工具类以及c3p0-config.xml配置（配置文件必须叫这个）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<c3p0-config>
<!--    使用默认的配置读取连接池对象-->
    <default-config>
<!--        连接参数-->
        <property name="driverClass">com.mysql.jdbc.Driver</property>
        <property name="jdbcUrl">jdbc:mysql://localhost:3306/juc</property>
        <property name="user">root</property>
        <property name="password">qaz12345</property>
<!--        连接池参数-->
        <property name="initialPoolSize">5</property>
        <property name="maxPoolSize">10</property>
        <property name="checkoutTimeout">3000</property>
    </default-config>
</c3p0-config>
```

```java
public class JdbcUtils {
    //c3p0数据库连接池对象属性
    private static final ComboPooledDataSource ds = new ComboPooledDataSource();
    // 获取连接
    public static Connection getConnection() throws SQLException{
        return ds.getConnection();
    }
    //释放资源
    public static void release(AutoCloseable ... ios){
        for(AutoCloseable io:ios){
            if(io!=null){
                try{
                    io.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }
    // 提交
    public static void commitAndClose(Connection conn){
        try{
            if(conn != null){
                // 提交事务
                conn.commit();
                // 释放连接
                conn.close();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    // 回滚
    public static void rollbackAndClose(Connection conn){
        try{
            if(conn!=null){
                // 回滚事务
                conn.rollback();
                // 释放连接
                conn.close();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

2、Dao层使用 JDBC进行数据查询（PreparedStatement）

```java
public class AccountDao {
    /**
     * 转出操作
     */
    public void out(String outUser, int money) throws SQLException {
        String sql = "update account set money = money - ? where name = ?";

        Connection connection = JdbcUtils.getConnection();
        PreparedStatement pstm = connection.prepareStatement(sql);
        pstm.setInt(1, money);
        pstm.setString(2, outUser);
        pstm.executeUpdate();

        JdbcUtils.release(pstm, connection);
    }

    /**
     * 转入操作
     */
    public void in(String inUser, int money) throws SQLException {
        String sql = "update account set money = money + ? where name = ?";

        Connection connection = JdbcUtils.getConnection();
        PreparedStatement pstm = connection.prepareStatement(sql);
        pstm.setInt(1, money);
        pstm.setString(2, inUser);
        pstm.executeUpdate();

        JdbcUtils.release(pstm, connection);
    }

}
```

3、service层进行转账，使用JDBC开启事务控制

| Connection接口方法        | 作用                             |
| ------------------------- | -------------------------------- |
| void setAutoCommit(false) | 禁用事务自动提交（改为手动提交） |
| void commit()             | 提交事务                         |
| void rollback()           | 回滚事务                         |

```java
public class AccountService {
    public boolean transfer(String outUser, String inUser, int money){
        AccountDao dao = new AccountDao();
        Connection connection = null;

        try{
            // 开启事务
            connection = JdbcUtils.getConnection();
            connection.setAutoCommit(false);
            //转出
            dao.out(outUser,money);
            //转入
            dao.in(inUser,money);

            // 成功提交
            JdbcUtils.commitAndClose(connection);
        } catch (SQLException e) {
            e.printStackTrace();
            //失败回滚
            JdbcUtils.rollbackAndClose(connection);
            return false;
        }
        return true;
    }
}
```

4、Controller层进行模拟数据传入调用即可

```java
public class AccountSWeb {
    public static void main(String[] args) {
        //模拟转账：Jack给Rose转账100
        String outUser = "Jack";
        String inUser = "Rose";
        int money = 100;

        AccountService service = new AccountService();
        boolean result = service.transfer(outUser,inUser,money);

        if(result==false){
            System.out.println("转账失败");
        }else{
            System.out.println("转账成功");
        }
    }
}
```

但是但是，**上述代码并不能保证dao层和service层的connection是同一个，因此即使发生错误依旧不能回滚**，并发环境下，必须保证所有的操作在一个事务中案例中使用的连接必须是同一个：service层开启事务的 connection需要跟dao层访问数据库的 connection保持一致，否则线程并发情况下，每个线程会能操作各自的 connection。

即需要保证：

1. service层和dao层的Connection对象是同一个
2. 每个线程的Connection对象即使发生线程切换，也必须保持一致（线程隔离）

**常规的解决方案：**

1. **传参+加锁：**

   将service 的Connection对象传入dao层即可，必须加锁，否则赋值那里可能多个线程操作一个Connection对象，再对应修改下dao层的代码即可

   ```java
   public class AccountService {
       public boolean transfer(String outUser, String inUser, int money) {
           AccountDao dao = new AccountDao();
           Connection connection = null;
   
           try {
               synchronized (AccountService.class) {
                   // 开启事务
                   connection = JdbcUtils.getConnection();
                   connection.setAutoCommit(false);
                   //转出
                   dao.out(outUser, money, connection);
                   //转入
                   dao.in(inUser, money, connection);
   
                   // 成功提交
                   JdbcUtils.commitAndClose(connection);
               }
   
           } catch (SQLException e) {
               e.printStackTrace();
               //失败回滚
               JdbcUtils.rollbackAndClose(connection);
               return false;
           }
           return true;
       }
   }
   
   ```

   弊端：

   - 提高代码的耦合度（传参）
   - 降低了程序的性能（加锁失去并发性）

2. **使用ThreadLocal**

   1、直接获取当前线程绑定的连接对象

   2、如果连接对象是空的

   - 再去连接池中获取连接
   - 将连接对家跟当前线程进行绑

   ![image-20200613023926759](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200613023926759.png)

   只需要修改JdbcUtils即可，因为Connection对象是从这里拿到的，当然这并没有完，因为如果不释放对该Connection对象释放连接，会造成**内存泄漏**，怎么解决，放到下文继续阐述

   ```java
   public class JdbcUtils {
       //c3p0数据库连接池对象属性
       private static final ComboPooledDataSource ds = new ComboPooledDataSource();
       // 获取连接，其他方法不变
       static ThreadLocal<Connection> tl = new ThreadLocal<>();
   
       public static Connection getConnection() throws SQLException{
           Connection connection = tl.get();
           if(connection == null){
               connection = ds.getConnection();
               tl.set(connection);
           }
           return connection;
       }
   }
   ```

   从上述的案例中我们可以看到，在一些特定场景下，Threadlocal方案有两个突出的优势:

   **1.传递数据：**保存每个线程绑定的数据，在需要的地方可以直接获取，避免参数直接传递带来的代码耦合问题

   **2.线程隔离：**各线程之间的数据相互隔离却又具备并发性，避免同步方式带来的性能损失



## ThreadLocal的内部结构

通过以上的学习，我们对 Threadloca的作用有了一定的认识。现在我们一起来看一下 ThreadLoca的内部结构，探究它能够实现线程数据隔离的原理。

### 常见的误区

如果我们不去看源代码的话，可能会猜测 Threadlocal是这样子设计的：每个 Threadlocal都创建一Map，然后用线程作为Map的key，要存储的局部变量作为Map的 value，这样就能达到各个线程的局部变量隔离的效果。**这是最简单的设计方法，JDK最早期的 ThreadLocal确实是这样设计的，但现在早已不是了。**

![image-20200613122535545](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200613122535545.png)

### 现在的设计

但是，JDK后面优化了设计方案，在JDK8中 Threadlocal 的设计是：每个 Thread维护一个ThreadLocaIMap，这个Map的key是 ThreadLocal实例本身，value才是真正要存储的值 Object

具体的过程是这样的

1. 每个 Thread线程内部都有一个Map（ThreadLocal.ThreadLocalMap）
2. Map里面存储 Threadlocal对象（key）和线程的变量副本（value）
3. Thread内部的Map是由 ThreadLocal维护的，由 ThreadLocal 负责向map获取和设置线程的变量值。
4. 对于不同的线程，每次获取副本值时，别的线程并不能获取到当前线程的副本值，形成了副本的隔离，互不干扰。

![image-20200613123409659](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200613123409659.png)

看到这里

![image-20200613125651431](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200613125651431.png)

JDK8的设计方案的好处——节省内存开销：

1. 每个Map存储的Entry数量变少（不是所有线程都会用到ThreadLocal，对于单个Map而言，Key-Value减少了，也减少了哈希冲突）
2. 当 Thread销毁的时候，ThreadLocalMap也会随之销毁，减少内存的使用。（原先的Thread失效了，而Map依旧存着该key-value）



## ThreadLocal核心方法源码

| 方法声明                 | 描述                       |
| ------------------------ | -------------------------- |
| ThreadLocal()            | 创建ThreadLocal对象        |
| public void set(T value) | 设置当前线程绑定的局部变量 |
| public T get()           | 取当前线程绑定的局部变量   |
| public void remove()     | 移除当前线程绑定的局部变量 |

以下是这4个方法的详细源码分析（为了保证思路清晰，ThreadLocalMap部分暂时不展开，下一个知识点详解）

默认空参构造方法内部没有任何语句，没必要讲了

### set方法

JDK1.8源码如下	

```java
	/**
	* 设置当前线程的ThreadLocal值
	*/
	public void set(T value) {
    	// 获取当前线程对象
        Thread t = Thread.currentThread();
    	// 获取此线程对象中维护的ThreadLocalMap对象
        ThreadLocalMap map = getMap(t);
    	// 判断map是否存在
        if (map != null)
            // 存在则调用map.set设置该实体entry
            map.set(this, value);
        else
            // 1.当前线程Thread 不存在ThreadLocalMap对象，则调用create对ThreadLocalMap对象初始化
            // 2.并将t（当前线程）的ThreadLocal和value作为第一个Entry存入ThreadLocalMap中
            createMap(t, value);
    }
	
	/**
	* 获取当前线程Thread对象t对应的ThreadLocalMap
	*/
	ThreadLocalMap getMap(Thread t) {
        return t.threadLocals;
    }

	/**
	*	创建当前线程Thread对应维护的ThreadLocalMap
	*/
	void createMap(Thread t, T firstValue) {
        // this是调用该方法的ThreadLocal对象
        t.threadLocals = new ThreadLocalMap(this, firstValue);
    }
```

**代码执行流程**

1. 首先获取当前线程，并根据当前线程获取一个Map 
2. 如果获取的Map不为空，则将参数设置到Map中（当前 Threadlocal的引用作为key）（这里调用了 ThreadLocalMap的set方法）
3. 如果Map为空，则给该线程创建Map，并把该Entry作为第一个数据存入Map中（这里调用了 ThreadLocalMap的构造方法）



### get方法

JDK1.8源码如下

```java
	 /**
        *	返回当前线程中缓存ThreadLocal对象
        *	如果当前线程没有次ThreadLocal变量
        *	则它会通过调用{@link #initialValue} 方法进行初始化值
        */
	public T get() {
        // 获取当前线程对象
        Thread t = Thread.currentThread();
        // 获取此线程对象中维护的ThreadLocalMap对象
        ThreadLocalMap map = getMap(t);
        // 如果此map存在
        if (map != null) {
            // 以当前的ThreadLocal 为key，调用getEntry得到该键值对Entry对象
            ThreadLocalMap.Entry e = map.getEntry(this);
            // 若能从Map查到对应Entry
            if (e != null) {
               	// 获取键值对对象对应的value值
                // 即为我们一开始存入此线程的对应ThreadLocal在ThreadLocalMap的值
                @SuppressWarnings("unchecked")
                T result = (T)e.value;
                return result;
            }
        }
        // 初始化：有以下两种情况执行下面的代码
        // 1、map不存在，表示此线程没有创建ThreadLocalMap对象
        // 2、map存在，但是没有与当前ThreadLocal关联的entry
        return setInitialValue();
    }
	
	/**
	* 初始化
	*/
	private T setInitialValue() {
        // 调用initialValue获取初始化的值
        // 此方法可以被子类重写，如果不重写返回null
        T value = initialValue();
        // 获取当前线程对象以及对应ThreadLocalMap
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
        // 判断map是否存在
        if (map != null)
            // 存在则调用map.set设置此实体entry
            map.set(this, value);
        else
            // 1.当前线程Thread 不存在ThreadLocalMap对象，则调用create对ThreadLocalMap对象初始化
            // 2.并将t（当前线程）的ThreadLocal和value作为第一个Entry存入ThreadLocalMap中
            createMap(t, value);
        // 返回设置的值value
        return value;
    }
```

**代码执行流程**

1. 首先获取当前线程根据当前线程获取一个Map
2. 如果获取的Map不为空，则在Map中以 ThreadLocall的引用作为key来在Map中获取对应的 Entry e，否则转4
3. 如果e不为null，则返回 e.value，否则转到4
4. Map为空或者e为空，则通过 initialvalue 函数获取初始值value，然后用 ThreadLoca的引用和value作为firstKey和 firstvalue创建一个新的Map

**总结：先获取当前线程的 ThreadLocalMap变量，如果存在则返回值，不存在则创建并返回初始值**

### remove方法

JDK1.8源码如下

```java
	/**
	* 删除当前线程中保存的 Threadlocal对应的实体 entry
	*/
	public void remove() {
        //获取当前线程对象中维护的 ThreadLocalMap对象
         ThreadLocalMap m = getMap(Thread.currentThread());
        // 如果此map存在
         if (m != null)
             // 存在则调用map.remove
             // 以当前 Threadlocal为key删除对应的实体 entry
             m.remove(this);
     }
```

代码执行流程：

1. 首先获取当前线程，并根据当前线程获取一个Map 
2. 如果获取的Map不为空，则移除当前 ThreadLocal对象对应的 entry



### initialValue方法

上面提到get方法如果map不存在或者Map中该ThreadLocal不存在，就会调用setInitialValue存一个初始化的值，这个初始化的值在不重写的情况下为null，代码如下

```java
	/**
     * 返回当前线程对应的 ThreadLocal的初始值
     * 此方法的第一次调用发生在当线程通过get方法访间此线程的 Theadloccal值时
     * 除非线程先调用了set方法，在这种情况下，initialvalue才不会被这个线程调用
     * 通常情况下，每个线程最多调用一次这个方法。
     * 
     * 这个方法仅仅简单的返回null
     * 如果程序员想 ThreadLocal线程局部变量有一个除null以外的初始值必须通过子类继承Threadlocal的方式去重写此方法
     * 通常，可以通过匿名内部类的方式实现
     */

	protected T initialValue() {
        return null;
    }
```

此方法的作用是返回该线程局部变量的初始值

1. 这个方法是一个延迟调用方法，从面的代码我们得知，在set方法还未调用而先调用了get方法时才执行，并且仅执行1次
2. 这个方法缺省实现直接返回一个null
3. 如果想要一个除null之外的初始值，可以重写此方法。（备注：该方法是一个 protected的方法，显然是为了让子类覆盖而设计的）



## ThreadLocalMap源码分析

在分析 ThreadLocal方法的时候，我们了解到heac的操作实际上是围绕 ThreadLocalMap展开的adLocalMap的源码相对比较复杂，我们从以下三个方面进行讨论。

### 基本结构

ThreadLocalMap是 Threadlocal 的静态内部类，没有实现Map接口，用独立的方式实现了Map的功能，其内部的Entry也是独立实现。

实际上ThreadLocal的get，set，remove基本也是调用ThreadLocalMap的方法

![image-20200613200611602](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200613200611602.png)



**1、成员变量**

```java
		// 初始容量，必须为2的整次幂
		private static final int INITIAL_CAPACITY = 16;

		// 存放数据的table，Entry类在下面分析
        private Entry[] table;

		// 数组里面 Entry对象的个数，可以用于判断 table当前使用量是否超过阈值
        private int size = 0;

		// 进行扩容的阈值，表示使用量大于它的时候进行扩容，默认为0
        private int threshold; 
```

跟 HashMap类似，INITIAL_CAPACITY代表这个Map的初始容量；tabe是一个Entry类型的数组，用于存储数据；size代表表中的存储数目；threshold代表需要扩容时对应size的阈值。

**2、存储结构——Entry**

```java
   /**
     * Entry继承 WeakReference，并且用 Threadlocal作为key
     * 如果key为 null（entry.get()==nu11），意味着key不再被引用，
     * 因此这时候 entry也可以从 table中清除
     */
	static class Entry extends WeakReference<ThreadLocal<?>> {
            /** The value associated with this ThreadLocal. */
            Object value;

            Entry(ThreadLocal<?> k, Object v) {
                super(k);
                value = v;
            }
```

在 ThreadLocalMap中，也是用Entry来保存KV结构数据的。不过Entry中的key只能是  ThreadLocal对象，这点在构造方法中已经限定死了。

另外，**Entry继承 WeakReference，也就是key（ThreadLocal）是弱引用**，其目的是将 ThreadLocal对象的生命周期和线程生命周期解绑。

### 弱引用和内存泄漏

有些程序员在使用 ThreadLocal的过程中会发现有内存泄漏的情况发生，就猜测这个内存泄漏跟Entry中使用了弱引用的key有关系。这个理解其实是不对的

**1、内存泄漏相关概念**

- Memory overflow：内存溢出，没有足够的内存提供申请者使用。
- Memory leak：内存泄漏，是指程序中己动态分配的堆內存由于某种原因程序未释放或无法释放，造成系统內存的浪费，导致程序运行速度减慢甚至系统崩溃等严重后果工内存泄漏的堆积终将导致内存溢出。（该回收的对象无法回收）

**2、弱引用相关概念（详细可以看JVM的垃圾回收）**

Java中的引用有4种类型：强、软、弱、虚。当前这个问题主要涉及到强引用和弱引用

- 强引用（"Strong"Reference），就是我们最常见的普通对象引用，只要还有强引用指向一个对象，就能表明对象还活着”，垃圾回收器就不会回收这种对象
- 弱引用（WeakReference），垃圾回收器一旦发现了**只具有弱引用的对象（没有其他引用类型）**，不管当前内存空间足够与否，都会回收它的内存。

3、如果key使用强引用

- 假设 ThreadLocalMap中的key使用了强引用，那么会出现内存泄漏吗？

  此时 ThreadLocal 的内存图（实线表示强引用）如下

  ![image-20200613203857663](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200613203857663.png)

  1. 假设在业务代码中使用完 ThreadLocal，局部变量表的ThreadLocal引用由于栈桢弹出而失效。
  2. 但是因为 ThreadLocalMapl的 Entry强引用（假设Key用的强引用）了 ThreadLocal，造成ThreadLocal无法被回收。
  3. 在没有手动删除这个 Entry以及 CurrentThread然运行的前提下始终有强引用链 Current Thread Ref-> Current Thread-> ThreadLocalMap-> Entry，Entry就不会被回收（Entry中包括了 ThreadLocal实例和 value），导致 Entry内存泄漏

  也就是说，即使ThreadLocalMap中的key使用了强引用，也无法避免内存泄漏。

- 那么 Thread LocalMap中的key使用了弱引用，会出现内存泄漏吗？

  ![image-20200613205408026](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200613205408026.png)

  1. 同样假设在业务代码中使用完 ThreadLocal，ThreadLocal Ref被回收了
  2. 由于ThreadLocalMap只持有 ThreadLocal的弱引用，浸有任何强引用指向ThreadLocal实例所以 ThreadLocal就可以利被gc回收，此时 Entry中的key=null
  3. 但是在没有手动删除这个 Entry以及 CurrentThread依然运行的前提下，也存在有强引用链 thread Ref-> currentThread-> thread Local Map-> entry->value，value不会被回收，也即该Entry对象也不会被回收，而这块 value永远不会被访问到了，导致内存泄漏。

  也就是说，Thread LocalMap中的key使用了弱引用，也有可能内存泄漏

### 出现内存泄漏的原因

比上述两种情况，我们就会发现，**内存泄漏的发生跟 ThreadLocalMap中的Key是否使用什么引用是没有关系的**。那么内存泄漏的的真正原因是什么呢？

在以上两种内存泄漏的情况中，都有两个前提：

1. **没有手动删除这个 Entry**
2. **CurrentThread依然运行**

第一点很好理解，只要在使用完 ThreadLocal，调用其 remove方法删除对应的Entry，就能避免内存泄漏。

第二点稍微复杂一点，由于 ThreadLocalMap是 Thread的个属性，被当前线程所引用，所以它的生命周期跟 Thread一样长。那么在使用完ThreadLocal的使用，如果当前 Thread也随之执行结束，ThreadLocalMap自然也会被gc回收，从根源上避免了内存泄漏。

**综上，ThreadLocal内存泄漏的根源是：由于 ThreadLocalMap的生命周期跟Thread样长，如果没有手动删除对应Entry就会导致内存泄漏。**

要避免内存泄漏有两种方式：

1. 使用完 ThreadLocal，调用其 remove方法删除对应的 Entry
2. 使用完 ThreadLocal，当前 Thread也随之运行结束（太苛刻）

相对第一种方式，第二种方式显然更不好控制，特别是使用线程池的时候，线程结束是不会销毁的也就是说，只要记得在使用完 Threadlocal及时的调用 remove，无论key是强引用还是弱引用都不会有问题。

### Key使用弱引用的原因

那么为什么key要用弱引用呢？

**事实上，在 ThreadLocalMap中的 set/gemEntry方法中，会对key为null（也即是 ThreadLocal被回收后Key为null）进行判断，如果为null的话，那么是会对value置为null的。**

这就意味着使用完 ThreadLocal，CurrentThread依然运行的前提下，就算忘记调用 remove方法，**==弱引用比强引用可以多一层保障：==** **弱引用的 ThreadLocal对象会被回收，对应的value在下一次 ThreadLocalMap调用set，get，remove中的任一方法的时候（可能又需要用另一个ThreadLocal对象时）会被清除，从而避免内存泄漏。**



### hash冲突的解决

hash冲突的解决是Map中的一个重要内容。我们以hash冲奕的解决为线索，来研究一下 ThreadLocal核心源码。

前面提到set方法，流程是拿到当前线程以及对应的ThreadLocalMap，判断是否为空，为空则调用ThreadLocalMap的构造方法；不为空则调用ThreadLocalMap的set方法

```java
	public void set(T value) {
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
        if (map != null)
            // 调用了ThreadLocalMap的set方法
            map.set(this, value);
        else
            createMap(t, value);
    }

	ThreadLocalMap getMap(Thread t) {
        return t.threadLocals;
    }

	void createMap(Thread t, T firstValue) {
        // 调用了ThreadLocalMap的构造方法
        t.threadLocals = new ThreadLocalMap(this, firstValue);
    }	
```

**ThreadLocalMap的构造方法**

```java
	/**
    * firstKey：本 ThreadLocal实例（this）
    * firstValue：要保存的线程本地变量
    */
		ThreadLocalMap(ThreadLocal<?> firstKey, Object firstValue) {
        	// 初始化table
            table = new Entry[INITIAL_CAPACITY];
            // 计算索引值
            int i = firstKey.threadLocalHashCode & (INITIAL_CAPACITY - 1);	// 可以看到java源码上很多取模操作用与操作代替以提高效率
            // 设置值
            table[i] = new Entry(firstKey, firstValue);
            size = 1;		// 数组里面Entry个数
            
            // 设置阈值，是这个初始容量的2/3
            setThreshold(INITIAL_CAPACITY);
        }
```

构造函数首先创建一个长度为16的Enty数组，然后计算出 firstKey 对应的索引，然后存储到table中，并设置size和 threshold

重点分析

```java
int i = firstKey.threadLocalHashCode & (INITIAL_CAPACITY - 1);
```

关于`firstKey.threadLocalHashCode`

```java
// ThreadLocal内部属性threadLocalHashCode
private final int threadLocalHashCode = nextHashCode();

private static int nextHashCode() {
        return nextHashCode.getAndAdd(HASH_INCREMENT);
    }

//AtomicInteger是一个提供原子操作的 Integer美，通过CAS算法保证线程安全的方式操作加减，适合高并发情况下的使用
private static AtomicInteger nextHashCode =
        new AtomicInteger();

//特殊的hash值
private static final int HASH_INCREMENT = 0x61c88647;
```

这里定义了一个 AtomicInteger类型，每次获取当前值并加上HASH_INCREMENT，0x61c88647 这个值跟**斐波那契数列（黄金分割数）**有关，其主要目的就是为了**让哈希码能均匀的分布**在2的n次方的数组里也就是 Entry table中，这样做可以尽量避免hash冲突



**ThreadLocalMap中的set方法**

```java
		private void set(ThreadLocal<?> key, Object value) {
            Entry[] tab = table;
            int len = tab.length;
            // 计算索引
            int i = key.threadLocalHashCode & (len-1);
			/**
			* 使用线性探测法查找元素（重点代码）
			*/
            for (Entry e = tab[i];
                 e != null;
                 e = tab[i = nextIndex(i, len)]) {	// 冲突则index+1向前查询，直到遇到Entry为空的位置
                ThreadLocal<?> k = e.get();
                
				// ThreadLocal对应的Key存在，直接覆盖之前的值
                if (k == key) {
                    e.value = value;
                    return;
                }
				// key为null，说明之前的ThreadLocal已经被回收了
                // 当前数组中的Entry 是一个陈旧的（stale）的元素
                if (k == null) {
                    // 用新元素替换陈旧元素，这个方法进行了不少的垃圾清理动作，防止内存泄漏
                    replaceStaleEntry(key, value, i);
                    return;
                }
            }
			//ThreadLocal对应的key不存在并且没有找到陈旧的元素，则在空元素的位置创建一个新的 Entry
            tab[i] = new Entry(key, value);
            int sz = ++size;
            /**
            * cleanSomeSlots用于清除那些e.get() == null的元素（ThreadLocal为null的元素）,
            这种数据key关联的对象已经被回收，所以这个 Entry(table[index])可以被置null
            如果没有清除任何 entry，并且当前使用量达到了负载因子所定义（长度的2/3），那么进行rehash（执行一次全表的扫描清理工作）
            rehash里面当size大于 3/4的threshold则要扩容，扩容后位2倍
            */
            if (!cleanSomeSlots(i, sz) && sz >= threshold)
                rehash();
        }
		// 获取环形数组的下一个索引，注意超过数组长度则会重定向到下标0
		private static int nextIndex(int i, int len) {
            	return ((i + 1 < len) ? i + 1 : 0);
        }
```

代码执行流程：

1. 首先还是根据key计算出索引i，然后查找置上的 Entry，
2. 若是Enrty已经存在并且key等于传入的key，那么这时候直接给这个Entry赋新的aue值
3. 若是Entry存在，但是key为null，则调用 replaceStaleEntry来更换这个key为空的Enty 
4. 不断循环检测，直到遇到为null的地方，这时候要是还没在循环过程中 return，那么就在这个null的位置新建一个 Entry，并且插入，同时size增加1。
5. 最后调用cleanSomeSlots，清理key为null的Entry，最后返回是否清理了Entry，接下来再判断sz是否 >=
   threshold达到了 rehash的条件，达到的话就会调用 rehash函数执行一次全表的扫描清理

**重点分析：ThreadLocalMap使用==线性探测法==来解决哈希冲突的**

该方法一次探测下一个地址，直到有空的地址后插入，若整个空间都找不到空余的地址，则产生溢出。

举个例子，假设当前tabe长度为16，也就是说如果计算出来key的hash值为14，如果tabe[14]上已经有值，并且其key与当前key不一致，那么就发生了hash冲突，这个时候将14加1得到15，取tabel[15] 进行判断，这个时候如果还是冲突会回到0，取tabe[0]以此类推，直到可以插入。

按照上面的描述，可以把 Entry table看成一个环形数组。

**是否会发生死循环呢？（当数组全满的时候）**

并不会，首先因为ThreadLocalMap是一个Map，而该Map是有一个存储的阈值的，也就是threshold属性，当存储的数值达到阈值上线，就会进行扩容的。

因此绝对不会出现数组全满的时候，当达到阈值就会扩容。