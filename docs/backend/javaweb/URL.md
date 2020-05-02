## URL
统一资源定位符，由4部分组成：协议、存放资源的主机域名、端口号和资源文件名
![image-20200426020634861](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200426020634861.png)



举个例子，个人的身份证号就是URN，个人的家庭地址就是URL，URN可以唯一标识一个人，而URL可以告诉邮递员怎么把货送到你手里

URL是一种URI，它标识一个互联网资源，并指定对其进行操作或获取该资源的方法。可能通过对主要访问手段的描述，也可能通过网络“位置”进行标识。URI可被视为定位符（URL），名称（URN）或两者兼备。统一资源名（URN）如同一个人的名称，而统一资源定位符（URL）代表一个人的住址。换言之，URN定义某事物的身份，而URL提供查找该事物的方法。URN仅用于命名，而不指定地址。

目前HTTP规范已经不使用URL，而是使用URI了。

## URL的java api

```java
URL u=new URL("http://www.baidu.con:80/index.html#aa?cansu=shsxt");

System.out.println("获取与此url关联的协议的默认端口："+u.getDefaultPort());

System.out.println("getFile:"+u.getFile());		//端口号后面的内容

System.out.println("主机名："+u.getHost());		//www.baidu.com

System.out.println("路径："+u.getPath());		//端口号后，参数前的内容

System.out.println("端口："+u.getPort());		//存在返回80.否则返回-1

System.out.println("协议："+u.getProtocol());

System.out.println("参数部分："+u.getQuery());

System.out.println("锚点："+u.getRef());

URL u1=new URL("http://www.abc.com/aa/");

URL u2=new URL(u1,"2.html");//相对路径构建url对象System.out.println(u2.toString());//http://www.abc.com/aa/2.html
```



