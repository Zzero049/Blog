1、框架；高度抽取可重用代码的一种设计；高度的通用性；

## Spring
Spring是一个IOC（控制反转）和AOP（面向切面编程）容器（可以管理所有的组件(类)）框架。Spring为简化企业级开发而生，使用Spring，JavaBean就可以实现很多以前要靠EJB才能实现的功能。同样的功能，在EJB中要通过繁琐的配置和复杂的代码才能够实现，而在Spring中却非常的优雅和简洁。

### Spring的优良特性
- [1]非侵入式：基于spring开发的应用中的对象可以不依赖于Spring的APle
- [2]依赖注入：DI—-Dependency Injection，反转控制（IOC）最经典的实现。
- [3]面向切面编程：Aspect Oriented Programming——AOP。
- [4]容器：Spring是一个容器，因为它包含并且管理应用对象的生命周期。
- [5]组件化：Spring实现了使用简单的组件配置组合成一个复杂的应用。在Spring中可以使用XML和Java注解组合这些对象。
- [6]一站式：在IOC和AOP的基础上可以整合各种企业应用的开源框架和优秀的第三方类库（实际上Spring自身也提供了表述层的SpringMVC和持久层的Spring JDBC）。

## spring 的下载
Spring官网并不直接提供Spring的下载，GitHub上也只提供spring的源码，不提供jar包。


