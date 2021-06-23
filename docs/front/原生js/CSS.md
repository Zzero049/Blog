# CSS

CSS是“层叠样式表单”。是用于（增强）控制网页样式并允许将样式信息与网页内容分离的一种标记性语言。

### 语法规则

![image-20200420181102263](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200420181102263.png)

**选择器：**浏览器根据“选择器”决定受CSS样式影响的HTML元素（标签）。

**属性（property）**是你要改变的样式名，并且每个属性都有一个值。属性和值被冒号分开，并由花括号包围，这样就组成了一个完整的样式声明（declaration），例如：p{color:blue}

**多个声明：**如果要定义不止一个声明，则需要用分号将每个声明分开。虽然最后一条声明的最后可以不加分号（但尽量在每条声明的末尾都加上分号）

## CSS与HTML结合方式(每个样式用;结尾)

### 行内样式（在html的标签中用style）

在标签的 style 属性上设置"key:value value；"，修改标签样式。

```html
 <div style="border: brown solid 2px ">lalala</div>
```

把css样式写戴一个单独的css文件，再通过limk标签引入即可复用。把css样式写戴一个单独的css文件，再通过limk标签引入即可复用。然而这样会出现问题：

1.如果标签多了。样式多了。代码量非常庞大。

2.可读性非常差。

3.Css代码**没什么复用性**可方言。

### 内部样式（在head标签定义style）

在head标签来定义各种自己需要的css样式。

格式如下：

xxx{

​	Key:value value;

}

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
<!--    style标签专门用来定义css样式代码-->
    <style type="text/css">
        div{
            /*分修改每个div标签的样式为：边框2个像素，实线，棕色。*/            
            border: brown solid 2px
        }
    </style>
</head>
<body>
<div>lalala</div>
</body>
</html>
```

### 外部样式（在另一个css文件定义style，head用link标签导入）

1、 链接式（使用link标签，rel="stylesheet"，href="xxx"）

把css样式写在一个单独的css文件，再通过link标签引入即可复用。

```css
/*1.css*/
div{
  	border: brown solid 2px;
}
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <!--    link标签专门用来引入css样式代码-->
    <link rel="stylesheet" type="text/css" href="css/1.css">

</head>
<body>
<div>lalala</div>
</body>
</html>
```

2、导入式，CSS2.1后特有，使用@import url 有个问题是，一些大型网页会先展示骨架，再进行渲染(因此不常用)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
<!--导入式-->
    <style>
        @import "CSSDemo/H1Demo.css";
    </style>

</head>
<body>
    <h1 >我是标题</h1>
</body>
</html>
```



### 三者优先级

自上而下，行内一定是最下的，因此优先级最高，其次就是看谁再最近了

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>

    <link rel="stylesheet" type="text/css" href="CSSDemo/H1Demo.css">

    <style>
        h1{
            color: green;
        }
    </style>


</head>
<body>
    <h1 style="color: black;">我是标题</h1>
</body>
</html>
```



## 1、基本选择器



### 标签名选择器

跟上面一样，根据div、span等标签定义各自类型的样式即可，但是很不方便,有时候不想匹配所有的标签

```html
<style>
        h1{
            color: green;
        }
    </style>
```



### id选择器

id名必须保证全局唯一！

#id名{
	属性:值
}

```html

<style type="text/css">
    #id001{
         border: brown solid 2px
     }
</style>

<div id="id001">
    lallaa
</div>
```

### class选择器（类选择器）

.class名{
	属性:值
}

```html

<style type="text/css">
    .class01{
        border: brown solid 2px
    }
</style>

<div class="class01">lallaa</div>
```

class类型选择器，可以通过class属性有效的选择性地去使用这个样式。

类选择器后接空格，表明只对包含该顺序下的标签引用时有效

```css
.class a div{
    
}
```

**优先级**

不遵循就近原则

id选择器 >class选择器>标签选择器

### 组合选择器

就是即id和class声明在一起，即可以通过id引用，也可以通过class引用

```html
#id名,.class名{
	属性:值
}
```



## 2、CSS层次选择器

层级选择器是为了定制相关层次的css样式，而不用管理那么多class或id

![image-20200524130343694](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524130343694.png)

```html
<body>
<p>p1</p>
<p>p2</p>
<p>p3</p>
<ul>
    <li>
        <p>p4</p>
    </li>
    <li>
        <p>p5</p>
    </li>
    <li>
        <p>p6</p>
    </li>
