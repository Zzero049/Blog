# SpringBoot

Spring Boot是一个快速开发框架，可以迅速搭建出一套基于Spring框架体系的应用，是Spring Cloud的基础。

Spring Boot开启了各种自动装配，从而简化代码的开发，不需要编写各种配置文件，只需要引入相关依赖就可以迅速搭建一个应用。Spring Boot整合了所有的框架，通过少量的代码就能创建一个独立的、产品级别的Spring应用。

特点

1、不需要web.xml

2、不需要 springmvc.xml

3、不需要tomcat，Spring Boot 内嵌了tomcat

4、不需要配置JSON解析，支持REST架构

5、个性化配置非常简单



![image-20200426235142001](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200426235142001.png)

![image-20200426235214934](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200426235214934.png)

入门使用

pom.xml导入依赖

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
    </dependencies>
```

导入依赖之后基于注解的SSM可以照常使用，不需要配置xml，自动扫描，服务器直接通过下面代码运行。

注意Application类（叫什么都可以）@SpringBootApplication表示当前类是Spring Boot的入口，Application类的存放位置必须是其他相关业务类的存放位置的父级，也不能直接在源文件（Java包）下。**要将Application（入口类）放在最外层，也就是要包含所有子包，否则Controller无效。**

```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
```

若需要配置服务器，需要在resources下创建application.yml配置文件

![image-20200425011149996](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200425011149996.png)

如

```yml
server:
  port: 9090
```



## SpringBoot与微服务

SpringBoot 特点

1、使用Spring项目引导页面可以在几秒构建一个项目

2、方便对外输出各种形式的服务，如REST API、WebSocket、Web、Streaming、Tasks

3、非常简洁的安全策略集成

4、支持关系数据库和非关系数据库

5、支持运行期内嵌容器，如Tomcat、Jetty

6、自动管理依赖



- Spring Boot的一系列特性有助于实现微服务架构的落地，从目前众多的技术栈对比来看它是Java领域微服务架构最优落地技术，没有之一。

- Spring Cloud 依赖于Spring Boot

- Spring Boot 专注于快速开发个体微服务，Spring Cloud是关注全局的微服务协调治理框架