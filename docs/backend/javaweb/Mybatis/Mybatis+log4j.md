1、POM的依赖引入
```xml
<!-- log4j -->
        <!-- https://mvnrepository.com/artifact/log4j/log4j -->
        <dependency>
            <groupId>log4j</groupId>
            <artifactId>log4j</artifactId>
            <version>1.2.17</version>
        </dependency>
```
2、在resources加入log4j.properties，内容如下：
```
log4j.rootLogger=DEBUG,Console
log4j.appender.Console=org.apache.log4j.ConsoleAppender
log4j.appender.Console.layout=org.apache.log4j.PatternLayout
log4j.appender.Console.layout.ConversionPattern=%d [%t] %-5p [%c] - %m%n
log4j.logger.org.apache=INFO
#ex:http://www.cnblogs.com/zhaozihan/p/6371133.html
```

3、在Mybatis主配置的xml加入如下配置：

```xml
    <properties>
        <property name="dialect" value="mysql" />
    </properties>
    <settings>
        <setting name="logImpl" value="LOG4J" />
    </settings>
```
配置好之后，运行效果如下：
<img src="./pictures/Annotation 2020-03-31 115940.png
"  div align=center />

