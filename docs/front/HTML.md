# HTML

1. 标签的格式：
   	<标签名>封装的数据</标签名>
   
2. 标签名大小写不敏感。

3. 标签拥有自己的属性。

    i.分为基本属性：bgcolor="red”      可以修改简单的样式效果

    ii.事件属性：onclick="alert(''你好！');”    可以直接设置事件响应后的代码

    ```html
    <body >
    hello
    <button onclick="alert('heieheihei')">按钮</button>
    </body>
    ```

    

4. 标签又分为，单标签和双标签。
   i.单标签格式：<标签名/>

   ```html
   <br/>
   ```

   ii.双标签格式：<标签名>.封装的数据..…</标签名>

   ```html
   <p>   </p>
   ```

   

## 常用标签

### font

font标签是字体标签，宫可以用来修改文本的字体，颜色，大小（尺寸）

color属性修改颜色
face属性修改字体
size属性修改文本大小

```html
<font color="#a52a2a" face="宋体" size="3">hello</font>
```



### 常用的特殊字符

常用的特殊字符：

```html
<      &lt;
>      &gt;
空格    &nbsp;
```



### 标题标签

h1-h6 都是标题标金
h1最大
h6最小
	align 属性是对齐属性
			Left左对齐（默认）
			center   居中
			right      右对齐

```html
<h1 align="center">h哈啊</h1>
```



### 超链接

a标签是超链接

​	href属性设置连接的地址

​		target属性设置服个目标进行跳转
​			_self表示当前页面（默认）
​			_blank表示打开新页面来进行跳转

```html
<a href="https://www.baidu.com" target="_self">百度</a>
```



### 列表标签

ul是无序列表，ol为有序列表
	type属性可以修改无序列表项前面的符号
Li是列表项

```html
<ul type="none">
    <li>李白</li>
    <li>杜甫</li>
    <li>辛弃疾</li>
</ul>
```



### <font color="red">img标签</font>

img标签是图片标签，用来显示图片

- src属性可以设置图片的路径

- width属性设置图片的毫度
- height属性设置图片的高度
- border属性设置图片边相大小
- alt属性设置当指定路径统不到图片时，用来代答显示的文本内容

在JavaSE中路径也分为相对路径和绝对路径。
		相对路径：从工程含开始算
		绝对路径：盘符：/目录/文件名

在web中辟径分为相对路径和绝对路径两种相对路径：
			.  表示当前文件所在的目录
			.. 表示当前文件所在的上一级目录
			文件名  表示当就文件所在目录的文件，相当于./文件名  ./可以省略

绝对路径：
正确格式是：htte://ip:port/工程名/资源路径

```html
<img src="https://www.baidu.com/img/bd_logo1.png" border="1" alt="找不到">
```



### <font color="red">table表格</font>

table标签是表格标签
		border 设置表格标签
		width 设置表格宽度
		height 设置表格高度
		cellspace 设置单元格间距

tr是行标签
th是表头标签
td 是单元格标签

​		align 设置单元格文本对齐方式

​		colspan 属性设置跨列

​		rowspan 属性设置跨行

```html
<table  border="1" width="600" height="300">
    <tr>
        <th>省份</th>
        <th>市</th>
        <th>区</th>
    </tr>
    <tr>
        <td align="center">广东省</td>
        <td align="center">深圳市</td>
        <td align="center">龙岗区</td>
    </tr>
</table>
```



### iframe内联页面

ifarme标签可以在页面上开辟一个小区域显示一个单独的页面

ifarme和a标签组合使用的步骤：
	1.在iframe标签中使用name属性定义一个名称
	2.在a标签的target属性上设置iframe的name的属性值

```html
<body>

<iframe src="https://zzero049.github.io/Blog/#/" width="300" height="400" name="abc"></iframe>

<a href="https://github.com/" target="abc">测试</a>
</body>
```

![image-20200524111212226](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524111212226.png)

![image-20200524111225212](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524111225212.png)

### <font color="red">表单form</font>

form标签就是表单

- input type=text是文件输入框              
  -  value设置默认显示内容
- input type=password是密码输入框     
  -  value设置默认显示内容
- input type=radio 是单选框      
  - name属性可以对其进行分组checked="checked”表示默认选中
- input type=checkbox 是多选框 
  - checked="checked“表示默认选中
- input type=reset 是重置按钮
  - value属性修改按钮上的文本
- input type=submit 是提交按钮
  - value属性修改按钮上的文本
- input type=button 是按钮
  - value属性修改按钮上的文本
- input type=file是文件上传域
- input type=hidden 是隐藏域
  - 当我们要发送某些信息，而这些信息，不需要用户参与，就可以使用隐藏域（提交的时候同时发送给服务器）
- input type=email 是基本的邮箱验证
- input type=url 是基本的url验证
- input type=range 是滑块
- input type=serach 是搜索框
- select 标签是下拉列表框
  - option标签是下拉列表框中的选项selected="selected“设置默认选中
- textarea表示多行文本输入框（起始标签和结束标签中的内容是默认值）
  - rows属性设置可以显示几行的高度
  - cols属性设置每行可以显示几个字符宽度



