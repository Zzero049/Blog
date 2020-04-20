## Mybatis注解开发

### 单表查询
在mybatis中针对CRUD一共有四个注解,写在dao接口的方法上面
@SELECT @INSERT @UPDATE @DELETA

语句与xml的是一样的，xml与注解不能同时使用，否则报错

```java
public interface IUserDao {
    @Select("select * from user")
    List<User> findAll();

}
```

当表与实体类属性名不同时
```java
//该对应关系名称为userMap
@Select("select *from user")
@Results(id="userMap" value={
    @Result(id=true,column="id",property="userId"),
    @Result(column="username",property="userName"),
    @Result(column="address",property ="userAddress"),
    @Result(column="sex",property="userSex"),
    @Result(column="birthday",property="userBirthday"), 
})
List<User> findAll();

@Select("select * from user where id=#{id}")
@ResultMap(value={"userMap"})
User findById(Integer userId);
```

### 多表查询
查询所有账户，并且获取每个账户所属的用户信息(一对一)
```java
//accountDao
@Select("select * from account")
@Results(id="accountMap",value={
    @Result(id=true，column="id",property="id"),
    @Result(column="uid",property="uid"),
    @Result(column="money",property="money"),
    @Result(property="user",column="uid",one=@One(select="com.itheima.dao.IUserDao.findById",fetchType=FetchType.EAGER）)})//立即加载
List<Account>findAll();

@Select("select * from account where uid=#{userId}")
List<Account> findAccountByUid(Integer userId);
```
根据用户id查询账户信息(一对多)

```java
@Select("select *from user")
@Results(id="userMap" value={
    @Result(id=true,column="id",property="userId"),
    @Result(column="username",property="userName"),
    @Result(column="address",property ="userAddress"),
    @Result(column="sex",property="userSex"),
    @Result(column="birthday",property="userBirthday"), 
    @Result(property="accounts",column="id",many = @Many(select="com.itheima.dao.IAccountDao.findAccountByUid",fetchType=FetchType.LAZY)//延迟加载
})
List<User> findAll();


@Select("select * from user where id=#{userId}")
List<Account> findById(Integer userId);
```

注意Result注解下的one 和many以及加载方式fetchType即可

#### 开启二级缓存

```java
@CacheNamespace(blocking = true)
public interface IUserDao {
    @Select("select * from user")
    List<User> findAll();

}
```