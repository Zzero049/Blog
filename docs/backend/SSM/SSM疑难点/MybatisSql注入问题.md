### SQL 注入攻击

首先了解下概念，什么叫SQL 注入：

> SQL注入攻击，简称SQL攻击或注入攻击，是发生于应用程序之数据库层的安全漏洞。简而言之，是在输入的字符串之中注入SQL指令，在设计不良的程序当中忽略了检查，那么这些注入进去的指令就会被数据库服务器误认为是正常的SQL指令而运行，因此遭到破坏或是入侵。

最常见的就是我们在应用程序中使用字符串联结方式组合 SQL 指令，有心之人就会写一些特殊的符号，恶意篡改原本的 SQL 语法的作用，达到注入攻击的目的。

举个栗子：

比如验证用户登录需要 username 和 password，编写的 SQL 语句如下：

```
select * from user where (name = '"+ username +"') and (pw = '"+ password +"');
```

username 和 password 字段被恶意填入

```
username = "1' OR '1'='1";
```

与

```
password = "1' OR '1'='1";
```

将导致原本的 SQL 字符串被填为：

```
select * from user where (name = '1' or '1'='1') and (pw = '1' or '1'='1');
```

实际上运行的 SQL 语句将变成：

```
select * from user;
```

也就是不再需要 username 和 password 账密即达到登录的目的，结果不言而喻。

### mybatis 解决 SQL 注入问题

我们使用 mybatis 编写 SQL 语句时，难免会使用模糊查询的方法，mybatis 提供了两种方式 `#{}` 和 `${}` 。

- `#{value}` 在预处理时，会把参数部分用一个占位符 ? 替代，其中 value 表示接受输入参数的名称。能有效解决 SQL 注入问题
- `${}` 表示使用拼接字符串，将接受到参数的内容不加任何修饰符拼接在 SQL 中，使用`${}`拼接 sql，将引起 SQL 注入问题。

举个例子：

1 查询数据库 sample 表 user 中的记录，我们故意使用特殊符号，看能否引起 SQL 注入。使用 mybatis 在 mapper.xml 配置文件中编写 SQL 语句，我们先采用拼接字符串形式，看看结果如何：

```
 <select id="findUserByName" parameterType="java.lang.String" resultType="cn.itcast.mybatis.po.User">
        <!-- 拼接 MySQL,引起 SQL 注入 -->
        SELECT * FROM user WHERE username LIKE '%${value}%'
    </select>
```

注意在配置文件中编写 SQL 语句时，后边不需要加分号。

调用配置文件，编写测试文件，查询数据库内容，采用特殊符号，引起 SQL 注入：

```
    @Test
    public void testFindUserByName() throws Exception{

        SqlSession sqlSession=sqlSessionFactory.openSession();

        //创建UserMapper代理对象
        UserMapper userMapper=sqlSession.getMapper(UserMapper.class);

        //调用userMapper的方法
        List<User> list=userMapper.findUserByName("' or '1'='1");

        sqlSession.close();

        System.out.println(list);
    }
}
```

运行结果如下图所示：

![img](http://wx1.sinaimg.cn/mw690/007el5a4gy1fujgmcak54j30sr06zgnd.jpg)

可以看到执行语句其实变为了

```
select * from user
```

将user 表中的全部记录打印出来了。发生了 SQL 注入。

2 如果将配置文件中的 SQL 语句改成 `#{}` 形式，可避免 SQL 注入。

```
 <select id="findUserByName" parameterType="java.lang.String" resultType="cn.itcast.mybatis.po.User">
        <!-- 使用 SQL concat 语句,拼接字符串,防止 SQL 注入 -->
        SELECT * FROM USER WHERE username LIKE CONCAT('%',#{value},'%' )
    </select>
```

再次运行测试程序，控制台输出如下：

![img](http://wx1.sinaimg.cn/mw690/007el5a4gy1fujgsn6g4mj30rz06c404.jpg)

可以看到程序中参数部分用 ? 替代了，很好地解决了 SQL 语句的问题，防止了 SQL 注入。查询结果将为空。