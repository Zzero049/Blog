## 案例代码
目录路径
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-04-12 120209.png">

springmvc.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="
        http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd
        http://www.springframework.org/schema/mvc
        http://www.springframework.org/schema/mvc/spring-mvc.xsd">

    
    <!--开启注解扫描-->
    <context:component-scan base-package="Controller"/>

    <!--视图解析器对象-->
    <bean id="internalResourceViewResolver" class="org.springframework.web.servlet.view.InternalResourceViewResolver">
      <!--前缀-->
        <property name="prefix" value="/WEB-INF/pages/"/>
        <!--后缀-->
        <property name="suffix" value=".jsp"/>
    </bean>

    <!--开启springMVC注解的支持-->
    <mvc:annotation-driven/>

</beans>
```
HelloController.java
```java
package Controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

/**
 * 控制器
 */

@Controller
public class HelloController {

    @RequestMapping(path="/hello")
    public String sayHello(){
        System.out.println("hello stringmvc");
        return "success";//解析器根据返回值拼接跳转页面的名称
    }
}

```
web.xml
```xml
<!DOCTYPE web-app PUBLIC
 "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
 "http://java.sun.com/dtd/web-app_2_3.dtd" >

<web-app>
  <display-name>Archetype Created Web Application</display-name>
  
  <servlet>
    <servlet-name>dispatcherServlet</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <init-param>
      <param-name>contextConfigLocation</param-name>
      <param-value>classpath:springmvc.xml</param-value>
    </init-param>
    <!--对象创建即加载-->
    <load-on-startup>1</load-on-startup>
  </servlet>
  
  <servlet-mapping>
    <servlet-name>dispatcherServlet</servlet-name>
    <url-pattern>/</url-pattern>
  </servlet-mapping>
</web-app>

```
开始页面index.jsp
```jsp
<%--
  Created by IntelliJ IDEA.
  User: Lin
  Date: 2020/4/11
  Time: 16:46
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
    <h3>入门程序</h3>
    <a href="hello">入门程序</a>
</body>
</html>

```
跳转成功页面success.jsp
```jsp
<%--
  Created by IntelliJ IDEA.
  User: Lin
  Date: 2020/4/12
  Time: 11:35
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
    <h3>入门成功</h3>

</body>
</html>

```
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-04-12 120622.png">
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-04-12 120651.png">
程序打印
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-04-12 120713.png">

## 流程
1. 启动服务器，加载一些配置文件
    * Dispatcherservlet对象创建
    * springmvc-xml被加载了
    * Hellocontrol1er创建成对象
2. 发送请求，后台处理请求
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-04-12 122544.png">

