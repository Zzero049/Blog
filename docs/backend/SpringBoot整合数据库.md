# SpringBoot整合数据库

## 数据校验

```java
@Data
public class User {
    @NotNull(message = "id不能为空")
    private Long id;
    @NotEmpty(message = "姓名不能为空")
    @Length(min = 2,message = "姓名⻓度不能⼩于2位")
    private String name;@Min(value = 16,message = "年龄必须⼤于16岁")
    private int age;
}
```

```java
@GetMapping("/validator")
public void validatorUser(@Valid User user,BindingResult bindingResult){
        System.out.println(user);
        if(bindingResult.hasErrors()){
        List<ObjectError> list=bindingResult.getAllErrors();
        for(ObjectError objectError:list){
        System.out.println(objectError.getCode()+"-
        " + objectError.getDefaultMessage());
        }
        }
}
```

## Spring Boot 整合 JDBC

- pom.xml

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.11</version>
</dependency>
```

- application.yml

```yaml
server:
  port: 9090
spring:
  thymeleaf:
    prefix: classpath:/templates/
    suffix: .html
    mode: HTML5
    encoding: UTF-8
  datasource:
    url: jdbc:mysql://localhost:3306/test?useUnicode=true&characterEncoding=UTF-8
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver
```

- User

```java
package com.southwind.entity;

import lombok.Data;
import org.hibernate.validator.constraints.Length;

import javax.validation.constraints.Min;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

@Data
public class User {
    @NotNull(message = "id不能为空")
    private Long id;
    @NotEmpty(message = "姓名不能为空")
    @Length(min = 2,message = "姓名长度不能小于2位")
    private String name;
    @Min(value = 60,message = "成绩必须大于60分")
    private double score;
}
```

- UserRepository

```java
package com.southwind.repository;

import com.southwind.entity.User;

import java.util.List;

public interface UserRepository {
    public List<User> findAll();
    public User findById(long id);
    public void save(User user);
    public void update(User user);
    public void deleteById(long id);
}
```

- UserRepositoryImpl

```java
package com.southwind.repository.impl;

import com.southwind.entity.User;
import com.southwind.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class UserRepositoryImpl implements UserRepository {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Override
    public List<User> findAll() {
        return jdbcTemplate.query("select * from user",new BeanPropertyRowMapper<>(User.class));
    }

    @Override
    public User findById(long id) {
        return jdbcTemplate.queryForObject("select * from user where id = ?",new Object[]{id},new BeanPropertyRowMapper<>(User.class));
    }

    @Override
    public void save(User user) {
        jdbcTemplate.update("insert into user(name,score) values(?,?)",user.getName(),user.getScore());
    }

    @Override
    public void update(User user) {
        jdbcTemplate.update("update user set name = ?,score = ? where id = ?",user.getName(),user.getScore(),user.getId());
    }

    @Override
    public void deleteById(long id) {
        jdbcTemplate.update("delete from user where id = ?",id);
    }
}
```

- Handler

```java
package com.southwind.controller;

import com.southwind.entity.User;
import com.southwind.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/user")
public class UserHandler {

    @Autowired
    private UserRepository userRepository;

    @GetMapping("/findAll")
    public List<User> findAll(){
        return userRepository.findAll();
    }

    @GetMapping("/findById/{id}")
    public User findById(@PathVariable("id") long id){
        return userRepository.findById(id);
    }

    @PostMapping("/save")
    public void save(@RequestBody User user){
        userRepository.save(user);
    }

    @PutMapping("/update")
    public void update(@RequestBody User user){
        userRepository.update(user);
    }

    @DeleteMapping("/deleteById/{id}")
    public void deleteById(@PathVariable("id") long id){
        userRepository.deleteById(id);
    }
}
```

## Spring Boot 整合 MyBatis

- pom.xml 

```xml
<dependency>
  <groupId>org.mybatis.spring.boot</groupId>
  <artifactId>mybatis-spring-boot-starter</artifactId>
  <version>1.3.1</version>
</dependency>
```

- application.yml

```yaml
server:
  port: 9090
