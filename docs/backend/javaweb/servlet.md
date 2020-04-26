# Servlet
Servlet是Java Web开发的基石，与平台无关的服务器组件，它是运行在Servlet 容器/Web应用服务器/Tomcat，负责与客户端进行通信。
![image-20200426131459468](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200426131459468.png)

Servlet的功能：
1、创建并返回基于客户请求的动态HTML页面。
2、与数据库进行通信。

Servlet本身是一组接口，自定义一个类，并且实现Servlet接口(javax.servlet)，这个类就具备了接受客户端请求以及做出的功能。

浏览器不能直接访问Servlet文件，只能通过映射的方式来间接访问Servlet，映射需要开发者手动配置，有两种配置方式。（不能都配置）
- 基于xml
```xml
<servlet>
<servlet-name>hello</servlet-name>
<servlet-class>com.southwind.servlet.HelloServlet</servlet-class>
</servlet>

<servlet-mapping>
<servlet-name>hello</servlet-name>
<url-pattern>/demo2</url-pattern>
</servlet-mapping>
```
- 基于注解
```java
@WebServlet("/demo2")
public class HelloServlet implements Servlet{

}
```

## Servlet生命周期
1、当浏览器访问Servlet的时候，Tomcat会查询当前Servlet的实例化对象是否存在，如果不存在，则通过反射机制动态创建对象，如果存在，直接执行第3步。
2、调用init方法完成初始化操作。
3、调用 service方法完成业务逻辑操作。
4、关闭Tomcat时，会调用destory方法，释放当前对象所占用的资源。
```java
package com;

import javax.servlet.*;
import javax.servlet.annotation.ServletSecurity;
import javax.servlet.annotation.WebServlet;
import java.io.IOException;
@WebServlet("/demo1")
public class HelloServlet implements Servlet {
    @Override
    public void init(ServletConfig servletConfig) throws ServletException {
        System.out.println("初始化");
    }

    @Override
    public ServletConfig getServletConfig() {
        return null;
    }

    @Override
    public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {
        System.out.println("ahahahahaha");
        //设置UTF-8解决中文乱码
        servletResponse.setContentType("text/html;charset=UTF-8");
        servletResponse.getWriter().write("黑恶黑河");
    }

    @Override
    public String getServletInfo() {
        return null;
    }

    @Override
    public void destroy() {

    }
}

```
Servlet的生命周期方法：无参构造函数、init、service、destory
1、无参构造函数只调用一次，创建对象。
2、init只调用一次，初始化对象。
3、service调用N次，执行业务方法。
4、destory 只调用一次，卸载对象。

###ServletConfig
该接口是用来描述Servlet的基本信息的。
```java
//返回Servlet的名称，全类名（带着包名的类名）
getServletName()
//获取init参数的值（web.xml）
getlnitParameter(String key)
//返回所有的initParamter的name值，一般用作遍历初始化参数
getlnitParameterNames()
//返回ServletContext对象(常用)，它是Servlet的上下文，整个Servlet的全局信息
getServletContext()
```
ServletConfig作用于某个Servlet实例，每个Servlet 都有对应的ServletConfig，ServletContext作用于整个Web应用，一个Web应用对应一个ServletContext，多个Servlet 实例对应一个ServletContext。

## Servlet的层次结构
>Servlet--》GenericServlet---》HttpServlet

GenericServlet实现了Servlet接口，HttpServlet是GenericServlet的子类


HTTP请求有很多种类型，常用的有四种：
GET-----------读取
POST----------保存
PUT-----------修改
DELETE--------删除


GenericServlet实现Serlet接口，同时为它的子类屏蔽了不常用的方法，子类只需要重写 service方法即可。

HttpServlet 继承 GenericServlet，service方法根据请求类型进行分发处理，GET进入doGET方法，POST进入doPOST方法。

开发者自定义的Servlet 类只需要继承 HttpServlet即可，重写doGET和doPOST。