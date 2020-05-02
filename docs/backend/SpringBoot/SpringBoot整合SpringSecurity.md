# Spring Boot 整合 Spring Security  

常用的框架有Shiro、 Spring Security  

1、pom.xml添加依赖

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.0.7.RELEASE</version>
  </parent>

  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-thymeleaf</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
  </dependencies>
```

2、创建 Handler  

```java
@Controller
public class HelloHandler {
	@GetMapping("/index")
	public String index(){
		return "index";
	}
}
```

3、创建 HTML  

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>Hello World</h1>
</body>
</html>
```

4、创建 application.yml  

```yaml
spring:
  thymeleaf:
    prefix: classpath:/templates/
    suffix: .html
```

5、创建启动类 Application  

```java
@SpringBootApplication
public class application {
    public static void main(String[] args) {
        SpringApplication.run(application.class,args);
    }
}

```

由于项目导入了安全框架的依赖，如果没有登录，会自动跳转到一个页面

![image-20200502145055075](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200502145055075.png)

控制台会自动生成密码，用户名默认为user

![image-20200502145330148](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200502145330148.png)



6、设置自定义的密码

```yaml
spring:
  thymeleaf:
    prefix: classpath:/templates/
    suffix: .html
  security:
    user:
      name: admin
      password: 123
```



## 权限管理

定义两个 HTML 资源： index.html、 admin.html，同时定义两个⻆⾊ ADMIN 和 USER， ADMIN 拥有
访问 index.html 和 admin.html 的权限， USER 只有访问 index.html 的权限。(权限赋予角色，角色赋予用户)

7、创建 SecurityConfig 类  ，继承WebSecurityConfigurerAdapter，重写两个configure方法

```java
@Configuration
@EnableWebSecurity
public class EcurityConfig extends WebSecurityConfigurerAdapter {
    /**
     * 该方法添加账户和角色
     * @param auth
     * @throws Exception
     */
    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws
            Exception {
        auth.inMemoryAuthentication().passwordEncoder(new MyPasswordEncoder())
                .withUser("user").password(new
                MyPasswordEncoder().encode("000")).roles("USER")    //添加了一个账户账户名为user，密码000，角色是USER
                .and()//追加一个
                .withUser("admin").password(new
                MyPasswordEncoder().encode("123")).roles("ADMIN","USER"); //添加了一个账户账户名为admin，密码123，角色是USER和ADMIN
    }

    /**
     * 角色和权限管理
     * @param http
     * @throws Exception
     */
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests().antMatchers("/admin").hasRole("ADMIN")//地址是admin进行ADMIN角色判断
                .antMatchers("/index").access("hasRole('ADMIN') or hasRole('USER')")
                        .anyRequest().authenticated()   //权限验证
                        .and()
                        .formLogin()
                        .loginPage("/login")    //自定义登录页面
                        .permitAll()            //登录页面不需要验证角色权限
                        .and()
                        .logout()
                        .permitAll()            //退出页面不用角色权限验证
                        .and()
                        .csrf()                 
                        .disable();
    }
}
```

8、创建MyPasswordEncoder类继承PasswordEncoder

```java
public class MyPasswordEncoder implements PasswordEncoder {
    @Override
    public String encode(CharSequence charSequence) {
        return charSequence.toString();
    }

    @Override
    public boolean matches(CharSequence charSequence, String s) {
        return s.equals(charSequence);
    }
}
```

9、修改 Handler  

```java
@Controller
public class HelloHandler {
    @GetMapping("/index")
    public String index(){
        return "index";
    }
    @GetMapping("/admin")
    public String admin(){
        return "admin";
    }
    @GetMapping("/login")
    public String login(){
        return "login";
    }
}
```

10、login.html  

```html
<!DOCTYPE html>
<!--需要th-->
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form th:action="@{/login}" method="post">
    ⽤户名： <input type="text" name="username"/><br/>
    密码： <input type="text" name="password"/><br/>
    <input type="submit" value="登录"/>
</form>
</body>
</html>
```

11、index.html  

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>Hello World</h1>
<form action="/logout" method="post">
    <input type="submit" value="退出"/>
</form>
</body>
</html>
```

12、admin.html  

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>后台管理系统</h1>
<form action="/logout" method="post">
    <input type="submit" value="退出"/>
</form>
</body>
</html>
```



访问index会自动跳转到login页面，输入写好的用户名密码，登录成功

![image-20200502151916911](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200502151916911.png)

![image-20200502151639633](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200502151639633.png)

![image-20200502151648612](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200502151648612.png)



访问admin，也会自动跳转到login页面

![image-20200502151952611](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200502151952611.png)

![image-20200502152008947](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200502152136831.png)

![image-20200502152053489](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200502152008947.png)

![image-20200502152136831](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200502152053489.png)