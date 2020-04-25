## 连接池
我们在实际开发中都会使用连接池。
因为它可以减少我们获取连接所消耗的时间。

连接池就是用于存储连接的一个容器

容器其实就是一个集合对象，该集合必须：是线程安全的，不能两个线程拿到同一连接

该集合还必须实现队间的特性：先进先出
<img src="./pictures/Annotation 2020-03-31 113122.png
"  div align=center />

## Mybatis的连接池
mybatis连接池提供了3种方式的配置：
配置的位置：
&emsp;主配置文件SqlMapConfig.xml中的dataSource标签，type属性就是表示采用何种连接池方式。type属性的取值：
* POOLED
采用传统的javax.sql.DataSource规范中的连接池，mybatis中有针对规范的实现
* UNPOOLED
采用传统的获取连接的方式，虽然也实现Javax.sql.DataSource接口，但是并没有使用池的思想。（每次用的重新创建一个连接而非从池中取）
* JNDI
采用服务器提供的JNDI技术实现，来获取DataSource对象，不同的服务器所能拿到DataSource是不一样的
注意：如果不是web或者maven的war工程，是不能使用的。
使用的tomcat服务器，采用连接池就是dbcp连接池。

<img src="./pictures/Annotation 2020-03-31 120610.png
"  div align=center />
相应地，MyBatis内部分别定义了实现了java.sql.DataSource接口的UnpooledDataSource，PooledDatasource 类来表示UNPOOLED、POOLED类型的数据源。

连接池图解：
<img src="./pictures/Annotation 2020-03-31 121737.png
"  div align=center />
空闲池是否还有=》活动池是否还能加=》活动池取出一个最老的用

### JNDI
JNDI:Java Naming and Directory Interface。是SUN公司推出的一套规范，属于JavaEE技术之一。目的是模仿 windowe.系统中的注册表。
<img src="./pictures/Annotation 2020-03-31 163533.png
"  div align=center />

在tomcat服务器中注册教据源(以后再了解)
<img src="./pictures/Annotation 2020-03-31 163957.png
"  div align=center />
