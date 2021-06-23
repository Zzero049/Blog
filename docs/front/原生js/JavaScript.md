# JavaScript

​	Javascript 语言诞生主要是完成页面的数据验证。因此它运行在客户端，需要运行浏览器来解析执行Javascript代码。

​	Js是Netscape网景公司的产品，最早取名为Livescript；为了吸引更多java程序员。名为Javascript。

​	JS是弱类型，Java是强类型。（弱类型就是类型可变；强类型，就是定义变量的时候。类型已确定。而且不可变。）

特点：

​	1.交互性（它可以做的就是信息的动态交互）

​	2.安全性（不允许直接访问本地硬盘）

​	3.跨平台性（只要是可以解释Js的浏览器都可以执行，和平台无关）



## HTML与CSS与JS

**1、结构层（HTML）**

**2、表现层（css）**

CSS层叠样式表是一门标记语言，并不是编程语言，因此不可以自定义变量，不可以引用等，换句话说就是不具备任何语法支持，它主要缺陷如下

- 语法不够强大，比如无法嵌套书写，导数模块化开发中需要写很多重复的选择器
- 没有变量和合理的样式复用机制，使得逻辑上相关的属性值必须以字面量的形式重复输出，导致难以维护

这就导致了我们在工作中无端增加了许多工作量。为了解决这个问题，前端开发人员会使用一种称之为**【CSS预处理器】**的工具，提供CSS缺失的样式层复用机制、减少冗余代码，提高样式代码的可维护性。大大提高了前端在样式上的开发效率

**什么是CSS预处理器**

CSS预处理器定义了一种新的语言，其基本思想是，用**一种专门的编程语言，为CSS增加了一些编程的特性**，将CSS作为目标生成文件，然后开发者就只要使用这种语言进行CSs的编码工作。转化成通俗易懂的话来说就是“用一种专门的编程语言，进行Web页面样式设计，再通过编译器转化为正常的CSS文件，以供项目使用”

**常用的CSS预处理器**

- **SASS：**基于Ruby，通过服务端处理，功能强大。解析效率高。需要学习Ruby语言，上手难度高于LESS
- **LESS：**基于 NodeJS，通过客户端处理，使用简单。功能比SASS简单，解析效率也低于SASS，但在实际开发中足够了，所以我们后台人员如果需要的话，建议使用LESS。



**3、行为层（js）**

JavaScript一门弱类型脚本语言，其源代码在发往客户端运行之前不需经过编译，而是将文本格式的字符代码发送给浏览器由浏览器解释运行

Native原生Js开发

原生JS开发，也就是让我们按照【ECMAScript】标准的开发方式，简称是ES，特点是所有浏器都支持。截止到2020年，ES标准已发布如下版本
1、ES4（内部，未正式发布）

2、ES5（全浏览器支持）

3、ES6（常用，当前主流版本：webpack打包成为ES5支持！）

4、ES7

5、ES8

6、ES9（草案阶段）

区别就是逐步增加新特性。

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



## 浏览器必备调试须知

![image-20200525174609377](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200525174609377.png)

console.log(xxx) 在浏览器的控制台打印变量！

调试：

![image-20200525175431311](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200525175431311.png)

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

| 特殊值    | 含义                                                         |
| --------- | ------------------------------------------------------------ |
| undefined | 未定义，所有js变量未赋于初始值的时候，默认值都是undefined.   |
| null      | 空值                                                         |
| NAN       | 全称是：Not a Number。非字符。非数值。只能用过isNaN判断（NaN与NaN也是不相等的） |

JS中的定义变量格式：

**全局变量**

​	var 变量名;

​	var 变量名=值;

**局部变量**

​	let 变量名

'use strict'；写在第一行，严格检查摸式，放置防止 Javascript的随意性导致产生的一些问题



### 字符串

1、正常字符串我们使用单引号，或者双引号包裹

2、注意转义字符\

```
\
\n
\t
u4e2d   \u#### Unicode字符
x41     Asc11字符
```

3、多行字符串编写 ``

