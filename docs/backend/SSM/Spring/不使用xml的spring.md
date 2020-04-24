## 不使用xml的spring
通过一个配置类，达到xml配置文件效果，通过使用spring中的新注解

>@Configuration

作用：指定当前类是一个配置类

>@ComponentScan

作用：用于通过注解指定spring在创建容器时要扫描的包
属性：
value：它和basePackages的作用是一样的，都是用于指定创建容器时要扫描的包。
我们使用此注解就等同于在xml中配置了`<context:component-scan base-package="com.itheima"></context:component-scan>`

示例



