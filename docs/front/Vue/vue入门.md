# vue

vue（读音/vju/，类似于view）是一套用于构建用户界面的**渐进式框架**，发布于2014年2月,与其它大型框架不同的是，Vue被设计为可以自底向上逐层应用。**vue的核心库只关注视图层（HTMl+CSS+JS）**，不仅易于上手，还便于与第三方库（如：wue-router：跳转，wue-re sour ce：通信，vuex：管理）或既有项目整合

官网：https://cn.vuejs.org/v2/guide

网络通信：axios

页面跳转：vue-router

状态管理：vuex

Vue-UI：ICE

## 前言

### js框架

- jQuery：大家熟知的 JavaScript框架，优点是简化了DoM操作，缺点是DoM操作太频繁影响前端性能；在前端眼里使用它仅仅是为了兼容IE6、7、8

- **Angular**：Google收购的前端框架，由一群Java程序员开发，其特点是**将后台的MVC模式搬到了前端**并增加了**模块化开发**的理念，与微软合作，采用 Type Script语法开发；对后台程序员友好，对前端程序员不太友好；最大的缺点是版本迭代不合理（如：1代->2代，除了名字，基本就两个东西；截止2020年已推出了 Angular6）

- **React：**Facebook出品，一款高性能的JS前端框架；特点是提岀了新概念**【虚拟DOM】**用于减少真实DoM操作，在內存中横拟DoM操作，有效的提升了前端渲染效率；缺点是使用复杂，因为需要额外学习一门**【JSX】**语言

- **vue**：一款漸进式 Java Script框架，所谓渐进式就是逐步实现新特性的意思，如实现模块化开发、路由、状态管理等新特性。其特点是综合了 Angular（模块化）和 React（虚拟DOM）的优点

  vue、react、angular为前端三大框架

- Axios：前端通信框架；因为`vue`的边界很明确，就是为了处理DOM，所以并不具备通信能力，此时就需要额外使用一个通信框架与服务器交互；当然也可以直接选择使用 jQuery提供的AJAX通信功能(jQuery占内存大)

### js构建工具

- Babel:Js编译工具，主要用于浏览器不支持的ES新特性，比如用于编译 TypeScript 

- WebPack：模块打包器，主要作用是打包、压缩、合并及按序加载（一般用）

### UI框架

- Ant-Design：阿里巴巴出品，基于 React的UI框架
- ElementAl、Iview、ice：饿了么出品，基于Vue的Ul框架
- Bootstrap：Twitter推出的一个用于前端开发的开源工具包
- AmazeUI：又叫"妹子UI"，一款HTML5跨屏前端框架

### 三端统一

1、混合开发

主要目的是实现一套代码三端统一（PC、Android:apk、ios:ipa）并能够调用到设备底层硬件（如：传感器、GPS、摄像头等），打包方式主要有以下两种

- 云打包：HBuild-> HBuildx，DCloud出品；API Cloud
- 本地打包：Cordova（前身是 PhoneGap）

2、微信小程序

详见微信官网，这里就是介绍一个方便微信小程序U开发的框架：WeUI

### 后端技术

前端人员为了方便开发也需要掌握一定的后端技术，但我们Java后台人员知道后台知识体系极其庞大复杂，所以为了方便前端人员开发后台应用，就出现了 **NodeJS**这样的技术。

NodeJS的作者已经声称放弃 Nodes（说是架构做的不好再加上笨重的 node_modules，可能让作者不爽了吧），开始开发全新架构的Deno

既然是后台技术，那肯定也需要框架和项目管理工具，NodeJS框架及项目管理工具如下

- Express：Nodes框架

- Koa：Express简化版

- NPM：项目综合管理工具，类似于 Maven 

- YARN:NPM的替代方案，类似于 Maven和 Gradle的关系

### Vue实现

主要用的以下几种，其实还有很多，这里就不介绍了

#### iview

IvIew是一个强大的基于vue的UI库，有很多实用的基础组件比 element ui的组件更丰富，主要服务于PC界面的中后台产品。使用单文件的vue组件化开发模式基于npm+ webpack+ babel开发，支持ES2015高质量、功能丰富友好的API，自由灵活地使用空间。

