redis默认只能localhost登录，所以需要开启远程登录。

#### 一、修改 redis.conf

1、将 bind 127.0.0.1 这一行注释掉。
 这里的bind指的是只有指定的网段才能远程访问这个redis。  注释掉后，就没有这个限制了。或者bind 自己所在的网段。
 band localhost   只能本机访问,局域网内计算机不能访问。
 bind  局域网IP    只能局域网内IP的机器访问, 本地localhost都无法访问。

想要bind 指定ip只需要 **bind 127.0.0.1 xxx.xxx.xxx.xxx**即可

![](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529090223847.png)

 验证方法：

```ruby
[work@el ~]$ ps -ef | grep redis
work     30830     1  0 11:38 ?        00:00:00 /usr/local/bin/redis-server *:6379
```

2、将 protected-mode 要设置成no   （默认是设置成yes的， 防止了远程访问，在redis3.2.3版本后）

 3、设置远程连接密码

 取消注释 requirepass foobared，将 foobared 改成任意密码，用于验证登录。默认是没有密码的就可以访问的，我们这里最好设置一个密码。（vim 命令模式/requirepass foobared回车查找 ）

![image-20200529094236152](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529094236152.png)

 4、重启 reids

客户端需要认证，才能使用服务

```bash
[root@VM_0_10_centos ~]# redis-cli -p 6379
127.0.0.1:6379> auth 123
OK
```



#### 二、防火墙放行 6379 端口

启动防火墙输入Linux命令systemctl start firewalld
放行6379

```bash
firewall-cmd --permanent --zone=public --add-port=6379/tcp --permanent
```

放行指定ip

```bash
firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="xxx.xxx.xxx.xxx"   accept" 
#重新载入
firewall-cmd --reload
```



注意由于nat，不能取到真实的ip地址，要获取window端的公网ip，百度“本机IP地址查询”





#### 二、腾讯云添加安全组

设置方法如下

安全组

![image-20200530122101231](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530122101231.png)

选中一个安全组，增加规则

![image-20200530122118391](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530122118391.png)

![image-20200530122139914](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200530122139914.png)

最好不要设置成0.0.0.0/0 会有人从redis恶意植入木马，指定自己ip最好



测试远程连接

```java
public class JedisDemo1 {
    public static void main(String[] args) {
        // 1、new Jedis
        Jedis jedis = new Jedis("xxx.xxx.xxx.xxx",6379);
        jedis.auth("123");
        System.out.println(jedis.ping());
    }
}
```

![image-20200529102314712](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200529102314712.png)





注意：实际公司不可能会在服务器开放端口的，他们都是通过局域网进行连接的，而非这种远程连接