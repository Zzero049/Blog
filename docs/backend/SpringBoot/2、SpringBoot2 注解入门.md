# SpringBoot2 入门——注解



## 1. 组件注入

**@Confiuration**

使用该注解的类相当于以前spring的xml配置文件，示例如下，主要有proxyBeanMethods属性

这里MyConfig设置proxyBeanMethods为true时，MyConfig对象会交给spring进行代理（cglib），如`com.zero.boot.config.MyConfig$$EnhancerBySpringCGLIB$$4658f1a9@415e0bcb`，启动时对每个对象需要检查是否为单例；设置proxyBeanMethods为false时，只是一个普通对象`com.zero.boot.config.MyConfig@1e7f2e0f`，启动时无需保证单例，每次创建的对象都不同（直接调用），因此启动速度更快

```java
/**
 * 1、配置类里面使用@Bean标注在方法上给容器注册组件，默认是单例的
 * 2、配置类本身也是组件
 * 3、proxyBeanMethods：代理bean的方法
 *      Full(proxyBeanMethods = true)、【保证每个@Bean方法被调用多少次返回的组件都是单实例的】
 *      Lite(proxyBeanMethods = false)【每个@Bean方法被调用多少次返回的组件都是新创建的】
 *      组件依赖必须使用Full模式默认。其他默认是否Lite模式
 */
@Configuration(proxyBeanMethods = false)   // 告诉 SpringBoot这是一个配置类==配置文件
public class MyConfig {

    @Bean //给容器中添加组件。以方法名作为组件的id。返回类型就是组件类型
    public User user01(){
        return new User("zhangsan", 15);
    }

    @Bean("tom")				// 自定义bean名称，否则就是方法名cat
    public Pet cat(){
        return new Pet("niuniu");
    }
}
```

```java
@SpringBootApplication
public class Main {
    public static void main(String[] args) {
        ConfigurableApplicationContext run = SpringApplication.run(Main.class, args);
        
        MyConfig config = run.getBean(MyConfig.class);
        User user01 = config.user01();
        User user02 = config.user01();
        System.out.println(config);
        System.out.println("组件同一个？" + (user01==user02));
    }
}

```



**@Component @Controller @Service @Repository**

后面三个注解他们的作用和属性与component是一模一样。他们三个是spring框架为我们提供明确的三层使用，使我们的三层对象更加清晰

ControlLer：一般用在表现层

Service：一般用在业务层

Repository：一般用在持久层

```java
@Component("accountService")
public class AccountServiceImpl implements IAccountService{

}
```



**@Bean**

作用：用于把当前方法的返回值作为bean对象存入spring的ioc容器

属性：

- name：用于指定bean的id。当不写时，默认值是当前方法的名称

细节：

- 当我们使用注解配置方法时，如果方法有参数，spring框架会去容器中查找有没有可用的bean对象。

- 查找的方式和Autowired注解的作用是一样的（按类型匹配）

```java
@Configuration
@ComponentScan("com.zero")
public class SpringConfig {
    /**
     * 用于创建一个QueryRunner对象,此法创建的默认为单例的
     */
    @Bean(name="runner")
    //@Scope("prototype")多例
    public QueryRunner createQueryRunner(DataSource dataSource){
        return new QueryRunner(dataSource);
    }
    /**
     * 创建数据源对象
     */
    @Bean(name="dataSource")
    public DataSource createDaaSource() throws PropertyVetoException {
        ComboPooledDataSource ds = new ComboPooledDataSource();
        ds.setDriverClass("com.mysql.jdbc.Driver");
        ds.setJdbcUrl("jdbc:mysql://localhost/3306/eesy");
        ds.setUser("root");
        ds.setPassword("1234");
        return ds;
    }
}
```



**@ComponentScan**

作用：用于通过注解指定spring在创建容器时要扫描的包

```java
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan("com.zero")
public class Main {
    public static void main(String[] args) {
        ConfigurableApplicationContext run = SpringApplication.run(Main.class, args);
    }
}

```



**@Import**

给某个类导入Bean，使用默认的无参构造方法（一般设计bean可以使用无参构造，后面用set方法去设置）

```java
@Configuration(proxyBeanMethods = false)   // 告诉 SpringBoot这是一个配置类==配置文件
@Import({User.class, DBHelper.class})       // 给容器中自动创建出这两个类型的组件，默认组件的名字就是全类名
public class MyConfig {

    @Bean //给容器中添加组件。以方法名作为组件的id。返回类型就是组件类型
    public User user01(){
        return new User("zhangsan", 15);
    }

    @Bean("tom")
    public Pet cat(){
        return new Pet("niuniu");
    }
}

```