- [官网地址](http://v1.iviewui.com/)
- [github地址](https://github.com/iview/iview)
- [iview-admin](http://admin.iviewui.com/)

**备注：属于前端主流框架，选型时可考虑使用，主要特点是移动端支持较多**

#### ElementUI

Element是饿了么前端开源维护的VueUI组件库，组件齐全，基本涵盖后台所需的所有组件，文档讲解详细，例子也很丰富。主要用于开发PC端的页面，是一个质量比较高的VueUI组件库。

- [官网地址](https://element.eleme.cn/#/zh-CN)
- [github地址](https://github.com/ElementUI/element-starter)
- [vue-element-admin](https://panjiachen.github.io/vue-element-admin-site/zh/)

**备注：属于前端主流框架，选型时可考虑使用，主要特点是桌面端支持较多**

#### ICE

飞冰是阿里巴巴团队基于 React/Angular/vue的中后台应用解决方案，在阿里巴巴内部，已经有270多个来自几乎所有BU的项目在使用。飞冰包含了一条从设计端到开发端的完整链路，帮助用户快速搭建属于自己的中后台应用。

- [官网地址](https://ice.work/)
- [Github](https://github.com/alibaba/ice)

**备注：主要组件还是以 React为主，对vue的支持还不太完善，目前尚处于观望阶段**



## 前后端分离历史

### 1、以后端为主的MVC时代

为了降低开发的复杂度，以后端为出发点，比如：Struts、SpringMVC等框架的使用，就是后端的MVC时代

以`SpringMVC`流程为例：

![image-20200526134544443](H:\Desktop\新建文件夹\Blog\docs\front\pictures\image-20200526134544443.png)

1、发起请求到前端控制器（`DispatcherServlet`）

2、前端控制器请求 `HandlerMapping`查找 `Handler`，可以根据xml配置、注解进行查找

3、处理器映射器 `HandlerMapping`向前端控制器返回 `Handler`

4、前端控制器调用处理器适配器去执行 `Handler`

5、处理器适配器去执行`Handler Handler`

6、执行完成给适配器返回 `ModelAndView`

7、处理器适配器向前端控制器返回 `ModelAndview`，ModelAndView是 SpringMVC框架的一个底层对象，包括Mdel和View

8、前端控制器请求视图解析器去进行视图解析，根据**逻辑视图名解析**成真正的视图（`JSP`）

9、视图解析器向前端控制器返回`View`

10、前端控制器进行视图渲染，视图渲染将模型数据（在 `ModelAndView`对象中）填充到 **request域**

11、前端控制器向用户响应结果

**优点：**

​	MVC是一个非常好的协作模式，能够有效降低代码的耦合度，从架构上能够让开发者明臼代码应该写在哪里。为了让View更纯粹，还可以使用 Thymeleaf、Freemarker等模板引擎，使模板里无法写入Java代码，让前后端分工更加清晰。

**缺点：**

- 前端开发重度依赖开发环境，开发效率低，这种架构下，**前后端协作**有两种模式
  - 第一种是前端写DEMO，写好后，让后端去套模板。好处是DEMO可以本地开发，很高效不足是还需要后端套模板，有可能套错，套完后还需要前端确定，**来回沟通**调整的成本比较大
  - 另一种协作模式是前端负责浏览器端的所有开发和服务器端的view层模板开发。好处是UI相关的代码都是前端去写就好，后端不用太关注，不足就是**前端开发重度绑定后端环境**，环境成为影晌前端开发效率的重要因素。
  - **前后端职责纠缠不清：**模板引擎功能强大，依旧可以通过拿到的上下文变量来实现各种业务逻辑。这样，只要前端弱势一点，往往就会被后端要求在模板层写出不少业务代码。还有一个很大的灰色地带是 `Controller`，页面路由等功能本应该是前端最关注的，但却是由后端来实现`Controller`本身与 `Model`往往也会纠缠不清，看了让人咬牙的业务代码经常会出现在`Controller`层。这些问题不能全归结于程序员的素养，否则JSP就够了。
- 对前端发挥的局限性：性能优化如果只在前端做空间非常有限，于是我们经常需要后端合作，但由于后端框架限制，我们很难使用【Comet】、【Big Pipe】等技术方案来优化性能。



### 2、基于AJax的SPA（web2.0）

时间回到2005年AJAX（Asynchronous Java Script And XML，异步 Java Script和xML老技术新用法）被正式提出并开始使用DN作为静态资源存储，于是出现了 Java Script王者归来（在这之前JS都是用来在网页上贴狗皮膏药广告的）的SPA（Single Page Application）单页面应用时代。

![image-20200526140614501](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526140614501.png)

**优点**

这种模式下，**前后端的分工非常清晰，前后端的关键协作点是AJAX接口**。看起来是如此美妙，但回过头来看看的话，这与JSP时代区别不大。复杂度从服务端的JSP里移到了浏览器的 JavaScript，浏览器端变得很复杂。类似 Spring MVC，**这个时代开始出现浏览器端的分层架构:**

![image-20200526140754557](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526140754557.png)

**缺点**

- **前后端接口的约定：**如果后端的接口一塌糊涂，如果后端的业务模型不够稳定，那么前端开发会很痛苦：不少团队也有类似尝试，通过接口规则、接口平台等方式来做。**有了和后端一起沉淀的接口规则，还可以用来模拟数据，使得前后端可以在约定接口后实现高效并行开发**
- **前端开发的复杂度控制：**SPA应用大多以功能交互型为主，JavaScript代码过十万行很正常量JS代码的组织，与View层的绑定等，都不是容易的事情。

### 3、以前端为主的MV*时代

此处的MV*模式如下

- MVC（同步通信为主）：Model、View、Controller 
- MVP（异步通信为主）：Model、View、Presenter 
- MVVM（异步通信为主）：Model、view、View Model



​	为了降低前端开发复杂度，涌现了大量的前端框架，比如；：`Angular]S`、`React`、`vue.js`,`EmberJs`等，这些框架总的原则是先按类型分层，比如 Templates、Controllers、Models，然后再在层内做切分，如下图

![image-20200526141218610](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526141218610.png)

**优点**

- **前后端职责很清晰：**前端工作在浏览器端，后端工作在服务端。清晰的分工，可以让开发并行，测试数据的模拟不难，前端可以本地开发。**后端则可以专注于业务逻辑的处理，输出 RESTful等接口**
- **前端开发的复杂度可控**：前端代码很重，但合理的分层，让前端代码能各司其职。这一块蛮有意思的，简单如模板特性的选择，就有很多很多讲究。并非越强大越好，限制什么，留下哪些自由，代码应该如何组织，所有这一切设计，得花一本书的厚度去说明
- **部署相对独立：**可以快速改进产品体验

**缺点**

- 代码不能复用。比如后端依旧需要对数据做各种校验，校验逻辑无法复用浏览器端的代码。如果可以复用，那么后端的数据校验可以相对简单化。
- 全异步，对SEO不利。往往还需要服务端做同步渲染的降級方案
- 性能并非最佳，特别是移动互联网环境下
- SPA不能满足所有需求，依旧存在大量多页面应用。URL Design需要后端配合，前端无法完全掌控。

### 4、NodeJS带来的全栈模式

​	前端为主的MV*模式解决了很多很多问题，但如上所述，依旧存在不少不足之处。随着NodeJS的兴起，JavaScript开始有能力运行在服务端。意味着可以有一种新的研发模式

![image-20200526141949033](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526141949033.png)

在这种硏发模式下，前后端的职责很清晰。对前端来说，两个UI层各司其职：

- Front-end UI layer处理浏览器层的展现逻辑。通过css渲染样式，通过 Java Script添加交互力能，HTML的生成也可以放在这层，具体看应用场景。
- Back-end Ul layer处理路由、模板、数据获取、Cookie等。通过路由，前端终于可以自主把控URL Design，这样无论是单页面应用还是多页面应用，前端都可以自由调控。后端也终于可以摆脱对展现的强关注，转而可以专心于业务逻辑层的开发

通过Node，Web Server层也是 JavaScript代码，这意味着部分代码可前后复用，需要SEO的场景可以在服努端同步渲染，由于异步请求太多导致的性能问题也可以通过服务端来缰解。前一种模式的不足，通过这种模式几乎都能完美解决掉。
与JSP模式相比，全栈模式看起来是一种回归，也的确是一种向原始开发模式的回归，不过是一种螺旋上升式的回归。
基于 Nodes的全栈模式，依旧面临很多挑战：

- 需要前端对服务端编程有更进一步的认识。比如TCP/IP等网络知识的掌握。
- NodeJs层与Java层的高效通信。NodeJS模式下，都在服务器端，Restful Http通信未必高效，通过SOAP等方式通信更高效。一切需要在验证中前行
- 对部署、运维层面的熟练了解，需要更多知识点和实操经验
- 大量历史遗留问题如何过渡。这可能是最大最大的阻力



## 为什么使用Vue.js

- 轻量级，体积小是一个重要指标。Vue.js压缩后有只有20多kb（Angular压缩后56kb+
  React压缩后44kb+）
- 移动优先。更适合移动端，比如移动端的 Touch事件
- 易上手，学习曲线平稳，文档齐全
- 吸收了 Angular（模块化）和 React（虚拟DOM）的长处，并拥有自己独特的功能，如：计算属性
- 开源，社区活跃度高

## 入门案例

【说明】IDEA可以安装vue的插件！

Plugin -> vue.js

注意：Vue不支持IE8及以下版本，因为vue使用了lE8无法模拟的 ECMAScript5特性。但它支持所有兼容 ECMAScript5的浏览器

### 下载地址

- 开发版本  [官网提供的github地址](https://github.com/vuejs/vue)

- CDN

  - `<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.js"></script>`
  - `<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>`

### 第一个Vue程序

```html
<body>
<!--view层，模版-->
<div id="app">
	<div>{{message}}</div>
    <h1>{{helloVue()}}</h1>
</div>

<!--    1、导入vue-->
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>
    // 绑定
    var vm = new Vue({
        el: "#app",
        // Model：数据
        data: {
            message: "hello vue"
        }
        methods: {
            helloVue: function () {
                return "你好 vue"
            }
        }
    });
</script>

</body>
```



**不刷新页面，通过修改vm就可以修改视图层**，如果是以前的MVC模式，需要对内容标签各种拼接修改，非常麻烦

![image-20200526153825219](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526153825219.png)

### MVVM

MvvM（Model.-view-View Mode）是一种软件架构设计模式，由微软WPF（用于替代in Form，以前就是用这个技术开发桌面应用程序的）和 Silverlight（类似于 Java Applet，简单点说就是在浏览器上运行的WPF）的架构师 Ken Cooper和 Ted Peters开发，是一种简化用户界面的**事件驱动编程方式**。由 John gossman（同样也是WPF和 Silverlight的架构师）于2005年在他的博客上发表

MVVM源白于经典的MVC（Model-View-Controller）模式。MVVM的核心是 View Model层，负责转换Mode中的数据对象来让数据变得更容易管理和使用，其作用如下

- 该层向上与视图层进行双向数据绑定
- 向下与Mode层通过接口请求进行数据交互

![image-20200526154049938](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526154049938.png)

MVVM已经相当成熟了，主要运用但不仅仅在网络应用程序开发中。当下流行的MVVM框架有vue.js，AngularJS等。

#### 为什么要用MVVM

MVVM模式和MVC模式一样，主要目的是分离视图（View）和模型（Model），有几大好处

- 低耦合：视图（view）可以独立于Mode变化和修改，一个 View Model可以绑定到不同的View上，当View变化的时候Mode可以不变，当 Model变化的时候vew也可以不变。
- 可复用：你可以把一些视图逻辑放在一个 View Model里面，让很多Vew重用这段视图逻辑。·独立开发：开发人员可以专注于业务逻辑和数据的开发（View Model），设计人员可以专注于页面设计。
- 可测试：界面素来是比较难于测试的，而现在测试可以针对 View Model来写

### MVVM组成部分

![image-20200526155831760](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526155831760.png)

#### View

view是视图层，也就是用户界面。前端主要由`HTML`和`Css`来构建，为了更方便地展现`ViewModel`或者 `Model`层的数据，已经产生了各种各样的前后端模板语言，比如 FreeMarker Thymeleaf等等，各大MWM框架如 Vue js，AngularIS，EJS等也都有自己用来构建用户界面的内置模板语

#### Model

Model是指数据模型，泛指后端进行的各种业务逻辑处理和欻据操控，主要围绕数据库系统展开。这里的难点主要在于需要和前端约定统一的接口规则

#### ViewModel

View Model是由前端开发人员组织生成和维护的视图数据层。在这一层，前端开发者对从后端获取的Mode数据进行转换处理，做二次封装，以生成符合iew层使用预期的视图数据模型。

需要注意的是 View<odel所封装出来的数据模型包括视图的状态和行为两部分，而Model数据模型是只包含状态的

- 比如页面的这一块展示什么，那一块展示什么这些都属于视图状态（展示）
- 页面加载进来时发生什么，点击这一块发生什么，这一块滚动时发生什么这些都属于视图行为（交互）



​	视图状态和行为都封装在了 ViewMode里。这样的封装使得 Viewl。del可以完整地去描述View层。由于实现了双向绑定，View Mode的内容会实时展现在view层，这是激动人心的，因为前端开发者再也不必低效又麻烦地通过操纵DOM去更新视图。

MVVM框架已经把最脏最累的一块做好了，我们开发者只需要处理和维护 ViewMode，更新数据视图就会自动得到相应更新，**真正实现事件驱动编程**

​	View层展现的不是 `Model`层的数据，而是 `ViewModel`的数据，由` ViewMode`负责与 `Model`层交互，这就**完全解耦了view层和Model层，这个解耦是至关重要的，它是前后端分离方案实施的重要一环。**



## Vue：MVVM模式的实现者

- Model：模型层，在这里表示 JavaScript对象

- View：视图层，在这里表示DOM（HTML操作的元素）

- View Model：连接视图和数据的中间件，Vue.js就是MVM中的 View Mode层的实现者

  在MVVM架构中，是不允许数据和视图直接通信的，只能通过 View Model来通信，而View Model就是定义了一个 Observer观察者

- View Model能够观察到数据的变化，并对视图对应的内容进行更新

- View Model能够监听到视图的变化，并能够通知数据发生改变

至此，我们就明白了，Vue.js就是一个MVVM的实现者，他的核心就是实现了DOM监听与数据绑定

## vue常用7个属性

- el属性
- 用来指示vue编译器从什么地方开始解析 vue的语法，可以说是一个占位符。
- data属性
- 用来组织从view中抽象出来的属性，可以说将视图的数据抽象出来存放在data中。
- template属性
  - 用来设置模板，会替换页面元素，包括占位符。
- methods属性
  - 放置页面中的业务逻辑，js方法一般都放置在methods中
- render属性
  - 创建真正的Virtual Dom
- computed属性
  - 用来计算
- watch属性
  - watch:function(new,old){}
  - 监听data中数据的变化
  - 两个参数，一个返回新值，一个返回旧值，



本篇不可能完全介绍完所有方法，需要详细的用法可以参考

https://www.runoob.com/vue2/vue-template-syntax.html



**vue的开发都是要基于 NodeJs，实际开发采用vue-ci脚手架开发，vue-router路由，vuex做状态管理；vueUI，界面我们一般使用 ElementAl（饿了么出品），或者ICE（阿里巴巴出品！）来快速搭建前端项目**

## vue生命周期

vue实例有一个完整的生命周期，也就是从开始创建、初始化数据、编译模板、挂载DOM、渲染→更新→渲染、卸载等一系列过程，我们称这是Vue的生命周期。通俗说就是vue实例从创建到销毁过程，就是生命周期。

在vue的整个生命周期中，它提供了一系列的事件，可以让我们在事件触发时注册Js方法，可以让我们用自己注册的JS方法控制整个大局，在这些事件响应方法中的this直接指向的是vue的实例。

![](https://gitee.com/zero049/MyNoteImages/raw/master/lifecycle.png)

## v-bind

我们已经成功创建了第一个Vue应用！看起来这跟渲染一个字符串模板非常类似，但是vue在背后做了大量工作。现在数据和DoM已经被建立了关联，所有东西都是响应式的。我们在控制台操作对象属性，界面可以实时更新！

我们还可以使用`v-bind`来绑定元素特性！

```html
<h1>
    Vue学习
</h1>
<div id="app">
    <span v-bind:title = "message">
        鼠标悬停几秒查看此处的动态绑定提示信息
    </span>
</div>

<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>
    // 绑定
    var vm = new Vue({
        el: "#app",
        // Model：数据
        data:{
            message: "hello vue"
        }
    });
</script>
</body>
```

![image-20200526164725920](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526164725920.png)

你看到的v-bind等被称为指令。指令带有前缀ⅴ-，以表示它们是vue提供的特殊特性。可能你已经猜到了，它们会在渲染的DOM上应用特殊的响应式行为。在这里，该指令的意思是：“将这个元素节点的tite特性和vue实例的 message属性保持一致”。

如果你再次打开浏览器的 Java Script控制台，输入app.message='新消息'，就会再一次看到这个绑定了tite特性的HTML已经进行了更新







## 判断循环

### v-if、v-else

条件判断实例1

```html
<body>
<div id="app">
<h1 v-if="ok">OK</h1>
<h1 v-else>NOT OK</h1>
</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>
    // 绑定
    var vm = new Vue({
        el: "#app",
        // Model：数据
        data:{
            ok: false
        }
    });
</script>
</body>
```

条件判断实例2

```html
<body>
<div id="app">
<h1 v-if="type==='A'">A</h1>
<h1 v-else-if="type==='B'">B</h1>
    <h1 v-else>C</h1>
</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>
    // 绑定
    var vm = new Vue({
        el: "#app",
        // Model：数据
        data:{
            type: 'A'
        }
    });
</script>
</body>
```



### v-for

遍历实例

```html
<body>
<div id="app">
    <ul>
        <!--注意for 里面in的写法-->
        <li v-for="item in items">
            {{item.message}}
        </li>
    </ul>
</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>
    // 绑定
    var vm = new Vue({
        el: "#app",
        // Model：数据
        data:{
            // 1个数组中有2个对象
            items: [
                {message: "vivo"},
                {message: "oppo"}
            ]
        }
    });
</script>
</body>
```

Items是数组，item是数组元素迭代的别名。我们之后学习的 Thymeleaf模板引擎的语法和这个十分的相似！

自己可以通过控制台再加

![](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526172727860.png)



## 绑定事件v-on

事件有vue的事件、和前端页面本身的一些事件！我们这里的 click是vue的事件，可以绑定到Vue中的 methods中的方法事件！

通过v-on可以绑定事件如click、blur等

```java
<body>
<div id="app">
    <button v-on:click="sayHi">clickMe</button>
</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>
    // 绑定
    var vm = new Vue({
        el: "#app",
        // Model：数据
        data:{
            message: "Just a test"
        },
        methods: {
            sayHi: function () {
                alert(this.message)
            }
        }
    });
</script>
</body>
```



## 过滤器

Vue.js 允许你自定义过滤器，被用作一些常见的文本格式化。由"管道符"指示, 格式如下：

```html
<!-- 在两个大括号中 -->
{{ message | capitalize }}

<!-- 在 v-bind 指令中 -->
<div v-bind:id="rawId | formatId"></div>
```

过滤器函数接受表达式的值作为第一个参数。

以下实例对输入的字符串第一个字母转为大写：

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Vue 测试实例 - 菜鸟教程(runoob.com)</title>
<script src="https://cdn.staticfile.org/vue/2.2.2/vue.min.js"></script>
</head>
<body>
<div id="app">
  {{ message | capitalize }}
</div>
	
<script>
new Vue({
  el: '#app',
  data: {
	message: 'runoob'
  },
  filters: {
    capitalize: function (value) {
      if (!value) return ''
      value = value.toString()
      return value.charAt(0).toUpperCase() + value.slice(1)
    }
  }
})
</script>
</body>
</html>
```

过滤器可以串联：

```
{{ message | filterA | filterB }}
```

## 

## 缩写

### v-bind 缩写

Vue.js 为两个最为常用的指令提供了特别的缩写：

```
<!-- 完整语法 -->
<a v-bind:href="url"></a>
<!-- 缩写 -->
<a :href="url"></a>
```

### v-on 缩写

```
<!-- 完整语法 -->
<a v-on:click="doSomething"></a>
<!-- 缩写 -->
<a @click="doSomething"></a>
```



## v-model双向绑定

Vue.js是一个MVVM框架，即数据双向绑定，即当数据发生变化的时候，视图也就发生变化视图发生变化的时候，数据也会跟着同步变化。这也算是 Vue.js的精髓之处了

值得注意的是，我们所说的数据双向绑定，一定是对于UI控件来说的，非UI控件不会涉及到数据双向绑定。单向数据绑定是使用状态管理工具的前提。如果我们使用vuex，那么数据流也是单项的，这时就会和双向数据绑定有冲突

### 在表单中使用双向数据绑定

你可以用v-model指令在表单`<input>`、`< textarea>`及`< select>`元素上创建双向数据绑定。它会根据控件类型自动选取正确的方法来更新元素尽管有些神奇，但 v-mode本质上不过是语法糖。它负责监听用户的输入事件以更新数据，并对一些极端场景进行一些特殊处理。

**注意：v-model会忽略所有表单元素的 value、checked、selected特性的初始值而总是将vue实例的数据作为数据来源。你应该通过 JavaScript在组件的data选项中声明初始值**



**绑定input**

input跟message绑定，div也跟message绑定

```html
<body>
<div id="app">
    <div>输入<input v-model="message" type="text"></div>
    <div>你输入的是{{message}}</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>
    var vm = new Vue({
        el: "#app",
        data: {
            message: ""
        }
    })
</script>
</body>
```

![image-20200526183738808](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526183738808.png)

textarea也是一样的



**绑定checkbox和class：**

```html
<!DOCTYPE html>
<html lang="en" xmlns:v-bind="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        .class1{
            background: black;
            color: #f9fbff;
            font-size: 20px;
        }
    </style>
</head>
<body>
<div id="app">
    <div>切换颜色？<input v-model="use" type="checkbox"></div>
    <div v-bind:class="{'class1': use}">哈哈哈哈哈</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>
    var vm = new Vue({
        el: "#app",
        data: {
            use: false
        }
    })
</script>
</body>
</html>
```

![image-20200526183721438](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526183721438.png)

**绑定单选框的value**

```html
<body>
<div id="app">

    男<input value="男" name="sex" type="radio" v-model="sex">
    女<input value="女" name="sex" type="radio"v-model="sex">
    <div>选中的是 {{sex}}</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>
    var vm = new Vue({
        el: "#app",
        data: {
            sex: ""
        }
    })
</script>
</body>
```

![image-20200526183700913](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526183700913.png)

**下拉框绑定**

```html
<body>
<div id="app">

    <select v-model="selectX">
        <option value="" disabled>--请选择--</option>
        <option>A</option>
        <option>B</option>
        <option>C</option>
    </select>
    <div>选中的是 {{selectX}}</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>
    var vm = new Vue({
        el: "#app",
        data: {
            selectX: ""
        }
    })
</script>
</body>
```

![image-20200526184035433](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526184035433.png)

注意：如果v-model表达式的初始值未能匹配任何选项，< select>元素将被渲染为“未选中”状态。在IOS中，这会使用户无法选择第一个选项。因为这样的情况下，iOS不会触发 change事件。因此，更推荐像上面这样提供一个值为空的禁用选项。



## 组件

组件是可复用的Vue实例，说白了就是一组可以重复使用的模板，跟`JSTL`的自定义标签，`Thymeleaf`的`th：fragment`等框架有着异曲同工之妙。通常一个应用会以一棵嵌套的组件树的形式来组织

![image-20200526190041626](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526190041626.png)

例如，你可能会有页头、侧边栏、内容区等组件，每个组件又包含了其它的像导航链接、博文之类为了能在模板中使用，这些组件必须先注册以便Wue能够识别。

这里有两种组件的注册类型：**全局注册和局部注册**。至此，我们的组件都只是运过`Vue.component`全局注册的：

```html
<body>
<div id="app">
    <!--定义的标签-->
    <zhangsan></zhangsan>
</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>
    //定义一个Vue.component
    Vue.component("zhangsan",{
        template: '<li>啧啧啧啧啧啧</li>'
    });

    var vm = new Vue({
        el: "#app"
    })
</script>
</body>
```

说明

- **Vue.component()**：注册组件
- my-component-li：自定义组件的名字
- template：组件的模板



### 传递参数

像上面那样用组件没有任何意义，所以我们是需要传递参数到组件的，此时就需要使用props属性了！

注意：默认规则下 props属性里的值不能为大写

```html
<body>
<div id="app">
    <!--组件，注意标签名,v-bind:xxx中xxx可以随便写，绑定名-->
    <zhangsan v-for="item in items" v-bind:xxx="item"></zhangsan>
</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>
    //定义一个Vue.component
    Vue.component("zhangsan",{
        //接收参数，不可以直接访问item
        props: ['xxx'],
        // 模版
        template: '<li>{{xxx}}</li>'
    });
	//实例化vue
    var vm = new Vue({
        el: "#app",
        data: {
            items: ["Java","Linux","Vue"]
        }
    })
</script>
</body>
```

- v-for="item in items"遍历Vue实例中定义的名为 items的数组，并创建同等数量的组件
- v-bind:xxx="item"：将遍历的item项绑定到组件中 props定义的名为xxx属性上；=号左边的xxx为 props定义的属性名，右边的为 item in items中遍历的item项的值



## Axios网络通信

Axios是一个开源的可以用在浏览器端和 `NodeJS`的异步通信框架，她的主要作用就是实现AJAX异步通信，其功能特点如下

- 从浏览器中创建 XmlHttpRequests
- 从node.js创建http请求
- 支持 Promise apl[Js中链式编程]
- 拦截请求和晌应
- 转换请求数据和响应数据
- 取消请求
- 自动转换JSON数据
- 客户端支持防御XSRF（跨站请求伪造）

Github:https://github.com/axios/axios

中文文档：http://www.axios-js.com/

- cdn

```html
<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
```

```html
<script src="https://cdn.staticfile.org/axios/0.18.0/axios.min.js"></script>
```



### 为什么要用Axios

由于`vue.js`是一个视图层框架并且作者（尤雨溪）严格准守SoC（关注度分离原则），所以**`vue.js`并不包含AJAX的通信功能**，为了解决通信问题，作者单独开发了一个名为`vue-resource`的插件，不过在进入2.0版本以后停止了对该插件的维护并推荐了`Axios`框架。**少用 jQuery，因为它操作Dom太频繁**！

### GET方法

链式编程，在Vue对象需要写一个data()函数，返回我们需要的属性，我们可以简单的读取 JSON 数据：

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Vue 测试实例 - 菜鸟教程(runoob.com)</title>
<script src="https://cdn.staticfile.org/vue/2.4.2/vue.min.js"></script>
<script src="https://cdn.staticfile.org/axios/0.18.0/axios.min.js"></script>
</head>
<body>
<div id="app">
  {{ info }}
</div>
<script type = "text/javascript">
new Vue({
  el: '#app',
  data () {	// 注意data()
    return {
      info: null
    }
  },
  mounted () {
      //链式编程
    axios
      .get('data.json')
      .then(response => (this.info = response))
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
  }
})
</script>
</body>
</html>
```

使用 **response.data** 读取 JSON 数据：

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Vue 测试实例 - 菜鸟教程(runoob.com)</title>
<script src="https://cdn.staticfile.org/vue/2.4.2/vue.min.js"></script>
<script src="https://cdn.staticfile.org/axios/0.18.0/axios.min.js"></script>
</head>
<body>
<div id="app">
  <h1>网站列表</h1>
  <div v-for="site in info">
    {{ site.name }} 通过. 的方式去取
  </div>
</div>
<script type = "text/javascript">
new Vue({
  el: '#app',
  data () {
    return {
      info: null
    }
  },
  mounted () {
    axios
      .get('data.json')	//自己提供的data.json
      .then(response => (this.info = response.data.sites))
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
  }
})
</script>
</body>
</html>
```

GET 方法传递参数格式如下：

```js
// 直接在 URL 上添加参数 ID=12345
axios.get('/user?ID=12345')
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
 
// 也可以通过 params 设置参数：
axios.get('/user', {
    params: {
      ID: 12345
    }
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
```

### POST方法

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Vue 测试实例 - 菜鸟教程(runoob.com)</title>
<script src="https://cdn.staticfile.org/vue/2.4.2/vue.min.js"></script>
<script src="https://cdn.staticfile.org/axios/0.18.0/axios.min.js"></script>
</head>
<body>
<div id="app">
  {{ info }}
</div>
<script type = "text/javascript">
new Vue({
  el: '#app',
  data () {
    return {
      info: null
    }
  },
  mounted () {
    axios
      .post('https://www.runoob.com/try/ajax/demo_axios_post.php')
      .then(response => (this.info = response))
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
  }
})
</script>
</body>
</html>
```

POST 方法传递参数格式如下：

```js
axios.post('/user', {
    firstName: 'Fred',        // 参数 firstName
    lastName: 'Flintstone'    // 参数 lastName
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
```

### 执行多个并发请求

```js
function getUserAccount() {
  return axios.get('/user/12345');
}
 
function getUserPermissions() {
  return axios.get('/user/12345/permissions');
}
axios.all([getUserAccount(), getUserPermissions()])
  .then(axios.spread(function (acct, perms) {
    // 两个请求现在都执行完成
  }));
```



## 计算属性

计算属性的重点突出在**属性**两个字上（属性是名词），首先它是个属性，其次这个属性有计算的能力（计算是动词），这里的计算就是个函数；简单点说，它就是一个**能够将计算结果缓存起来的属性**（将行为转化成了静态的属性），仅此而已；可以想象为缓存。

利用computed属性

```html
<body>

<div id="app">
    <div>
        currentTime1: {{currentTime1()}}
    </div>
<!--    currentTime2是属性-->
    <div>
        currentTime2: {{currentTime2}}
    </div>

</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>

<script>
    var vm = new Vue({
        el: "#app",
        data: {
            message: "hello,zhangsan"
        },
        methods: {
            currentTime1: function () {
                return Date.now();  //返回当前时间戳
            }
        },
        computed: {//计算属性：methods，computed方法名不能重名,重名之后只调method方法
            currentTime2: function () {
                this.message;	//this.message改变缓存就失效
                return Date.now();  //返回当前时间戳
            }
        }
    })
</script>
</body>
```

![image-20200526211131371](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526211131371.png)

- methods：定义方法，调用方法使用 currenttime1()，需要带括号

- computed：定义计算属性，调用属性使用 currentTime2，不需要带括号；this.message是为了能够让 currenttime2观察到数据变化而变化
- 如何在方法中的值发生了变化，则缓存就会刷新！可以在控制台使用vm，message="qinjiang"，改变下数据的值，再次测试观察效果

**结论**
调用方法时，每次都需要进行计算既然有计算过程则必定产生系机米销，那如果这个结果是不经常变化的呢？此时就可以考虑将这个结果缓存起来，采用计算属性可以很方便的做到这一点，**计算属性的主要特性就是为了将不经常变化的计算结果进行缓存，以节约我们的系统开销**



## slot插槽（TODO）

在Vue.js中我们使用`<s1ot>`元素作为承载分发内容的出口，作者称其为插槽，可以应用在组合组件的场景中，相当于给一个位置占位



比如准备制作一个待办事项组件（todo），该待办标题（todo-title）和待办内容（tod-items）组成，但这三个组件又是相互独立的，该如何操作呢？

代码如下,初看可能会 有些难度，实际上就是在todo定义了两个插槽，将todo-title和todo-item组件插进来就行了

```html
<body>

<div id="app">
    <todo>
        <todo-title slot="todo-title" v-bind:title="todoTitle"></todo-title>
        <todo-item slot="todo-item" v-bind:item="item" v-for="item in todoItems"></todo-item>
    </todo>

</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>

    //todo插槽
    Vue.component("todo",{
        template:   '<div>\
                      <slot name="todo-title"></slot>\
                      <ul>\
                        <slot name="todo-item"></slot>\
                      </ul>\
                      </div>'

    });

    //todo-title插槽
    Vue.component("todo-title",{
        props: ['title'],
        //插到第一个slot
        template:   '<div>{{title}}</div>'

    });

    //todo-item插槽
    Vue.component("todo-item",{
        props: ['item'],
        template:   '<li>{{item}}</li>'

    });

    var vm = new Vue({
        el: "#app",
        data: {
            todoTitle: '学java',
            todoItems: ['学JVM','学中间件','学分布式']
        }
    })
</script>
</body>
```

![image-20200526215504700](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526215504700.png)

## 自定义事件分发

如果组件里面，想要删除vm的数据，本来调用vm的方法就可以了，然而组件只能绑定当前组件的方法，而删不到vm上的节点，因此就需要自定义事件，在组件中通过**this.$emit()**取到自定义的事件

![image-20200526221119768](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526221119768.png)

![image-20200526222825692](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526222825692.png)

```html
<body>

<div id="app">
    <todo>
        <todo-title slot="todo-title" v-bind:title="todoTitle"></todo-title>
        <todo-item slot="todo-item" v-bind:item="item" v-bind:index="index" v-for="(item,index) in todoItems" v-on:remove="removeItems(index)"></todo-item>
        <!--在v-on里自定义一个事件remove，并绑定vm的removeItems方法-->
    </todo>

</div>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.min.js"></script>
<script>

    //todo插槽
    Vue.component("todo",{
        template:   '<div>\
                      <slot name="todo-title"></slot>\
                      <ul>\
                        <slot name="todo-item"></slot>\
                      </ul>\
                      </div>'

    });

    //todo-title插槽
    Vue.component("todo-title",{
        props: ['title'],
        //插到第一个slot
        template:   '<div>{{title}}</div>'

    });

    //todo-item插槽
    Vue.component("todo-item",{
        props: ['item','index'],
        //只能绑定当前组件的方法，而删不到vm上的节点
        template:   '<li>{{item}}&nbsp;<button @click="remove">删除</button></li>',
        methods: {

            remove: function (index) {
                // 把自定义的事件拿来用
                this.$emit('remove',index)
            }
        }
    });

    var vm = new Vue({
        el: "#app",
        data: {
            todoTitle: '学java',
            todoItems: ['学JVM','学中间件','学分布式']
        },
        methods:{
            removeItems:function(index){
                console.log("删除"+this.todoItems[index]+" OK");
                this.todoItems.splice(index,1)  //splice方法既可以删除数组元素，还可以在index追加插入
            }
        }
    })
</script>
</body>
```

![image-20200526222952715](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200526222952715.png)