

## @RequestMapping(path="")
用于建立请求URL和处理请求方法之间的对应关系。
可以加到类上，也可以加在方法上，加在类上代表该类所有方法的资源路径前缀为${path}
    
####  属性
* value：用于指定请求的URL。它和path属性的作用是一样的。
* method：用于指定请求的方式。（枚举类RequestMethod.GET，RequestMethod.POST等）
* params：用于指定限制请求参数的条件。它支持简单的表达式。要求请求参数的key和value必须和配置的一模一样。
例如：
params={"accountName"},表示请求参数必须有 accountName (如a标签中href="user/testRequestMapping?accountName=haha")
params={"moeny!=100"}，表示请求参数中money不能是100。

* headers：请求消息中必须有的值，用于指定限制请求消息头的条件。

注意：
以上四个属性只要出现2个或以上时，他们的关系是与的关系。

## @RequestParam
把请求中指定名称的参数给控制器中的形参赋值。
#### 属性：
value：请求参数中的名称。
required：请求参数中是否必须提供此参数。默认值；true。表示必须提供，如果不提供将报错。

```java
public String testRequestParam(@RequestParam(name="name")String username)
```

## @RequestBody
* 用于获取请求体内容。直接使用得到是key=valueskey=value...结构的数据。
* get请求方式不适用。
#### 属性：
required；是否必须有请求体。默认值是：true。当取值为true时，get请求方式会报错。如果取值为false，get 请求得到是null。

```java
public String testRequestParam(@RequestBody String body)
```

## @PathVariable
拥有绑定url中的占位符的。例如：url中有/delete/{id}，{id}就是占位符.是Restful编程风格用的注解
#### 属性
value：用于指定url中占位符名称。
required：是否必须提供占位符。

Restful风格的URL
1.请求路径一样，可以根据不同的请求方式去执行后台的不同方法

 restful风格的URL优点
1.结构清晰2.符合标准3.易于理解4.扩展方便

```java
@RequestMapping("/testPathVariable/{sid}")
public String testPathVariable(@PathVariable(name="sid")String id)
```

## @RequestHeader：
用于获取请求消息头。
#### 属性：
value：提供消息头名称required：是否必须有此消息头

注：
在实际开发中一般不怎么用。
```java
public String testRequestHeader(@RequestHeader(value="Accept")String header)
```

## CookieValue
用于把指定cookie名称的值传入控制器方法参数。
####属性：
value：指定cookie的名称。
required：是否必须有此 cookie。

注：
在实际开发中一般不怎么用。
```java
public String testCookieValue(@CookieValue(value="JSESSIONID") String cookieValue){
```

## @ModelAttribute
* 出现在方法上，表示当前方法会在控制器的方法执行之前，先执行。它可以修饰没有返回值的方法，也可以修饰有具体返回值的方法

* 出现在参数上，获取指定的数据给参数赋值。

#### 属性：
value：用于获取数据的key。key可以是POJo的属性名称，也可以是map结构的key。

应用场景：
当表单提交数据不是完整的实体类数据时，保证没有提交数据的字段使用数据库对象原来的数据。

例如：
我们在编辑一个用户时，用户有一个创建信息字段，该字段的值是不允许被修改的。在提交表单数据是肯定没有此字段的内容，一旦更新会把该字段内容置为null，此时就可以使用此注解解决问题。

```java
/**
*该方法会先执行，定义在方法上
*/
@ModelAttribute public User showUser（String uname）{
    System.out.printin("showUser执行了…");
    //通过用户查询数据库并返回数据（模拟）
    User user=new User();
    user.setUname(uname);
    user.setAge(20);
    user.setDate((new Date()))
    return user;
}
```

```java
/**
*作用在参数上
*/
@RequestMapping(value="/testModelAttribute")
public String testModelAttribute(@ModelAttribute("abc") User user){

}
@ModelAttribute 
public User showUser（String uname,Map<String,User> map）{
    System.out.printin("showUser执行了…");
    //通过用户查询数据库并返回数据（模拟）
    User user=new User();
    user.setUname(uname);
    user.setAge(20);
    user.setDate((new Date()))；
    map.put("abc",user);    //无返回值
}
```

## @SessionAttribute
用于多次执行控制器方法间的参数共享。作用在类上
#### 属性：
value：用于指定存入的属性名称
type：用于指定存入的数据类型。


```java
@Controller
@RequestMapping(path="/user")
@SessionAttributes(value={"msg"}) //把美美存入session域中
public class HelloController {
    @RequestMapping(value = "/testSessionAttributes")
    public String testSessionAttributes(Model model) {
        System.out.println("testSessionAttributes...");
        //底层会存储到request域对象中
        model.addAttribute("msg", "美美");
        return "success";
    }

    /**
     * 从session域获取值
     */
    @RequestMapping(value = "/getSessionAttributes")
    public String getSessionAttributes(ModelMap modelMap){
        System.out.println("getSessionAttributes");
        String msg = (String) modelMap.get("msg");
        System.out.println(msg);
        return "success";
    }
    /**
     * 清空session域的值
     */
    @RequestMapping(value="delSessionAttributes")
    public String delSessionAttributes(SessionStatus status){
        System.out.println("delSessionAttributes");
        status.setComplete();
        return "success"; 
    }
}
```
```java
@RequestMapping(value = "/testSessionAttributes")
    public String testSessionAttributes(Model model) {
        System.out.println("testSessionAttributes...");
        //底层会存储到request域对象中
        model.addAttribute("msg", "美美");
        return "success";
    }
```

```jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
    ${msg}
     ${sessionScope}
</body>
</html>
```