```html
<form action="" method="POST">
        用户名: <input type="text"/><br/>
        用户密码: <input type="password"/><br/>
        确认密码: <input type="password"/><br/>

        性别: <input type="radio" name="sex" checked="checked"/>男<input type="radio" name="sex"/>女<br/>

        兴趣爱好：<input type="checkbox" checked="checked"/>java<input type="checkbox" />python<input type="checkbox" />c++<br/>

        国籍：<select>
        <option>---请输入国籍---</option>
        <option>---中国---</option>
        <option>---美国---</option>
    </select><br/>

        自我评价：<textarea rows="10" cols="20">我才是默认值</textarea><br/>

        <p>
            搜索：<input type="search" name="搜索">
        </p>
        滑块: <input type="range" min="10" max="100" step="2">


        <input type="reset" value="重置"/>
        <input type="submit" value="提交"/>
        <input type="button" value="一个小按钮"/>
    </form>
```

![image-20200524105709864](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524105709864.png)

可以看出相当不美观，可以结合表格进行优化

```html
<form>
    <table>
        <tr>
            <td>
                用户名:
            </td>
            <td>
                <input type="text"/><br/>
            </td>
        </tr>
        <tr>
            <td>
                用户密码:
            </td>
            <td>
                <input type="password"/><br/>
            </td>
        </tr>
        <tr>
            <td>
                确认密码:
            </td>
            <td>
                <input type="password"/><br/>
            </td>
        </tr>
        <tr>
            <td>
                性别:
            </td>
            <td>
                <input type="radio" name="sex" checked="checked"/>男<input type="radio" name="sex"/>女<br/>
            </td>
        </tr>
        <tr>
            <td>
                兴趣爱好：
            </td>
            <td>
                <input type="checkbox" checked="checked"/>java<input type="checkbox" />python<input type="checkbox" />c++<br/>
            </td>
        </tr>
        <tr>
            <td>
                国籍：
            </td>
            <td>
                <select>
                    <option>---请输入国籍---</option>
                    <option>---中国---</option>
                    <option>---美国---</option>
                </select><br/>
            </td>
        </tr>
        <tr>
            <td>
                自我评价：
            </td>
            <td>
                <textarea rows="10" cols="20">我才是默认值</textarea><br/>
            </td>
        </tr>
        <tr>
            <td>
                <input type="reset" value="重置"/>


            </td>
            <td>
                <input type="submit" value="提交"/>
            </td>
            <td>
                <input type="button" value="一个小按钮"/>
            </td>
        </tr>
    </table>
</form>
```

![image-20200420170824728](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200420171303746.png)



注意上面的标签中没有name属性，无论是POST请求还是GET请求都不会带有其中的数据

#### 表单属性限制

1. 只读，加上readonly属性

```html
<form action="" method="POST">
    用户名: <input type="text" value="张三" readonly/>
    
</form>
```

![image-20200524105857105](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524105857105.png)



2. checkbox、radio禁选，加上disabled

```html
<form action="" method="POST">
        你最喜欢:
        <input type="checkbox" value="eat" name="hobby"> 吃饭
        <input type="checkbox" value="sleep" name="hobby"> 睡觉
        <input type="checkbox" value="punch" name="hobby" disabled> 打豆豆

    </form>
```



![image-20200524110339815](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524110339815.png)

3、hidden 隐藏域 隐藏一些信息不给用户看到

```html
<form action="" method="get">
    用户名: <input type="text" name="name"/><br/>
    用户密码: <input type="password" name="password" value="zansan" hidden/><br/>
    确认密码: <input type="password" name="rePassword" value="zansan"hidden/><br/>
    <input type="submit" value="提交">
</form>
```

![image-20200524111911385](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524111911385.png)

4、 label增加鼠标可用性，点击label的文本会跳转到for指向的id

```html
<form action="" method="get">
    用户名: <input type="text" name="name" id="mark"/><br/>
    用户密码: <input type="password" name="password" /><br/>
    确认密码: <input type="password" name="rePassword" /><br/>
<!--    指向mark标记-->
    <label for="mark">指向用户名</label>
</form>
```





![image-20200524112254674](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524112254674.png)

#### 表单初级验证

1、placeholder 提示信息

```html
<form action="" method="get">
    用户名: <input type="text" name="name" placeholder="请输入用户名"/><br/>
    用户密码: <input type="password" name="password" placeholder="请输入密码"/><br/>

</form>
```



![image-20200524112627129](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524112627129.png)

2、required  非空判断

```html
<form action="" method="get">
    用户名: <input type="text" name="name" placeholder="请输入用户名" required/><br/>
    用户密码: <input type="password" name="password" placeholder="请输入密码"/><br/>
    <input type="submit" value="提交">
</form>
```

![image-20200524112754830](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524112754830.png)

3、pattern 正则表达式判断

```html
<form action="" method="get">
    邮箱： <input type="text" pattern="^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$">
    <input type="submit" value="提交">
</form>
```



![image-20200524113108764](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200524113108764.png)

4、密码隐藏

```html
<form action="#" method="post">
<p>
    <!--还需要进行操作，由于表单不含name，可以进一步结合js用md5修改-->
    <span>密码：</span><input  type="password" id="input-password">
    <input type="hidden" id="md5-password" name="password">
    <input type="submit" value="提交">
</p>
</form>
```



#### 表单提交的时候，数据没有发送给服务器的三种情况：

​	1、表单项没有**name**属性值

​	2、单选、复选（下拉列表中的option标签）没有添加**value**属性，服务器接受到的是on或off

​	3、表单项不在提交的**form**标签中（input、select、textarea）



### div、span、p标签

div标签默认独占一行

span标签它的长度是封装数据的长度

p段落标签默认会在段落的上方和下方各空出一行来（如果已有就不再空）