</ul>
</body>
```



对于一些层级，不一定要存在，比如基于class写的路径，中间的可以不用定义

1. 后代选择器：满足最后一个元素前的层次的所有后代，全部使用

```html
<style>
    /*后代选择器*/
    body p{
        color: red;
    }
</style>
```

![image-20200524131120455](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524131120455.png)

2. 子选择器，选择直接后代

```html
<style>
    /*子选择器*/
    body>p{
            background: green;
        }
</style>
```



![image-20200524131228956](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524131228956.png)

3. 相邻（向下的一个）兄弟选择器

   ```html
   <p>p1</p>
   <p class="active">p2</p>
   <p>p3</p>
   ```

   ```html
   <style>
       /*相邻兄弟选择器*/
       .active + p{
               background: green;
           }
   </style>
   ```

   ![image-20200524131654875](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524131654875.png)

4. 通用选择器

通用兄弟选择器，当前进中元素的向下的所有兄弟元素

```html
<style>
    /*通用兄弟选择器*/
    .active ~ p{
            background: green;
        }
</style>
```



![image-20200524131904270](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524131904270.png)



## 3、结构伪类选择器

可以通过**冒号再选中一些结构**

如不用class和id选择器，选择ul的第一个子元素

```html
<body>
<p>p1</p>
<p>p2</p>
<p>p3</p>
<ul>
    <li>li1</li>
    <li>li2</li>
    <li>li3</li>
</ul>

</body>
```

```html
	<style>
        /*第一个元素*/
        ul li:first-child{
            background: green;
        }
        /*最后一个元素*/
        ul li:last-child{
            background: red;
        }
    </style>
```

![image-20200524133047424](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524133047424.png)



还有更强大的定位功能，比如通过自己定位到父级的第一个标签，且该标签是p

```html
	<style>
        /*选中p1：定位到父元素，选择当前的第一个元素，根据标签位置
        选择当前元素的父级元素，选中父级元素的第一个,并且是当前元素才生效！*/
        p:nth-child(1){
            background: #0b37ff;
        }
        /*选中父元素，下的p元素的第一个，根据标签类型*/
        p:nth-of-type(1){
            background: #0b37ff;
        }
    </style>
```

![image-20200524134114929](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524134114929.png)

给a标签添加特效

```html
	<style>
        /*鼠标移过去会有背景*/
       a:hover{
            background: aqua;
        }
    </style>
```



![image-20200524134306982](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524134306982.png)





## 4、属性选择器

通过[]，再进行通配选择，既可以使用id也可以使用到class，属性名=属性值，支持正则表达式

= 绝对等于

*= 包括这个元素

^= 以这个元素开头

$= 以这个元素结尾

示例：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>


    <style>
        /*设置a标签通用格式*/
        .demo a{
            float: left;
            display: block; /*点击整个块都可以触发a标签*/
            height: 50px;
            width: 50px;
            border-radius: 10px;
            background: #52ff77;
            color: black;
            text-align: center;
            text-decoration: none;
            margin-right: 5px;
            font: bold 20px/50px Arial;
        }

        a[id=first]{
            background: #0b37ff;
        }

        a[href^="http:"]{
            background: gold;
        }

        a[class*="test"]{
            background: blueviolet;
        }
        a[href$=".java"]{
            background: brown;
        }
    </style>
</head>
<body class="demo">


<a href="https://leetcode-cn.com/" class="item first" id="first">1</a>
<a href="http://msdn.itellyou.cn/" target="_blank" title="test">2</a>
<a href="" class="item test">3</a>
<a href="abc.pdf" class="item test">4</a>
<a href="images/123.word" class="item test">5</a>
<a href="/a.java" class="item last">6</a>


</body>
</html>
```



![image-20200524145809976](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524145809976.png)

## 美化元素

### 字体样式

1、重点要突出的字，用span标签

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        .span1{
            font-size: 50px;
        }
    </style>
