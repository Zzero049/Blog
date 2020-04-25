默认的抛异常
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-04-14 135836.png">

友好的异常处理
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-04-14 140014.png">

1.编写自定文异常类（做提示信息的）--------继承Exceptions
```java
public class SysException {
    //存储错误信息
    private String message;

    public SysException(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}

```
2.编写异常处理器----------------实现HandlerExceptionResolver
```java
public ModelAndView resolveException(HttpServletRequest request,HttpServletResponse response,Object handler,Exception ex){
        //获取到异常对象
        SysException e= null;
        if(ex instanceof SysException) {
            e = (SysException) ex;
        }else {
            e = new SysException("系统正在维护…");
        }
        //创建ModelAndView对象
        ModelAndView mv =new ModelAndView();
        mv.addObject("errorMsg",e.getMessage());
        mv.setViewName("error");
        return mv;
    }
```
3.配置异常处理器（跳转到提示页面）-------xml配置resolver的bean标签
```xml
<！--配置异常处理器-->
<bean id="sysExceptionResolver" class="cn.itcast.exception.SysExceptionResolver"/>
```