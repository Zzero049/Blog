## Mybatis的延迟加载
问题：在一对多中，当我们有一个用户，它有100个账户。
&emsp;&emsp;在查询用户的时候，要不要把关联的账户查出来？
&emsp;&emsp;在查询账户的时候，要不要把关联的用户查出来？

&emsp;在查询用户时，用户下的账户信息应该是，什么时候使用，什么时候才查询。
&emsp;在查询账户时，账户的所属用户信息应该是随着账户查询时一起查询出来。

**延迟加载**
&emsp;在真正使用数据时才发起查询，不用的时候不查询。按需加载（懒加载）
**立即加载**
&emsp;不管用不用，只要一调用方法，马上发起查询。（两张表一起查，即内外连接查询）

一对多，多对多：通常情况下我们都是采用延迟加载。（一个人有很多账户，不一定每次都要显示）
多对一，一对一：通常情况下我们都是采用立即加载。(多个账户一个人，显示该账户的用户)

一对一的关系映射：配置封装user的内容
associateion标签的属性
select属性指定的内容：查询用户的唯一标识：
column属性指定的内容：用户根据id查询时，所需要的参数的值

```xml
<!--accountDao.xml-->
<resultMap id="userAccountMap" type="user">
        <id property="id" column="id"></id>
        <result column="username" property="username"></result>
        <result column="address" property="address"></result>
        <result column="sex" property="sex"></result>
        <result column="birthday" property="birthday"></result>
    <association property="user" column="uid" javaType="user" select="com.itheima.dao.IUserDao.findById"></association>
    <!--findById是userDao的方法-->
</resultMap>

<select id="findAll" resultMap="userAccountMap">
select * from account
</select>

```

```xml
<！--主配置文件参数-->
<settings>
<！--开启Mybatis支持延迟加载-->
<setting name="lazyLoadingEnabled" value="true"/>
<setting name="aggressivelazyLoading" value="false" ></setting>
</settings>
```
实际上延迟加载是配置文件在resultMap的assciation或collection标签下标明调用了对方的一个方法

## Mybatis缓存
什么是缓存
* 存在于内存中的临时数据。

为什么使用缓存
* 减少和数据库的交互次数，提高执行效率。
什么样的数据能使用缓存，什么样的数据不能使用|
    * 适用于缓存：
&emsp;&emsp;&emsp;经常查询并且不经常改变的。
&emsp;&emsp;&emsp;数据的正确与否对最终结果影响不大的。
    * 不适用于缓存：
&emsp;&emsp;&emsp;经常改变的数据
&emsp;&emsp;&emsp;数据的正确与否对最终结果影响很大的。
&emsp;&emsp;&emsp;例如：商品的库存，银行的汇率，股市的牌价。

Mybatis中的一级缓存和二级缓存
* 一级缓存：它指的是Mybatis中SqlSession对象的缓存。


    * 当我们执行查询之后，查询的结果会同时存入到SqlSession为我们提供一块区域中。
    * 该区域的结构是一个Map。当我们再次查询同样的数据，mybatis会先去sqlsession中查询是否有，有的话直接拿出来用。
    * 当SqlSession对象消失时，mybatis的一级缓存也就消失了。
    * SqlSession对象有clearCache()方法主动清空缓存
    * 一级缓存是Sqlsession 范围的缓存，当调用Sqlsession的修改，添加，删除，commit()，close()等方法时，就会清空一级缓存。
    <br></br>
* 二级缓存：它指的是Mybatis中SqlSessionFactory对象的缓存。由同一个SqlSessionFactory对象创建的SqlSession共享其缓存。
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-04-01 155247.png"  div align=center />
    * 二级缓存的使用步骤：
第一步：让Mybatis框架支持二级缓存（在SqlMapConfig.xml中配置）
        ```xml
        <!--实际上默认开启-->
            <settings>
            <setting name="cacheEnabled" value="true"/>
            </settings>
        ```
        第二步：让当前的映射文件支持二级缓存（在IUserDao.xml中配置）
        第三步：让当前的操作支持二级缓存（在select标签中配置）

    ```xml
    <!--开启user支持二级缓存-->
    <cache/>

    <！--根据id查询用户-->
    <select id="findById" parameterType="INT"  resultType="user" useCache="true">
    select * from user where id=#{uid}
    </select>
    ```

    注意，二级缓存中存的是数据而不是对象，获取对象则是把缓存中数据给新的对象