</head>
<body>
    欢迎学习<span class="span1">Java</span>
</body>
</html>
```

2、字体样式

font-family:&emsp;字体

font-size: &emsp;字体大小

font-weight:&emsp;字体粗细

color: &emsp;字体颜色

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        body{
            font-family: "Agency FB",华文楷体;
        }

        h1{
            font-size: 50px;
        }
        .p1{
            font-weight: bolder;
        }
    </style>
</head>
<body>
<h1>故事介绍</h1>
<p class="p1">
    平静安详的元泱境界，每隔333年，总会有一个神秘而恐怖的异常生物重生，它就是魁拔！魁拔的每一次出现，都会给元泱境界带来巨大的灾难！即便是天界的神族，也在劫难逃。在天地两界各种力量的全力打击下，魁拔一次次被消灭，但又总是按333年的周期重新出现。魁拔纪元1664年，天神经过精确测算后，在魁拔苏醒前一刻对其进行毁灭性打击。但谁都没有想到，由于一个差错导致新一代魁拔成功地逃脱了致命一击。很快，天界魁拔司和地界神圣联盟均探测到了魁拔依然生还的迹象。因此，找到魁拔，彻底消灭魁拔，再一次成了各地热血勇士的终极目标。
</p>
<p>在偏远的兽国窝窝乡，蛮大人和蛮吉每天为取得象征成功和光荣的妖侠纹耀而刻苦修炼，却把他们生活的村庄搅得鸡犬不宁。村民们绞尽脑汁把他们赶走。一天，消灭魁拔的征兵令突然传到窝窝乡，村长趁机怂恿蛮大人和蛮吉从军参战。然而，在这个一切都凭纹耀说话的世界，仅凭蛮大人现有的一块冒牌纹耀，不要说参军，就连住店的资格都没有。受尽歧视的蛮吉和蛮大人决定，混上那艘即将启程去消灭魁拔的巨型战舰，直接挑战魁拔，用热血换取至高的荣誉。</p>
</body>
</html>
```

也可以用一个font搞定

```html
	<style>
        ..p1{
            font: ordinal bolder 20px "华文仿宋";
        }
    </style>
```



### 文本样式

1、color 颜色

1. 使用单词，如green
2. 使用RGB，如#0b37ff
3. 使用rgb，rgba函数，a代表透明度 ，如rgba(0,255,255,0.9)

2、文本对齐的方式

- text-align:&emsp;排版，通常用居中center

3、首行缩进

- text-indent&emsp; 段落首行缩进，如2em缩进两个字符；

4、行高

- line-height&emsp;行高，和块的高度一致，就可以上下居中

5、装饰

- text-decoration   &emsp;可以指定划线和划线颜色，下划线underline，中划线line-through，上划线overline

6、 文本阴影

- text-shadow: &emsp;阴影颜色，水平偏移，垂直偏移，阴影半径，如text-shadow: #3cc7f5 10px 0px 2px;

### 超链接伪类

一个不带任何样式的a标签是很丑的

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<img src="../images/s29877467.jpg" alt="">
<p>
    <a href="#">码出高效：java开发手册</a>
</p>
<p>
    <a href="#">作者：孤尽老师</a>
</p>
<p>
    ￥99
</p>

</body>
</html>
```



![image-20200524154040704](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524154040704.png)

增加超链接伪类主要是用a:hover和a:active

- a:hover 鼠标悬浮的样式
- a:active 鼠标按住不放的样式

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        a{
            text-decoration: none;
            color: black;
        }
        /*鼠标悬浮*/
        a:hover{
            color: orange;
            /*字体变大*/
            font-size: 30px;
        }
        /*鼠标点击不放*/
        a:active{
            color: green;
        }
        /*已访问*/
        a:visited{
            color: bisque;
        }
    </style>
</head>
<body>

<img src="../images/s29877467.jpg" alt="">
<p>
    <a href="#">码出高效：java开发手册</a>
</p>
<p>
    <a href="#">作者：孤尽老师</a>
</p>
<p>
    ￥99
</p>

</body>
</html>
```

当鼠标移到了码出高效的效果