```javascript
var content =
    				`
                    n你好
                    sssss
                    ccccz
                    `
```

4、模版字符串 ``

```javascript
let name = 'zhangsan'
let msg = `你好，${name}`
```

5、字符串长度

```javascript
str.length
```

6、字符串的可变性，不可变

![image-20200525183333285](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200525183333285.png)

7、大小写转换

```javascript
//注意，这里是方法，不是属性了
student.toUpperCase()
student.toLowerCase()
```

8、 student. indexOf('t')
9、 substring

```javascript
// [a,b)
student.substring(1)	//从第一个字符串截取到最后一个字符串
student substring(1,3)	//[1,3)
```



### 关系运算

​	等于：                     ==               等于是简单的做字面值的比较

​	全等于：                 ===             除了做字面值的比较之外，还会比较两个变量的数据类型(尽量使用)

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
  
  alert(c || d) 		//false
  alert(c || a || b)	//abc
  ```

  ### 作用域

绝大多数和java是一样的，只不过不先声明使用一个变量，不会不能运行，只是undefined

然而在一个方法定义全局变量var 出了方法也取不到

```js
function f1() {
            var a = 2;
            var b = 4;
        }

        f1();
        console.log(a);		// Uncaught ReferenceError: a is not defined
```



Javascript实际上只有一个全局作用域，任何变量（函数也可以视为变量），假设没有在函数作用范围内找到，就会向外查找，如果在全局作用域都没有找到，报错 RefrenceError

### 全局变量

由于我们所有的全局变量都会绑定到我们的 window上。

如果不同的js文件，使用了相同的全局变量，则会冲突

把自己的代码全部放入自己定义的唯一空间名字中，降低全局命名冲突的问题(定义一个自己专用的变量)

```js
// 全局变量
var ZeroApp = {};
// 定义全局变量
ZeroApp.name = 'zero';
```

### 常量

在ES6引入了**常量关键字const**

```js
const PI = 3.14;
PI = 111; //Uncaught TypeError: Assignment to constant variable.
```



## <font color="red">数组(属于对象类型)</font>



JS中数组可以包含任意的数据类型，定义：
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

1、长度

```
arr.length
```

注意：加入给 arr.length赋值，数组大小就会发生变化~，如果赋值过小，元素就会丢失

2、indexOf，通过元素获得下标索引，注意元素类型不同，得到的下标也不同

**3、slice()**   截取Arry的一部分，**返回一个新数组**，类似于 String中的 substring

**4、push()、pop()**，尾部弹入弹出，返回值是数组长度和弹出元素，数组长度是动态变化的

**5、unshift()，shift()** 头部弹入弹出

6、排序sort()

```javascript
(3)["B","C","A"]
arr.sort
(3)["A","B","c"]
```

7、元素反转 reverse()

```javascript
(3)["A","B","C"]
arr.reverse()
(3)["C","B","A"]
```

**8、 concat()**

```javascript
arr
(3)["C","B","A"]
arr.concat([1, 2, 3])
(6)["C","B","A",1,2,3]
```

注意：concat（）并没有修改数组，只是会**返回一个新的数组**

9、连接符join打印拼接数组，使用特定的字符串连接

```js
(3)["C","B","A"]
arr.join(-)
"C-B-A"
```

10、多维数组

```js
arr=[[1,2],[3,4],["5","6"]]; 
arr[1][1];
4
```

### 遍历

1、可以用while,for的形式

```js
for(var i=0;i<arr.length;i++){
    alert(arr[i]);
}
```

2、forEach循环

```js
vaa age = [1,23,3];

age.forEach(function(value){
    console.log(value);
})
```

3、 for in/of  in是下标，of是元素

```js
		let arr = [1,3,5,7];
        for(let num in arr){	//num是下标
            console.log(arr[num]);
        }

        for(let num of arr){	// num是元素
            console.log(num);
        }
```



## Map和Set

> ES6的新特性~

map，new的方法传入的东西与java不太一样，是个二维数组

```js
		var map = new Map([['tom',123],['zz',224]]);
        var name = map.get('tom');
        map.set('admin',123);  //不是put
		map.delete('tom');
        console.log(name);