[下载地址](https://repo.spring.io/webapp/#/artifacts/browse/tree/General/libs-release-local/org/springframework/spring)

<img src="https://gitee.com/zero049/MyNoteImages/raw/master/1685101-20200122091908380-524394528.png"  div align=center />

<br></br>

<img src="https://gitee.com/zero049/MyNoteImages/raw/master/1685101-20200122092328332-1015565000.png"  div align=center />

docs文件夹里是一些html文件，是Spring的API文档。

libs文件夹里是Spring的jar包，一共63个。
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/1685101-20190630040632071-589731235.png"  div align=center />
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-03-15 213228.png"  div align=center />
3个一组，.RELEASE.jar是在项目中使用的，.RELEASE-javadoc.jar是这个jar包的说明文档，.RELEASE-source.jar是这个jar包的源码。真正在项目中用的就21个。


+
其中，有4个是Spring的基础包，对应Spring核心容器的4个模块，是Spring项目必需的：

spring-core-5.1.8.RELEASE.jar    //Spring的核心工具类，其它jar包是建立这个包基础上的，都要用到这个包中的类。
spring-beans-5.1.8.RELEASE.jar     //配置、创建、管理Bean，负责Ioc、DI
spring-context-5.1.8.RELEASE.jar   //提供在基础IoC上的扩展服务
spring-expression-5.1.8.RELEASE.jar   //提供对Spring表达式语言的支持
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/1685101-20190630040825905-1082151482.png"  div align=center />

* Test : spring的单元测试模块
* Core container： 核心容器（IoC）黑色方框代表这部分的功能由哪些jar包组成；要使用这个部分的完整功能，这些jar都需要导入
分别是
    ```
    spring-beans-x.x.x.RELEASE
    spring-core-x.x.x.RELEASE
    spring-context-x.x.x.RELEASE
    spring-expression-x.x.x.RELEASE
    ```
* AOP + Aspects(面向切面编程模块)
    ```
    spring-aop-x.x.x.RELEASE
    spring-aop-x.x.x.RELEASE
    ```
* 数据访问/集成
    ```
    spring-jdbc-x.x.x.RELEASE
    spring-orm（Object Relation Mapping）-x.x.x.RELEASE
    spring-ox（xml）m-x.x.x.RELEASE
    spring-jms-x.x.x.RELEASE
    spring-tx-x.x.x.RELEASE（事务）
    ```

* Web： Spring开发web应用模块
    ```
    spring-websocket（新的技术）-x.x.x.RELEASE
    spring-web-x.x.x.RELEASE、和原生的web相关（servlet）
    spring-webmvc-4.0.0.RELEASE、开发web项目的（web）
    spring-webmvc-portlet-4.0.0.RELEASE（开发web应用的组件集成）
    ```

### 程序的耦合实例
耦合：程序间的依赖关系包括：

&emsp;&emsp;类之间的依赖

&emsp;&emsp;方法间的依赖

解耦：

&emsp;&emsp;降低程序间的依赖关系

实际开发中：

&emsp;&emsp;应该做到：编译期不依赖，运行时才依赖。

解耦的思路：

&emsp;&emsp;第一步：使用反射来创建对象，而避免使用new关键字。

&emsp;&emsp;第二步：通过读取配置文件来获取要创建的对象全限定类名


pom.xml文件下引入依赖，install

```xml
<dependencies>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.8</version>
        </dependency>

</dependencies>
```

```java
import java.sql.*;

public class JdbcDemo1 {
    public static void main(String[] args) throws SQLException {
        //1.注册驱动,依赖包发挥作用
        DriverManager.registerDriver(new com.mysql.jdbc.Driver());
        //2.获取连接
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/testjdbc","root","qaz12345");
        //3.获取操作数据库的预处理对象
        PreparedStatement pstm = conn.prepareStatement("select * from account");
        //4.执行sQL，得到结果集
        ResultSet rs = pstm.executeQuery();
        //5.遍历结果集
        while(rs.next()){
            System.out.println(rs.getString("name"));
        }

        //6.释放资源
        rs.close();
        pstm.close();
        conn.close();
    }
}

```

IOC示意：将管理类的控制权交给工厂
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-01-27 133025.png"  div align=center />

#### spring的控制反转
在resources下创建xml文件
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd">

    <!--把对象交给spring来管理-->
    <bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl"></bean>
    <bean id="accountDao" class="com.itheima.dao.impl.AccountDaoImpl"></bean>

</beans>
```
```java
public static void main(String[] args) throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException {
        //1.获取核心容器对象
        ApplicationContext ac = new ClassPathXmlApplicationContext("bean.xml");
        //2.根据id获取Bean对象
        IAccountService as = (IAccountService) ac.getBean("accountService");
        IAccountDao adao = ac.getBean("accountDao",IAccountDao.class);
//        as.saveAccount();

        System.out.println(as);
        System.out.println(adao);
    }
```

#### 获取核心容器
**ApplicationContext**的三个常用实现类：（单例模式适用，通常用此接口）
* ClassPathXmLAppLicationContext：它可以加载类路径下的配置文件，要求配置文件必须在类路径下。不在的话，加载不了。
* FileSystemXmlApplicationContext：它可以加载磁盘任意路径下的配置文件（必须有访问权限）
* AnnotationConfigApplicationcontext：它是用于读取注解创建容器的

存在的问题：
* 它在构建核心容器时，创建对象采取的策略是采用立即加载的方式。也就是说，只要一读取完配置文件马上就创建配置文件中配置的对象。

**BeanFactory**（ApplicationContext父类HierarchicalBeanFactory的父类）：它在构建核心容器时，创建对象采取的策略是采用延迟加载的方式。也就是说，什么时候根据id获取对象了，什么时候才真正的创建对象。（多例适用）

### 创建bean的三种方式
1. 第一种方式：使用默认构造函数创建。
在spring的配置文件中使用bean标签，配以id和class属性之后，且没有其他属性和标签时。
采用的就是默认构造函数创建bean对象，此时如果类中**没有默认构造函数**，则对象无法创建。
如：
```xml
  <bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl"></bean>
```
2. 第二种方式：使用普通工厂中的方法创建对象（使用某个类中的方法创建对象,并存入spring容器)，如：
```xml
<!--通过instanceFactory工厂的getAccountService方法获取对象-->
  <bean id="instanceFactory" class="com.itheima.factory.InstanceFactory"></bean>
  <bean id="accountService" factorty-bean="InstanceFactory" factory-method="getAccountService"></bean>
```

3. 第三种方式：使用工厂中的静态方法创建对象（使用某个类中的静态方法创建对象，并存入spring容器,与法二区别在于工厂方法是否为静态方法）
```xml
<bean id="accountService"  class="com.itheima.factory.StaticFactory" factory-method="getAccountService"></bean>
```

### bean的作用范围
bean标签的**scope**属性：
作用：用于指定bean的作用范围
取值：
* singleton：单例
* prototype 多例的
* request  作用于web应用的请求范围
* session  作用于web应用的会话范围
* global-session 作用于集群环境的会话范围（全局会话范围），当不是集群环境时，它就是session

global-session解释：
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-03-22 215659.png"  div align=center />

### bean对象的生命周期
1. 单例对象
    * 出生：当容器创建时对象出生（解析配置文件后创建）
    * 活着：只要容器还在，对象一直活着
    * 死亡：容器销毁，对象消亡
    * 总结：单例对象的生命周期和容器相同

2. 多例对象
    * 出生：当我们使用对象时spring框架为我们创建
    * 活着：对象只要是在使用过程中就一直活着。
    * 死亡对象长时间不用，且没有别的对象引用时，由Java的垃圾回收器回收

### spring 中的依赖注入
依赖注入：

&emsp;Dependency Injection 

IOC的作用：

&emsp;降低程序间的耦合（依赖关系）

依赖关系的管理：

&emsp;以后都交给spring来维护

在当前类需要用到其他类的对象，由spring为我们提供，我们只需要在配置文件中说明

依赖关系的维护：

&emsp;就称之为依赖注入。

依赖注入：能注入的数据：有三类

&emsp;1. 基本类型和String

&emsp;2. 其他bean类型（在配置文件中或者注解配置过的bean）

&emsp;3. 复杂类型/集合类型

注入的方式：有三种

&emsp;&emsp;&emsp;第一种：使用构造函数提供

&emsp;&emsp;&emsp;第二种：使用set方法提供

&emsp;&emsp;&emsp;第三种：使用注解提供

#### 构造函数注入
当创建对象需要注入必要的数据（如创建对象需要初始化的数据）

使用的标签：constructor-arg

标签出现的位置：bean标签的内部

标签中的属性
* type：用于指定要注入的数据的数据类型，该数据类型也是构造函数中某个或某些参数的类型
* index：用于指定要注入的数据给构造函数中指定索引位置的参数赋值。索引的位置是从0开始
* name：用于指定给构造函数中指定名称的参数赋值（常用）

-------以上三个用于指定给构造函数中哪个参数赋值------

value：用于提供基本类型和String类型的数据

ref：用于指定其他的bean类型数据。它指的就是在spring的Ioc核心容器中出现过的bean对象

```xml
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl">
    <constructor-arg name="name" value="test"></constructor-arg>
    <constructor-arg name="age" value="18"></constructor-arg>
    <constructor-arg name="birthday" ref="now"></constructor-arg>
</bean>

<!--配置一个日期对象-->
<bean id="now"class="java.util.Date"></bean>
```

优势：
* 在获取bean对象时，注入数据是必须的操作，否则对象无法创建成功。

弊端：
* 改变了bean对象的实例化方式，使我们在创建对象时，如果用不到这些数据，也必须提供。

#### set方法注入
涉及的标签；property

出现的位置：bean标签的内部标签的属性

name：用于指定注入时所调用的set方法名称（名称为set方法去掉set，头字母变为小写）

value：用于提供基本类型和String类型的数据

ref：用于指定其他的bean类型数据。它指的就是在spring的Ioc核心容器中出现过的bean对象

```xml
<bean id="accountService2" class="com.itheima.service.impl.AccountServiceImpl2">
    <property name="name" value="TEST"></property>
    <property name="age" value="21"></property>
</bean>
```

优势：
* 创建对象时没有明确的限制，可以直接使用默认构造函数

弊端：
* 如果有某个成员必须有值，则获取对象是有可能set方法没有执行


#### 复杂类型的注入/集合类型的注入
遇到List，Map等集合类型时使用

涉及的标签；property的子标签

用于给List结构集合注入的标签：
* list array set

用于Map结构集合注入的标签：
* map props

结构相同，标签可以互换，注入的数据会到所在结构中

```xml
<bean id="accountService3"class="com.itheima.service.impl.AccountServiceImp13">
    <property name="myStrs">
        <set>
            <value>AAA</value>
            <value>BBB</value>
            <value>CCC</value>
        </set>
    </property>
    <property name="myList">
        <array>
            <value>AAA</value>
            <value>BBB</value>
            <value>CCC</value>
        </array>
    </property>
    <property name="myProps">
        <props>
            <prop key="testc">ccc</prop>
        </props>
    </property>
    <property name="myMap">
        <map>
            <entry key="testA" value="aaa"></entry>
            <!--两种map注入方式-->
            <entry key="testB">
                <value>BBB</value>
        </entry>
        </map>
    </property>
    <!--即便map与property对调也不报错-->
</bean>
```

### 实例（使用bean与数据库交互）
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd">

    <!-- 配置services -->
    <bean id="accountService" class="com.itheima.ui.domain.com.itheima.ui.service.impl.AccountserviceImpl">
        <!--注入dao-->
        <property name="dao" ref="accountDao"></property>
    </bean>
    <bean id="accountDao" class="com.itheima.ui.domain.com.itheima.ui.service.dao.impl.AccountDaoImpl">
        <property name="runner" ref="runner"></property>
    </bean>
    <!--注入QueryRunner，并考虑线程安全问题设置为多例对象-->
    <bean id="runner" class="org.apache.commons.dbutils.QueryRunner" scope="prototype">
        <!--注入数据源-->
        <constructor-arg name="ds" ref="dataSource"></constructor-arg>
    </bean>
    <!--配置数据源-->
    <bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource">
        <!--连接数据库的必备信息-->
        <property name="driverClass" value="com.mysql.jdbc.Driver"></property>
        <property name="jdbcUrl" value="jdbc:mysql://localhost:3306/eesy"></property>
        <property name="user" value="root"></property>
        <property name="password" value="1234"></property>
    </bean>
    

</beans>
```
