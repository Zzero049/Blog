# CSS

CSS是“层叠样式表单”。是用于（增强）控制网页样式并允许将样式信息与网页内容分离的一种标记性语言。

### 语法规则

![image-20200420181102263](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200420181102263.png)

**选择器：**浏览器根据“选择器”决定受CSS样式影响的HTML元素（标签）。

**属性（property）**是你要改变的样式名，并且每个属性都有一个值。属性和值被冒号分开，并由花括号包围，这样就组成了一个完整的样式声明（declaration），例如：p{color:blue}

**多个声明：**如果要定义不止一个声明，则需要用分号将每个声明分开。虽然最后一条声明的最后可以不加分号（但尽量在每条声明的末尾都加上分号）

## CSS与HTML结合方式

### 第一种方式

在标签的 style 属性上设置"key:value value；"，修改标签样式。

```html
xxxxxxxxxx <div style="border: brown solid 2px ">lalala</div>html
```

把css样式写戴一个单独的css文件，再通过limk标签引入即可复用。|把css样式写戴一个单独的css文件，再通过limk标签引入即可复用。|然而这样会出现问题：



1.如果标签多了。样式多了。代码量非常庞大。
2.可读性非常差。
3.Css代码没什么复用性可方言。

### 第二种方式

在headd标签来定义各种自己需要的css样式。
格式如下：
xxx{
	Key:value value;

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

### 第三种

把css样式写在一个单独的css文件，再通过link标签引入即可复用。

```css
/*1.css*/
div{
  	border: brown solid 2px
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

    <style type="text/css">

    </style>
</head>
<body>
<div>lalala</div>
</body>
</html>
```

## CSS选择器

### 标签名选择器

跟上面一样，根据div、span等标签定义各自类型的样式即可

### id选择器

```html
#id名{
	属性:值
}

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

```html
.class名{
	属性:值
}

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



### 组合选择器

就是即id和class声明在一起，即可以通过id引用，也可以通过class引用

```html
#id名,.class名{
	属性:值
}
```



## 常用样式

1、字体颜色
	color:red；

颜色可以写颜色名如：black，blue，red，green等颜色也可以写rgb值和十六进制表示值：如rgb（255，0，0），#00F6DE，如果写十六进制值必须加#

2、宽度
	width:19px；

​	宽度可以写像素值：19px；也可以写百分比值：20%；

3、高度
	height:20px;

​	宽度可以写像素值：19px；也可以写百分比值：20%；

4、背景颜色
	background-color:#0F2D4C

4、字体样式：
	color:#FFO000;      字体颜色红色

​	font-size：20px；字体大小

5、像素实线边框
	border：1px solid red；

7、DIV居中
	margin-left:auto；

​	margin-right:auto;

8、文本居中：
	text-align:center；

9、超连接去下划线
	text-decoration:none；

10、表格细线

```css
table{
		border:1px solid black;/*设置边框*/
		border-collapse:collapse;/*将边框合并*/
	}
td，th{
	border:1px solid black;/*设置边框*/
}
```

11、列表去除修饰(去前缀符号)

```html
ul{
	list-style:none；
}
```



