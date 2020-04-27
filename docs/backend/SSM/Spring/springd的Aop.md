# Aop
AoP：全称是Aspect oriented programming即：面向切面编程。简单的说它就是把我们程序重复的代码抽取出来，在需要执行的时候，使用动态代理的技术，在不修改源码的基础上，对我们的已有方法进行增强。

作用：

在程序运行期间，不修改源码对已有方法进行增强。(通过实现动态代理)

优势：

减少重复代码

提高开发效率

维护方便

## spring中的aop
* Joinpoint（连接点）：
    * 所谓连接点是指那些被拦截到的点。在spring中，这些点指的是方法，因为spring只支持方法类型的连接点。（业务层里的方法如findAllAccount(),saveAccount()）
* Pointcut（切入点）：
    * 所谓切入点是指我们要对哪些Joinpoint进行拦截的定义。(连接点中需要被增强的方法)

* Advice（通知/增强）：
    * 所谓通知是指拦截到 Joinpoint 之后所要做的事情就是通知。
    * 通知的类型：前置通知，后置通知，异常通知，最终通知，环绕通知（整个invoke方法执行）。
    ![image-20200426025419851](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200426025419851.png)

* Introduction（引介）：
    * 引介是一种特殊的通知在不修改类代码的前提下，Introduction 可以在运行期为类动态地添加一些方法或Field。
* Target（目标对象）：
    * 代理的目标对象（被代理对象）
* Weaving（织入）：
    * 是指把增强应用到目标对象来创建新的代理对象的过程。
    * spring采用动态代理织入，而AspectJ采用编译期织入和类装载期织入。
* Proxy（代理）：
    * 一个类被AOP织入增强后，就产生一个结果代理类。
* Aspect（切面）：
    * 是切入点和通知（引介）的结合。（配置）


### 简单示例
需要依赖：aspectjweaver解析aop配置
```xml
        <dependency>
            <groupId>org.aspectj</groupId>
            <artifactId>aspectjweaver</artifactId>
            <version>1.8.7</version>
        </dependency>
```
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/aop
        https://www.springframework.org/schema/aop/spring-aop.xsd">

    <!--配置spring的Ioc，把service对象配置进来-->
    <bean id="service" class="day03_eesy_03springAOP.com.impl.AccountServiceImpl"></bean>

    <!--spring中基于xml的AOp配置步骤
        1. 把通知Bean也交给spring来管理
        2. 使用aop:config标签表明开始AOP的配置
        3、使用aop:aspect标签表明配置切面
                id属性：是给切面提供一个唯一标识
                ref属性：是指定通知类bean的Id。
        4、在aop:aspect标签的内部使用对应标签来配直通知的类型
                我们现在示例是让printLog方法在切入点方法执行之前之前：所以是前置通知
                aop:before：表示配置前置通知
                    method属性：用于指定Logger类中哪个方法是前置通知
                    pointcut属性：用于指定切入点表达式，该表达式的含义指的是对业务层中哪些方法增强

            切入点表达式的写法：
                关键字：execution（表达式）
                表达式：
                    访问修饰符 返回值  包名.包名.包名...类名.方法名(参数列表)
                标准的表达式写法：
                    public void day03_eesy_03springAOP.com.impl.AccountServiceImpl.saveAccount()
    -->
    <!--配置Logger类-->
    <bean id="logger" class="day03_eesy_03springAOP.com.utils.Logger"></bean>
    <!--配置AOP-->
    <aop:config>
        <!--配置切面-->
        <aop:aspect id="logAdvice" ref="logger">
            <!--配置通知的类型，并且建立通知方法和切入点的关联-->
            <aop:before method="printLog" pointcut="execution(public void day03_eesy_03springAOP.com.impl.AccountServiceImpl.saveAccount())"></aop:before>
            <!--后置通知-->
            <aop:after-returning method="printLog" pointcut="execution(public void day03_eesy_03springAOP.com.impl.AccountServiceImpl.saveAccount())"></aop:after-returning>
            <!--异常通知-->
            <aop:after-throwing method="printLog" pointcut="execution(public void day03_eesy_03springAOP.com.impl.AccountServiceImpl.saveAccount())"></aop:after-throwing>
            <!--最终通知-->
            <aop:after method="printLog" pointcut="execution(public void day03_eesy_03springAOP.com.impl.AccountServiceImpl.saveAccount())"></aop:after>
             <aop:after method="printLog" pointcut-ref="pt1"></aop:after>
             
            <!--pointcut标签写在aop:aspect标签内部只能当前切面使用。
                它还可以写在aop:aspect外面，此时就变成了所有切面可用-->

            <aop:pointcut id="pt1" expression="execution(public void day03_eesy_03springAOP.com.impl.AccountServiceImpl.saveAccount())"></aop:pointcut>
            
            
        </aop:aspect>
    </aop:config>

