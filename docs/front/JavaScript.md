

# JavaScript

​	Javascript 语言诞生主要是完成页面的数据验证。因此它运行在客户端，需要运行浏览器来解析执行Javascript代码。

​	Js是Netscape网景公司的产品，最早取名为Livescript；为了吸引更多java程序员。名为Javascript。

​	JS是弱类型，Java是强类型。（弱类型就是类型可变；强类型，就是定义变量的时候。类型已确定。而且不可变。）

特点：

​	1.交互性（它可以做的就是信息的动态交互）

​	2.安全性（不允许直接访问本地硬盘）

​	3.跨平台性（只要是可以解释Js的浏览器都可以执行，和平台无关）



## 与Html结合使用

### 第一种方式

只需要在head标签中，或者在body标签中，使用script 标签来书写Javgscript代码

```html
<body>
    <script type="text/javascript">
        alert("!!!!!!")
    </script>
</body>
```



### 第二种方式

使用script标签引入单独的Javascript代码文件

src属性专门用来引入Js文件路径（可以是相对路径，也可以是绝对路径）

一个script标签可以用来定义js代码，也可以用来引入js文件。但是，两个功能二选一使用。不能同时使用两个功能

```html
<script type="text/javascript" src="JS/1.js"></script>
```



## 变量

JavaScript的变量类型：

|  数据类型  | 数据类型名 |
| :--------: | :--------: |
|  数值类型  |   number   |
| 字符串类型 |   string   |
|  对象类型  |   object   |
|  布尔类型  |  boolean   |
|  函数类型  |  function  |

Javascript里特殊的值：

| 特殊值    | 含义                                                       |
| --------- | ---------------------------------------------------------- |
| undefined | 未定义，所有js变量未赋于初始值的时候，默认值都是undefined. |
| null      | 空值                                                       |
| NAN       | 全称是：Not a Number。非字数。非数值。                     |

JS中的定义变量格式：

​	var 变量名;

​	var 变量名=值;

### 关系运算

​	等于：                     ==               等于是简单的做字面值的比较

​	全等于：                 ===             除了做字面值的比较之外，还会比较两个变量的数据类型

```js
var a = 12;
var b = "12";

alert(a==b)//true
alert(a===b)//false
```



### 逻辑运算

运算符：

​	且运算：&&

​	或运算：ll

​	取反运算：！

在JavaScript语言中，所有的变量，都可以做为一个boolean类型的变量去使用。

0、null、undefined、"" (空字符串)  都认为是false；

- 8&且运算。有两种情况：
  
  ​	第一种：当表达式全为真的时候。返回最后一个表达式的值。

  ​	第二种：当表达式中，有一个为假的时候。返回第一个为假的表达式的值
  
  ```js
  var a = "abc";
  var b = true;
  var c = null;
  var d = false;
  
  alert(a && b) 		//true
  alert(b && a)		//abc
alert(a && c && d)	//null
  ```

  
  
- ||或运算
  
​	第一种情况：当表达式全为假时，返回最后一个表达式的值
  
​	第二种情况：只要有一个表达式为真。就会把回第一个为真的表达式的值
  
  ```js
  var a = "abc";
  var b = true;
  var c = null;
  var d = false;
  
  alert(c && d) 		//false
  alert(c || a || b)	//abc
```
  
  

## <font color="red">数组</font>

JS中数组的定义：
格式：
	var 数组名=[]；								//空数组
	var 数组名=[1, 'abc', true]；		 //定义数组同时赋值元素

```js
var arr = [];

arr[0] = 12;
//javaScript语言中的数组，只要我们通过数细下标财值，那么最大的下标值，就会自动的给数组做扩容操作。
arr[2] = "abc";
alert(arr.length);	//3
```

### 遍历

```js
for(var i=0;i<arr.length;i++){
    alert(arr[i]);
}
```



## <font color="red">函数</font>

### 函数定义的第一种方式