```

set，无需不重复，传入一位数组

```js
		var set = new Set([1,4,6,8]);
        set.add(2);     //添加
        set.delete(4);  // 删除
        console.log(set.has(3));    // 是否有某个元素
```

### 遍历

1、for of

```js
		for(let element of set){	//map也一样的
            console.log(element);
        }
```





## <font color="red">函数(属于对象类型)</font>

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

### 返回结果

一旦执行到 return代表函数结束，返回结果！

如果没有执行 return，函数执行完也会返回结果，结果就是 **undefined**



### 不支持重载

在Java中函数允许重载。但是在JS中函数的重载会直接覆盖掉上一次的定义



### 隐形参数

就是在function函数中不需要定义，但却可以直接用来获取所有参数的变量。我们管它叫隐形参数。类似java中的可变长参数（Object ... args）。可以通过**arguments去操作**传入的参数列表。

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

如果传入的空参数，我们可以进行限制

```js
var abs = function(x){
    if(typeof x !== 'number'){	// typeof返回的是字符串才比较 !== 只比较同类型的
        throw 'Not a number';
    }
    if(x>=0){
        return x;
    }else{
        return -x;
    }
}
```

ES6引入的新特性，获取除了已经定义的参数之外的所有参数,通过...rest，rest参数只能写在最后面，必须用…表示

```js
 function aaa(a,b,...rest){
     console.log(rest);	//获得除a，b以外的所有参数
 }
```

### 改变指向

一个方法不使用任何对象调用的话，执行xxx方法是默认window.xxx(..)进行执行的，而通过apply可以改变指向和传入参数

```js
		function getAge(){
            let now = new Date().getFullYear();
            return now - this.birth;
        }
        
        var zhangsan = {
            birth: 1999,
            age: getAge
        };
        
        getAge.apply(zhangsan,[]);  // this指向zhangsan，参数为空
```



### 闭包

当一个嵌套的内部（子）函数引用了就的外部（父）函数的变量（时就产生了闭包

```js
function f1() {
            var a = 2;
            var b = 4;

            function f2() {
                console.log(a);
            }
        }

f1();
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



### {}花括号形式的自定义对象（属性名:值）

属性名:值,  多个属性之间使用逗号隔开，最后一个属性不加逗号！

