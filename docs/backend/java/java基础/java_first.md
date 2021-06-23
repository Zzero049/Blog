# java入门篇
-- -
## 简述
>java是类c语言发展的产物，纯粹的**面向对象**的语言，舍弃了c语言中容易引起错误的*指针*（以引用替代）、*运算符重载*、*多重继承*等特性，增加了垃圾回收器功能、泛型编程、类型安全的枚举、不定长参数和自动装/拆箱

## java技术体系平台
* **Java se（Java Standard Edition）标准版**
支持面向桌面级应用（如windows下的应用程序），提供完整的java核心API
* **Java ee（Java Enterprise Edition）企业版**
为开发企业环境下的应用程序提供的一套解决方案，包含：Servlet、Jsp等，主要针对Web应用开发
* **Java me（Java Micro Edition）小型版**
支持java运行坐在移动终端的平台，精简Api
* **Java card**
支持一些java小程序运行在小内存设备的凭条

## Java语言的特点   
* **面向对象**
    * 概念：类、对象
    * 特性：继承、封装、多态 
* **健壮性 完整性**
        吸收了C/C++的优点，去除了影响健壮性的部分（指针、内存的申请和释放等），提供一个相对安全的内存访问机制
* **跨平台 jvm**
    * 跨平台性：不同的操作系统通过安装不同的java虚拟机（JVM Java Virtual Machine），由JVM负责java程序在系统的运行
### java核心机制
* java虚拟机（JVM）
* 垃圾回收机制（GC）

### JDK与JRE
* JDK(Java Development Kit   &emsp;Java开发工具包)
    * 包含开发工具（能编译打包java文件）
* JRE（Java Runtime Environment  &emsp;Java运行环境）
    * 能运行java文件
* 包含关系
&emsp;&emsp;**JVM《JRE《JDK**
### java hello world
```java
package com.company;
public class Main{
    public static void main(String[] args){
        System.out.print("Hello World")
    }
}

```
### hello world小结
* java源文件以.java为扩展名。源文件的基本组成部分是类(class)
* Java应用入口是main()方法。有固定的书写格式：public static void main(String[] args){}
* 严格区分大小写，以;结束，括号成对存在

### 注释
* 文档注释 
```java

            /**文档注释
            *
            *@author:
            *@version:
            */
```
* 单行注释 //
* 多行注释 /* */

### Scanner获取输入
https://blog.csdn.net/u013568373/article/details/92803182