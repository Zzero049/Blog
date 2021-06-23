

# Vue-cli

vue-cli官方提供的一个脚手架，用于快速生成一个vue的项目模板

预先定义好的目录结构及基础代码，就**类似创建 Maven项目时可以选择创建一个骨架项目**，这个骨架项目就是脚手架，我们的开发更加的快速；

主要功能：

- 统一的目录结构
- 本地调试
- 热部署
- 单元测试
- 集成打包上线

 ## 需要的环境

**1、安装Node.js**

- Nodejs:http://nodejs.cn/download/

  安装就无脑下一步就好，安装在自己的环境目录下

- Git:https://git-scm.com/downloads

- 镜像：https://npm.taobao.org/mirrors/git-for-windows/

**确认 nodes安装成功：**

- cmd下输入node -v，查看是否能够正确打印出版本号即可！

- cmd下输入npm -v，查看是否能够正确打印出版本号即可!

  

这个npm，就是一个软件包管理工具就和inux下的apt软件安装差不多！

**安装 Node.js淘宝镜像加速器（cnpm）**这样子的话，下载会快很多~

cmd

```cmd
 npm install -g cnpm --registry=https://registry.npm.taobao.org
```

等待安装完成即可，以后就可以把npm install 换成cnpm install来完成加速。

安装过程可能有点慢~，耐心等待！虽然安装了cnpm，但是尽量少用(能用，但是打包的时候就出错)

安装的位置：C:\Users\Lin\AppData\Roaming\npm

![image-20200527000537996](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200527000537996.png)

**2、安装vue-cli**

```shell
cnpm install vue-cli -g
# 测试是否安装成功
# 查看可以基于哪些模板创建vue应用程序，通常我们选择 webpack 
vue list
```

安装的位置：C:\Users\Lin\AppData\Roaming\npm\node_modules



## 第一个vue-cli应用程序

1、创建一个vue项目，我们随便建立一个空的文件夹在电脑上我这里在F盘下新建一个目录

`F:\Project\vue`

2、创建一个基于 webpack模板的vue应用程序

```shell
#这里的 myvue是项目名称，可以根据自己的需
vue init webpack myvue
```

会有一个选项的过程

![image-20200527002041098](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200527002041098.png)

安装完之后的工程

![image-20200527002010407](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200527002010407.png)



3、初始化运行

```shell
cd myvue
npm install	# 根据package.json安装依赖
npm run dev
```

![image-20200527002858197](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200527002858197.png)



大致分析一下几个比较常用的文件把，如下图

![image-20200527115745927](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200527115745927.png)

1.build：主要用来配置构建项目以及webpack

2.config：项目开发配置

3.node_modules：npm或者cnpm所下载的依赖包

4.src：你的源代码

5.static：静态文件夹，webpack打包时不会打包这里文件，直接可以通过路径访问

6.index.html：最外层的页面一般title等都设置在这里

7.package.json：存放你要npm依赖包的json数据

## 什么是Webpack（为了模块化打包）

本质上，webpack是一个现代 JavaScript应用程序的**静态模块打包器（module bundler）**。当webpack处理应用程序时，它会递归地构建一个依赖关系图 （dependency graph），其中包含应用程序需要的每个模块，然后将所有这些模块打包成一个或多个 bundle 

Webpack是当下最热门的前端资源模块化管理和打包工具，它可以将许多松散耦合的模块按照依赖和规则打包成符合生产环境部署的前端资源。还可以将按需加载的模块进行代码分离，等到实际需要时再异步加载。通过 loader转换，任何形式的资源都可以当做模块，比如 Commonss、AMD、ES6、CSS、JSON、CoffeeScript、LESS等；

伴随着移动互联网的大潮，当今越来越多的网站已经从网页模式进化到了 **WebApp模式**。它们运行在现代浏览器里，使用HTML5、CSS3、ES6等新的技术来开发丰富的功能，网页已经不仅仅是完成浏览器的基本需求；Web App通常是一个SPA（单页面应用），每一个视图通过异步的方式加载，这导致页面初始化和使用过程中会加载越来越多的JS代码，这给前端的开发流程和资源组织带来了巨大挑战。

前端开发和其他开发工作的主要区别，首先是前端基于多语言、多层次的编码和组织工作，其次前端产品的交付是基于浏览器的，这些资源是通过增量加载的方式运行到浏览器端，如何在开发环境组织好这些碎片化的代码和资源，并且保证他们在浏览器端快速、优雅的加载和更新，就需要一个模块化系统，这个理想中的模块化系统是前端工程师多年来一直探索的难题。



## 模块化的演进(了解)

### script标签

```html
<script src="module1.js"></script>
<script src="module2.js"></script>
<script src="module3.js"></script>
<script src="module4.js"></script>
```

这是最原始的 JavaScript文件加载方式，如果把每一个文件看做是一个模块，那么他们的接口通常是暴露在全局作用域下，也就是定义在 window对象中，不同模块的调用都是一个作用域。

