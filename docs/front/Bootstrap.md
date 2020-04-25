# Bootstrap 



​	一个前端开发的框架，Bootstrap，来自Twitter，是目前很受欢迎的前端框架。Bootstrap是基于HTML、CSS、Javascript的，它简洁灵活，使得Web开发更加快捷。

​	1.定义了很多的css样式和js插件。我们开发人员直接可以使用这些样式和插件得到丰富的页面效果

​	2.响应式布局。(同一套页面可以兼容不同分辨率的设备。)



官网地址[Bootstrap](https://v3.bootcss.com/)

![image-20200421233732830](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200421233719601.png)

下载即可

![image-20200421233719601](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200421233732830.png)

快速入门
1.下载Bootstrap
2.在项目中将这三个文件夹复制
3.创建html页面，引入必要的资源文件



Bootstrap提供的基本模版

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>Bootstrap 101 Template</title>

    <!-- Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 shim 和 Respond.js 是为了让 IE8 支持 HTML5 元素和媒体查询（media queries）功能 -->
    <!-- 警告：通过 file:// 协议（就是直接将 html 页面拖拽到浏览器中）访问页面时 Respond.js 不起作用 -->
    <!--[if lt IE 9]>
      <script src="https://cdn.jsdelivr.net/npm/html5shiv@3.7.3/dist/html5shiv.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/respond.js@1.4.2/dest/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <h1>你好，世界！</h1>

    <!-- jQuery (Bootstrap 的所有 JavaScript 插件都依赖 jQuery，所以必须放在前边) -->
    <script src="https://cdn.jsdelivr.net/npm/jquery@1.12.4/dist/jquery.min.js"></script>
    <!-- 加载 Bootstrap 的所有 JavaScript 插件。你也可以根据需要只加载单个插件。 -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js"></script>
  </body>
</html>
```

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>Bootstrap 101 Template</title>

    <!-- Bootstrap -->
    <link href="../css/bootstrap.min.css" rel="stylesheet">


<!--    jQuery (Bootstrap 的所有 JavaScript 插件都依赖 jQuery，所以必须放在前边)&ndash;&gt;-->
    <script src="../js/jquery-3.5.0.min.js"></script>
<!--     加载 Bootstrap 的所有 JavaScript 插件。你也可以根据需要只加载单个插件。-->
    <script src="../js/bootstrap.min.js"></script>
    <![endif]-->
</head>
<body>
<h1>你好，世界！</h1>


</body>
</html>
```



## 响应式布局

同一套页面可以兼容不同分辨率的设备。

实现：依赖于栅格系统。将一行平均分成12个格子，可以指定元素占几个格子

![image-20200421235425746](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200421235425746.png)

步骤：

1.定义容器。相当于之前的table、
			*容器分类：
					1.container：两边留白
					2.container-fluid：每一种设备都是100%宽度
2.定义行。相当于之前的tr       样式：row
3.定义元素。指定该元素在不同的设备上，所占的格子数目。   样式：co1-设备代号-格子数目

​			*设备代号：

​				1.xs：超小屏幕手机（<768px）：co1-xs-12
​				2.sm：小屏幕平板（2768px）
​				3.md：中等屏幕桌面显示器（2992px）
​				4.lg：大屏幕大桌面显示器（21200px）

```html
<body>
<!--定义容器-->
    <div class="container-fluid">
<!--        定义行-->
        <div class="row">
<!--            定义元素-->
<!--            在大显示器一行12个格子-->
<!--            在pad上一行6个格子-->
            <div class="col-lg-1 col-sm-2 inner">栅格</div>
            <div class="col-lg-1 col-sm-2 inner">栅格</div>
            <div class="col-lg-1 col-sm-2 inner">栅格</div>
            <div class="col-lg-1 col-sm-2 inner">栅格</div>
            <div class="col-lg-1 col-sm-2 inner">栅格</div>
            <div class="col-lg-1 col-sm-2 inner">栅格</div>
            <div class="col-lg-1 col-sm-2 inner">栅格</div>
            <div class="col-lg-1 col-sm-2 inner">栅格</div>
            <div class="col-lg-1 col-sm-2 inner">栅格</div>
            <div class="col-lg-1 col-sm-2 inner">栅格</div>
            <div class="col-lg-1 col-sm-2 inner">栅格</div>
            <div class="col-lg-1 col-sm-2 inner">栅格</div>

        </div>
    </div>
</body>
```

注意：

1.一行中如果格子数目超过12，则超出部分自动换行。
2.栅格类属性可以向上兼容。棚格类适用于与屏幕宽度大于或等于分界点大小的设备。
3.如果真实设备宽度于了设置栅格类属性的设备代码的最小值，会一个元素占满一整行。

## CSS样式和JS插件

查看文档即可，以下是重点

全局CSS样式：

- 按钮   如默认样式class="btn btn-default"
- 图片
  - class="img-responsive”：图片在任意尺寸都占100%
  - 图片形状
    /<img src="..." alt=".."class="img-rounded">：圆形
    /<img src="..” alt="...”class="img-circle">：方形
    /<img src="..." alt=".…"class="img-thumbnail">：相框
- 表格 
- 表单

组件：

- 导航条
- 分页条

插件：

- 轮播图