![image-20200524155150783](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524155150783.png)

### 背景样式

- background-image: 背景图片，默认平铺，写法是url("xxx");
- background-repeat: 平铺的轴，reapeat-x只水平平铺，repeat-y只垂直平铺
- opacity: 透明度
- 也可以一次性写齐 如background: red url("../images/a.jpeg") 200px 10px no-repeat;

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        div{
            width: 1000px;
            height: 700px;
            border: 2px solid red;
            background-image: url("../images/u=1530628949,1867294524&fm=26&gp=0.jpg");
        }
    </style>
</head>
<body>
<div id="div1"></div>
</body>
</html>
```

![image-20200524171636102](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524171636102.png)



有趣的玩法，渐变色写法，给百度加上

```html
<style>	
		body{
            background-image: linear-gradient(19deg, #21D4FD 0%, #B721FF 100%);
        }
</style>
```

![image-20200524172834857](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524172834857.png)

### 列表样式

对于ul样式

- list-style 修改列表前面圆点，none为无，decimal为有序列表

  

示例：

原始列表，不加任何样式

```html
<body>
<h2 class="title">全部商品分类</h2>

<ul>
    <li><a href="#">图书</a>&nbsp;&nbsp;<a href="#">音像</a>&nbsp;&nbsp;<a href="#">数字商品</a></li>
    <li><a href="#">家用电器</a>&nbsp;&nbsp;<a href="#">手机</a>&nbsp;&nbsp;<a href="#">数码</a></li>
    <li><a href="#">电脑</a>&nbsp;&nbsp;<a href="#">办公</a></li>
    <li><a href="#">家居</a>&nbsp;&nbsp;<a href="#">家装</a>&nbsp;&nbsp;<a href="#">厨具</a></li>

</ul>
</body>
```



![image-20200524164016592](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524164016592.png)

参照淘宝京东，进行改造，添加样式

![image-20200524164112702](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524164112702.png)



```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="../CSSDemo/list.css">
</head>
<body>

<div id="nav">
    <h2 class="title">全部商品分类</h2>
    <ul>
        <li><a href="#">图书</a>&nbsp;&nbsp;<a href="#">音像</a>&nbsp;&nbsp;<a href="#">数字商品</a></li>
        <li><a href="#">家用电器</a>&nbsp;&nbsp;<a href="#">手机</a>&nbsp;&nbsp;<a href="#">数码</a></li>
        <li><a href="#">电脑</a>&nbsp;&nbsp;<a href="#">办公</a></li>
        <li><a href="#">家居</a>&nbsp;&nbsp;<a href="#">家装</a>&nbsp;&nbsp;<a href="#">厨具</a></li>

    </ul>
</div>

</body>
</html>
```

没找到下拉和右拉合适的照片就没加上，需要指定偏移，和不填充

```css
div[id="nav"]{
    width: 300px;
}

.title{
    font-size: 18px;
    font-weight: bolder;
    text-indent: 1em;
    line-height: 30px;
    color: aliceblue;
    background: orange ;
}

ul{
    background: aliceblue;
}
ul li{
    height: 30px;
    list-style: none;
    text-indent: 1em;
}

a{
    text-decoration: none;
    font-size: 18px;
    color: black;
}

a:hover{
    color: orange;
    text-decoration: underline orange;
}
```

![image-20200524172418039](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524172418039.png)

### 盒子模型

每个元素相当于在一个盒子里

![image-20200524175712151](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524175712151.png)



如果不处理边距，效果如下

![image-20200524180127497](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524180127497.png)

![image-20200524180214423](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524180214423.png)

margin：外边距  现在为8
padding：内边距
border：边框

**1、边框**

可以设置边框的颜色，线，粗细，也可以专门定义某一条边

```css
border: 2px solid black;
```

**圆角边框**，2个参数按左上，右下；4个参数按左上，右上，右下，左下

```css
border: 10px solid red;
border-radius: 50px 20px 10px 5px;
```

![image-20200524185411970](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524185411970.png)

通过圆角标签可以画圆和各种扇形，一般通过设定边框可以弄成一个圆形的头像

**2、margin外边距**

一个参数则是设置上下左右都是这个宽度，两个参数则是，上下、左右，四个参数则是，上右下左顺时针

居中展示

```css
margin: 0 auto;
```

**3、padding内边距**

类似的margin，只是border内部的

**4、元素实际总大小**

margin+ border+ padding+内容宽度



优化后

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        #app{
            width: 300px;
            border: 1px solid red ;
            margin: 0 auto;
        }
        h2{
            font-size: 16px;
            height: 20px;
            background: orange;
            line-height: 20px;
            color: #f9fbff;
            margin: 0;
        }
        form{
            background: #f9f9fd;
        }

        div:nth-of-type(1){
            margin: 10px;
        }
        div:nth-of-type(2){
            margin: 10px;
        }
        div:nth-of-type(3){
            margin: 10px;
        }
    </style>
</head>
<body>

<div id="app">
    <h2>会员登录</h2>
    <form action="#" method="post">
        <div>
            <span>用户名：</span>
            <input type="text">
        </div>
        <div>
            <span>密码：</span>
            <input type="text">
        </div>
        <div>
            <span>邮箱：</span>
            <input type="text">
        </div>
    </form>
</div>

</body>
</html>
```



![image-20200524182556054](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524182556054.png)



### 盒子阴影

在元素外层加一层阴影

```css
box-shadow: 10px 10px 15px yellow;
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        img{
            height: 500px;
            width: 500px;
            margin: 0;
            padding: 0;
            border: black solid 1px;
            border-radius: 250px;
            box-shadow: yellow 10px 10px 15px;
        }
    </style>
</head>
<body>


<img src="../images/u=2919831077,1230952122&fm=26&gp=0.jpg">
</body>
</html>
```

![image-20200524191050620](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524191050620.png)

### 浮动（display、float，多数用float）

标准文档流

![image-20200524192309130](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524192309130.png)

其中分为块级元素和行内元素

块级元素，独占一行，比如 h1~h6、p、div、ul等

行内元素：不独占一行，比如span、a、img等

行内元素可以被包含在块级元素中，反之，则不可以

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        div{
            height: 100px;
            width: 100px;
            border: red solid 1px;
        }
        span{
            height: 100px;
            width: 100px;
            border: red solid 1px;
        }
    </style>
</head>
<body>
<div>div块元素，1111111111111111111</div>
<span>span行内元素,文字有多长我就多长</span>
</body>
</html>
```

![image-20200524192840878](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524192840878.png)

**1、通过display改变块元素和行内元素**

block块元素

inline行内元素

inline-block是块元素，年是可以内联，在一行！

none 不展示

```html
 <style>
        /*块元素*/
        div{
            height: 100px;
            width: 100px;
            border: red solid 1px;
            display: inline-block;
        }
        span{
            height: 100px;
            width: 100px;
            border: red solid 1px;
            display: block;
        }
    </style>
```



![image-20200524193412026](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524193412026.png)

**2、float 浮动 能够实现排版**，但是存在问题是浮动之后跳出父级元素后出现塌陷和页面大小改变后，元素位置改变

float: left 左浮

float: right 右浮

![image-20200524200306149](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524200306149.png)



![image-20200524200330336](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524200330336.png)

```css
div{
    margin: 10px;
    padding: 5px;
}

#father{
    border: 1px #000 solid;
}

