# maven 3.6.3 安装及配置

**1、下载**

下载地址：http://maven.apache.org/download.cgi

![img](pictures/1561523-20200114182545485-1893330803.png)

 

**2、配置环境变量**

解压压缩包到磁盘。

注意：各种系统配置环境变量位置不一样，已windows10为例。

我的电脑（右击）=> 属性 => 高级系统设置 => 环境变量 => （系统环境变量）

```
新建 变量名：MAVEN_HOME 变量值：E:\tb\apache-maven-3.6.3    //maven目录
新建 变量名：MAVEN_OPTS 变量值：-Xms128m -Xmx1024m
修改 变量名：Path       变量值在前面新加：%MAVEN_HOME%\bin;
```

**3、测试**

```
win+r 输入cmd 回车
mvn -v      
输出版本号安装成功
```

**4、配置maven**

记事本打开apache-maven-3.6.3\conf\setting.xml

//修改本地仓库目录

```
找到<localRepository>标签，注释掉，添加
<localRepository>E:/program_tool/others/Maven/repository</localRepository>     //本地目录、不存在自动新建文件夹
```

//修改源可按照官方文档修改（https://maven.aliyun.com/mvn/view）

```
找到<mirrors>...</mirrors>，添加
<mirror>
　　<id>alimaven</id>
   <name>aliyun maven</name>
   <url>https://maven.aliyun.com/repository/central</url>
   <mirrorOf>central</mirrorOf>
</mirror>
```

最终配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
    
    <pluginGroups />
    <proxies />
    <servers />
    
    <localRepository>E:/program_tool/others/Maven/repository</localRepository>
    
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

保存退出。