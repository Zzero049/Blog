#  使用SpringBoot 整合前端页面

## Spring Boot中JSP的使用

实际上SSM的内容写法是不变的。就是配置yml比以前的xml方便很多

1、配置pom.xml

```xml
	<parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.0.7.RELEASE</version>
    </parent>
    <dependencies>
        <!-- web-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!--整合jsp-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </dependency>

        <dependency>
            <groupId>org.apache.tomcat.embed</groupId>
            <artifactId>tomcat-embed-jasper</artifactId>
        </dependency>

        <!--        JSTL-->
        <dependency>
            <groupId>jstl</groupId>
            <artifactId>jstl</artifactId>
            <version>1.2</version>
        </dependency>
    </dependencies>
```

2、创建配置文件application.yml

```yaml
server:
  port: 8181

spring:
  mvc:
    view:
      prefix: /
      suffix: .jsp
```

3、编写Controller(与SpringMVC一致)

```java
@Controller
@RequestMapping("/hello")
public class HelloHandler {

    @GetMapping("/index")
    public String index(){
        System.out.println("index..");
        return "index";
    }
}
```

4、入口函数(Controller要在Application的子包里)

```java
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}

```



## Spring Boot中Thymeleat模版的使用(整合html)

html只能通过js的ajax获取java对象，但是如果是同步刷新页面，html是无法获取java对象的

Spring Boot 可以结合Thymeleaf模版来整合HTML，使用原生的HTML作为视图。

Thymeleaf 模版是面向 Web和独立环境的Java模版引擎，能够处理HTML、XML、JavaScript、CSS等。

```html
<!--html语句-->
<p th:text="${message}"></p>
```

1、pom.xml添加依赖

```xml
<parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.0.7.RELEASE</version>
    </parent>
    <dependencies>
        <!-- web-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-thymeleaf</artifactId>
        </dependency>
    </dependencies>
```

2、application.yml配置文件

```yaml
server:
  port: 8181
spring:
  thymeleaf:
    prefix: classpath:/templates/
    suffix: .html
    mode: HTML5
    encoding: UTF-8
    
```

3、Controller层

```java
@Controller
@RequestMapping("/index")
public class indexHandler {
    @GetMapping("/index")
    public String index(Model model){
        System.out.println("index..");
        List<Student> list = new ArrayList<>();
        list.add(new Student("1","张三"));
        list.add(new Student("2","李四"));
        list.add(new Student("3","王五"));
        model.addAttribute("list",list);
        return "index";
    }
}

```

4、HTML文件（在resources/templates包下）

```html
<!DOCTYPE html>

<!--引入标签,也可以放到下面html里面，不会标红-->
<html xmlns:th="http://www.thymeleaf.org"></html>
<!--正常页面html-->
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <table>
        <tr>
            <th>学生ID</th>
            <th>学生姓名</th>
        </tr>
        <!--th指的是xmls:th-->
        <tr th:each="student:${list}">
            <td th:text="${student.id}"></td>
            <td th:text="${student.name}"></td>
        </tr>
    </table>
</body>
</html>
```

5、Application类同上

```java
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
```

如果希望客户端可以直接访问HTML资源，将这些资源放置在static路径下即可，否则必须通过Handler的后台映射才可以访问静态资源（/后直接输入html文件全名）。

### Thymeleaf 常用语法

1、赋值、拼接  

```java
@GetMapping("/index2")
        public String index2(Map<String, String> map){
        map.put("name","张三");
        return"index";
        }
```

页面语句

```html
<p th:text="${name}"></p>
<p th:text="'学⽣姓名是'+${name}+2"></p>
<p th:text="|学⽣姓名是,${name}|"></p>
```

2、条件判断： if/unless

th:if 表示条件成⽴时显示内容， th:unless 表示条件不成⽴时显示内容

```java
@GetMapping("/if")
public String index3(Map<String,Boolean> map){
        map.put("flag",true);
        return "index";
        }
```

```html
<p th:if="${flag == true}" th:text="if判断成⽴"></p>
<p th:unless="${flag != true}" th:text="unless判断成⽴"></p>
```

3、循环