</beans>
```

### AOP配置
1. 把通知Bean也交给spring来管理
2. 使用aop:config标签表明开始AOP的配置
3. 使用aop:aspect标签表明配置切面
    * id属性：是给切面提供一个唯一标识
    * ref属性：是指定增强类bean的Id。
4. 在aop:aspect标签的内部使用对应标签来配直通知的类型
    * 我们现在示例是让printLog方法在切入点方法执行之前之前：所以是前置通知
      前置通知：在切入点方法执行之前执行
      后置通知：在切入点方法**正常执行之后**值
      异常通知：在切入点方法执行产生异常之后执行
      最终通知：无论切入点方法是否正常执行它都会在其后面执行
    
    * aop:before：表示配置前置通知
        * method属性：用于指定Logger类中哪个方法是前置通知
    * pointcut属性：用于指定切入点表达式，该表达式的含义指的是对业务层中哪些方法增强
   
   * 切入点表达式的写法：
        * 关键字：execution（表达式）
        * 表达式：
        * 访问修饰符 返回值  包名.包名.包名...类名.方法名(参数列表)
        
    * 标准的表达式写法：
         `public void day03_eesy_03springAOP.com.impl.AccountServiceImpl.saveAccount()`
      
         其中，访问修饰符可以省略`public void`==》`void `
   
      `day03_eesy_03springAOP.com.impl.AccountServiceImpl.saveAccount()`
         
   返回值可以使用通配符，表示任意返回值(void ==》*)
      
         包名可以使用通配符，表示任意包。但是有几级包，就需要写几个*

         `* *.*.*.AccountServiceImpl.saveAccount()`
   
         包名可以使用..表示当前包及其子包
         
         `* *..AccountServiceImpl.saveAccount()`
        
        类名和方法名都可以使用*来实现通配
        
        参数列表：可以直接写数据类型：
        
           &emsp;基本类型直接写名称 &emsp;int
           &emsp;用类型写包名.类名的方式  &emsp;java.lang.String
        
        可以使用通配符表示任意类型，但是必须有参数
        可以使用..表示有无参数均可，有参数可以是任意类型
        
    * 全通配写法
      
        * `* *..*.*(..)`

<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-03-27 153932.png"  div align=center />

#### 关于环绕通知
问题：
* 当我们配置了环绕通知之后，切入点方法没有执行，而通知方法执行了

分析：
* 通过对比动态代理中的环绕通知代码，发现动态代理的环绕通知有明确的切入点方法调用，而我们的代码中没有。

解决：
* Spring框架为我们提供了一个接口：ProceedingJoinPoint。该接口有一个方法proceed（），此方法就相当于明确调用切入点方法
* 该接口可以作为环绕通知的方法参数，在程序执行时，spring框架会为我们提供该接口的实现类供我们使用。

spring中的环绕通知：
* 它是spring框架为我们提供的一种可以在代码中手动控制增强方法何时执行的方式（通过代码控制前置、后置、异常通知而不是配置）
           
```xml
<aop:config>
    <aop:aspect>
        <aop:around method="aroundLog" pointcut-ref="pt1"></aop:around>
    </aop:aspect>
</aop:config>
```
```java
public Object aroundLog(ProceedingJoinPoint pjp){
        Object rtValue=null;
        try {
            Object[] args = pjp.getArgs();//得到方法执行所需参数
            System.out.println("前置通知");
            rtValue= pjp.proceed(args);//明确调用业务层方法（切入点方法）
            System.out.println("后置通知");
            return rtValue;
        } catch (Throwable throwable) {
            System.out.println("异常通知");
            throw new RuntimeException(throwable);
        }finally {
            System.out.println("最终通知");
        }
    }
```

### 通过注解的AOP

```java
@Component("logger")
@Aspect//表示当前类是一个切面类
public class Logger {
    @Pointcut("execution (* *..*.*(..))")
    private void pt1(){}
    @Before("pt1()")
    public void beforePrintLog(){
        System.out.println("前置");
    }
    @AfterReturning("pt1()")
    public void afterReturningPrintLog(){
        System.out.println("后置");
    }
    @AfterThrowing("pt1()")
    public void afterThrowingPrintLog(){
        System.out.println("异常");
    }
    @After("pt1()")
    public void afterPrintLog(){
        System.out.println("最终");
    }

   @Around("pt1()")
    public Object aroundLog(ProceedingJoinPoint pjp){
        Object rtValue=null;
        try {
            Object[] args = pjp.getArgs();//得到方法执行所需参数
            System.out.println("前置通知");
            rtValue= pjp.proceed(args);//明确调用业务层方法（切入点方法）
            System.out.println("后置通知");
            return rtValue;
        } catch (Throwable throwable) {
            System.out.println("异常通知");
            throw new RuntimeException(throwable);
        }finally {
            System.out.println("最终通知");
        }
    }
}
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/aop
        https://www.springframework.org/schema/aop/spring-aop.xsd
        http://www.springframework.org/schema/context
        https://www.springframework.org/schema/context/spring-context.xsd">
    
    <!--配置spring创建容器时要扫描的包-->
    <context:component-scan base-package="day03_eesy_03springAOP"></context:component-scan>
    <!--配置spring开启注解AOp的支持-->
    <aop:aspectj-autoproxy></aop:aspectj-autoproxy>


</beans>
```

注意，基于注解的AoP在调用顺序是有问题的，因此对于增强顺序敏感的业务需要改造成环绕方法

<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-03-27 180216.png"  div align=center />



### 不使用XML的配置方式

```java
@configuration 
@ComponentScan(basePackages="com.itheima")
@EnableAspectJAutoProxy 
public class springconfiguration {
}
```

