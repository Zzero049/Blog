
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2020-04-12 125913.png">

## DispatcherServlet：前端控制器
用户请求到达前端控制器，它就相当于mvc模式中的c，dispatcherservlet是整个流程控制的中心，由它调用其它组件处理用户的请求，dispatcherServlet的存在降低了组件之间的耦合性。

## HandlerMapping：处理器映射器
HandlerMapping 负责根据用户请求找到Handler即处理器，SpringMVC提供了不同的映射器实现不同的映射方式，例如：配置文件方式，实现接口方式，注解方式等。

## Handler：处理器
它就是我们开发中要编写的具体业务控制器。由DispatcherServlet把用户请求转发到Handler。由Handler对具体的用户请求进行处理。

## HandlAdapter：处理器适配器
通过HandlerAdapter对处理器进行执行，这是适配器模式的应用，通过扩展适配器可以对更多类型的处理器进行执行。



##  View Resolver：视图解析器
View Resolver 负责将处理结果生成View视图，View Resolver 首先根据逻辑视图名解析成物理视图名即具体的页面地址，再生成View视图对象，最后对View进行渲染将处理结果通过页面展示给用户。

## View 视图
SpringMVC 框架提供了很多的View视图类型的支持，包括：jstlView、freemarkerView、pdfView等。我们最常用的视图就是sp。
一般情况下需要通过页面标签或页面模版技术将模型数据通过页面展示给用户，需要由程序员根据业务需求开发具体的页面。

## <<mvc:annotation-driven>>说明
在SpringMVC的各个组件中，处理器映射器、处理器适配器、视图解析器称为SpringMVC的三大组件。
使用<<mvc:annotation-driven>>自动加载 RequestMappinglHandlerMapping（处理映射器）和RequestMappingHandlerAdapter（处理适配器），可用在SpringMVC.xml配置文件中使用
<<mvc:annotation-driven>>替代注解映射器和适配器的配置。