spring:
  thymeleaf:
    prefix: classpath:/templates/
    suffix: .html
    mode: HTML5
    encoding: UTF-8
  datasource:
    url: jdbc:mysql://localhost:3306/test?useUnicode=true&characterEncoding=UTF-8
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver
mybatis:
  mapper-locations: classpath:/mapping/*.xml
  type-aliases-package: com.southwind.entity
```

- UserRepository

```java
package com.southwind.mapper;

import com.southwind.entity.User;

import java.util.List;

public interface UserRepository {
    public List<User> findAll(int index,int limit);
    public User findById(long id);
    public void save(User user);
    public void update(User user);
    public void deleteById(long id);
    public int count();
}
```

- UserRepository.xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
        <!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.southwind.mapper.UserRepository">

    <select id="findAll" resultType="User">
        select * from user limit #{param1},#{param2}
    </select>

    <select id="count" resultType="int">
        select count(id) from user
    </select>

    <select id="findById" parameterType="long" resultType="User">
        select * from user where id = #{id}
    </select>

    <insert id="save" parameterType="User">
        insert into user(name,score) values(#{name},#{score})
    </insert>

    <update id="update" parameterType="User">
        update user set name = #{name},score = #{score} where id = #{id}
    </update>

    <delete id="deleteById" parameterType="long">
        delete from user where id = #{id}
    </delete>
</mapper>
```

- User

```java
package com.southwind.entity;

import lombok.Data;
import org.hibernate.validator.constraints.Length;

import javax.validation.constraints.Min;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

@Data
public class User {
    @NotNull(message = "id不能为空")
    private Long id;
    @NotEmpty(message = "姓名不能为空")
    @Length(min = 2,message = "姓名长度不能小于2位")
    private String name;
    @Min(value = 60,message = "成绩必须大于60分")
    private double score;
}
```

- Handler

```java
package com.southwind.controller;
import com.southwind.entity.User;
import com.southwind.mapper.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;

@Controller
@RequestMapping("/mapper")
public class UserMapperHandler {

    @Autowired
    private UserRepository userRepository;
    private int limit = 10;

    @GetMapping("/findAll/{page}")
    public ModelAndView findAll(@PathVariable("page") int page){
        ModelAndView modelAndView = new ModelAndView();
        int index = (page-1)*limit;
        modelAndView.setViewName("show");
        modelAndView.addObject("list",userRepository.findAll(index,limit));
        modelAndView.addObject("page",page);
        //计算总页数
        int count = userRepository.count();
        int pages = 0;
        if(count%limit == 0){
            pages = count/limit;
        }else{
            pages = count/limit+1;
        }
        modelAndView.addObject("pages",pages);
        return modelAndView;
    }

    @GetMapping("/deleteById/{id}")
    public String deleteById(@PathVariable("id") long id){
        userRepository.deleteById(id);
        return "redirect:/mapper/findAll/1";
    }

    @GetMapping("/findById")
    public ModelAndView findById(@RequestParam("id") long id){
        ModelAndView modelAndView = new ModelAndView();
        modelAndView.addObject("user",userRepository.findById(id));
        modelAndView.setViewName("update");
        return modelAndView;
    }

    @PostMapping("/update")
    public String update(User user){
        userRepository.update(user);
        return "redirect:/mapper/findAll/1";
    }

    @PostMapping("/save")
    public String save(User user){
        userRepository.save(user);
        return "redirect:/mapper/findAll/1";
    }

    @GetMapping("/redirect/{name}")
    public String redirect(@PathVariable("name") String name){
        return name;
    }
}
```

- HTML

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form action="/mapper/save" method="post">
        用户姓名：<input type="text" name="name" /><br/>
        用户成绩：<input type="text" name="score" /><br/>
        <input type="submit" value="提交"/>
    </form>
</body>
</html>
```



```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form action="/mapper/update" method="post">
        用户ID：<input type="text" name="id" th:value="${user.id}" readonly/><br/>
        用户姓名：<input type="text" name="name" th:value="${user.name}" /><br/>
        用户成绩：<input type="text" name="score" th:value="${user.score}" /><br/>
        <input type="submit" value="提交"/>
    </form>
</body>
</html>
```



```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript" th:src="@{/jquery-3.3.1.min.js}"></script>
    <script type="text/javascript">
        $(function(){
            $("#first").click(function(){
                var page = $("#page").text();
                page = parseInt(page);
                if(page == 1){
                    return false;
                }
                window.location.href="/mapper/findAll/1";
            });
            $("#previous").click(function(){
                var page = $("#page").text();
                page = parseInt(page);
                if(page == 1){
                    return false;
                }
                page = page-1;
                window.location.href="/mapper/findAll/"+page;
            });
            $("#next").click(function(){
                var page = $("#page").text();
                var pages = $("#pages").text();
                if(page == pages){
                    return false;
                }
                page = parseInt(page);
                page = page+1;
                window.location.href="/mapper/findAll/"+page;
            });
            $("#last").click(function(){
                var page = $("#page").text();
                var pages = $("#pages").text();
                if(page == pages){
                    return false;
                }
                window.location.href="/mapper/findAll/"+pages;
            });
        });
    </script>
</head>
<body>
    <h1>用户信息</h1>
    <table>
        <tr>
            <th>用户ID</th>
            <th>用户名</th>
            <th>成绩</th>
            <th>操作</th>
        </tr>
        <tr th:each="user:${list}">
            <td th:text="${user.id}"></td>
            <td th:text="${user.name}"></td>
            <td th:text="${user.score}"></td>
            <td>
                <a th:href="@{/mapper/deleteById/{id}(id=${user.id})}">删除</a>
                <a th:href="@{/mapper/findById(id=${user.id})}">修改</a>
            </td>
        </tr>
    </table>
    <a id="first" href="javascript:void(0)">首页</a>
    <a id="previous" href="javascript:void(0)">上一页</a>
    <span id="page" th:text="${page}"></span>/<span id="pages" th:text="${pages}"></span>
    <a id="next" href="javascript:void(0)">下一页</a>
    <a id="last" href="javascript:void(0)">尾页</a><br/>
    <a href="/mapper/redirect/save">添加用户</a>
</body>
</html>
```

## Spring Boot 与Spring Data JPA整合

JPA Hibernate框架就是一个JPA的实现。

Spring DataJPA不是对JPA规范的具体实现，本身是一个抽象层，底层是Hibernate实现的

1、pom.xml导入依赖

```xml
<parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.0.7.RELEASE</version>
    </parent>
    <dependencies>
        <!-- web-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.8</version>
        </dependency>
        
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
        </dependency>
      
       
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
    </dependencies>
```

2、创建Student实体类

```java
@Data
@Entity 
public class Student {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)//表示自增
    private Long id;
    @Column
    private String age;
    @Column
    private String name;

}
```

3、创建StudentRepository接口。

```java
public interface StudentRepository extends JpaRepository<Student,Long> {//实体类型，主键类型
//    由于需要返回类型是Student的findById(返回类型是Optional)，重新声明（符合命名规则），自动匹配
    public Student getById(Long id);
}
```

4、创建StudentHandler，注入StudentRepository

```java
@RestController
public class StudentHandler {
    //大部分增删改查方法repository都有,但是返回类型不同需要在Repository重新定义
    @Autowired
    private StudentRepository repository;

    @GetMapping("/findAll")
    public List<Student> findAll(){
        return repository.findAll();
    }

    @GetMapping("/findById/{id}")
    public Student findById(@PathVariable("id")Long id){
        return repository.getById(id);
    }

    @PostMapping("/save")
    public Student save(@RequestBody Student student){
        return repository.save(student);
    }
    @PutMapping("/update")
    public Student update(@RequestBody Student student){
        return repository.save(student);
    }

    @DeleteMapping("/delete/{id}")
    public void deleteById(@PathVariable("id") Long id){
        repository.deleteById(id);
    }
}

```

5、配置yml

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/testjdbc?useUnicode=true&characterEncoding=UTF-8
    username: root
    password: qaz12345
    driver-class-name: com.mysql.jdbc.Driver
  jpa:
    show-sql: true
    properties:
      hibernate: 
        format_sql: true # 格式化输出
```



## Spring Boot与MongoDB整合

MongoDB数据格式

```
BSON类似于JSON的一种数据格式
{
	"_id":Objectid("Scfdd7ce7e8642046e75f77a"),
	"student_age":20,
	"student_name":"张三",
	"_class":"com.southwind.entity.Student"
}
```

pom.xml

```xml
	<parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.0.7.RELEASE</version>
    </parent>
	<dependencies>
		<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-mongodb</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
        </dependency>
     </dependencies>
```

2、创建实体类

```java
@Data
@Document(collection = "my_student") //mongoDB的表名，下面value是mongoDB的属性名
public class Student {
    @Id
    private String id;
    @Field(value = "student_age")
    private String age;
    @Field(value = "student_name")
    private String name;
    
}
```

3、创建StudentRepository接口，与Spring DataJPA一样，只需要定义不需要实现。

```java
package application.dao;

import application.entity.Student;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface StudentRepository extends MongoRepository<Student,String> {//实体类型，主键类型
//    由于需要返回类型是Student的findById，重新声明（符合命名规则），自动匹配
    public Student getById(String id);

}

```

4、创建Handle处理请求

```java
package application.controller;

import application.dao.StudentRepository;
import application.entity.Student;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class StudentHandler {
    //大部分增删改查方法repository都有,但是返回类型不同需要在Repository重新定义
    @Autowired
    private StudentRepository repository;

    @GetMapping("/findAll")
    public List<Student> findAll(){
        return repository.findAll();
    }

    @GetMapping("/findById/{id}")
    public Student findById(@PathVariable("id")String id){
        return repository.getById(id);
    }

    @PostMapping("/save")
    public Student save(@RequestBody Student student){
        return repository.save(student);
    }
    @PutMapping("/update")
    public Student update(@RequestBody Student student){
        return repository.save(student);
    }

    @DeleteMapping("/delete/{id}")
    public void deleteById(@PathVariable("id") String id){
        repository.deleteById(id);
    }
}

```

5、配置application.yml

```yaml
spring:
  data:
    mongodb:
      database: my_test
      host: 127.0.0.1
      port: 12345
```



##  Spring Boot与Redis的整合

1、pom.xml

```xml
		<parent>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-parent</artifactId>
            <version>2.1.5.RELEASE</version>
        </parent>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-web</artifactId>
            </dependency>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-data-redis</artifactId>
            </dependency>
            <dependency>
                <groupId>org.apache.commons</groupId>
                <artifactId>commons-pool2</artifactId>
            </dependency>
            <dependency>
                <groupId>org.projectlombok</groupId>
                <artifactId>lombok</artifactId>
            </dependency>
        </dependencies>
```

2、创建实体类，实现序列化接⼝，否则⽆法存⼊ Redis 数据库。  

```java
package com.southwind.entity;
import lombok.Data;
import java.io.Serializable;
import java.util.Date;
@Data
public class Student implements Serializable {
	private Integer id;
	private String name;
	private Double score;
	private Date birthday;
}
```

3、创建控制器

```java
package com.southwind.controller;
import com.southwind.entity.Student;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.*;
@RestController
public class StudentHandler {
    @Autowired
    private RedisTemplate redisTemplate;
    @PostMapping("/set")
    public void set(@RequestBody Student student){
        redisTemplate.opsForValue().set("student",student);
    }
    @GetMapping("/get/{key}")
    public Student get(@PathVariable("key") String key){
        return (Student) redisTemplate.opsForValue().get(key);
    }
    @DeleteMapping("/delete/{key}")
    public boolean delete(@PathVariable("key") String key){
        redisTemplate.delete(key);
        return redisTemplate.hasKey(key);
    }
}
```

4、创建配置⽂件 application.yml  

```yaml
spring:
  redis:
    database: 0
    host: localhost
    port: 6379
```

5、创建启动类  

```java
package com.southwind;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
@SpringBootApplication
public class Application {
	public static void main(String[] args) {
		SpringApplication.run(Application.class,args);
	}
}
```

### redis5种数据类型封装使用

- 字符串

```java
@GetMapping("/string")
public String stringTest(){
        redisTemplate.opsForValue().set("str","Hello World");
        String str = (String) redisTemplate.opsForValue().get("str");
        return str;
        }
```

- 列表  

```java
@GetMapping("/list")
public List<String> listTest(){
        ListOperations<String, String> listOperations=redisTemplate.opsForList();
        listOperations.leftPush("list","Hello");
        listOperations.leftPush("list","World");
        listOperations.leftPush("list","Java");
        List<String> list=listOperations.range("list",0,2);
        return list;
        }
```

- 集合

```java
@GetMapping("/set")
public Set<String> setTest(){
        SetOperations<String, String> setOperations=redisTemplate.opsForSet();
        setOperations.add("set","Hello");
        setOperations.add("set","Hello");
        setOperations.add("set","World");
        setOperations.add("set","World");
        setOperations.add("set","Java");
        setOperations.add("set","Java");
        Set<String> set=setOperations.members("set");
        return set;
        }
```

- 有序集合

```java
@GetMapping("/zset")
public Set<String> zsetTest(){
        ZSetOperations<String,String> zSetOperations = redisTemplate.opsForZSet();
        zSetOperations.add("zset","Hello",1);
        zSetOperations.add("zset","World",2);
        zSetOperations.add("zset","Java",3);
        Set<String> set = zSetOperations.range("zset",0,2);
        return set;
        }
```

- 哈希
  HashMap key value

  HashOperations key hashkey value

  key 是每⼀组数据的 ID， hashkey 和 value 是⼀组完整的 HashMap 数据，通过 key 来区分不同的
  HashMap。  

```java
HashMap hashMap1 = new HashMap();
hashMap1.put(key1,value1);
HashMap hashMap2 = new HashMap();
hashMap2.put(key2,value2);
HashMap hashMap3 = new HashMap();
hashMap3.put(key3,value3);
HashOperations<String,String,String> hashOperations =
redisTemplate.opsForHash();
hashOperations.put(hashMap1,key1,value1);
hashOperations.put(hashMap2,key2,value2);
hashOperations.put(hashMap3,key3,value3);
```