```java
@GetMapping("/index")
public String index(Model model){
	System.out.println("index...");
	List<Student> list = new ArrayList<>();
	list.add(new Student(1L,"张三",22));
	list.add(new Student(2L,"李四",23));
	list.add(new Student(3L,"王五",24));
	model.addAttribute("list",list);
	return "index";
}
```

```html
<table>
    <tr>
        <th>index</th>
        <th>count</th>
        <th>学⽣ID</th>
        <th>学⽣姓名</th>
        <th>学⽣年龄</th>
    </tr>
    <tr th:each="student,stat:${list}" th:style="'backgroundcolor:'+@{${stat.odd}?'#F2F2F2'}">
        <td th:text="${stat.index}"></td>
        <td th:text="${stat.count}"></td>
        <td th:text="${student.id}"></td>
        <td th:text="${student.name}"></td>
        <td th:text="${student.age}"></td>
    </tr>
</table>
```

stat 是状态变量，属性：

- index 集合中元素的index（从0开始）
- count 集合中元素的count（从1开始）
- size 集合的⼤⼩
- current 当前迭代变量
- even/odd 当前迭代是否为偶数/奇数（从0开始计算）
- first 当前迭代的元素是否是第⼀个
- last 当前迭代的元素是否是最后⼀个  



4、URL

Thymeleaf 对于 URL 的处理是通过 @{...} 进⾏处理，结合 th:href 、 th:src  

```html
<h1>Hello World</h1>
<a th:href="@{http://www.baidu.com}">跳转</a>
<a th:href="@{http://localhost:9090/index/url/{na}(na=${name})}">跳转2</a>
<img th:src="${src}">
<div th:style="'background:url('+ @{${src}} +');'">
<br/>
<br/>
<br/>
</div>
```

5、switch

```java
@GetMapping("/switch")
public String switchTest(Model model){
	model.addAttribute("gender","⼥");
	return "test";
}
```

```html
<div th:switch="${gender}">
	<p th:case="⼥">⼥</p>
	<p th:case="男">男</p>
	<p th:case="*">未知</p>
</div>
```

6、基本对象

- #ctx ：上下⽂对象
- #vars ：上下⽂变量
- #locale ：区域对象
- #request ： HttpServletRequest 对象
- #response ： HttpServletResponse 对象
- #session ： HttpSession 对象
- #servletContext ： ServletContext 对象  

```java
@GetMapping("/object")
public String object(HttpServletRequest request){
	request.setAttribute("request","request对象");
	request.getSession().setAttribute("session","session对象");
	return "test";
}
```

```html
<p th:text="${#request.getAttribute('request')}"></p>
<p th:text="${#session.getAttribute('session')}"></p>
<p th:text="${#locale.country}"></p>
```

7、内嵌对象
可以直接通过 # 访问。

- dates： java.util.Date 的功能⽅法
-  calendars： java.util.Calendar 的功能⽅法
-  numbers：格式化数字
-  strings： java.lang.String 的功能⽅法
-  objects： Object 的功能⽅法
-  bools：对布尔求值的⽅法
- arrays：操作数组的功能⽅法
-  lists：操作集合的功能⽅法
-  sets：操作集合的功能⽅法
-  maps：操作集合的功能⽅法  

```java
@GetMapping("/util")
public String util(Model model){
	model.addAttribute("name","zhangsan");
	model.addAttribute("users",new ArrayList<>());
	model.addAttribute("count",22);
	model.addAttribute("date",new Date());
	return "test";
}
```

```html
<!-- 格式化时间 -->
<p th:text="${#dates.format(date,'yyyy-MM-dd HH:mm:sss')}"></p>
<!-- 创建当前时间，精确到天 -->
<p th:text="${#dates.createToday()}"></p>
<!-- 创建当前时间，精确到秒 -->
<p th:text="${#dates.createNow()}"></p>
<!-- 判断是否为空 -->
<p th:text="${#strings.isEmpty(name)}"></p>
<!-- 判断List是否为空 -->
<p th:text="${#lists.isEmpty(users)}"></p>
<!-- 输出字符串⻓度 -->
<p th:text="${#strings.length(name)}"></p>
<!-- 拼接字符串 -->
<p th:text="${#strings.concat(name,name,name)}"></p>
<!-- 创建⾃定义字符串 -->
<p th:text="${#strings.randomAlphanumeric(count)}"></p>
```



