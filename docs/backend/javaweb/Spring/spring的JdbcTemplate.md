## JdbcTemplate
它是spring框架中提供的一个对象，是对原始Jdbc API对象的简单封装。spring框架为我们提供了很多的操作模板类。

操作关系型数据的：
* JdbcTemplate 
* HibernateTemplate

操作nosql数据库的：
* RedisTemplate
操作消息队列的：
* JmsTemplate

我们今天的主角在spring-jdbc-5.0.2.RELEASE.jar中，我们在导包的时候，除了要导入这个jar包外，还需要导入一个spring-tx-5.0.2.BELEASE.jar（它是和事务相关的）。

<img src="./pictures/Annotation 2020-03-28 135415.png"  div align=center />


### JdbcTemplate的作用
它就是用于和数据库交互的，实现对表的CRUD操作(增删改查)

实例：
```java
package day04_eesy_01jdbctemplate.jdbctemplate;

import day04_eesy_01jdbctemplate.domain.Account;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.datasource.DriverManagerDataSource;

import javax.sql.DataSource;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

public class jdbcTemplateDemo2 {
    public static void main(String[] args) {
        ApplicationContext ac= new ClassPathXmlApplicationContext("bean4.xml");

        JdbcTemplate jt = (JdbcTemplate)ac.getBean("jdbcTemplate");
        //3,执行操作
        //更新
        jt.update("update account set name=?,money=? where id=?", "ccc", 3000,3);
        //删除
        jt.update("delete from account where id=?",5);
        //查询所有
//        List<Account> accounts = jt.query("select * from account where money>?",new AccountRowMapper(),0f);
        //spring提供了mapper类不用自己写
        List<Account> accounts = jt.query("select * from account where money>?",new BeanPropertyRowMapper<Account>(Account.class),10f);
        for(Account account:accounts){
            System.out.println(account);
        }
        //查询一个
        List<Account> accounts2 = jt.query("select * from account where id=?",new BeanPropertyRowMapper<Account>(Account.class),7);
        System.out.println(accounts2.isEmpty()?"没有内容":accounts2.get(0));
        //查询一行一列（使用聚合函数，但不加group by）
        Long count = jt.queryForObject("select count(*) from account where money>?", Long.class , 0f);//返回类型为Long
        System.out.println(count);
    }

}

/**
 * 定义account的封装策略
 */
class AccountRowMapper implements RowMapper<Account>{
    /**
     * 把结果集中在数据封装到Account中，然后由spring把每个Account加到集合中
     * @param resultSet
     * @param i
     * @return
     * @throws SQLException
     */
    @Override
    public Account mapRow(ResultSet resultSet, int i) throws SQLException {
        Account account = new Account();
        account.setId(resultSet.getInt("id"));
        account.setName(resultSet.getString("name"));
        account.setMoney(resultSet.getFloat("money"));
        return account;
    }
}
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">
        <property name="dataSource" ref="dataSource"></property>
    </bean>
    <bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
        <property name="driverClassName" value="com.mysql.jdbc.Driver"></property>
        <property name="url" value="jdbc:mysql://localhost:3306/eesy"></property>
        <property name="username" value="root"></property>
        <property name="password" value="qaz12345"></property>
    </bean>


</beans>
```

Template 重复代码有spring有JdbcDaoSupport简化，一旦继承了JdbcDaoSupport后，无法再随意增加注解