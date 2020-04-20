
<img src="./pictures/Annotation 2020-03-29 132213.png
"  div align=center />

### 框架
 它是我们软件开发中的一套解决方案，不同的框架解决的是不同的问题。

使用框架的好处：
&emsp;&emsp;框架封装了很多的细节，使开发者可以使用极简的方式实现功能。大大提高开发效率。

### 三层架构
表现层：
&emsp;&emsp;是用于展示数据的
业务层：
&emsp;&emsp;是处理业务需求
持久层：
&emsp;&emsp;是和数据库交互的

<img src="./pictures/Annotation 2020-03-29 132700.png"  div align=center />

### 持久层技术解决方案

JDBC技术：
* Connection 
* PreparedStatement 
* ResultSet

 Spring的JdbcTemplate：
 * Spring中对jdbc的简单封装
Apache的DBUtils：
* 它和Spring的JdbcTemplate很像，也是对Jdbc的简单封装

以上这些都不是框架
* JDBC是规范
* Spring的JdbcTemplate和Apache的DBUti1s都只是工具类

### 回顾初学jdbc时与数据库交互语句
```java
public class JdbctTest {
    public static void main(String[] args) {
        Connection conn = null;
        PreparedStatement preparedStatement =null;
        ResultSet resultSet = null;


        try {
            //加载数据驱动
            Class.forName("com.mysql.jdbc.Driver");
            //获取连接
            conn = (Connection) DriverManager.getConnection("jdbc:mysql://localhost:3306/eesy","root","qaz12345");
            String sql = "select * from account where money>?";
            //预处理
            preparedStatement = (PreparedStatement) conn.prepareStatement(sql);
            preparedStatement.setFloat(1,1000);
            //执行查询，查询出结果集
            resultSet = preparedStatement.executeQuery();
            /*  execute：它能执行CRUD中的任意一种语句表示是否有结果集。有结桌集是true，没有false
                executeUpdate：它只能执行CUD语句，查询语句无法执行。他的返回值是影响数据库记录的行数
                executeQuery：它只能执行SELECT语句，无法执行增删改。执行结果封装的结果集ResultSet对象*/
            //遍历结果集
            while(resultSet.next()){
                System.out.println(resultSet.getInt("id")+""+ resultSet.getString("name")+""+resultSet.getFloat("money"));
            }

        } catch (ClassNotFoundException | SQLException e) {
            e.printStackTrace();
        }finally{
            if(resultSet!=null){
                try {
                    //释放资源
                    resultSet.close();
                    preparedStatement.close();
                    conn.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }
    }

}
```

## Mybatis框架
&emsp;mybatis是一个优秀的基于java的持久层框架，它内部封装了jdbc，使开发者**只需要关注sql语句本身，而不需要花费精力去处理加载驱动、创建连接、创建 statement等繁杂的过程**。
&emsp;mybatis通过xml或注解的方式将要执行的各种statement配置起来，并通过java对象和statement中sql的动态参数进行映射生成最终执行的sql语句，最后由mybatis框架执行sql并将结果映射为java对象并返回。
&emsp;采用 **ORM思想（Object Relational Mapping对象关系映射）** 解决了实体和数据库映射的问题，对jdbc进行了封装，屏蔽了jdbc api底层访问细节，使我们不用与jdbc api打交道，就可以完成对数据库的持久化操作 **（就是把数据库表和实体类及实体类的属性对应起来）**。
&emsp;为了我们能够更好掌握框架运行的内部过程，并且有更好的体验，下面我们将从自定义Mybatis框架开始来学习框架。此时我们将会体验框架从无到有的过程体验，也能够很好的综合前面阶段所学的基础。

## Mybatis入门
依赖
```xml
        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis</artifactId>
            <version>3.4.5</version>
        </dependency>
```

主配置
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
  PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
  "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
	<!-- 这里写配置内容 -->
</configuration>
```
映射文件
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
  PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
  "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="命名空间">
	<!-- SQL语句 -->
</mapper>
```

mybatis的环境搭建:
第一步：创建maven工程并导入坐标
第二步：创建实体类和dao的接口
第三步：创建Mybatis的主配置文件
第四步：创建映射配置文件(mybatis的映射配置文件位置必须和dao接口的包结构相同)