这种原始的加载方式暴露了一些显而易见的弊端

- 全局作用域下容易造成变量冲突
- 文件只能按照< script>的书写顺序进行加载
- 开发人员必须主观解决模块和代码库的依赖关系
- 在大型项目中各种资源难以管理，长期积累的问题导致代码库混乱不堪

### CommonsJS

服务器端的 Nodes遵循 Commons规范，该规范核心思想是允许模块通过 require方法来同步加载所需依赖的其它模块，然后通过 exports或 module.exports来导出需要暴露的接口

```js
require("module");
require("../module.js")
export.doStuff = function(){}; 
module.exports = someValue
```

**优点：**

- 服务器端模块便于重用
- NPM中已经有超过45万个可以使用的模块包
- 简单易用

**缺点**

- 同步的模块加载方式不适合在浏览器环境中，同步意味着阻塞加载，浏览器资源是异步加载的
- 不能非阻塞的并行加载多个模块

**实现**

- 服务端的 NodeJS
- Browserify，浏览器端的 Commons实现，可以使用NPM的模块，但是编译打包后的文件体积较大
- modules-webmake，类似 Browserify，但不如 Browserify灵活
- wreq，Browserify的前身

### AMD

Asynchronous Module Definition规范其实主要一个主要接口 define（id?,dependencies?，factory）；它要在声明模块的时候指定所有的依赖 dependencies，并且还要当做形参传到 factory中，对于依赖的模块提前执行。

```js
define("module",["depl", "dep2"], function(d1, d2){
    return someExportedValue;
});
require(["module","./fileis"], function (module, file){});
```

优点

- 适合在浏览器环境中异步加载模块
- 可以并行加载多个模块

缺点

- 提高了开发成本，代码的阅读和书写比较困难，模块定义方式的语义不畅
- 不符合通用的模块化思维方式，是一种妥协的实现

实现

- RequireJS
- curl

### CMD

Commons module definition规范和AMD很相似，尽量保持简单，并与 Commons和Nodes的 Modules规范保持了很大的兼容性。

```js
define(function (require, exports, module){
    var $= require("jquery"); 
    var Spinning = require("./spinning");
	exports. dosomething =...; 
    module.exports = ...;
});
```

优点

- 依赖就近，延迟执行
- 可以很容易在 Nodes中运行

缺点

- 依赖SPM打包，模块的加载逻辑偏重

实现

- Sea.js
- coolie

### ES6(现在的主流)

EcmaScript6标准增加了 JavaScript语言层面的模块体系定义。ES6模块的设计思想，是尽量静态化，使编译时就能确定模块的依赖关系，以及输入和输岀的变量。CommonsJS和AMD模块，都只能在运行时确定这些东西。

```js
import "jquery";
export function doStuff(){}
module "localModule" {}
```

优点

- 容易进行静态分析
- 面向未来的 EcmaScript标准

缺点

- **原生浏览器端还没有实现该标准（ES5）**
- 全新的命令，新版的 Nodes才支持

实现

- Babel

## 安装Webpack

Webpack是一款模块加载器兼打包工具，它能把各种资源，如JS、JSX、ES6、SASS、LESS、图片等都作为模块来处理和使用。（如把ES6打包兼容ES5）

```shell
npm install webpack -g
npm install webpack-cli -g
```

测试安装成功

```shell
webpack -v
webpack-cli -v
```

![image-20200527005941718](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200527005941718.png)

### 配置

创建 `webpack.config.js`配置文件

- entry：入口文件指定 Web pack用哪个文件作为项目的入口
- output：输出，指定 Web pack把处理完成的文件放置到指定路径
- module：模块，用于处理各种类型的文件
- plugins：插件，如：热更新、代码重用等
- resolve：设置路径指向
- watch：监听，用于设置文件改动后直接打包

直接运行 `webpack`命令打包

### 使用webpack

1、创建项目文件夹F:\Project\vue\mywebpack

2、创建一个名为 modules的目录，用于放置JS模块等资源文件

3、在 modules下创建模块文件，如 hello.js，用于编写Js模块相关代码

```js
// hello.js
// 暴露一个方法
exports.sayHi = function () {
    document.write("<h1>ES6 First Test</h1>");
}
```

4、在 modules下创建一个名为 mains的入口文件，用于打包时设置 entry属性

```js
// main.js
var hello = require("./hello");

hello.sayHi();
```

5、在项目目录下创建 webpack.config.js配置文件，使用 webpack命令打包

```js
// webpack.config.js
module.exports = {
    entry: './modules/main.js',	//程序入口
    output: {
        filename: "./js/bundle.js"
    }
};
```

6、webpack打包之后，生成bundle.js（ES6转换成ES5语法后的js）

7、在项目目录下创建HTML页面，如 index.htm，导入 Web Pack打包后的JS文件

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<script src="dist/js/bundle.js"></script>
</body>
</html>
```

8、运行HTML看效果

![image-20200527012726548](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200527012726548.png)

```shell
#参数 --watch 用于监听变化
webpack --watch
```



