### 多表查询
关系型数据库的表之间有一对一（身份证号和人），一对多/多对一（用户和订单关系），多对多（学生和老师）的关系，Mybatis把多对一关系看成了一对一（如果拿出每一个订单，他都只能属于一个用户。）

mybatis中的多表查询：
示例：用户和账户
&emsp;&emsp;一个用户可以有多个账户
&emsp;&emsp;一个账户只能属于一个用户（多个账户也可以属于同一个用户）

步骤：
>步骤：
1、建立两张表：用户表，账户表
&emsp;让用户表和账户表之间具备一对多的关系：需要使用外键在账户表中添加
2、建立两个实体类：用户实体类和账户实体类
&emsp;让用户和账户的实体类能体现出来一对多的关系
3、建立两个配置文件
    &emsp;用户的配置文件
    &emsp;账户的配置文件
4、实现配置：
&emsp;当我们查询用户时，可以同时得到用户下所包含的账户信息
&emsp;当我们查询账户时，可以同时得到账户的所属用户信息

```java
//主表实现类
public class  User implements Serializable {
    private Integer id;
    private String username;
    private Date birthday;
    private String sex;
    //一对多关系映射：主表实体应该保函从表实体的集合引用
    private List<Account> accounts;

    public List<Account> getAccounts() {
        return accounts;
    }

    public void setAccounts(List<Account> accounts) {
        this.accounts = accounts;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", birthday=" + birthday +
                ", sex='" + sex + '\'' +
                ", address='" + address + '\'' +
                '}';
    }

    public Date getBirthday() {
        return birthday;
    }

    public void setBirthday(Date birthday) {
        this.birthday = birthday;
    }

    public String getSex() {
        return sex;
    }

    public void setSex(String sex) {
        this.sex = sex;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    private String address;
}

```
```java
//从表实现类
public class Account implements Serializable {
    private Integer id;
    private Integer uid;
    private Double money;

    private User user;

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    @Override
    public String toString() {
        return "Account{" +
                "id=" + id +
                ", uid=" + uid +
                ", money=" + money +
                '}';
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getUid() {
        return uid;
    }

    public void setUid(Integer uid) {
        this.uid = uid;
    }

    public Double getMoney() {
        return money;
    }

    public void setMoney(Double money) {
        this.money = money;
    }
}
```
查询账户表关联所有的用户的信息（一对一）
property实体类属性名
column数据库表的字段名
select语句里注意是resultMap
```xml
<resultMap id="accountUserMap" type="account">
        <id property="id" column="aid"></id>
        <result property="uid" column="uid"></result>
        <result property="money" column="money"></result>
        <!--一对一的关系映射：配置封装user的内容，javaType封装到哪个类-->
        <association property="user" column="uid" javaType="user">
            <id property="id" column="id"></id>
            <result column="username" property="username"></result>
            <result column="address" property="address"></result>
            <result column="sexy" property="sex"></result>
            <result column="birthday" property="birthday"></result>
        </association>

    </resultMap>


    <select id="findAll" resultMap="accountUserMap">
        select a.*,u.username,u.address from account a, user u where u.id=a.uid;
    </select>
```
一对多关系，查询对应账户（注释的语句并没有起aid别名所以没有封装到account.id中）
```xml
<resultMap id="userAccountMap" type="user">
        <id property="id" column="id"></id>
        <result column="username" property="username"></result>
        <result column="address" property="address"></result>
        <result column="sex" property="sex"></result>
        <result column="birthday" property="birthday"></result>
        <!--account集合映射-->
        <collection property="accounts"  ofType ="account" >
            <id  column="aid" property="id" ></id>
            <result  column="uid" property="uid" ></result>
            <result column="money" property="money" ></result>
        </collection>

    </resultMap>
<!--     SQL语句 -->
    <select id="findAll" resultMap="userAccountMap">
    <!--     select u.*,a.id as aid,a.uid,a.money from user u left outer join account a on u.id=a.uid -->
        
        select * from user u left outer join (select x.id as aid,uid,money from account x) a on u.id=a.uid;
    </select>
```

多对多关系也是同理，让实现类各自持有对方的一个集合引用（通过中间表两次左外连接）
<img src="./pictures/Annotation 2020-03-31 162748.png"  div align=center />
