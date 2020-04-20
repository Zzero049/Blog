# JSP

JSP本质上就是一个Servlet，JSP主要负责与用户交互，将最终的界面呈现给用户，HTML+JS+CSS+Java的混合文件。

将html代码写在jsp文件，jsp文件会转换成java文件再用write方法将写好的html代码写入页面。说白了JSP文件只是一个中间层，但是既能展示页面，又能在java文件对数据进行操作

当服务器接收到一个后缀是jsp的请求时，将该请求交给JSP引擎去处理，每一个JSP页面第一次被访问的时候，JSP引擎会将它翻译成一个Servlet文件(java)，再由Web容器调用Servlet完成响应。

单纯从开发的角度看，JSP就是在HTML中嵌入Java程序。

具体的嵌入方式有3种：
1、JSP脚本，执行Java逻辑代码
```xml
<% java 代码 %>
```
```jsp
<!--在控制台输出str-->
<%
    String str = "hello world";
    System.out.println(str);
  %>
```

2、JSP声明
```xml
<%! 
    声明java方法 
%>
```
```jsp
<!--只是声明-->
<%!
    public String test(){
      return "hello world";
    }
  %>
<%
    test();
  %>
```

3、JSP表达式：把Java对象直接输出到HTML页面中
```xml
<%=Java对象%>
```
```jsp
<%=str%>
```

### 页面状态
200：正常
404：资源找不到
400：请求类型不匹配（GET,POST）
500：Java程序抛出异常
## JSP内置对象 9个
1、request：表示一次请求，HttpServletRequest。
2、response：表示一次响应，HttpServletResponse。
3、pageContext：页面上下文，获取页面信息，PageContext。
4、session：表示一次会话，保存用户信息，HttpSession。
5、application：表示当前Web应用，全局对象，保存所有用户共享信息，ServletContext。
6、config：当前JSP对应的Servlet的ServletConfig对象，获取当前Servlet的信息。
7、out：向浏览器输出数据，JspWriter。
8、page：当前JSP对应的Servlet对象，Servlet。
9、excerption：表示JSP页面发生的异常，Exception。

常用的是request、response、session、application、pageContext

#### request常用方法
1、String getParameter（String key）获取客户端传来的参数。（获取浏览器传入服务器的参数）
2、void setAttribute（String key，Object value）通过键值对的形式保存到request。
3、Object getAttribute（String key）通过key 取出value。(JSP内部传数据用)
4、RequestDispatcher getRequestDispatcher（String path）返回一个RequestDispatcher对象，该对象的forward方法用于请求转发。
5、String[] getParameterValues() 获取客户端传来的多个同名参数
6、void setCharacterEncoding（String charset）指定每个请求的编码。
7、Session getSession() 获取当前session对象
#### response常用方法
1、sendRedirect（String path）重定向，页面之间的跳转。
>转发getRequestDispatcher 和重定向 sendRedirect的区别：
转发是将同一个请求传给下一个页面，重定向是创建一个新的请求传给下一个页面,之前的请求结束生命周期。
转发：同一个请求在服务器之间传递，地址栏不变，也叫服务器跳转。
重定向：由客户端发送一次新的请求来访问跳转后的目标资源，地栏改变，也叫客户端跳转。
如果两个页面之间需要通过 request来传值，则必须使用转发，不能使用重定向。
比如：
用户登录，如果用户名和密码正确，则跳转到首页（转发），并且展示用户名，否则重新回到登陆页面（重定向）

## Session
用户会话
服务器无法识别每一次HTTP请求的出处（不知道来自于哪个终端），它只会接受到一个请求信号，所以就存在一个问题：将用户的响应发送给其他人，必须有一种技术来让服务器知道请求来自哪，这就是会话技术。

会话：就是客户端和服务器之间发生的一系列连续的请求和响应的过程，打开浏览器进行操作到关闭浏览器的过程。属于同一次会话的请求都有一个相同的标识符，sessionlD
会话状态：指服务器和浏览器在会话过程中产生的状态信息，借助于会话状态，服务器能够把属于同一次会话的一系列请求和响应关联起来。

实现会话有两种方式：
- session
- cookie

### Session常用方法

- String getld()
获取 sessionlD 
- void setMaxlnactivelnterval(int interval)
设置session的失效时间，单位为秒
- int getMaxlnactivelnterval()
获取当前session的失效时间
- void invalidate()
设置session 立即失效
- void setAttribute(String key，Object value)
通过键值对的形式来存储数据
- Object getAttribute(String key)
通过键获取对应的数据
- void removeAttribute(String key)
通过键删除对应的数据

## Cookie
Cookie 是服务端在HTTP响应中附带传给浏览器的一个小文本文件，一旦浏览器保存了某个Cookie，在之后的请求和响应过程中，会将此Cookie来回传递，这样就可以通过Cookie这个载体完成客户端和服务端的数据交互。 

- 创建 Cookie
```java
Cookie cookie = new Cookie("name", "zhangsan");
response.addCookie(cookie);
```
- 获取Cookie
```java
Cookie[] cookies = request.getCookies();
```
- void setMaxAge（int age）
设置Cookie的有效时间，单位为秒，默认-1，代表关闭session时销毁

- int getMaxAge()
获取Cookie的有效时间

- String getName()
获取Cookie的name
- String getValue()
获取Cookie的 value

### Session和Cookie区别

session：
- 保存在服务器
- 保存的数据是Object
- 会随着会话的结束而销毁
- 保存重要信息
- 声明周期：
    - 服务端：只要WEB应用重启就销毁，
    - 客户端：只要浏览器关闭就销毁。

cookie：
- 保存在浏览器
- 保存的数据是String
- 可以长期保存在浏览器中，与会话无关
- 保存不重要信息
- 生命周期：不随服务端的重启而销毁，客户端：默认是只要关闭浏览器就销毁，我们通过 setMaxAge()方法设置有效期，一旦设置了有效期，则不随浏览器的关闭而销毁，而是由设置的时间来决定。(没有销毁方法，只能setMaxAge(0)将有效期设置为0)

## JSP内置对象作用域
page作用域：对应的内置对象是pageContext。
request作用域：对应的内置对象是request。
session作用域：对应的内置对象是session。
application 作用域：对应的内置对象是application。
都有setAttribute、getAttribute方法

作用范围
page<request<session<application
page只在当前页面有效。
request在一次请求内有效。
session 在一次会话内有效。
application 对应整个WEB应用的。