var 变量名 = {        				  //空对象
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



### 注意

1、使用一个不存在的对象属性，不会报错！undefined

2、动态删减属性，通过 delete删除对象的属性

```js
delete person.name
```

3、动态添加 变量名.属性名 = 值；即可

```js
person.name = "zzzz";
```

4、判断属性值是否在这个对象中！'XXX' in xXX

```js
'toString' in person
true	//继承
```

6、判断一个属性是否是这个对象自身拥有的 hasOwnProperty("xxxx")，不包括初始继承而来的

```js
person.hasOwnProperty ('toString')
false 
person.hasOwnProperty('age'
)
true
```

### 常用类

**1、Date**

```js
var now= new Date();    //  标准时间
        now.getFullYear();      // 年
        now.getMonth();         // 0~11代表月
        now.getDate();          // 日
        now.getDay();           //星期几
        now.getHours();          //时
        now.getMinutes();         //分
        now.getSeconds();          //秒
        now.getTime();             //时间戳全世界统一19701.10：00：00毫秒数
        
        conso1e.log(new Date(1578106175991));//时间戳转为时间
```



**2、JSON**

> JSON是什么

早期，所有数据传输习惯使用XML文件！

- JSON(JavaScript Object Notation，Js对象简谱）是一种轻量级的数据交换格式。
- 简洁和清晰的**层次结构**使得JSON成为理想的数据交换语言。
- 易于人阅读和编写，同时也易于机器解析和生成，并有效地提升网络传输效率。



在 javaScript一切皆为对象、任何js支持的类型都可以用JSON来表示；

格式：

- 对象都用{}
- 数组都用
- 所有的键值对都是用key：value

```js
var user = {
            name: "zhangsan",
            age: 23,
            sex: "男"
        };
        //对象转化为json字符串
        var jsonUser = JSON.stringify(user);

        // json字符串转化为对象
        var temp = JSON.parse(jsonUser);

        console.log(temp);
```

JSON和JS对象区别

一个是字符串一个是对象，JSON属性名带双引号

```js
var obj = {a:'hello'};
var json = '{"a": 'hello'}';
```

### 通过对象原型继承

通过\__proto__进行指向

```js
	//原型对象
    var person = {
        run: function () {
            alert("人在跑");
        }
    };
    //原型对象
    var bird = {
        fly: function () {
            alert("鸟在飞");
        }
    };

    var zhangsan = {
        name: "zhangsan"
    }
    //继承原型对象
    zhangsan.__proto__ = person;
    zhangsan.run();

```

### class继承

1、定义一个类，属性，方法

```js
class Student{
        constructor(name) {
            this.name = name;
        }
        
        hello(){
            alert("hello");
        }
        
    }
    
    var zhangsan = new Student("zhangsan");
```

2、继承(和java差不多)

```js
class xiaoxuesheng extends Student{
        mygrade(){
            alert("我是一个小学生");
        }
    }
```



在 JavaScrip中，每个函数都有一个 prototype属性，这个属性指向函数的原型对象![image-20200525221144671](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200525221144671.png)

## <font color="red">BOM对象(重点)</font>

**1、window（重要）** 

代表 浏览器窗口

```js
window.innerHeight
657
window.innerWidth
766
```

**2、navigator** 

封装了浏览器的信息，大多数不会使用，因为会被人为修改！

不建议使用这些属性来判断和编写代码

```js
navigator.appCodeName
"Mozilla"
navigator.appVersion
"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
navigator.userAgent
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
```

**3、screen**

表示屏幕信息

```js
screen.height
864
screen.width
1536
```

**4、location（重要）**

代表当前页面的url信息

```js
host:"www.baidu.com"
href:"https://www.baidu.com"
protocol:"https:"
reload：f reload() //刷新网页
//设置新的地址
location.assign('https://deepi.sogou.com/')
```

**5、document（重要）**

document代表当前的页面，HTML DOM文档树，后面的DOM模型的实现

cookie是不安全的，可能会被劫持

```js
document.cookie
"Hm_lvt_d214947968792b839fd669a4decaaffc=1590330936; Hm_lpvt_d214947968792b839fd669a4decaaffc=1590331003"
```

6、history

代表浏览器的历史记录

```js
history.back()//后退
history.forward()//前进
```



## <font color="red">DOM树模型（重点）</font>

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

### Dom对象中的方法（类似css选择器）

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

如果id属性和name属性都没有最后再按标签名查 getElementsByTagName

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

获取节点之后就可以进行增删改

- 方法：

  增：

  1、appendChild（oChildNode）

  可以添加一个子节点，oChildNode是要添加的孩子节点

  改：

  1、setAttribute(属性名,属性值)

  ```js
  js.setAttribute('type','text/javascript');
  ```

  删：

  1、removeChild(oChildNode)

  删除一个子节点，如果想删除当前节点，找到父类再执行该方法即可

  

- 属性（赋值的方式修改）
  - childNodes属性，获取当前节点的所有子节点
  
  - firstChild 属性，获取当前节点的第一个子节点
  
  - lastChild属性，获取当前节点的最后一个子节点
  
  - parentNode属性，获取当前节点的父节点
  
  - nextSibling属性，获取当前节点的下一个节点
  
  - previousSibling属性，获取当前节点的上一个节点
  
  - className用于获取或设置标签的class属性值
  
  - <mark>style</mark> 获取和修改样式
  
  - <mark>innerHTML</mark>属性，表示**获取/设置**起始标签和结束标签中的**内容**（包括包含的标签）
  
  - <mark>innerText</mark>属性，表示**获取/设置**起始标签和结束标签中的文本（**仅文本**）
  
    

## js中的事件（重点）

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

## 