.lay01{
    border: 1px #F00 dashed;
    display: inline-block;
    float: right;
}
.lay02{
    border: 1px #F00 dashed;
    display: inline-block;
    float: right;
}
.lay03{
    border: 1px #F00 dashed;
    display: inline-block;
    float: right;
}
```

页面坍塌解决

1、增加父级元素的高度

```css
#father{
    border: 1px #000 solid;
    height: 800px;
}
```



2、用clear解决,底部增加一个空div标签，并把样式修改

clear: right；右侧不允许有浮动元素

clear: left；左侧不允许有浮动元素

clear: both；两侧不允许有浮动元素

```html
<div class="clear"></div>

.clear{
	clear: both;
	margin: 0;
	padding: 0;
}
```

3、overflow 在父级元素中增加一个

```css
overflow: hidden;
```

4、通过伪类（最通用）

```css
#father:after{
    content: "";
    display: block;
    clear: both;
}
```

![image-20200524224514163](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524224514163.png)

总结：

1.浮动元素后面增加空dⅳ简单，代码中尽量避免空dⅳ

2.设置父元素的高度

简单，元素假设有了固定的高度，就会被限制

3.overflow简单，下拉的scroll一些场景避免使用

4.父类添加一个伪类：after（推荐）

写法稍微复杂一点，但是没有副作用，推荐使用！

**float与display对比**

1、display方向不可以控制

2、float浮动起来的话会脱离标准文档流，所以要解决父级边框塌陷的问题



### 定位

让某些元素固定在页面的某些位置

**1、相对定位**

相于自已原来的位置进行偏移,下面是距离上面-20，即往上移20px，还有bottom，left，right

```css
	position: relative;
    top: -20px;

