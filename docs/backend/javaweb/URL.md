## URL
统一资源定位符，由4部分组成：协议、存放资源的主机域名、端口号和资源文件名
![image-20200426020634861](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200426020634861.png)
####URL的java api

URL u=new URL("http://www.baidu.con:80/index.html#aa？cansu=shsxt");

System.out.println("获取与此url关联的协议的默认端口："+u.getDefaultPort());

System.out.println("getFile:"+u.getFile());//端口号后面的内容

System.out.println("主机名："+u.getHost());//www.baidu.com

System.out.println("路径："+u.getPath());//端口号后，参数前的内容

System.out.println("端口："+u.getPort());//存在返回80.否则返回-1

System.out.println("协议："+u.getProtocol());

System.out.println("参数部分："+u.getQuery());

System.out.println("锚点："+u.getRef());

URL u1=new URL("http://www.abc.com/aa/");

URL u2=new URL(u1,"2.html");//相对路径构建url对象System.out.println(u2.toString());//http://www.abc.com/aa/2.html



