# SpringBoot2 基础入门

本篇思维导图如下：

![](https://gitee.com/zero049/MyNoteImages/raw/master/SpringBoot2基础入门.png)



## Spring和SpringBoot的关系

`Spring`框架为开发`Java`应用程序提供了全面的基础架构支持。它包含一些很好的功能，如依赖注入和开箱即用的模块，如：`Spring JDBC 、Spring MVC 、Spring Security、 Spring AOP 、Spring ORM 、Spring Test`等等，这些模块覆盖了**Web开发、数据访问、安全控制、分布式、消息服务、移动开发、批处理**等生产问题，提供了一套高效的解决方案，缩短应用程序的开发时间，提高了应用开发的效率。

![img](https://gitee.com/zero049/MyNoteImages/raw/master/1602641710418-5123a24a-60df-4e26-8c23-1d93b8d998d9.png)

`Spring Boot`基本上是`Spring`框架的扩展，能快速创建出生产级别的 Spring应用，强调<mark>**“约定大于配置”**</mark>，它**消除了设置`Spring`应用程序所需的`XML配置`，开箱即用，快速启动**，为更快，更高效的开发生态系统铺平了道路。简而言之，可以说`Spring Boot`只是`Spring`本身的扩展，使开发，测试和部署更加方便。

**SpringBoot优点：**

> SpringBoot是整合Spring技术栈的一站式框架
>
> SpringBoot是简化Spring技术栈的快速开发脚手架（只需开发组件，环境无需搭建）

- Create stand-alone Spring applications
  - 创建独立Spring应用
- Embed Tomcat, Jetty or Undertow directly (no need to deploy WAR files)
  - 内嵌web服务器（spring要封成war包给tomcat使用，springboot内嵌了tomcat）
- Provide opinionated ‘starter’ dependencies to simplify your build configuration
  - 自动starter依赖，简化构建配置（spring开发，需要导springMVC、Mybatis等配置，一个组件没有配置好都无法启动，springboot提供starter，导入starter自动配置各组件）
- Automatically configure Spring and 3rd party libraries whenever possible
  - 自动配置Spring以及第三方功能（上述提到的springboot提供start会自动配置并进行版本匹配）
- Provide production-ready features such as metrics, health checks, and externalized configuration
  - 提供生产级别的监控、健康检查及外部化配置
- Absolutely no code generation and no requirement for XML configuration
  - 无代码生成、无需编写XML

**SpringBoot 缺点：**

- 人称版本帝，迭代快，需要时刻关注变化
- 封装太深，内部原理复杂，不容易精通



## SpringBoot的时代背景

### 微服务

[James Lewis and Martin Fowler (2014)](https://martinfowler.com/articles/microservices.html)  提出微服务完整概念。https://martinfowler.com/microservices/

>In short, the microservice architectural style is an approach to developing a single application as a suite of small services, each running in its own process and communicating with lightweight mechanisms, often an HTTP resource API. These services are built around business capabilities and independently deployable by fully automated deployment machinery. There is a bare minimum of centralized management of these services, which may be written in different programming languages and use different data storage technologies.——James Lewis and Martin Fowler (2014)

解读：

- 微服务是一种架构风格
- 一个应用拆分为一组小型服务
- 每个服务运行在自己的进程内，也就是可独立部署和升级
- 服务之间使用轻量级HTTP交互
- 服务围绕业务功能拆分
- 可以由全自动部署机制独立部署
- 去中心化，服务自治。服务可以使用不同的语言、不同的存储技术

### 分布式

由于微服务拆分，一个服务可能依赖于部署在不同集群机器上的服务，现有的分布式应用节点链路示意图如下，

![image-20210313152628476](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210313152628476.png)

**分布式的难点**

- 远程调用
- 服务发现
- 负载均衡
- 服务容错
- 配置管理
- 服务监控
- 链路追踪
- 日志管理
- 任务调度
- …

**Spring 提供的解决方案：**

![image-20210313153157640](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210313153157640.png)

### 云原生

原生应用如何上云。 Cloud Native

**上云的难点：**

- 服务自愈
- 弹性伸缩
- 服务隔离
- 自动化部署
- 灰度发布
- 流量治理
- ......

## SpringBoot学习方法

查看官方文档 https://spring.io/projects/spring-boot#learn

![image-20210313154029300](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210313154029300.png)

![image-20210313154345398](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210313154345398.png)

![image-20210313154629144](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210313154629144.png)

其中Decoumentation  Overview可以下载pdf官方文档

![image-20210313154504726](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210313154504726.png)

查看版本新特性，https://github.com/spring-projects/spring-boot/wiki#release-notes

![image-20210313154805330](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210313154805330.png)

![image-20210313154830975](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210313154830975.png)





## SpringBoot2 入门

### 系统要求

- Java8&兼容java14
- Maven 3.3+
- idea2019.1.2

 maven 配置要求：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
    
    <pluginGroups />
    <proxies />
    <servers />
    
    <localRepository>E:/program_tool/IDE/intelliJ_IDEA/Maven/repository</localRepository>
    
    <mirrors>
        <mirror>
            <id>alimaven</id>
            <name>aliyun maven</name>
            <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
            <mirrorOf>central</mirrorOf>
        </mirror>
 
        <mirror>
            <id>uk</id>
            <mirrorOf>central</mirrorOf>
            <name>Human Readable Name for this Mirror.</name>
            <url>http://uk.maven.org/maven2/</url>
        </mirror>
 
        <mirror>
            <id>CN</id>
            <name>OSChina Central</name>
            <url>http://maven.oschina.net/content/groups/public/</url>
            <mirrorOf>central</mirrorOf>
        </mirror>
 
        <mirror>
            <id>nexus</id>
            <name>internal nexus repository</name>
            <!-- <url>http://192.168.1.100:8081/nexus/content/groups/public/</url>-->
            <url>http://repo.maven.apache.org/maven2</url>
            <mirrorOf>central</mirrorOf>
        </mirror>
    
    </mirrors>

      <profiles>
         <profile>
              <id>jdk-1.8</id>
              <activation>
                <activeByDefault>true</activeByDefault>
                <jdk>1.8</jdk>
              </activation>
              <properties>
                <maven.compiler.source>1.8</maven.compiler.source>
                <maven.compiler.target>1.8</maven.compiler.target>
                <maven.compiler.compilerVersion>1.8</maven.compiler.compilerVersion>
              </properties>
         </profile>
  </profiles>
    
</settings>
```



### hello world实践

需求：浏览器客户端发送/hello请求，服务器响应 Hello

**1、引入依赖**

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.3.4.RELEASE</version>
</parent>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

</dependencies>
```

**2、创建主程序**

```java
/**
 * 主程序类
 * @SpringBootApplication 这是一个SpringBoot应用
 */
@SpringBootApplication
public class Main {
    public static void main(String[] args) {
        SpringApplication.run(Main.class, args);
    }
}
```

**3、创建处理器**

注意项目层级，主程序类需要单独放在项目包的一层，其余包与主程序类保持平级及以下

```java
/**
 * @ResponseBody    放在类上说明该类所有方法返回数据直接填充response body返回给客户端
 * @Controller      说明是一个控制器
 * @RestController  直接集成了上述两个注解，包括@Target({ElementType.TYPE})、@Retention(RetentionPolicy.RUNTIME)、@Documented、@Controller、@ResponseBody
 */

@RestController
public class HelloController {

    @RequestMapping("/hello")
    public String handle01(){
        return "Hello, SpringBoot2";
    }
}
```

**4、运行main方法，访问 http://localhost:8080/hello**

**5、应用配置**

在resources 包下**创建application.properties（SpringBoot应用默认配置名）**，重启main，访问http://localhost:8888/hello，此处配置可参考官方文档对应版本的Application Properties章节

```
server.port=8888
```

**6、打包部署**

pom.xml添加打包插件和输出文件格式

```xml
	<packaging>jar</packaging>
	<build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
```

```
mvn package
```

**7、启动项目**

```
java -jar xxx.jar
```



### 自动配置原理浅析

上面我们提到了pom.xml需要引入两个配置，一个依赖配置`spring-boot-starter-web`， 一个父项目`spring-boot-starter-parent`

```xml
<!--引入父项目-->
<parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.3.4.RELEASE</version>
</parent>
```

而项目`spring-boot-starter-parent`又引入了父项目`spring-boot-dependencies`

```xml
<!--引入父项目-->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-dependencies</artifactId>
    <version>2.3.4.RELEASE</version>
</parent>

```

`spring-boot-dependencies` 中 几乎声明了所有开发中常用的依赖的版本号，自动版本仲裁机制（最终版本以pom.xml上的为准）

![image-20210314140634916](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210314140634916.png)

**开发中依赖使用步骤**

**1、导入starter场景启动器**

1. 依赖导入spring-boot-starter-* ： *就某种场景，如上述的web

2. 只要引入starter，这个场景的所有常规需要的依赖我们都自动引入。starter-web的依赖关系如下

   ![image-20210314145139197](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210314145139197.png)

3. SpringBoot所有支持的场景https://docs.spring.io/spring-boot/docs/current/reference/html/using-spring-boot.html#using-boot-starter

4. 见到的  *-spring-boot-starter： 第三方为我们提供的简化开发的场景启动器。

5. 所有场景启动器最底层的依赖如下：

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter</artifactId>
  <version>2.3.4.RELEASE</version>
  <scope>compile</scope>
</dependency>
```

**2、无需关注版本号，自动版本仲裁**

1. 引入依赖默认都可以不写版本，也可以自定义版本号，查看spring-boot-dependencies里面规定当前依赖的版本 用的 key，重写value

   ```xml
   	<properties>
           <mysql.version>5.1.43</mysql.version>
       </properties>
   ```

2. 引入**非版本仲裁的jar，要写版本号**。



### 自动配置

可以通过如下程序查看IOC管理的类

```java
/**
 * 主程序类
 * @SpringBootApplication 这是一个SpringBoot应用
 */
@SpringBootApplication
public class Main {
    public static void main(String[] args) {
        // 返回IOC容器
        ConfigurableApplicationContext run = SpringApplication.run(Main.class, args);
	   // 查看容器的组件
        String[] names = run.getBeanDefinitionNames();
        for (String name : names) {
            System.out.println(name);
        }
    }
}
```



**1、自动配好Tomcat**

- 引入Tomcat依赖。
- 配置Tomcat

```xml
<dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-tomcat</artifactId>
      <version>2.3.4.RELEASE</version>
      <scope>compile</scope>
    </dependency>
```



**2、自动配好SpringMVC**

- 引入SpringMVC全套组件
- 自动配好SpringMVC常用组件（功能）

**3、自动配好Web常见功能**

- SpringBoot帮我们配置好了所有web开发的常见场景（如：字符编码问题characterEncodingFilter，文件上传multipartResolver等）

- **默认的包结构**

  - **主程序所在包及其下面的所有子包里面的组件都会被默认扫描进来**，无需以前的包扫描配置

    ```
    com
     +- example
         +- myapplication
             +- Application.java  -- 主程序
             |
             +- customer		 -- 该应用下的其他组件
             |   +- Customer.java
             |   +- CustomerController.java
             |   +- CustomerService.java
             |   +- CustomerRepository.java
             |
             +- order
                 +- Order.java
                 +- OrderController.java
                 +- OrderService.java
                 +- OrderRepository.java
    ```

  - **想要改变扫描路径，@SpringBootApplication(scanBasePackages="com.zero")** 或者@ComponentScan 指定扫描路径

    ```java
    @SpringBootApplication(scanBasePackages = "com.zero.boot")
    public class Main {
        public static void main(String[] args) {
            SpringApplication.run(Main.class, args);
        }
    }
    ```

    ```java
    /*
    @SpringBootApplication
    等同于
    @SpringBootConfiguration
    @EnableAutoConfiguration
    @ComponentScan("com.zero.boot")
    */
    
    @SpringBootConfiguration
    @EnableAutoConfiguration
    @ComponentScan("com.zero")
    public class Main {
        public static void main(String[] args) {
            ConfigurableApplicationContext run = SpringApplication.run(Main.class, args);
        }
    }
    
    ```

  - 

**4、各种配置拥有默认值**

- 默认配置最终都是映射到某个类上，如：MultipartProperties
- 配置文件（application.properties）的值最终会绑定每个类上，这个类会在容器中创建对象

**5、 按需加载所有自动配置项**

- 非常多的starter

- 引入了哪些场景这个场景的自动配置才会开启

- SpringBoot所有的自动配置功能都在 spring-boot-autoconfigure 包里面

  ![image-20210314153431229](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210314153431229.png)



### 实践步骤

- 查看需求场景，引入对应场景依赖

  - https://docs.spring.io/spring-boot/docs/current/reference/html/using-spring-boot.html#using-boot-starter

- 查看自动配置了哪些（选做）

  - 自己分析，引入场景对应的自动配置一般都生效了

  - 配置文件`application.properties`中debug=true开启自动配置报告。Negative（不生效）\Positive（生效）

    ![image-20210315080716628](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210315080716628.png)

    ![image-20210315080858993](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210315080858993.png)

- 是否需要修改

  - 参照文档修改配置`application.properties`对应项目
    - https://docs.spring.io/spring-boot/docs/current/reference/html/appendix-application-properties.html#common-application-properties
    - 自己分析。xxxxProperties绑定了配置文件的哪些前缀。
  - 自定义加入或者替换组件
    - @Bean、@Component。。。
  - 自定义器  **XXXXXCustomizer**；



## 开发小技巧

### lombok

1、引入依赖

```xml
		<dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
        </dependency>
```

2、idea安装lombok插件

3、实体类编写

```java
@Data					// 自动生成get和set方法
@ToString				// 自动生成toString方法
@NoArgsConstructor		// 自动生成无参构造方法
@AllArgsConstructor		// 自动生成全参构造方法
@EqualsAndHashCode		// 重写hashCode和equals方法
public class Dog {
    private String name;
    private Integer age;
}
```

4、日志功能

```java
@Slf4j							// lombok提供日志功能，在控制台打印请求信息
@RestController
public class HelloController {

    @RequestMapping("/hello")
    public String handle01(@RequestParam("name") String name){
        log.info("请求进来");
        return "Hello, SpringBoot2 + 你好：" + name;
    }
}
```

```
2021-03-15 08:30:47.585  INFO 24056 --- [nio-8111-exec-1] o.apache.tomcat.util.http.parser.Cookie  : A cookie header was received [1587796026,1587821983; Webstorm-d58b33b4=a9756940-a535-4334-8289-0d26e529c812; fblo_213=y] that contained an invalid cookie. That cookie will be ignored.
 Note: further occurrences of this error will be logged at DEBUG level.
2021-03-15 08:30:47.591  INFO 24056 --- [nio-8111-exec-1] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring DispatcherServlet 'dispatcherServlet'
2021-03-15 08:30:47.591  INFO 24056 --- [nio-8111-exec-1] o.s.web.servlet.DispatcherServlet        : Initializing Servlet 'dispatcherServlet'
2021-03-15 08:30:47.592 DEBUG 24056 --- [nio-8111-exec-1] o.s.web.servlet.DispatcherServlet        : Detected StandardServletMultipartResolver
2021-03-15 08:30:47.596 DEBUG 24056 --- [nio-8111-exec-1] o.s.web.servlet.DispatcherServlet        : enableLoggingRequestDetails='false': request parameters and headers will be masked to prevent unsafe logging of potentially sensitive data
2021-03-15 08:30:47.597  INFO 24056 --- [nio-8111-exec-1] o.s.web.servlet.DispatcherServlet        : Completed initialization in 6 ms
2021-03-15 08:30:47.606 DEBUG 24056 --- [nio-8111-exec-1] o.s.web.servlet.DispatcherServlet        : GET "/hello", parameters={}
2021-03-15 08:30:47.609 DEBUG 24056 --- [nio-8111-exec-1] s.w.s.m.m.a.RequestMappingHandlerMapping : Mapped to com.zero.boot.controller.test.HelloController#handle01(String)
2021-03-15 08:30:47.621 DEBUG 24056 --- [nio-8111-exec-1] .w.s.m.m.a.ServletInvocableHandlerMethod : Could not resolve parameter [0] in public java.lang.String com.zero.boot.controller.test.HelloController.handle01(java.lang.String): Required String parameter 'name' is not present
2021-03-15 08:30:47.624  WARN 24056 --- [nio-8111-exec-1] .w.s.m.s.DefaultHandlerExceptionResolver : Resolved [org.springframework.web.bind.MissingServletRequestParameterException: Required String parameter 'name' is not present]
2021-03-15 08:30:47.625 DEBUG 24056 --- [nio-8111-exec-1] o.s.web.servlet.DispatcherServlet        : Completed 400 BAD_REQUEST
2021-03-15 08:30:47.631 DEBUG 24056 --- [nio-8111-exec-1] o.s.web.servlet.DispatcherServlet        : "ERROR" dispatch for GET "/error", parameters={}
2021-03-15 08:30:47.635 DEBUG 24056 --- [nio-8111-exec-1] s.w.s.m.m.a.RequestMappingHandlerMapping : Mapped to org.springframework.boot.autoconfigure.web.servlet.error.BasicErrorController#errorHtml(HttpServletRequest, HttpServletResponse)
2021-03-15 08:30:47.646 DEBUG 24056 --- [nio-8111-exec-1] o.s.w.s.v.ContentNegotiatingViewResolver : Selected 'text/html' given [text/html, text/html;q=0.8]
2021-03-15 08:30:47.652 DEBUG 24056 --- [nio-8111-exec-1] o.s.web.servlet.DispatcherServlet        : Exiting from "ERROR" dispatch, status 400
2021-03-15 08:31:20.427 DEBUG 24056 --- [nio-8111-exec-2] o.s.web.servlet.DispatcherServlet        : GET "/hello?name=zhang", parameters={masked}
2021-03-15 08:31:20.427 DEBUG 24056 --- [nio-8111-exec-2] s.w.s.m.m.a.RequestMappingHandlerMapping : Mapped to com.zero.boot.controller.test.HelloController#handle01(String)
2021-03-15 08:31:20.431  INFO 24056 --- [nio-8111-exec-2] c.z.b.controller.test.HelloController    : 请求进来
2021-03-15 08:31:20.445 DEBUG 24056 --- [nio-8111-exec-2] m.m.a.RequestResponseBodyMethodProcessor : Using 'text/html', given [text/html, application/xhtml+xml, image/avif, image/webp, image/apng, application/xml;q=0.9, application/signed-exchange;v=b3;q=0.9, */*;q=0.8] and supported [text/plain, */*, text/plain, */*, application/json, application/*+json, application/json, application/*+json]
2021-03-15 08:31:20.446 DEBUG 24056 --- [nio-8111-exec-2] m.m.a.RequestResponseBodyMethodProcessor : Writing ["Hello, SpringBoot2 + 你好：zhang"]
2021-03-15 08:31:20.449 DEBUG 24056 --- [nio-8111-exec-2] o.s.web.servlet.DispatcherServlet        : Completed 200 OK
```



### dev-tools

是一个快速重启功能

1、引入依赖

```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-devtools</artifactId>
        <optional>true</optional>
    </dependency>
```

2、修改项目后，按**Ctrl+F9**（而不是Shift+F10，run项目），能快速重启，尤其适合静态页面变化时使用



### Spring Initializr

**1、选择我们需要的开发场景**

![image-20210315084447438](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210315084504866.png)

![image-20210315084504866](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210315084504866.png)

![image-20210315084603545](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210315084603545.png)

**2、自动导入依赖和创建项目结构**

![image-20210315084732195](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210315084732195.png)

![image-20210315085009264](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210315085009264.png)

**3、自动编写好主配置类**

![image-20210315085043992](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210315085043992.png)