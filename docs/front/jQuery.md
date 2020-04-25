# jQuery

​	Query，顾名思义，也就是JavaScript和查询（Query），它就是辅助JavaScript开发的js类库。它的核心思想是write less，do more（写得更少，做得更多），所以它实现了很多浏览器的兼容问题。jQuery 现在已经成为最流行的JavaScript库，在世界前10000个访问最多的网站中，有超过55%在使用jQuery。

​	jQuery是免费、开源的，jQuery的语法设计可以使开发更加便捷，例如操作文档对象、选择DOM元素、制作动画效果、事件处理、使用Aiax以及其他功能。



简单的入门案例：

jQuery中$是一个函数

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <!--引入库-->
    <script type="text/javascript" src="../script/jquery-3.5.0.min.js"></script>
    <script type="text/javascript">
        $(function () { //表示页面加载完成之后，相当于window.onLoad = function(){}事件
            var $btnObj = $("#btnID"); //表示按id查询标签对象,习惯jQuery对象用$开头
            $btnObj.click(function () {
                alert("jQuery的单击事件");
            });
        });
    </script>
</head>
<body>
    <button id="btnID">SayHello</button>
</body>
</html>
```



## jQuery的核心函数

$是jQuery的核心函数，能完成jQuery的很多功能。$()就是调用$这个函数

1、传入参数为[函数]时：
		表示页面加载完成之后。相当于window.onload=function(){}

2、传入参数为[HTML字符串]时：
		会对我们创建这个html标签对象

3、传入参数为[选择器字符串]时：
		$(“#id属性值”);              id 选择器，根据id查询标签对象

​		$(“标签名”);                 标签名选择器，根据指定的标签名查询标签对象

​		$(“.class属性值”);              类型选择器，可以根据class属性查询标签对象

4、传入参数为[DOM对象]时：
		会把这个dom 对象转换片jQuery对象

## Dom与jQuery

jQuery 对象是dom对象的数组+JQuery提供的一系列功能函数。

Dom对象

- 通过getElementByldl）查询出来的标签对象是Dom对象

- 通过getElementsByName（）查询出来的标签对象是Dom对象

- 通过getElementsByTagName（）查询出来的标签对象是Dom对象

- 通过createElement()方法创建的对象，是Dom对象DOM

  ​    	对象Alert出来的效果是：[object HTML标签名ELement]

jQuery对象

- 通过JQuery提供的APl创建的对象，是JQuery对象

- 通过JQuery包装的Dom对象，也是JQuery对象

- 通过JQuery 提供的API查询到的对象，是JQuery对象

   		jQuery对象Alert出来的效果是：[object object]

  

jQuery 对象不能使用DOM对象的属性和方法
DOM对象也不能使用jQuery对象的属性和方法

### Dom对象和jQuery对象互转

1、dom对象转化为jQuery对象
		1、先有DOM对象
		2、$(DOM对象) 就可以转换成为jQuery对象

2、jQuery对象转为dom对象
		1、先有jQuery对象
		2、jQuery对象[下标]  取出相应的DOM对象

![image-20200421120017707](F:\Project\cscode\markdown\java\javaWeb\前端\pictures\image-20200421120017707.png)



## 页面加载

$function(){}和window.onload=function(){}区别：

**触发顺序：**

1、jQuery页面加载完成之后先执行
2、原生js的页面加载完成jQuery执行之后执行

原因：

1、jQuery的页面加载完成之后是浏览器的内核解析完页面的标签创建好DOM对象之后就会马上执行。
2、原生s的页面加载完成之后，除了要等浏览器内核解析完标签创建好DOM对象，还要等标签显示时需要的内容加载完成。

**执行次数：**

1、原生js的页面加载完成之后，只会执行最后一次的赋值函数。
2、jQuery的页面加载完成之后是全部把注册的function函数，依次顺序全部执行。



## jQuery选择器

### 基础选择器

#ID                                       选择器：根据id查找标签对象
.class								   选择器：根据class查找标签对象
element                              选择器：根据标签名查找标签对象选择器：表示任意的，所有的元素
selector1，selector2        组合选择器：合并选择器1，选择器2的结果并返回

### 层级选择器

- 空格  在给定的祖先元素下匹配所有的后代元素

```html
<!--找到表单中所有的input元素-->
$("form input")
```

- \>      在给定的父元素下匹配所有的子元素(直接子元素)

```html
<!--找到表单直接子标签为input元素-->
$("form > input")
```

- \+     匹配所有紧接在prev元素后的next元素

```html
<!--匹配所有跟在 label 后面的input元素-->
$("form + input")
```

- \~    匹配prev元素之后的所有siblings元素

```html
<!--找到所有与表单同辈的input元素-->
$("form + input")
```

### 过滤选择器

#### 基础过滤选择器

通过冒号进行过滤

如：

```html
$("form:first")
```

想要具体了解有多少类型建议查看手册

#### 内容过滤选择器

:contains(text)		匹配包含给定文本的元素

:empty					 匹配所有不包含子元素或者文本的空元素

:parent					匹配含有子元素或有文本的元素

:has(selector)	     匹配含有选择器所匹配的元素的元

```html
<!--给所有包含p元素的div 元素添加一个text类-->
$("div:has(p).addClass("text")")
```

#### 属性过滤选择器

通过[]进行限定

```html
<!--查找所有含有id属性的div 元素-->
$("div[id]")
<!--查找所有含有id属性并为1的div 元素-->
$("div[id="1"]")
<!--查找所有含有id属性不为1的div 元素-->
$("div[id!="1"]")
<!--查找所有含有id属性以1开头的div 元素-->
$("div[id ^= "1"]")
<!--查找所有含有id属性以1结尾的div 元素-->
$("div[id $= "1"]")

