# Spring中事务控制
spring的事务控制是基于AOP的
## PlatformTransactionManager接口
该接口提供事务操作的方法

-获取事务状态信息
-TransactionStatus get Transaction（TransactionDefinition
definition）
-提交事务
-void commit（TransactionStatus status）
-回滚事务
-void rollback（TransactionStatus status）

实现类：
* org.springframework.jdbe.datasource.patasourceTransactionManager 使用Spring JoBC成iBatia进行持久化数据时使用

* org.springfxamework.orm.hibexnate5.iibernateTransactionManager 使用Hibernate版本进行持久化数据时使用

## TransactionDefinition接口
它是事务的定义信息对象，里面有如下方法：

获取事务对象名称
- String getName（）

获取事务隔离级
- int getlsolationLevel（） 

获取事务传播行为
- int getPropagationBehavior（）

获取事务超时时间
- int getTimeout（）

获取事务是否只读
- boolean isReadOnly（）

## TransactionStatus接口
此接口提供的是事务具体的运行状态，方法介绍如下；

TransactionStatus接口描述了某个时间点上事务对象的状态信息，包含有6个具体的操作

刷新事务
- void flush（）

获取是否是否存在存储点
- boolean hasSavepoint（）

获取事务是否完成
- boolean isCompleted（）

获取事务是否为新的事务
- boolean isNewTransaction（）

获取事务是否回滚
- boolearnisRollbackOnly
设置事务回滚 void setRollbackOnly（）

### 事务的隔离级别
事务隔离级反映事务提交并发访问时的处理态度
-ISOLATIONDEFAULT
-默认级别，归属下列某一种
-ISOLATION_READ_UNCOMMITTED
-可以读取未提交数据
-ISOLATION_READ_COMMITTED
-只能读取已提交数据，解决脏读问题（Oracle默认级别）
-ISOLATION_REPEATABLE_READ
-是否读取其他事务提交修改后的数据，解决不可重复读问题（MySQL默认级别）
-ISOLATION_SERIALIZABLE
-是否读取其他事务提交添加后的数据，解决幻影读问题

### 事务的传播行为

REQUIRED：如果当前没有事务，就新建一个事务，如果已经存在一个事务中，加入到这个事务中。一般的选择（默认值）

SUPPORTS：支持当前事务，如果当前没有事务，就以非事务方式执行（没有事务）

MANDATORY：使用当前的事务，如果当前没有事务，就抛出异常

REOUERS_NEW：新建事务，如果当前在事务中，把当前事务挂起。

N0T_SUPPORTED：以非事务方式执行操作，如果当前存在事务，就把当前事务挂起N

EVER：以非事务方式运行，如果当前存在事务，抛出异常

NESTED：如果当前存在事务，则在嵌套事务内执行。如果当前没有事务，则执行REOUERED类似的操作。

### 超时时间

默认值是-1，没有超时限制。如果有，以秒为单位进行设置。

### 是否是只读事务
建议查询时设置为只读


### 配置示例

```xml

<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xmlns:tx="http://www.springframework.org/schema/tx"
       xsi:schemaLocation="
        http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/tx
        https://www.springframework.org/schema/tx/spring-tx.xsd
        http://www.springframework.org/schema/aop
        https://www.springframework.org/schema/aop/spring-aop.xsd">

    <!--spring中基于xml的声明式事务控制配置步骤
        1.配置事务管理器
        2.配置事务的通知
        此时我们需要导入事务的约束tx名称空间和约束，同时也需要aop的
        使用tx:advice标签配置事务通知
            属性：
                id：给事务通知起一个唯一标识
                transaction-manager：给务通知提供一个务管理器引用
        3.配置AOP中的通用切入点表达式
        4、建立通知和切入点表达式的对应关系
        5、配置事务的属性
            是在事务的通知tx:advice标签的内部
                isolation:用于指定事务的隔离级别。默认值是DEFAULT，表示使用数据库的默认隔离级别"
                no-rollback-for:用于指定一个异常，当产生该异常时，事务不回滚，产生其他异常时的回滚。没有默认值。表示任何异常都回深
                propacation:用于指定事务的传播行为。默认值是REOUIRED，表示一定会有事务，增删改的选择。查询方法可以选择SUPPORTS。
                read-only:用于指定事务是否只读。只有查询方法才能设置为true。默认值是false.表示读写。
                rollback-for:用于指定一个异帘，当产生该异帘时，事务回滚，产生其他异帘时，幕务不回滚。没有默认值。表示任何异常都回滚。
                timeout： 用于指定事务的超时时间，默认值是-1.表示永不超时。如果指定了数值，以秒为单位
        -->
<!--    配置事务管理器-->
    <bean id="transactionManger" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="dataSource"></property>
    </bean>

<!--    配置事务的通知-->
    <tx:advice id="txAdvice" transaction-manager="transactionManger">

        <tx:attributes>
            <tx:method name="transfer" read-only="true"/>
        </tx:attributes>
    </tx:advice>
<!--    配置AOP-->
    <aop:config>
        <aop:pointcut id="pt1" expression="execution(public void day03_eesy_03springAOP.com.impl.AccountServiceImpl.saveAccount())"></aop:pointcut>
        <aop:advisor advice-ref="txAdvice" pointcut-ref="pt1"></aop:advisor>

    </aop:config>
</beans>
```

### 基于注解配置

```xml
<！--开启spring对注解事务的支持一>
<tx:annotation-driven transaction-manager="transactionManager"></tx:annotation-driven>
```
只需要在需要事务支持的类（业务层）或方法上加上
@Transactional即可