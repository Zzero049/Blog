

#### 反射
反射Reflection：把java类中的各种结构（方法、属性、构造器、类名）映射成一个个的Java对象。利用反射技术可以对一个类进行解剖，反射是框架设计的灵魂。
```java
//在运行期间，一个类，只有一个Class对象产生。
//1、源头：获取class对象(三种方式)
        //1. 对象.getClass()
        Iphone iphone = new Iphone();
        Class clz = iphone.getClass();
        //2. 类.class
        clz = Iphone.class;
        //3. Class.forName("包名.类名") 推荐
        clz = Class.forName("WebServerLearn.Iphone");
//2、创建对象：
WebServerLearn.Iphone stu =(WebServerLearn.Iphone)clz.getConstructor().newInstance();
```

### XML解析
XML:Extensible Markup Language，可扩展标记语言，作为数据的一种存储格式或用于存储软件的参数，程序解析此配置文件，就可以到达不修改代码就能更改程序的目的。java有四种方法对xml进行解析，下面讲的是SAX解析

```java
//SAX解析
//1、获取解析工厂
SAXParserFactory factory=SAXParserFactory.newInstance();
//2、从解析工厂获取解析器
SAXParser parse =factory.newSAXParser();
//3、加载文档Document注册处理器
//4、编写处理器
PersonHandler handler=new PersonHandler();
parse.parse(Thread.currentThread().getContextClassLoader().getResourceAsStream("person.xml"),handler);//这个
```

### HTML
Hyperlext Markup Language：超文本标记语言，简单理解为浏览器使用的语言。
#### 固定标签
```html
<html>——开始标签
<head>网页上的控制信息<title>页面标题
</title></head>
<body>页面显示的内容</body>
</html>——结束标签
```
#### 常用标签
* h1~h6
* p
* span
* form
* input
...
<img src="./pictures/Annotation 2019-12-05 113732.png"  div align=center />

post：提交，基于http协议，不同量大，请求参数url不可见安全
get：默认，获取，基于http协议，不同量小，请求参数url可见不安全
action：请求web服务器的资源
name：作为后端使用，区分唯一请求服务器，必须存在，数据不能提交
id：作为前端使用，区分唯一

### HTTP
超文本传输协议（HTTP，Hyper Text Transfer Protocol）是互联网上应用最为广泛的一种网络协议，所有的WWW文件都必须遵守这个标准。
<img src="./pictures/Annotation 2019-12-04 210312.png"  div align=center />

#### 请求协议
1、请求行：方法（GET/POST）、URI、协议版本
2、请求头：（Request header）
3、请求正文

经典的GET请求协议:
1、请求行
GET/index.html?name=test&pwd-123456 HTTP/1.1
2、请求体
Accept:text/html，application/xhtml+xml，\*/\*
Accept-Language:zh-CN 
User-Agent:Mozilla/5.0（compatible；MSIE 9.0；Windows NT 6.1；Trident/5.0）
Accept-Encoding:geip，deflate Host:localhost 
Connection:Keep-Alive
3、请求正文

经典的POST请求协议
1、请求行
POST/index.html HTTP/1.1
2、请求体
Accept:text/html，apdlication/xhtml+xml,\*/\*
Accept-Language:zh-CN 
User-Agent:Mozilla/5.0（compatible；MSIE 9.0；Windows NT 6.1；Trident/5.0）
Accept-Encoding:ggip，deflate Host:localhost 
Connection:Keep-Alive
3、请求正文
(空一行)
name=test&pwd=123456

#### 响应协议
1、状态行：方法（GET/POST）、URI、协议版本
2、响应头（Response Header）
3、响应正文

经典的响应协议
1、状态行：HTTP/1.0 200 OK
2、请求头：
Date:Mon，31Dec209904：25：57GMT 
Server:shsxt Server/0.0.1；charset=GBK Content-type:text/html 
Content-length：39725426
3、请求正文（注意与请求头之间有个空行）
 
xxxxxx

<img src="./pictures/Annotation 2019-12-05 120443.png"  div align=center />


<br>根据http协议的报文解析并返回相应报文，就是后台逻辑要做的事情</br>

html骨架框架
css皮肤
js交互