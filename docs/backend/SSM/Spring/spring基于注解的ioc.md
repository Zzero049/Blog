# spring基于注解的IOC以及IoC的案例

## spring中的ioc的常用注解
通过xml可以将一个类添加到spring管理，而通过注解可以告知spring在创建容器时要扫描的包，配置所需要的标签不是在beans的约束中，而是一个名称为context名称空间和约束中

#### @Component
```java
//添加注解
@Component("accountService")
public class AccountServiceImpl implements IAccountService{

}
```
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context
        https://www.springframework.org/schema/context/spring-context.xsd">
    <!--约束不在bean中-->
    <context:component-scan base-package="com.itheima"></context:component-scan>

</beans>
```

#### @Controller @Service @Repository
以上三个注解他们的作用和属性与component是一模一样。他们三个是spring框架为我们提供明确的三层使用，使我们的三层对象更加清晰
ControlLer：一般用在表现层
Service：一般用在业务层
Repository：一般用在持久层

### 注入数据
他们的作用就和在xml配置文件中的bean标签中写一个`<property>`标签的作用是一样的

#### @Autowired

作用：**自动按照类型注入**。只要容器中有唯一的一个bean对象类型和要注入的变量类型匹配，就可以注入成功
出现位置：
&emsp;&emsp;可以是变量上，也可以是方法

```java
@Component
public class AccountServiceImpl implements IAccountService{
    @Autowired
    private IAccountDao accountDao;
    //自动注入一个IAccountDao对象

    public void saveAccount() {
        accountDao.saveAccount();

    }
}
```
<img src="./pictures/Annotation 2020-03-24 222406.png"  div align=center />
如果有多个匹配时（IAccountService的实现类不止一个），如果变量名重名的则会报错

<br>
</br>

#### @Qualifier
作用：在**按照类中注入的基础之上再按照名称注入**。它在给类成员注入时不能单独使用,但是在给方法参数注入时可以。
属性：
&emsp;value：用于指定注入bean的id。

```java
@Component
public class AccountServiceImpl implements IAccountService{
    @Autowired
    @Qualifier("accountDao1")
    private IAccountDao accountDao=null;

    public void saveAccount() {
        accountDao.saveAccount();

    }
}
```
#### @Resource 
作用：直接按照bean的**名称**注入。它可以独立使用属性,需要在Maven中注入jar.annotation
name：用于指定bean的id。
```java
@Component
public class AccountServiceImpl implements IAccountService{
    @Resource(name="accountDao1")
    private IAccountDao acco
    
    untDao=null;

    public void saveAccount() {
        accountDao.saveAccount();

    }
}
```

以上三个注入都只能注入其他bean类型的数据，而基本类型和string类型无法使用上述注解实现。
另外，集合类型的注入只能通过XML来实现。

#### @Value
作用：用于注入基本类型和String类型的数据
属性：
&emsp;&emsp;value：用于指定数据的值。它可以使用spring中SpEL（也就是spring的el表达式）
SpEL的写法：${表达式}

### 改变作用范围
他们的作用就和在bean标签中使用scope属性实现的功能是一样的Scope作用：用于指定bean的作用范围
属性：
value：指定范围的取值。常用取值：singteton prototype

```java
@Service(accountService)
@Scope("prototype")
public class AccountServiceImpl implements IAccountService{
    @Resource(name="accountDao1")
    private IAccountDao acco
    
    untDao=null;

    public void saveAccount() {
        accountDao.saveAccount();

    }
}
```

### 生命周期相关
他们的作用就和在bean标签中使用init-method和destroy-methode的作用是一样的
PreDestroy
作用：用于指定销毁方法
PostConstruct
作用：用于指定初始化方法

### 通过注解可以不使用xml配置文件
通过一个配置类，达到xml配置文件效果，通过使用spring中的新注解

#### @Configuration

作用：指定当前类是一个配置类
细节：当配置类作为AnnotationConfigAppLicationContext对象创建的参数时，该注解可以不写。

####  @ComponentScan

作用：用于通过注解指定spring在创建容器时要扫描的包
属性：
&emsp;&emsp;value：它和basePackages的作用是一样的，都是用于指定创建容器时要扫描的包。
我们使用此注解就等同于在xml中配置了`<context:component-scan base-package="com.itheima"></context:component-scan>`

#### @Bean
作用：用于把当前方法的返回值作为bean对象存入spring的ioc容器
属性：
&emsp;&emsp;name：用于指定bean的id。当不写时，默认值是当前方法的名称
细节：
&emsp;&emsp;当我们使用注解配置方法时，如果方法有参数，spring框架会去容器中查找有没有可用的bean对象。
&emsp;&emsp;查找的方式和Autowired注解的作用是一样的（按类型匹配）

示例：
xml文件
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
与该类IOC效果相同

```java
package com.itheima.ui.domain.com.itheima.ui.service.dao.impl;

import com.mchange.v2.c3p0.ComboPooledDataSource;
import org.apache.commons.dbutils.QueryRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

