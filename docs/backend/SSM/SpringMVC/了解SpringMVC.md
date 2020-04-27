## SpringMVC

MVC全名是ModelView Controller，是模型（model）——视图（view）——控制器（controller）的缩写，是一种用于设计创建 Web应用程序**表现层（Controller）** 的模式。MVC中每个部分各司其职：
* Model（模型）：
  通常指的就是我们的数据模型。作用一般情况下用于封装数据。（JavaBean）

* View（视图）：
  通常指的就是我们的jsp或者html。作用一般就是展示数据的。（jsp）
  通常视图是依据模型数据创建的。

* Controller（控制器）我是应用程序中处理用户交互的部分。作用一般就是处理程序逻辑的。
  （Servlet）
  例如：

  我们要保存一个用户的信息，该用户信息中包含了姓名，性别，年龄等等。

  这时候表单输入要求年龄必须是1~100之间的整数。姓名和性别不能为空。并且把数据填充到模型之中。

  此时除了js的校验之外，服务器端也应该有数据准确性的校验，那么校验就是控制器的该做的。

  当校验失败后，由控制器负责把错误页面展示给使用者。

  如果校验成功，也是控制器负责把数据填充到模型，并且调用业务层实现完整的业务需求。

&emsp;&emsp;SpringMVC是一种基于Java的实现Mvc设计模型的请求驱动类型的轻量级Web框架，属于Spring FrameWork的后续产品，已经融合在Spring WebFlow里面。Spring 框架提供了构建Web应用程序的全功能MvC模块。使用Spring 可插入的MVC架构，从而在使用Spring 进行WEB开发时，可以选择使用Spring的Spring MVC 框架或集成其他MVC开发框架，如Struts1（现在一般不用），Struts2等。

&emsp;&emsp;SpringMVC已经成为目前最主流的MVC框架之一，并且随着Spring3.0的发布，全面超越Struts2，成为最优秀的MVC框架。

&emsp;&emsp;它通过一套注解，让一个简单的Java类成为处理请求的控制器，而无须实现任何接口。同时它还支持RESTfu1编程风格的请求。

<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-04-11 143431.png"  div align=center />


### SpringMVC 与 Struts2优劣对比
* 共同点：
    * 它们都是表现层框架，都是基于MVC模型编写的。它们的底层都离不开原始ServletAPI。
    * 它们处理请求的机制都是一个核心控制器。

* 区别：
    * Spring MVC的入口是Servlet，而 Struts2是Filter 
    * Spring MVC 是基于方法设计的，而Struts2是基于类，Struts2每次执行都会创建一个动作类。所以Spring MVc会稍微比 Struts2快些。
    * Spring MVC 使用更加简洁，同时还支持JSR303，处理ajax的请求更方便（JSR303是一套JavaBean参数校验的标准，它定义了很多常用的校验注解，我们可以直接将这些注解加在我们JavaBean的属性上面，就可以在需要校验的时候进行校验了。）
    * Struts2的OGNL表达式使页面的开发效率相比Spring MVC更高些，但执行效率并没有比JSTL提升，尤其是struts2的表单标签，远没有html执行效率高。


### 需要的依赖

```xml
<properties>
    <spring.version>5.2.3.RELEASE</spring.version>

  </properties>
<dependencies>
<dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-context</artifactId>
      <version>${spring.version}</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-web</artifactId>
      <version>${spring.version}</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-webmvc</artifactId>
      <version>${spring.version}</version>
    </dependency>
    <dependency>
      <groupId>javax.servlet</groupId>
      <artifactId>servlet-api</artifactId>
      <version>2.5</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>javax.servlet.jsp</groupId>
      <artifactId>jsp-api</artifactId>
      <version>2.0</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>
```

### 配置web.xml
```xml
<servlet>
    <servlet-name>dispatcherServlet</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
  </servlet>
  
  <servlet-mapping>
    <servlet-name>dispatcherServlet</servlet-name>
    <url-pattern>/</url-pattern>
  </servlet-mapping>
```