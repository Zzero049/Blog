

1.利用html的request和response直接进行响应（不使用视图解析器）
```java
@RequestMapping("/testVoid")
    public void testVoid(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
        System.out.println("testVoid方法执行了");

        //编写请求转发的程序
        request.getRequestDispatcher("/WEB-INF/pages/success.jsp").forward(request,response);
        //重定向
        response.sendRedirect(request.getContextPath()+"/index.jsp");
        //设置中文乱码
        response.setCharacterEncoding("UTF-8");
        response.setContentType("text/html；charset=UTF-8");
        //直接会进行响应
        response.getWriter().print("hello");
        return;
    }
```

2.使用ModelAndView，第一个方法其实底层就是用的ModelAndView
```java
@RequestMapping("/testString")
    public String testString(Model model){
        System.out.println("testString方法执行了");
        User user = new User();
        user.setAge(22);
        user.setName("阿三");
        model.addAttribute("user", user);
        return "success";
    }
    @RequestMapping("/testModelAndView")
    public ModelAndView testModelAndView(){
        //创建ModelAndView对象
        ModelAndView mv = new ModelAndView();
        System.out.println("testString方法执行了");
        //模拟从数据库中查询出User对象
        User user = new User();
        user.setAge(22);
        user.setName("阿三");

        //把user对象存储到mv对象中，也会把user对象存入到request对象
        mv.addObject("user", user);

        //跳转到哪个页面（基于视图解析器）
        mv.setViewName("success");
        return mv;
    }

```

3.使用关键字的方式进行转发或者重定向
```java
 public String testForwardOrRedirect() {
        System.out.println("testForwardOrRedirect方法执行了");
        //请求的转发
//        return "forward:/WEB-INF/pages/success.jsp";
        //重定向
        return "redirect:/index.jsp";
    }
```

4.ResponseBody响应json数据

DispatcherServlet会拦截到所有的资源，导致一个问题就是静态资源（img、css、js）也会被拦截到，从而不能被使用。解决问题就是需要配置静态资源不进行拦截，在springmvc.xml配置文件添加如下配置

1. mvc:resources标签配置不过滤
    * location元素表示webapp目录下的包下的所有文件
    * mapping元素表示以/static开头的所有请求路径，如/static/a或者/static/a/b

```xml
<!--设置静态资源不过滤-->
<mvc:resources location="/css/" mapping="/css/**"/><!--样式-->
<mvc:resources location="/images/" mapping="/images/**"/><!--图片-->
<mvc:resources location="/js/" mapping="/js/**"/><!--javascript-->
 ```