## Mybatis基本操作

### 数据库CRUD
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

<!--    保存用户-->
    <insert id="saveUser" parameterType="day01_eesy_01MybatisBuild.domain.User">
        insert into user(username,address,sex,birthday) values(#{username},#{address},#{sex},#{birthday});
    </insert>
<!--    更新-->
    <update id="updateUser" parameterType="day01_eesy_01MybatisBuild.domain.User">
        update user set username=#{username},address=#{address}, sex=#{sex}, birthday=#{birthday} where id=#{id}
    </update>
<!--    删除-->
    <delete id="deleteUser" parameterType="INT">
        delete from user where id= #{uid}
    </delete>
<!--    根据id查询用户-->
    <select id="findById" parameterType="INT" resultType="day01_eesy_01MybatisBuild.domain.User">
        select * from user where id = #{uid};
    </select>
<!--    根据名称模糊查询(传入实参需要符合模糊查询)-->
    <select id="findByName" parameterType="String" resultType="day01_eesy_01MybatisBuild.domain.User">
        select * from user where username like #{name}
    </select>
<!--    总记录数-->
    <select id="findTotal" resultType="INT">
        select count(id) from user;
    </select>
</mapper>
```

### Mybatis标签
mybatis主配置文件中的常用配置

#### properties标签
可以将property标签整合再用${name}作为引用值
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-03-30 235056.png"  div align=center />

可以在标签内部配置连接数据库的信息。也可以通过属性引用外部配置文件信息

属性值
resource属性：常用的
用于指定配置文件的位置，是按照类路径的写法来写，并且必须存在于类路径下。
url属性：
是要求按照Url的写法来写地址
URL:Uniform Resource Locator 统一资源定位符。它是可以唯一标识一个资源的位置。
它的写法：
http://localhost:8e8e/mybatisserver/demo1Servlet
协议 主机 端口 URI
(URI:Uniform Resource Identifier 统一资源标识符。它是在应用中可以唯一定位一个资源的。)
```xml
<properties resource="jdbcConfig.properties">
```

#### typeAliases标签 
typeAlias用于配置别名。type属性指定的是实体类全限定类名。alias属性指定别名，当指定了别名就再区分大小写.(可以在Mapper配置文件中使用)
```xml
<typeAliases>
    <typeAlias type="day01_eesy_01MybatisBuild.domain.User" alias="user"></typeAlias>
</typeAliases>
```
#### 子标签：package
1. 用于typeAliases标签 下
用于指定要配置别名的包，当指定之后，该包下的实体类都会注册别名，并且类名就是别名，不再区分大小写
```xml
<typeAliases>
    <package name="day01_eesy_01MybatisBuild.domain"></package>
</typeAliases>
```
2. 用于package标签是用于指定dao接口所在的包，当指定了之后就不需要在写resource或者class了
```xml
<mappers>
    <package name="day01_eesy_01MybatisBuild.dao"></package>
</mappers>
```
#### mapper配置 ：parameterType（输入类型） resultType（输出类型）
Mybatis使用ognl表达式解析对象字段的值，#{}或者${}括号中的值为pojo属性名称。


开发中通过pojo(实体类)传递查询条件，查询条件是综合的查询条件，不仅包括用户查询条件还包括其它的查询条件（比如将用户购买商品信息也作为查询条件），这时可以使用包装对象传递输入参数。Pojo类中包含pojo。

需求：根据用户名查询用户信息，查询条件放到QueryVo的user属性中。
```java
public class queryVo {
    private User user;

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }
}
```
```xml
<select id="findByName" parameterType="day01_eesy_01MybatisBuild.domain.queryVo" resultType="day01_eesy_01MybatisBuild.dao.IUserDao">
        select * from user where username like #{user.username}
</select>
```
```java
//测试方法
@Test
    public void testVo(){
        User user = new User();
        QueryVo vo = new QueryVo();
        user.setUsername("%王%");
        vo.setUser(user);

        List<User> users = userDao.findByVo(vo);

        for(User u:users){
            System.out.println(u);
        }
    }  
```

```xml
<select id="findByVo" parameterType="day01_eesy_01MybatisBuild.domain.QueryVo" resultType="day01_eesy_01MybatisBuild.domain.User">
        select * from user where username like #{user.username};
    </select>
```

### 封装问题
注意，当实体类属性与数据库表属性名不一致时，在windows系统下名字不区分大小写，此外不同名称无法进行匹配封装，即查询结果无法封装进入实体类。则需要起别名或配置对应关系:

起别名方式解析速度快，但写多条sql语句变得繁琐
```xml
<!--sql语句起别名-->
<select id="findAll" resultType="day01_eesy_01MybatisBuild.domain.User">
        select id as userId,username as userName,address as userAddress,sex as userSex,birthday as userBirthday from user;
</select>
```

```xml
<!--配置对应关系-->
<resultMap id="userMap" type="day01_eesy_01MybatisBuild.domain.User">
        <!--主键-->
        <id property="userId" column="id"></id>
        <!--非主键-->
        <result property="userName" column="username"></result>
</resultMap>
<!--使用配置好的Map-->
<select id="findAll" resultMap="userMap">
        select * from user;
</select>
```

### 条件查询
1. 使用if标签
根据传入的user对象什么属性不为空进行条件查询,条件where 1=1(永远为真)再用**if标签**（可用多个）输入条件注意test语句中要按sql语句的写法，但实际对象是java对象，注意要加上**and条件**
```xml
<select id="findUserByCondition" resultMap="userMap" parameterType="user">
    select * from user where 1=1
    <if test="username != nul1">
    and username=#{username}
    </if>
</select>
```
![image-20200426022936675](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200426022936675.png)


2. 使用where标签

```xml
<select id="findUserByCondition" resultMap="userMap" parameterType="user">
    select * from user 
    <where>
        <if test="username != null">
        and username=#{username}
        </if>
        <if test="userSex != null">
        and sex =#{userSex}
        </if>
    </where>
</select>
```
3. foreach标签
为了模拟在集合中遍历的sql语句如
```sql
select * from user where id in(41,42,43,46);
```

foreach标签用于遍历集合，它的属性：
collection：代表要遍历的集合元素，注意编写时不要写#{}
open：代表语句的开始部分
close：代表结束部分
item：代表遍历集合的每个元素，生成的变量名sperator代表分隔符
```xml
<!--queryVo有一个ids列表装的41，42，43，46-->
<select id="findUserByCondition" resultMap="userMap" parameterType="queryVo">
        select * from user
        <where>
            <if test="ids != null and ids.size()>0">
                <foreach collection="ids" open="and id in (" close=")" item="uid" separator=",">
                        #{uid}
                </foreach>
            </if>
        </where>
    </select>
```

#### 抽取重复的sql语句
注意分号会结束sql语句，一句话的sql不写分号也是可以的，若还有sql语句则会中断解析报错
```xml
<sq1 id="defaultuse">
select* from user;
</sql>

<select id="findAl1"resultMap="userMap">
<include refid="defaultuse"></include>
</select>
```