function 函数名（形参列表）{
	函数体

｝

```js
function fun1() {
    alert("无参函数fun1()被调用了")
}
function fun2(a,b) {
    alert("有参函数fun1()被调用了"+"a："+a+"b："+b)
}

fun1()
fun2(16516,"adad")
```

在JavaScript语言中，带有返回值的函数只需要在函数体内直接使用return语句返回值即可！

```java
function sum(numl,num2) {
    var result = numl + num2;
    return result;
}
```



### 函数定义的第二种方式

var 函数名 = function(形参列表){

}

```js
var fun1= function(){
    alert("无参函数fun1()被调用了")
}
fun1()
```



### 不支持重载

在Java中函数允许重载。但是在JS中函数的重载会直接覆盖掉上一次的定义



### 隐形参数

就是在function函数中不需要定义，但却可以直接用来获取所有参数的变量。我们管它叫隐形参数。类似java中的可变长参数（Object ... args）。

```js
//实际上传多少都可以
function sum(numl,num2) {
    var result = 0
    for(var i=0;i < arguments.length;i++){
        if(typeof (arguments[i])=="number"){
            result += arguments[i];
        }
    }
    return result;
}

sum(1,2,3,"999",7,3,22,"",false)
```



## 自定义对象

### object形式的自定义对象
对象的定义：

​		var 变量名=new Object();		//对象实例（空对象）

​		变量名.属性名 = 值；					//定义一个属性

​		变量名.函数名=function(){}		 //定义一个函数

```js
var obj = new Object();
obj.name = "张飞";
obj.age =  18;
obj.fun  = function () {
    alert(this.name);
}

obj.fun();
```



### {}花括号形式的自定义对象

var变量名={        				  //空对象
属性名:值,       					 //定义一个属性
属性名:值, 							//定义一个属性
函数名：function(){}		   //定义一个函数(注意都是冒号，不是等号)

}

```js
var obj ={
    name: "张飞",
    age: 18,
    fun: function(){
        alert(this.name);
    }
};

obj.fun();
```



## js中的事件

事件是电脑输入设备与页面进行交互的响应。

| 事件                      | 用途                                           |
| ------------------------- | ---------------------------------------------- |
| onload加载完成事件        | 页面加载完成之后，常用于做页面js代码初始化操作 |
| onclick单击事件           | 常用于按钮的点击响应操作                       |
| onblur失去焦点事件        | 常用用于输入框失去焦点后验证其输入内容是否合法 |
| onchange 内容发生改变事件 | 常用于下拉列表和输入框内容发生改变后操作       |
| onsubmit 表单提交事件     | 常用于表单提交前，验证所有表单项是否合法       |

### 事件的注册

其实就是告诉浏览器，当事件响应后要执行哪些操作代码，叫事件注册或绑定。

#### 静态注册

通过html标签的事件属性直接赋于事件响应后的代码，这种方式我们叫静态注册。

#### 动态注册

是指先通过js代码得到标签的dom对象，然后再通过dom对象.事件名=function(){}这种形式赋于事件响应后的代码，叫动态注册。

#### onload

静态注册

```html
<html>
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        function myOnLoad() {
            alert("静态注册一系列要做的操作");
        }

    </script>
</head>
<body onload="myOnLoad()">

</body>
</html>
```

动态注册

```html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        //onload动态注册，固定写法
        window.onload = function () {
            alert("动态注册一系列要做的操作");
        }
    </script>
</head>
<body>

</body>
</html>
```

#### onclick

静态注册

```html
<html>
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        function myOnClick() {
            alert("静态注册一系列要做的操作");
        }

    </script>
</head>
<body >
	<button onclick="myOnClick">按钮1</button>
</body>
</html>
```

动态注册

```html
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        //动态注册onclick事件，注意是用onload
        window.onload = function () {
            var btnObj = document.getElementById("btn");
            btnObj.onclick = function () {
                alert("动态注册onclick");
            }
        }
    </script>

</head>
<body>
    <button id="btn">按钮1</button>
</body>
</html>
```

####  onblur

输入框失去光标的事件

console是控制台对象，是由JavaScript语言提供，专门用来向浏览器的控制器打印输出，用于测试使用

静态注册

```html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        function MyOnblur() {
            console.log("静态失去焦点事件");
        }
    </script>
</head>
<body>
    用户名:<input type="text" onblur="MyOnblur();"/><br/>
</body>
</html>
```

动态注册

```html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        window.onload = function () {
            var nameObj = document.getElementById("name");
            nameObj.onblur = function () {
                console.log("动态注册失去焦点");
            }
        }
    </script>

</head>
<body>
    用户名:<input id="name" type="text"/><br/>
</body>
</html>
```

#### onchange

静态注册

```html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        function myOnChange() {
            alert("女神改变");
        }
    </script>
</head>
<body>
    女神:
    <select onchange="myOnChange()">
        <option>张曼玉</option>
        <option>关晓彤</option>
    </select>
</body>
</html>
```

动态注册

```html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        window.onload = function () {
            var change = document.getElementById("select");
            change.onchange = function () {
                alert("女神改变了！！！！");
            }
        }
    </script>
</head>
<body>
    女神:
    <select id="select">
        <option>张曼玉</option>
        <option>关晓彤</option>
    </select>
</body>
</html>
```

#### onsubmit

静态注册

```html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="javascript">
        function myOnSubmit() {
            // 要验证所有表单项是否合法，假设不合法就图止表单提交
            alert("静态注册表单提交事件--—-发现不合法");
            return false;
        }
    </script>
</head>
<body>
<!--return false可以阻止表单提交-->
    <form action="http://localhost:8080" method="get" onsubmit=" return myOnSubmit()">
        <input type="submit" value="提交"/>
    </form>
</body>
</html>
```

动态注册

```html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        window.onload = function () {
            var formObj = document.getElementById("form");
            formObj.onsubmit = function () {
                // 要验证所有表单项是否合法，假设不合法就图止表单提交
                alert("动态注册表单提交事件--—-发现不合法");
                return false;
            }
        }
    </script>
</head>
<body>
<!--return false可以阻止表单提交-->
    <form id="form" action="http://localhost:8080" method="get" >
        <input type="submit" value="提交"/>
    </form>
</body>
</html>
```



## <font color="red">DOM模型</font>

DOM全称是Document object Model文档对象模型

作用就是把文档中的标签，属性，文本，转换成为对象来管理。

<img src="https://gitee.com/zero049/MyNoteImages/raw/master/image-20200420230649118.png" alt="image-20200420230649118" style="zoom:80%;" />

Document 对象的理解：
	第一点：Document 它管理了所有的HTML文档内容。

​	第二点：document 它是一种树结构的文档。有层级关系

​	第三点：它让我们把所有的标签都对象化

​	第四点：我们可以通过document 访间所有的标签对象。

```html
<body>
    <div id="div01">div01</div>
</body>
```

相当于

```java
class Dom{
	private String id;			//id 属性
    private String tagName;		//表示标签名
    private Dom parentNode;		//父亲
    private List<Dom> children;	//孩子结点
    private String innerHTML;	//起始标签和结束标签中间的内容
}
```

### Dom对象中的方法

- document.getElementById（elementId）
  
通过标签的id属性查找标签dom对象，elementId是标签的id属性，返回查找成功的第一个对象
  
- document.getElementsByName（elementName）
  
通过标签的name属性查找标签dom对象，elementName标签的name 属性值
  
- document.getElementsByTagName（tagName）
  
通过标签名查找标签dom对象。tagName是标签名
  
- document.createElement（tagName）
  
通过给定的标签名，创建一个标签对象。tagName是要创建的标签名
  

  
document 对象的三个查询方法，如果有id属性，优先使用getElementById方法来进行查询
  
如果没有id属性，则优先使用getElementsByName方法来进行查询
  
如果id属性和name属性都没有最后再按标签名查 getElementsBy TagName
  
  注意html没有的属性是无法通过.属性赋值成功的，而且语句是从上向下执行创建对象的

#### getElementById

例子：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        function f() {
            // 验证的规则是：必须由字母，数字。下划线组成。并且长度是5到12位。
            var usernameObj = document.getElementById("username");
            //usernameObj就是dom对象，通过属性名取出其中的值，如usernameObj.value
            // 取出的dom对象可读可写
            var userSpanObj = document.getElementById("usernameSpan");
            var patt = /^\w{5,12}$/;
            // test（）方法用于测试某个字符串，是不是匹配规则，
            // 匹配就返回true。不匹配就返回false
            if(patt.test(usernameObj)){
                userSpanObj.innerHTML = "用户名合法";              
            }else{
                userSpanObj.innerHTML = "用户名不合法";
            }
        }
    </script>
</head>
<body>
用户名:<input type="text" id="username" value="xxx">
    <span id = "usernameSpan" style="color:red"></span>
<button onclick="f()">校验</button>

</body>
</html>
```

#### getElementsByName

例子：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        function clickAll() {
            // 达所有复选框部选中
            // document.getELementsByName（）；是根据指定name属性查询返回多个标态对象集合
            var hobbies = document.getElementsByName("hobby");
            for(var i=0;i<hobbies.length;i++){
                // checked表示复选框的进中状态。如果选中是true，不选中是false 
                // checked 这个属性可读，可写
                hobbies[i].checked = true;
            }
        }
    </script>
</head>
<body>
兴趣爱好：
<input type="checkbox" name="hobby" value="cpp" checked="checked">c++
<input type="checkbox" name="hobby" value="java">java
<input type="checkbox" name="hobby" value="python">python
<button onclick="clickAll()">全选</button>
</body>
</html>
```

#### getElementsByTagName

例子：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        function clickAll() {
            // 是按照指定标签名来进行查询并返回集合
            // 这个集合的操作跟数组一样
            // 集合中都是dom对象
            // 集合中元素顺序是他们在html页面中从上到下的顺序。
            var hobbies = document.getElementsByTagName("input");
            for(var i=0;i<hobbies.length;i++){
                // checked表示复选框的进中状态。如果选中是true，不选中是false
                // checked 这个属性可读，可写
                hobbies[i].checked = true;
            }
        }
    </script>
</head>
<body>
兴趣爱好：
<input type="checkbox" name="hobby" value="cpp" checked="checked">c++
<input type="checkbox" name="hobby" value="java">java
<input type="checkbox" name="hobby" value="python">python
<button onclick="clickAll()">全选</button>
</body>
</html>
```

#### createElement

```html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script type="text/javascript">
        //onload动态注册，固定写法
        window.onload = function () {
            //现在需要我们使用js代码来创建html标签，并显示在页面上
            // 标签的内容就是：<div>啦啦啦</div>
            var divObj=document.createElement("div");//在内存中<div></div>
            divObj.innerText="啦啦啦";          //<div>啦啦啦</div>，但，还只是在内存中
            //添加子元素
            document.body.appendChild(divObj)
        }
    </script>
</head>
<body>

</body>
</html>
```



### 节点常用方法和属性

节点就是标签对象

```html
<div id="div01">
    <input type="checkbox" name="hobby" value="cpp" checked="checked">c++
</div>
```

```js
//document.getElementById("div01")取出的就是一个节点
var inputs = document.getElementById("div01").getElementsByTagName("input")
```



- 方法：
  - getElementsByTagName（）
    
    通过具体的元素节点调用，获取当前节点的指定标签名孩子节点-
    
- appendChild（oChildNode）
    
    可以添加一个子节点，oChildNode是要添加的孩子节点
  
- 属性
  - childNodes属性，获取当前节点的所有子节点
  - firstChild 属性，获取当前节点的第一个子节点
  - lastChild属性，获取当前节点的最后一个子节点
  - parentNode属性，获取当前节点的父节点
  - nextSibling属性，获取当前节点的下一个节点
  - previousSibling属性，获取当前节点的上一个节点
  - className用于获取或设置标签的class属性值
  - innerHTML属性，表示获取/设置起始标签和结束标签中的内容（包括包含的标签）
  - innerText属性，表示获取/设置起始标签和结束标签中的文本（仅文本）