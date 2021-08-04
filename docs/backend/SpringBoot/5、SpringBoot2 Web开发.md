# Web开发

![image-20210322083004949](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210322083004949.png)

## 1. SpringMVC 自动配置

Spring Boot provides auto-configuration for Spring MVC that **works well with most applications.(大多场景我们都无需自定义配置)**

The auto-configuration adds the following features on top of Spring’s defaults:

- Inclusion of `ContentNegotiatingViewResolver` and `BeanNameViewResolver` beans.

- - 内容协商视图解析器和BeanName视图解析器

- Support for serving static resources, including support for WebJars (covered [later in this document](https://docs.spring.io/spring-boot/docs/current/reference/html/spring-boot-features.html#boot-features-spring-mvc-static-content))).

- - 静态资源（包括webjars）

- Automatic registration of `Converter`, `GenericConverter`, and `Formatter` beans.

- - 自动注册 `Converter，GenericConverter，Formatter `

- Support for `HttpMessageConverters` (covered [later in this document](https://docs.spring.io/spring-boot/docs/current/reference/html/spring-boot-features.html#boot-features-spring-mvc-message-converters)).

- - 支持 `HttpMessageConverters` （后来我们配合内容协商理解原理）

- Automatic registration of `MessageCodesResolver` (covered [later in this document](https://docs.spring.io/spring-boot/docs/current/reference/html/spring-boot-features.html#boot-features-spring-message-codes)).

- - 自动注册 `MessageCodesResolver` （国际化用）

- Static `index.html` support.

- - 静态index.html 页支持

- Custom `Favicon` support (covered [later in this document](https://docs.spring.io/spring-boot/docs/current/reference/html/spring-boot-features.html#boot-features-spring-mvc-favicon)).

- - 自定义 `Favicon`  

- Automatic use of a `ConfigurableWebBindingInitializer` bean (covered [later in this document](https://docs.spring.io/spring-boot/docs/current/reference/html/spring-boot-features.html#boot-features-spring-mvc-web-binding-initializer)).

- - 自动使用 `ConfigurableWebBindingInitializer` ，（DataBinder负责将请求数据绑定到JavaBean上）

> If you want to keep those Spring Boot MVC customizations and make more [MVC customizations](https://docs.spring.io/spring/docs/5.2.9.RELEASE/spring-framework-reference/web.html#mvc) (interceptors, formatters, view controllers, and other features), you can add your own `@Configuration` class of type `WebMvcConfigurer` but **without** `@EnableWebMvc`.
>
> **不用@EnableWebMvc注解。使用** **`@Configuration`** **+** **`WebMvcConfigurer`** **自定义规则**



> If you want to provide custom instances of `RequestMappingHandlerMapping`, `RequestMappingHandlerAdapter`, or `ExceptionHandlerExceptionResolver`, and still keep the Spring Boot MVC customizations, you can declare a bean of type `WebMvcRegistrations` and use it to provide custom instances of those components.
>
> **声明** **`WebMvcRegistrations`** **改变默认底层组件**



> If you want to take complete control of Spring MVC, you can add your own `@Configuration` annotated with `@EnableWebMvc`, or alternatively add your own `@Configuration`-annotated `DelegatingWebMvcConfiguration` as described in the Javadoc of `@EnableWebMvc`.
>
> **使用** **`@EnableWebMvc+@Configuration+DelegatingWebMvcConfiguration 全面接管SpringMVC`**



## 2. 静态资源映射功能

只要将静态资源放在类路径下：  `/static` (or `/public` or `/resources` or `/META-INF/resources` ，上述四个都可以

就能通过路径方式访问 ： 当前项目根路径/ + 静态资源名 

![image-20210322084249841](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210322084249841.png)

原理： 静态映射/**。

请求进来，**先去找Controller看能不能处理。不能处理的所有请求又都交给静态资源处理器**。静态资源也找不到则响应404页面

```java
@RestController
public class TestController {

    @RequestMapping("/1.jpg")
    public String handle(){
        return "aaaaaa";
    }
}
```

![image-20210322085146151](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210322085146151.png)

1. 改变默认的静态资源访问路径

   当前项目 + static-path-pattern + 静态资源名 = 静态资源文件夹下找

```yaml
spring:
  mvc:
    static-path-pattern: /zero/**
```

![image-20210322085606141](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210322085606141.png)

2. 改变默认的静态资源存放有效路径

```yaml
spring:
  web:
    resources:
      static-locations: classpath:/test/
```

![image-20210322091041580](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210322091041580.png)



**web jar 自动映射**

自动映射 /[webjars](http://localhost:8080/webjars/jquery/3.5.1/jquery.js)/**

https://www.webjars.org/

```xml
        <dependency>
            <groupId>org.webjars</groupId>
            <artifactId>jquery</artifactId>
            <version>3.5.1</version>
        </dependency>
```

访问地址：[http://localhost:8080/webjars/**jquery/3.5.1/jquery.js**](http://localhost:8080/webjars/jquery/3.5.1/jquery.js)  后面地址要按照依赖里面的包路径



**欢迎页配置**

- 静态资源路径下  index.html

- - 可以配置静态资源路径
  - 但是不可以配置静态资源的访问前缀。否则导致 index.html不能被默认访问

```yaml
spring:
# 这个会导致welcome page功能失效
#  mvc:
#    static-path-pattern: /zero/**
  web:
    resources:
      static-locations: classpath:/test/
```

- controller能处理/index



**自定义网站图标icon**

favicon.ico 放在静态资源目录下即可。前后端分离项目这部分由前端负责

```yaml
spring:
#  mvc:
#    static-path-pattern: /zero/**   这个会导致 Favicon 功能失效
```



## 3. 静态资源配置原理

SpringBoot启动默认加载  xxxAutoConfiguration 类（自动配置类）

SpringMVC功能的自动配置类`WebMvcAutoConfiguration`，生效

```java
@Configuration(proxyBeanMethods = false)
@ConditionalOnWebApplication(type = Type.SERVLET)
@ConditionalOnClass({ Servlet.class, DispatcherServlet.class, WebMvcConfigurer.class })  // 包下包括这几个类
@ConditionalOnMissingBean(WebMvcConfigurationSupport.class)
@AutoConfigureOrder(Ordered.HIGHEST_PRECEDENCE + 10)
@AutoConfigureAfter({ DispatcherServletAutoConfiguration.class, TaskExecutionAutoConfiguration.class,
        ValidationAutoConfiguration.class })
public class WebMvcAutoConfiguration {}
```

查看给容器中有一个静态内部类

```java
	@Configuration(
        proxyBeanMethods = false
    )
    @Import({WebMvcAutoConfiguration.EnableWebMvcConfiguration.class})
    @EnableConfigurationProperties({WebMvcProperties.class, ResourceProperties.class, WebProperties.class})
    @Order(0)
    public static class WebMvcAutoConfigurationAdapter implements WebMvcConfigurer {
    	...
    }
```

配置文件的相关属性和xxx进行了绑定。`WebMvcProperties==spring.mvc`、`ResourceProperties==spring.resources`、`WebProperties==spring.web`，2.4版本把spring.resources归到了spring.web下

**1、配置类只有一个有参构造器**

```java
	//有参构造器所有参数的值都会从容器中确定
//WebProperties 获取和webProperties spring.web绑定的所有值对象
//WebMvcProperties mvcProperties 获取和spring.mvc绑定的所有的值的对象
//ListableBeanFactory beanFactory Spring的beanFactory，Spring的beanFactory
//HttpMessageConverters 找到所有的HttpMessageConverters
//ResourceHandlerRegistrationCustomizer 找到 资源处理器的自定义器。
//DispatcherServletPath  
//ServletRegistrationBean   给应用注册Servlet、Filter....
	public WebMvcAutoConfigurationAdapter(WebProperties webProperties, WebMvcProperties mvcProperties, ListableBeanFactory beanFactory, ObjectProvider<HttpMessageConverters> messageConvertersProvider, ObjectProvider<WebMvcAutoConfiguration.ResourceHandlerRegistrationCustomizer> resourceHandlerRegistrationCustomizerProvider, ObjectProvider<DispatcherServletPath> dispatcherServletPath, ObjectProvider<ServletRegistrationBean<?>> servletRegistrations) {
            this.mvcProperties = mvcProperties;
            this.beanFactory = beanFactory;
            this.messageConvertersProvider = messageConvertersProvider;
            this.resourceHandlerRegistrationCustomizer = (WebMvcAutoConfiguration.ResourceHandlerRegistrationCustomizer)resourceHandlerRegistrationCustomizerProvider.getIfAvailable();
            this.dispatcherServletPath = dispatcherServletPath;
            this.servletRegistrations = servletRegistrations;
            this.mvcProperties.checkConfiguration();
        }
```

**2、 资源处理的默认规则**

2.4.3版本`addResourceHandlers`变为了重载方法，实际其他两个被一个调用，这里设置路径为`/META-INF/resources/webjars/`并按设置的缓存时间对静态资源缓存

```java
		protected void addResourceHandlers(ResourceHandlerRegistry registry) {
            super.addResourceHandlers(registry);
            if (!this.resourceProperties.isAddMappings()) {		// addMappings属性确定配置是否生效，配置false不生效
                logger.debug("Default resource handling disabled");
            } else {
                ServletContext servletContext = this.getServletContext();
                //webjars的规则
                this.addResourceHandler(registry, "/webjars/**", "classpath:/META-INF/resources/webjars/");
                // 获取mvcProperties设置的静态资源路径
                this.addResourceHandler(registry, this.mvcProperties.getStaticPathPattern(), (registration) -> {
                    registration.addResourceLocations(this.resourceProperties.getStaticLocations());
                    if (servletContext != null) {
                        registration.addResourceLocations(new Resource[]{new ServletContextResource(servletContext, "/")});
                    }

                });
            }
        }

		private void addResourceHandler(ResourceHandlerRegistry registry, String pattern, String... locations) {
            this.addResourceHandler(registry, pattern, (registration) -> {
                registration.addResourceLocations(locations);
            });
        }

        private void addResourceHandler(ResourceHandlerRegistry registry, String pattern, Consumer<ResourceHandlerRegistration> customizer) {
            if (!registry.hasMappingForPattern(pattern)) {
                ResourceHandlerRegistration registration = registry.addResourceHandler(new String[]{pattern});
                customizer.accept(registration);
                registration.setCachePeriod(this.getSeconds(this.resourceProperties.getCache().getPeriod()));
 			  //  设置过期时间
         registration.setCacheControl(this.resourceProperties.getCache().getCachecontrol().toHttpCacheControl());
                this.customizeResourceHandlerRegistration(registration);
            }
        }
```

add-mapping配置

```yaml
spring:
  web:
    resources:
      static-locations: classpath:/test/
      add-mappings: false
```

Resources 默认的静态资源路径

```java
@ConfigurationProperties("spring.web")
public class WebProperties {	
	public static class Resources {
        private static final String[] CLASSPATH_RESOURCE_LOCATIONS = new String[]{"classpath:/META-INF/resources/", "classpath:/resources/", "classpath:/static/", "classpath:/public/"};
        private String[] staticLocations;
        private boolean addMappings;
        private boolean customized;
        private final WebProperties.Resources.Chain chain;
        private final WebProperties.Resources.Cache cache;
        ... 
	}
 	...   
}
```

**3、欢迎页的处理规则**

HandlerMapping：处理器映射。保存了每一个Handler能处理哪些请求。 

```java
		@Bean
        public WelcomePageHandlerMapping welcomePageHandlerMapping(ApplicationContext applicationContext, FormattingConversionService mvcConversionService, ResourceUrlProvider mvcResourceUrlProvider) {
            WelcomePageHandlerMapping welcomePageHandlerMapping = new WelcomePageHandlerMapping(new TemplateAvailabilityProviders(applicationContext), applicationContext, this.getWelcomePage(), this.mvcProperties.getStaticPathPattern());
            welcomePageHandlerMapping.setInterceptors(this.getInterceptors(mvcConversionService, mvcResourceUrlProvider));
            welcomePageHandlerMapping.setCorsConfigurations(this.getCorsConfigurations());
            return welcomePageHandlerMapping;
        }
```



```java
	WelcomePageHandlerMapping(TemplateAvailabilityProviders templateAvailabilityProviders, ApplicationContext applicationContext, Resource welcomePage, String staticPathPattern) {
        if (welcomePage != null && "/**".equals(staticPathPattern)) {//要用欢迎页功能，必须是/**
            logger.info("Adding welcome page: " + welcomePage);
            this.setRootViewName("forward:index.html");
        } else if (this.welcomeTemplateExists(templateAvailabilityProviders, applicationContext)) {// 调用Controller  看谁能匹配/index的请求
            logger.info("Adding welcome page template: index");
            this.setRootViewName("index");
        }

    }
```



## 4. 请求参数处理

- @RequestMapping；
- Rest风格支持（*使用**HTTP**请求方式动词来表示对资源的操作*）

- - *以前：**/getUser*  *获取用户*   */deleteUser* *删除用户*   */editUser*  *修改用户*    */saveUser* *保存用户*
  - *现在： /user*   *GET-获取用户*   *DELETE-删除用户*   *PUT-修改用户*    *POST-保存用户*
  - 核心Filter；HiddenHttpMethodFilter
    - 用法： 表单method=post，隐藏域 _method=put
    - SpringBoot中手动开启
  - 扩展：如何把_method 这个名字换成我们自己喜欢的。

测试rest风格：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>你好，欢迎光临</h1>

测试rest风格
<form action="/user" method="get">
    <input value="REST-GET 提交" type="submit">
</form>
<form action="/user" method="post">
    <input value="REST-POST 提交" type="submit">
</form>
<form action="/user" method="delete">
    <input value="REST-DELETE 提交" type="submit">
</form>
<form action="/user" method="put">
    <input value="REST-PUT 提交" type="submit">
</form>
</body>
</html>
```

```java
@RestController
public class TestController {

    @RequestMapping(value = "/user", method = RequestMethod.GET)
    public String getUser() {
        return "GET-张三";
    }

    @RequestMapping(value = "/user", method = RequestMethod.POST)
    public String saveUser() {
        return "POST-张三";
    }


    @RequestMapping(value = "/user", method = RequestMethod.PUT)
    public String putUser() {
        return "PUT-张三";
    }

    @RequestMapping(value = "/user", method = RequestMethod.DELETE)
    public String deleteUser() {
        return "DELETE-张三";
    }
}

```

发现delete和put请求都用了get 方法处理

![image-20210325085620958](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210325085620958.png)

源码提示，想用rest风格，需要使用隐藏域，且需要配置spring.mvc.hiddenmethod.filter=true

```java
    @Bean
    @ConditionalOnMissingBean({HiddenHttpMethodFilter.class})
    @ConditionalOnProperty(
        prefix = "spring.mvc.hiddenmethod.filter",
        name = {"enabled"},
        matchIfMissing = false			// 默认不开启
    )
    public OrderedHiddenHttpMethodFilter hiddenHttpMethodFilter() {
        return new OrderedHiddenHttpMethodFilter();			// 接着看该fitter
    }
```

```java
// 接着看父类HiddenHttpMethodFilter
public class OrderedHiddenHttpMethodFilter extends HiddenHttpMethodFilter implements OrderedFilter {
    public static final int DEFAULT_ORDER = -10000;
    private int order = -10000;

    public OrderedHiddenHttpMethodFilter() {
    }

    public int getOrder() {
        return this.order;
    }

    public void setOrder(int order) {
        this.order = order;
    }
}
```

```java
public class HiddenHttpMethodFilter extends OncePerRequestFilter {
    private static final List<String> ALLOWED_METHODS;
    public static final String DEFAULT_METHOD_PARAM = "_method";
    private String methodParam = "_method";
    ...
}
```

如下修改

```yaml
spring:
  mvc:
    hiddenmethod:
      filter:
        enabled: true
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>你好，欢迎光临</h1>

测试rest风格
<form action="/user" method="get">
    <input value="REST-GET 提交" type="submit">
</form>
<form action="/user" method="post">
    <input value="REST-POST 提交" type="submit">
</form>
<form action="/user" method="post">
    <input name="_method" type="hidden" value="DELETE">
    <input value="REST-DELETE 提交" type="submit">
</form>
<form action="/user" method="post">
    <input name="_method" type="hidden" value="PUT">
    <input value="REST-PUT 提交" type="submit">
</form>
</body>
</html>
```

可以看到post发送带隐藏域的会自动解析成对应方法给处理器处理

![image-20210325090530163](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210325090530163.png)

![image-20210325090617065](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210325090617065.png)

Rest原理（表单提交要使用REST的时候）

- 表单提交会带上**_method=PUT**
- **请求过来被**HiddenHttpMethodFilter拦截
  - 请求是否正常，并且是POST
    - 获取到**_method**的值。
    - 兼容以下请求；**PUT**.**DELETE**.**PATCH**
    - **原生request（post），包装模式requesWrapper重写了getMethod方法，返回的是传入的值（即PUT/DELETE/PATCH）。**
    - **过滤器链放行的时候用wrapper。以后的方法调用getMethod是调用requesWrapper的。**

**Rest使用客户端工具，**

- 如PostMan直接发送Put、delete等方式请求，无需Filter。

```java
public class HiddenHttpMethodFilter extends OncePerRequestFilter {
    private String methodParam = "_method";
    private static final List<String> ALLOWED_METHODS;
    
    static {
        ALLOWED_METHODS = Collections.unmodifiableList(Arrays.asList(HttpMethod.PUT.name(), HttpMethod.DELETE.name(), HttpMethod.PATCH.name()));		// 允许PUT、DELETE、PATCH
    }
	...
	protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        HttpServletRequest requestToUse = request;
        if ("POST".equals(request.getMethod()) && request.getAttribute("javax.servlet.error.exception") == null) {
            String paramValue = request.getParameter(this.methodParam);		// 拿到_method参数
            if (StringUtils.hasLength(paramValue)) {
                String method = paramValue.toUpperCase(Locale.ENGLISH);		// 转大写
                if (ALLOWED_METHODS.contains(method)) {
                    requestToUse = new HiddenHttpMethodFilter.HttpMethodRequestWrapper(request, method);			// 新建wrapper对象
                }
            }
        }

        filterChain.doFilter((ServletRequest)requestToUse, response);		// 执行HttpMethodRequestWrapper的方法
    }
    
    private static class HttpMethodRequestWrapper extends HttpServletRequestWrapper {
        private final String method;

        public HttpMethodRequestWrapper(HttpServletRequest request, String method) {
            super(request);
            this.method = method;
        }

        public String getMethod() {
            return this.method;
        }
    }
	...   
}
```

如果想修改_method 名称，可以如下操作，更清晰认识容器，这里非单例模式也生效的原因应该是原本名称也为hiddenHttpMethodFilter

```java
@Configuration(proxyBeanMethods = false)
public class WebCoifg {
    @Bean
    public HiddenHttpMethodFilter hiddenHttpMethodFilter(){
        HiddenHttpMethodFilter methodFilter = new HiddenHttpMethodFilter();
        methodFilter.setMethodParam("_m");
        return methodFilter;
    }
}
```



## 5. 请求映射原理

SpringMVC功能分析都从 org.springframework.web.servlet.DispatcherServlet-》doDispatch()

![image-20210327224355462](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210327224355462.png)

doDispatch 方法

```java
    protected void doDispatch(HttpServletRequest request, HttpServletResponse response) throws Exception {
        // 初始化一些变量
        HttpServletRequest processedRequest = request;
        HandlerExecutionChain mappedHandler = null;			// 执行链
        boolean multipartRequestParsed = false;				// 是否文件上传标志
        WebAsyncManager asyncManager = WebAsyncUtils.getAsyncManager(request);		// 是不是异步请求

        try {
            try {
                ModelAndView mv = null;
                Object dispatchException = null;

                try {
                    processedRequest = this.checkMultipart(request);		// 判断是否为文件上传
                    multipartRequestParsed = processedRequest != request;
                    // 找到当前请求使用哪个Handler（Controller的方法）处理
                    mappedHandler = this.getHandler(processedRequest);
                    if (mappedHandler == null) {
                        this.noHandlerFound(processedRequest, response);
                        return;
                    }

                    HandlerAdapter ha = this.getHandlerAdapter(mappedHandler.getHandler());
                    String method = request.getMethod();
                    boolean isGet = "GET".equals(method);
                    if (isGet || "HEAD".equals(method)) {
                        long lastModified = ha.getLastModified(request, mappedHandler.getHandler());
                        if ((new ServletWebRequest(request, response)).checkNotModified(lastModified) && isGet) {
                            return;
                        }
                    }

                    if (!mappedHandler.applyPreHandle(processedRequest, response)) {
                        return;
                    }

                    mv = ha.handle(processedRequest, response, mappedHandler.getHandler());
                    if (asyncManager.isConcurrentHandlingStarted()) {
                        return;
                    }

                    this.applyDefaultViewName(processedRequest, mv);
                    mappedHandler.applyPostHandle(processedRequest, response, mv);
                } catch (Exception var20) {
                    dispatchException = var20;
                } catch (Throwable var21) {
                    dispatchException = new NestedServletException("Handler dispatch failed", var21);
                }

                this.processDispatchResult(processedRequest, response, mappedHandler, mv, (Exception)dispatchException);
            } catch (Exception var22) {
                this.triggerAfterCompletion(processedRequest, response, mappedHandler, var22);
            } catch (Throwable var23) {
                this.triggerAfterCompletion(processedRequest, response, mappedHandler, new NestedServletException("Handler processing failed", var23));
            }

        } finally {
            if (asyncManager.isConcurrentHandlingStarted()) {
                if (mappedHandler != null) {
                    mappedHandler.applyAfterConcurrentHandlingStarted(processedRequest, response);
                }
            } else if (multipartRequestParsed) {
                this.cleanupMultipart(processedRequest);
            }

        }
    }

```

getHandler方法

```java
	@Nullable
    protected HandlerExecutionChain getHandler(HttpServletRequest request) throws Exception {
         //HandlerMapping：处理器映射。/xxx->>xxxx
        if (this.handlerMappings != null) {
            Iterator var2 = this.handlerMappings.iterator();

            while(var2.hasNext()) {
                HandlerMapping mapping = (HandlerMapping)var2.next();
                HandlerExecutionChain handler = mapping.getHandler(request);
                if (handler != null) {
                    return handler;
                }
            }
        }
        return null;
    }
```

**RequestMappingHandlerMapping**：保存了所有@RequestMapping 和handler的映射规则。

![image-20210327231724845](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210327231724845.png)

![image-20210327232122489](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210327232122489.png)

总结：所有的请求映射都在HandlerMapping中。

- SpringBoot自动配置欢迎页的 WelcomePageHandlerMapping 。访问 /能访问到index.html；
- SpringBoot自动配置了默认 的 RequestMappingHandlerMapping
- 请求进来，遍历尝试所有的HandlerMapping看是否能匹配请求信息。

- - 如果有就找到这个请求对应的handler
  - 如果没有就是下一个 HandlerMapping

- 我们需要一些自定义的映射处理，我们也可以自己给容器中放**HandlerMapping**。自定义 **HandlerMapping**



## 6. 参数和基本注解

@PathVariable、@RequestHeader、@ModelAttribute、@RequestParam、@MatrixVariable、@CookieValue、@RequestBody

如请求路径

```
c/car/3/owner/lisi?age=18&in=basketball&in=game
```

@PathVariable：获取路径或其中的某个值（/car/3/owner/lisi）

@RequestHeader：获取请求头或其中的值

@RequestParam：获取请求参数的某个值（in=basketball&in=game）

@CookieValue：获取cookie值

@RequestBody：获取request body值

示例

```java
@RestController
public class ParameterTestController {
    @GetMapping("/car/{id}/owner/{username}")
    public Map<String, Object> getCar(@PathVariable Integer id,
                                      @PathVariable("username") String name,
                                      @PathVariable Map<String, String> pv, // pv，将请求中的PathVariable参数映射到该map
                                      @RequestHeader("User-Agent") String userAgent,
                                      @RequestHeader HttpHeaders headers,
                                      @RequestHeader Map<String, String> headMap,   // 获取全量请求头信息
                                      @RequestParam("age") Integer age,
                                      @RequestParam("in")List<String> ins,
                                      @RequestParam Map<String, List<String>> params,   // Map只能拿到列表一个元素放到key，value
                                      @RequestParam MultiValueMap<String, String> params2,
                                      @CookieValue("_ga") String _ga,
                                      @CookieValue("_ga") Cookie _ga2){
        Map<String, Object> map = new HashMap<>();
        map.put("id", id);
        map.put("name", name);
        map.put("pv", pv);
        map.put("userAgent", userAgent);
        map.put("header", headers);
        map.put("headMap", headMap);
        map.put("age", age);
        map.put("in", ins);
        map.put("map", params);
        map.put("map2", params2);
        map.put("_ga", _ga);
        map.put("_ga2", _ga2);
        return map;
    }

    @PostMapping("/save")
    public Map postMethod(@RequestBody String body){
        Map<String, Object> map = new HashMap<>();
        map.put("body", body);
        return map;
    }
}
```

```java
@Controller		// 主要用@Controller而不是@RestController
public class AttributeController {
    @GetMapping("/goto")
    public String goToPage(HttpServletRequest request){
        request.setAttribute("msg", "成功");
        request.setAttribute("code", "200");
        return "forward:/success";
    }

    @ResponseBody
    @GetMapping("/success")
    public Map<String, Object> success(@RequestAttribute("msg") String msg,
                                       @RequestAttribute("code") String code){
        Map<String, Object> map = new HashMap<>();
        map.put("msg", msg);
        map.put("code", code);
        return map;
    }
}

```

@MatrixVariable：矩阵变量

这个功能是被SpringBoot默认禁用的，手动开启：原理。对于路径的处理。UrlPathHelper进行解析。

removeSemicolonContent（移除分号内容）支持矩阵变量的。可以通过`/cars/sell;low=34;brand=byd;brand=audi;brand=yd`访问，通过@MatrixVariable取到，**矩阵变量必须有url路径变量（如{path}）才能被解析**，前面的路径只能带一个参数，最后一个路径可以带多个参数

先修改取消分号设置

```java
@Configuration(proxyBeanMethods = false)
public class WebCoifg {
    @Bean
    public WebMvcConfigurer webMvcConfigurer(){
        return new WebMvcConfigurer() {
            @Override
            public void configurePathMatch(PathMatchConfigurer configurer) {
                UrlPathHelper urlPathHelper = new UrlPathHelper();
                // 设置不移除分号内容
                urlPathHelper.setRemoveSemicolonContent(false);
                configurer.setUrlPathHelper(urlPathHelper);
            }
        };
    }
}

```

controller

```java
@RestController
public class ParameterTestController {

    	
   //cars/sell;low=34;brand=byd;brand=audi;brand=yd
    @GetMapping("/cars/{path}")
    public Map carsSell(@MatrixVariable("low") Integer low,
                        @MatrixVariable("brand") List<String> brands){
        Map<String, Object> map = new HashMap<>();
        map.put("low", low);
        map.put("brands", brands);
        return map;
    }

    // /boss/1;age=20/2;age=10
    @GetMapping("/boss/{bossId}/{empId}")
    public Map boss(@MatrixVariable(value = "age", pathVar = "bossId") Integer bossAge,
                        @MatrixVariable(value = "age", pathVar = "empId") List<String> empAge){
        Map<String, Object> map = new HashMap<>();
        map.put("bossAge", bossAge);
        map.put("empAge", empAge);
        return map;
    }
}
```





## 7.  参数处理原理

HandlerMapping中找到能处理请求的Handler（Controller.method()）

为当前Handler 找一个适配器 HandlerAdapter； **RequestMappingHandlerAdapter** ()

![image-20210327231724845](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210327231724845.png)

适配器执行目标方法并确定方法参数的每一个值



```java
//DispatcherServlet -- doDispatch

// Actually invoke the handler.
mv = ha.handle(processedRequest, response, mappedHandler.getHandler());
```

```java
// RequestMappingHandlerMapping

mav = invokeHandlerMethod(request, response, handlerMethod); //执行目标方法


//ServletInvocableHandlerMethod
Object returnValue = invokeForRequest(webRequest, mavContainer, providedArgs);
//获取方法的参数值
Object[] args = getMethodArgumentValues(request, mavContainer, providedArgs);
```





![image-20210406132247865](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210406132247865.png)