import javax.sql.DataSource;
import java.beans.PropertyVetoException;

@Configuration
@ComponentScan("com.itheima")
public class SpringConfig {
    /**
     * 用于创建一个QueryRunner对象,此法创建的默认为单例的
     */
    @Bean(name="runner")
    //@Scope("prototype")多例
    public QueryRunner createQueryRunner(DataSource dataSource){
        return new QueryRunner(dataSource);
    }
    /**
     * 创建数据源对象
     */
    @Bean(name="dataSource")
    public DataSource createDaaSource() throws PropertyVetoException {
        ComboPooledDataSource ds = new ComboPooledDataSource();
        ds.setDriverClass("com.mysql.jdbc.Driver");
        ds.setJdbcUrl("jdbc:mysql://localhost/3306/eesy");
        ds.setUser("root");
        ds.setPassword("1234");
        return ds;
    }
}

```
修改后获取容器的方法变为
```java
ApplicationContext ac = new AnnotationConfigApplicationContext(SpringConfig.class);

IAccountService as = ac.getBean("accountService", IAccountService.class);
```

#### @Import
作用：用于导入其他的配置类到这个类
属性：
&emsp;value：用于指定其他配置类的字节码。
&emsp;当我们使用Import的注解之后，有Import注解的类就父配置类，而导入的都是子配置类
如
```java
@Configuration
@ComponentScan({"com.itheima"})
@Import(JdbcConfig.class)
public class SpringConfig {

}
```

#### @PropertySource
作用：用于指定properties文件的位置（可方便修改某些属性值）
属性：
value：指定文件的名称和路径。
关键字：classpath，表示类路径下

示例

```java
@ComponentScan("com.itheima")
@Import(JdbcConfig.class)
@PropertySource("classpath:JdbcConfig.properties")
public class SpringConfig {
    @Value("${jdbc.driver}")
    private String driver;
    @Value("${jdbc.url}")
    private String url;
    @Value("${jdbc.user}")
    private String user;
    @Value("${jdbc.password}")
    private String password;
    /**
     * 用于创建一个QueryRunner对象,此法创建的默认为单例的
     */
    @Bean(name="runner")
    //@Scope("prototype")多例
    public QueryRunner createQueryRunner(DataSource dataSource){
        return new QueryRunner(dataSource);
    }
    /**
     * 创建数据源对象
     */
    @Bean(name="dataSource")
    public DataSource createDaaSource() throws PropertyVetoException {
        ComboPooledDataSource ds = new ComboPooledDataSource();
        ds.setDriverClass(driver);
        ds.setJdbcUrl(url);
        ds.setUser(user);
        ds.setPassword(password);
        return ds;
    }
}
```
JdbcConfig.properties文件内容

```
jdbc.driver=com.mysql.jdbc.Driver 
jdbc.url=jdbc:mysq1://localhost:3306/eesy 
jdbc.username=root
jdbc.password=1234
```

### 使用Junit测试出现的问题
1、应用程序的入口
* main方法

2、junit单元测试中，没有main方法也能执行
* junit集成了一个main方法
* 该方法就会判断当前测试类中哪些方法有@Test注解
* &emjunit就让有Test注解的方法执行

3、junit不会管我们是否采用spring框架
* 在执行测试方法时，junit根本不知道我们是不是使用了spring框架
* 所以也就不会为我们读取配置文件/配置类创建spring核心容器

4、由以上三点可知
* 当测试方法执行时，没有Ioc容器，就算写了Autowired注解，也无法实现注入

Spring整合junit的配置:
1、导入spring整合junit的jar（注入依赖）
```xml
<groupId>orc.springframework</groupId>
<artifactId>spring-test</artifactId>
<version></version>
```
2、使用Junit提供的一个汪解把原有的main方法替换了，替换成spring捉供的 **@RuniwLth**
3、告知spring的运行器，spring和ioc创建是基于xmL还是注解的，并且说明位置 
**@ContextConfiquration** 
&emsp;Locations：指定**xml文件**的位置，加上classpath关键宇，表示在类路径下
&emsp;classes：指定**注解类**所在地位置

当我们使用spring 5.x版本的时候，要求junit的jar必须是4.12及以上

```java


@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(classes = SpringConfig.class)
public class AccountServiceTest {
    @Autowired
    IAccountService as = null;
    @Test
    public void testFindAll(){
        List<Account> accounts = as.findAllAccount();
        for(Account account:accounts){
            System.out.println(account);
        }
    }
}
```

## 不使用xml的spring

通过一个配置类，达到xml配置文件效果，通过使用spring中的新注解

>@Configuration

作用：指定当前类是一个配置类

>@ComponentScan

作用：用于通过注解指定spring在创建容器时要扫描的包
属性：
value：它和basePackages的作用是一样的，都是用于指定创建容器时要扫描的包。
我们使用此注解就等同于在xml中配置了`<context:component-scan base-package="com.itheima"></context:component-scan>`

示例