```

相对定位的话，它任然在标准文档流中，原来的位置会被保留

实例题

使用<diV和超链接<a>布局页面

每个超链接宽度和高度都是100X，背景颜色是粉色，鼠标指针移上去时变为蓝色

使用相对定位改变每个超链接的位置

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        #father{
            height: 300px;
            width: 300px;
            border: red 2px solid;
            padding: 10px;
        }

        .a1{
            height: 100px;
            width: 100px;
            line-height: 100px;
            text-align: center;
            display: block;
            text-decoration: none;
            color: #f9fbff;
            background: #ff38f0;
        }
        .a2{
            height: 100px;
            width: 100px;
            line-height: 100px;
            text-align: center;
            display: block;
            text-decoration: none;
            color: #f9fbff;
            background: #ff38f0;
            position: relative;
            top: -100px;
            right: -200px;
        }
        .a3{
            height: 100px;
            width: 100px;
            line-height: 100px;
            text-align: center;
            display: block;
            text-decoration: none;
            color: #f9fbff;
            background: #ff38f0;
        }
        .a4{
            height: 100px;
            width: 100px;
            line-height: 100px;
            text-align: center;
            display: block;
            text-decoration: none;
            color: #f9fbff;
            background: #ff38f0;
            position: relative;
            top: -200px;
            right: -100px;
        }
        .a5{
            height: 100px;
            width: 100px;
            line-height: 100px;
            text-align: center;
            display: block;
            text-decoration: none;
            color: #f9fbff;
            background: #ff38f0;
            position: relative;
            top: -200px;
            right: -200px;
        }

        body a:hover{
            background: #93c2ff;
        }
    </style>
</head>
<body>
    <div id="father">
        <div>
            <a class="a1" href="#">链接1</a>
        </div>
        <div>
            <a class="a2" href="#">链接2</a>
        </div>
        <div>
            <a class="a3" href="#">链接3</a>
        </div>
        <div>
            <a class="a4" href="#">链接4</a>
        </div>
        <div>
            <a class="a5" href="#">链接5</a>
        </div>
    </div>
</body>
</html>
```

![image-20200524230947448](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524230947448.png)



**2、绝对定位**

1、没有父级元素定位的前提下，相对于浏览器定位

2、假设父级元素存在定位，我们通常会相对于父级元素进行偏移

3、应当让在父级元素范围内移动（可以设置overflow让其溢出隐藏）

相对于父级或浏览器的位置，进行指定的偏移，绝对定位的话，它不在在标准文档流中，原来的位置不会被保留

```css
			position: absolute;
            left: 70px;
```



**3、固定定位**

```css
position: fixed;
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>

<style>
    body{
        height: 10000px;
    }
    div:nth-of-type(1){
        width: 100px;
        height: 100px;
        background: red;
        position: absolute;
        right: 0;
        bottom: 0;
    }

    div:nth-of-type(2){
        width: 100px;
        height: 100px;
        background: yellow;
        position: fixed;
        right: 0;
        bottom: 0;
    }
</style>
<body>
<div>div1</div>
<div>div2</div>
</body>
</html>
```



一般用来做导航

![image-20200524233223683](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524233223683.png)

**4、z-index**

类似ps图层的定义   ，设定图层的等级，再通过透明度可以完成覆盖的一些操作

```css
z-index: 88;
```


