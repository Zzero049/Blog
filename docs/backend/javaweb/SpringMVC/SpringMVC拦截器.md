## 拦截器
&emsp;Spring MVC的处理器拦截器类似于Servlet开发中的过滤器Filter，用于对处理器进行预处理和后处理。
&emsp;用户可以自己定义一些拦截器来实现特定的功能。
&emsp;谈到拦截器，还要向大家提一个词—拦截器链（Interceptor Chain）。拦截器链就是将拦截器按一定的顺序联结成一条链。在访问被拦截的方法或字段时，拦截器链中的拦截器就会按其之前定义的顺序被调用。
&emsp;说到这里，可能大家脑海中有了一个疑问，这不是我们之前学的过滤器吗？是的它和过滤器是有几分相似，但是也有区别，接下来我们就来说说他们的区别：

&emsp;&emsp;过滤器是servlet规范中的一部分，任何java web工程都可以使用。
&emsp;&emsp;拦截器是SpringMVC框架自己的，只有使用了SpringVC框架的工程才能用。
&emsp;&emsp;过滤器在url-pattern中配置了/*之后，可以对所有要访问的资源拦截。
&emsp;&emsp;拦截器它是只会拦截访问的控制器方法，如果访问的是jsp，html，css，image或者js是不会进行拦截的。

它也是AOP思想的具体应用。
我们要想自定义拦截器，要求必须实现：**HandlerInterceptor接口。**

1.编写拦截器类，实现HandlerInterceptor接口
有以下方法，都有默认实现
<img src="pictures/Annotation 2020-04-14 145756.png">

```java
public class MyInterceptor1 implements HandlerInterceptor {
    /**
     * 预处理：在Controller方法之前
     * return true放行，执行下一个拦截器，如果没有，执行controlLer中的方法
     * return false不放行
     * @param request
     * @param response
     * @param handler
     * @return
     * @throws Exception
     */
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        System.out.println("preHandle处理");
        return true;
    }
}
```

2.配置拦截器
```xml
<!--配置拦截器-->
    <mvc:interceptors>
        <!--配置拦截器-->
        <mvc:interceptor>
            <!--要拦截的具体的方法-->
            <mvc:mapping path="/user/**"/>
            <!--不要拦截的方法
            <mvc:excLude-mapping path=""/>
            -->
            <！--配置拦截器对象-->
            <bean class="cn.itcast.controller.gn.itcast.interceptor.MyInterceptorl"/>
        </mvc:interceptor>
    </mvc:interceptors>
```
<img src="pictures/Annotation 2020-04-14 151012.png">