@Import 高级用法： https://www.bilibili.com/video/BV1gW411W7wy?p=8

**@Conditional**

条件装配：满足Conditional指定的条件，则进行组件注入

Conditional有很多派生类，如下

![image-20210314172159861](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210314172159861.png)

以下举例说明ConditionalOnBean，存在时才执行实例化

```java
@Configuration(proxyBeanMethods = true)   // 告诉 SpringBoot这是一个配置类==配置文件
public class MyConfig {

    //    @ConditionalOnMissingBean(name="tom")
    @ConditionalOnBean(name="tom")      // MyConfig 实例化是按顺序来的，此时不存在tom示例
    @Bean //给容器中添加组件。以方法名作为组件的id。返回类型就是组件类型
    public User user01(){
        User user = new User("zhangsan", 15);
        user.setPet(cat());
        return user;
    }

    @Bean("tom")
    public Pet cat(){
        return new Pet("niuniu");
    }

}
```

验证代码

```java
@SpringBootApplication
public class Main {
    public static void main(String[] args) {
        ConfigurableApplicationContext run = SpringApplication.run(Main.class, args);

        boolean tom = run.containsBean("tom");			// true，后面被实例化了
        System.out.println("容器中Tom组件："+tom);

        boolean user01 = run.containsBean("user01");	// false，一开始没有tom
        System.out.println("容器中user01组件："+user01);

        boolean tom22 = run.containsBean("tom22");		// false，压根没有tom22
        System.out.println("容器中tom22组件："+tom22);
    }
}

```



**@ImportResource**

有一些Spring的bean.xml做迁移成注解的方式比较麻烦，SpringBoot提供xml直接转换成config的注解@ImportResource

```xml

<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context https://www.springframework.org/schema/context/spring-context.xsd">

    <bean id="haha" class="com.atguigu.boot.bean.User">
        <property name="name" value="zhangsan"></property>
        <property name="age" value="18"></property>
    </bean>

    <bean id="hehe" class="com.atguigu.boot.bean.Pet">
        <property name="name" value="tomcat"></property>
    </bean>
</beans>
```


```java
@ImportResource("classpath:beans.xml")
public class MyConfig {

}
```



## 2. 配置绑定

如果我们需要从properties去解析自己的配置，用java程序可能需要自行解析封装进入bean

```java
public class getProperties {
     public static void main(String[] args) throws FileNotFoundException, IOException {
         Properties pps = new Properties();
         pps.load(new FileInputStream("a.properties"));
         Enumeration enum1 = pps.propertyNames();//得到配置文件的名字
         while(enum1.hasMoreElements()) {
             String strKey = (String) enum1.nextElement();
             String strValue = pps.getProperty(strKey);
             System.out.println(strKey + "=" + strValue);	// 打印key-value
             //封装到JavaBean。
         }
     }
 }
```

**@Component + @ConfigurationProperties**

使用@ConfigurationProperties，在定义实体类的时候就使用对应配置

```properties
# application.properties
mycar.brand=Audi
mycar.price=10000000
```

```java

/**
 * domain类
 * 只有在容器中的组件，才会有 SpringBoot提供的强大功能
 */
@Component
@ConfigurationProperties(prefix = "mycar")		// 使用上面定义的mycar前缀
public class Car {

    private String brand;
    private Integer price;

    @Override
    public String toString() {
        return "Car{" +
                "brand='" + brand + '\'' +
                ", price=" + price +
                '}';
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }

    public Integer getPrice() {
        return price;
    }

    public void setPrice(Integer price) {
        this.price = price;
    }
}

```

```java
// Controller

@RestController
public class CarController {
    @Autowired
    Car car;

    @RequestMapping("/car")
    public Car car(){
        return car;
    }
}
```

**@EnableConfigurationProperties + @ConfigurationProperties**

```java
/**
 * domain类
 */
@ConfigurationProperties(prefix = "mycar")		// 使用上面定义的mycar前缀
public class Car {

    private String brand;
    private Integer price;

	...
}
```

```java
// Controller
@RestController
@EnableConfigurationProperties(Car.class)		// //1、开启Car配置绑定功能 2、把这个Car这个组件自动注册到容器中
public class CarController {
    @Autowired
    Car car;

    @RequestMapping("/car")
    public Car car(){
        return car;
    }
}
```