<img src="./pictures/Annotation 2020-03-29 180154.png"  div align=center />

### 入门实例（基于xml）
mybatis的入门案例（该实例的实体类变量名与数据库变量名保持一致）
第一步：读取配置文件
第二步：创建SqlSessionFactory工厂
第三步：创建SqlSession
第四步：创建Dao接口的**代理对象**
第五步：执行dao中的方法
第六步：释放资源

注意事项：
不要忘记在映射配置中告知mybatis要封装到哪个实体类中
配置的方式：指定实体类的全限定类名
```java
public class MybatisTest {
    /**
     * 入门案例
     * @param args
     */
    public static void main(String[] args) throws IOException {
        //1.读取配置文件
        InputStream in = Resources.getResourceAsStream("SqlMapConfig.xml");
        //2.创建SqlSessionFactory工厂
        SqlSessionFactoryBuilder builder = new SqlSessionFactoryBuilder();
        SqlSessionFactory factory = builder.build(in);

        //3.使用工厂生产SqlSession对象
        SqlSession session = factory.openSession();
        //4.使用SqlSession创建Dao接口的代理对象
        IUserDao userDao = session.getMapper(IUserDao.class);
        //5.使用代理对象执行方法
        List<User> users = userDao.findAll();
        for(User user:users){
            System.out.println(user);
        }
        //6.释放资源
        session.close();
        in.close();
    }
}
```
主配置
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!-- 这里写配置内容 -->
    <environments default="mysql">
        <environment id="mysql">
<!--            配置事务的类型-->
            <transactionManager type="JDBC"></transactionManager>
<!--            配置数据源（连接池）-->
                <dataSource type="POOLED">
    <!--                配置连接数据库的基本信息-->
                    <property name="driver" value="com.mysql.jdbc.Driver"/>
                    <property name="url" value="jdbc:mysql://localhost:3306/eesy"/>
                    <property name="username" value="root"/>
                    <property name="password" value="qaz12345"/>
                </dataSource>

        </environment>
    </environments>

<!--    指定映射配置文件的位置，映射配置文件指的是每个dao独立的配置文件-->
    <mappers>
        <mapper resource="day01_eesy_01MybatisBuild/dao/IUserDao.xml" />
    </mappers>
</configuration>
```
mapper
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="day01_eesy_01MybatisBuild.dao.IUserDao">
    <!-- SQL语句 -->
    <select id="findAll" resultType="day01_eesy_01MybatisBuild.domain.User">
        select * from user
    </select>
</mapper>
```
### 入门实例（基于注解）
把IUserDao.xml移除，在dao接口的方法上使用@Select注解，并且指定SQL语句同时需要在SqlMapConfig.xml中的mapper配置时，使用class属性指定dao接口的全限定类
测试的java文件不变，在接口文件中加入注解

```java
package day01_eesy_01MybatisBuild.dao;

import day01_eesy_01MybatisBuild.domain.User;
import org.apache.ibatis.annotations.Select;

import java.util.List;

public interface IUserDao {
    @Select("select * from user")
    List<User> findAll();
}

```
更改mapper的class
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!-- 这里写配置内容 -->
    <environments default="mysql">
        <environment id="mysql">
<!--            配置事务的类型-->
            <transactionManager type="JDBC"></transactionManager>
<!--            配置数据源（连接池）-->
                <dataSource type="POOLED">
    <!--                配置连接数据库的基本信息-->
                    <property name="driver" value="com.mysql.jdbc.Driver"/>
                    <property name="url" value="jdbc:mysql://localhost:3306/eesy"/>
                    <property name="username" value="root"/>
                    <property name="password" value="qaz12345"/>
                </dataSource>

        </environment>
    </environments>

<!--    指定映射配置文件的位置，映射配置文件指的是每个dao独立的配置文件-->
    <mappers>
        <mapper class="day01_eesy_01MybatisBuild.dao.IUserDao" />
    </mappers>
</configuration>
```

明确：
我们在实际开发中，都是越简便越好，所以都是采用不写dao实现类的方式。
不管使用XML还是注解配置。
但是Mybatis它是支持写dao实现类的。

<img src="./pictures/Annotation 2020-03-29 201451.png"  div align=center />

<img src="./pictures/Annotation 2020-03-29 214935.png"  div align=center />

