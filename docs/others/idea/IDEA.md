# IDEA


## 设置

- 快捷键设置：file-->settings-->Keymap
- 字符集设置：file-->settings-->Editor-->File Encodings
- 插件：file-->settings-->Plugins
- 设置JVM运行参数 Help-->Edit Customer VM options 或者(用户目录/.IntelliJIdea2019.2/config/idea64.vmoptions)，编辑安装目录下的idea.vmoptions和idea64.vmoptions好像没什么卵用
- 设置鼠标悬浮提示
File–>settings–>Editor–>General–>勾选Show quick documentation…

- 显示方法分隔符
File–>settings–>Editor-> general–>Appearance–>勾选 show method separators

- 忽略大小写提示
idea的默认设置是严格区分大小写提示的，例如输入string不会提示String，不方便编码
File–>settings–>Editor–>General -->Code Completion --> 勾掉 Match case

- 自动导包，自动优化导包
File–>settings–>Editor–>general–>Auto Import–>将已下两个勾选
Add unambiguous imports on the fly：快速添加明确的导入。
Optimize imports on the fly：快速优化导入，优化的意思即自动帮助删除无用的导入。

- Intellij idea用快捷键自动生成序列化id
类继承了Serializable接口之后，鼠标放在类上就能生成serialVersionUID
进入setting→inspections→serialization issues→勾选serializable class without ‘serialVersionUID’
鼠标方法在继承了序列化接口的类上，就能看见了

- IDEA统一编辑文件编码
全局编码设置
File -> Other Settings -> Default Settings
file->setting->editor->file encodings
把transparent native-to-ascll conversion勾选上就行了。当idea中properties配置文件中文显示utf8编码乱码
## 插件

- `Alibaba java Coding Guidelines` 阿里巴巴java开发规格  帮助我们提高编码规范
- `Free Mybatis plugin` 帮助我们跳转mapper.xml文件和mapper类
- `Grep Console`  设置log的等级颜色  使日志更加显眼
- `Maven Helper` Mavne插件 可以右键 run maven
- `Translation` 翻译插件

## 问题解决

`maven`创建`web`项目`web.xml`版本问题解决，参考连接：[（亲测解决）Idea创建Maven Web工程的web.xml版本问题解决](https://blog.csdn.net/sinat_34104446/article/details/82895337 "Idea创建Maven Web工程的web.xml版本问题解决")

新建`maven`项目显示为灰色，右键没有`maven`菜单，点击File-->settings 搜索`maven`，选中 <mark>Ignored Files</mark>，取消对应的复选框

`Maven Helper` 删除不用的`goal`，找到 用户目录(/home/cloudlandboy)/.IntelliJIdea2019.2/config/options/mavenRunHelper.xml，删掉不要的goal标签，重启idea

## idea 快捷键

- ==Ctrl+Alt+左==：回到上次光标所在处
- ==Ctrl+F3==：向下搜索相同单词
- ==Shift+F3==：向上搜索相同单词
- ==Ctrl+n==：搜索java类名
- ==Ctrl+Shift+N==：搜索文件名
- ==Ctrl+Shift+F==：全局搜索文件内容
- ==ctrl+D== 复制一行到下一行
- ==ctrl+C ctrl+v ctrl+x==
- ==ctrl+alt+L== 美化代码
- ==ctrl+alt+o== 优化导包
- ==CTRL + SHIFT + ENTER== 快速补全分号 

- 建议修改的KeyMap 
    (find in path) 常用 本人修改 alt+f
    (generate) 常用 本人修改 alt+e

- shift+alt+ctrl 加鼠标多行操作

- 分屏操作