<!--复合属性选择器，需要同时满足多个条件时使用。-->
<!--找到所有含有id属性，并且它的name属性是以man结尾的-->
$("body[id][name$="man"]")
```

#### 表单过滤器

form表单下的所有type都有过滤器通过":type值"的方式取到，如:

```html
$(":input")
```

还有可用(enable)、不可用(disable)、单选、多选的选中如

```html
$("select option:selected")
```

### 遍历

```js
$("btn4").click(function () {
            //获欧全部选中的复选框标签对象
            var $checkboxs = $(":checkbox:checked");
            // 老式遍历
            // for(var i=0;i<$checkboxs.length;i++){
            //     alert(checkboxs[i].value);
            // }
            $checkboxs.each(function () {
                alert(this.value);
            })
        })
```

## jQuery元素筛选

跟选择器差不多，只不过用jQuery对象.属性的形式去取

![image-20200421155250164](F:\Project\cscode\markdown\java\javaWeb\前端\pictures\image-20200421155250164.png)

![image-20200421155355488](F:\Project\cscode\markdown\java\javaWeb\前端\pictures\image-20200421155355488.png)

如

```js
//取索引为1的div元素
$("div").eq(1)
```

## jQuery属性

html()     它可以设置和获取起始标签和结束标签中的内容。  跟dom属性innerHTML一样。
text()      它可以设置和获取起始标签和结束标签中的文本。   跟dom属性innerText一样。
val()          它可以设置和获取表单项的value属性值。                跟dom 属性value一样。

attr（）可以设置和获取属性的值（属性不存在返回undefined），不推荐操作checked、readonly、selected、disabled等等
prop（）可以设置和获取属性的值（属性不存在返回false），只推荐操作checked、readonly、selected、disabled等等

html()、text()、val()不传参数为获取，传参数为赋值

## Dom增删改

  ### 内部插入

a.appendTo(b) 	把a插入到b子元素末尾，成为最后一个子元素

a.prependTo(b) 	把a插到b所有子元素前面，成为第一个子元素

### 外部插入

a.insertAfter(b) 			得到ba

a.insertBefore(a)		  得到ab

### 替换

a.replaceWith(b)		用b替换掉a

a.replaceAll(b）		   用a替换掉所有b

### 删除

a.remove();				删除a标签

a.empty();		清空a标签内的内容

## CSS样式

addClass() 				添加样式

removeClass() 		  删除样式

toggleClass() 			有就删除，没有就添加样式。

offset()  				      获取和设置元素的坐标。

## jQery动画

基本动画

show()			将隐藏的元素显示

hide()			  将可见的元素隐藏。

toggle()		  可见就隐藏，不可见就显示。



淡入淡出动画

fadeln()							淡入

fadeOut()						淡出

fadeTo()						  在指定时长内慢慢的将透明度修改到指定的值。

fadeToggle()					淡入/淡出切换



以上动画方法都可以添加参数。

1、第一个参数是动画执行的时长，以毫秒为单位

2、第二个参数是动画的回调函数（动画完成后自动调用的函数）



## jQuery事件

和js的onXXXX方法差不多，都是可以用来绑定事件，也可以用来触发事件（定义后，不带参数 调用）

如：

```js
$(function()){
  $("h5").click(function(){
    alert("h5事件");
});

	$("button").click(function(){
        //调用h5.click方法
        $("h5").click();
    })
  }
```

click（）它可以绑定单击事件，以及触发单击事件

- mouseover（）						

  鼠标移入事件

- mouseout（）						 

  鼠标移出事件

- bind（）									

  可以给元素一次性绑定一个或多个事件。如

  ```js
  $("h5").bind("click mouseover mouseout", function(){
      console.log("这是bind绑定的事件");
  })
  ```

  

- one（）									

  使用跟bind一样一个或多个事件触发。但是one方法绑定的事件只会响应一次。

- unbind（）								

  跟bind 方法相反的操作，解除事件的绑定

- live（）					

  也是用来绑定事件，语法和bind差不多。它可以用来绑定选择器匹配的所有元素的事件。哪怕这个元素是后面动态创建出来的也有效。（如click绑定后，再创建一个绑定相同的标签，新标签不会触发事件，而用live绑定不会）

### 事件的冒泡

事件的冒泡是指，父子元素同时监听同一个事件。当触发子元素的事件的时候，同一个事件也被传递到了父元素的事件里去，父子事件都会触发。

解决办法：

在子元素事件函数体内，return false；可以阻止事件的冒泡传递。

### JavaScript事件对象

事件对象，是封装有触发的事件信息的一个javascript对象。

在给元素绑定事件的时候，在事件的function（event）参数列表中添加一个参数，这个参数名，我们习惯取名为event。这个event 就是javascript 传递参事件处理函数的事件对象。

```js
//js
window.onload = function () {
            document.getElementById("areDiv").onclick = function(event){
                console.log(event);
            }
        }

//jQuery
$(function(){
    $("areDiv").onclick = function(event){
        console.log(event);
    }
});
```

```js
$(function(){
    $("areDiv").bind("mouseover mouseout", function(event){
        if(event.type=="mouseover"){
             console.log("鼠标移入");
        }else if(event.type == "mouseout"){
            console.log("鼠标移出");
        }
    }
})； );
```

