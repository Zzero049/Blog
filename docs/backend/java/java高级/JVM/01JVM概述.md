# JVM（Java Virtual Machine）

本文当扩展知识看一下就好了，核心知识在后面

## 虚拟机

所谓虚拟机（Virtual machine），就是一台虚拟的计算机。它是一款**软件**，用来**执行一系列虚拟计算机指令**。大体上，虚拟机可以分为系统虚拟机和程序虚拟机。

- 大名鼎鼎的 VisualBox，VMware就属于系统虚拟机，它们**完全是对物理计算机的仿真**，提供了一个可运行完整操作系统的软件平台
- 程序虚拟机的典型代表就是Java虚拟机，它专门为**执行单个计算机程序而设计**，在Java虚拟机中执行的指令我们称为Java字节码指令。无论是系统虚拟机还是程序虚拟机，在上面运行的软件都被限制于虚拟机提供的资源中。

## JAVA虚拟机

- Java虚拟机是一台执行Java字节码的虚拟计算机，它拥有独立的运行机制，其运行的Java字节码也未必由Java语言编译而成。
- JVM平台的各种语言可以共享Java虚拟机带来的跨平台性、优秀的垃圾回器，以及可靠的即时编译器。
- **Java技术的核心就是Java虚拟机** JVM（Java Virtual Machine），因为所有的Java程序都运行在Java虚拟机内部

### 作用

==Java虚拟机就是**二进制字节码**的运行环境==，负责装载字节码到其内部，解释/编译为对应平台上的机器指令执行。每一条Java指令，Java虚拟机规范中都有详细定义，如怎么取操作数，怎么处理操作数，处理结果放在哪里

### 特点

- 一次编译，多次运行
- 自动内存管理
- 自动垃圾回收功能

### JVM位置

JVM是运行在操作系统之上的，它与硬件没有直接的交互

![image-20200531161530488](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200531161530488.png)



## JVM结构

**HotSpot VM**是目前市面上高性能虚拟机的代表作，它采用解释器与即时编译器并存的架构。这里讨论的都是HotSpot的实现。

![image-20200430163104536](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200430163104536.png)



## Java代码的执行流程

图示如下

![](https://gitee.com/zero049/MyNoteImages/raw/master/zhixing.png)

## JVM的架构模型

**由于跨平台性的设计，Java的指令都是根据==栈==来设计的。**不同平台CPU架构不同，所以**不能设计为基于寄存器**的。优点是**跨平台，指令集小，编译器容易实现**，缺点是性能下降，实现同样的功能需要更多的指令时至今日，尽管嵌入式平台已经不是Java程序的主流运行平台了（准确来说应该是 Hotspot的宿主环境已经不局限于嵌入式平台了）

通过反汇编 `javap -v JVMdemo1.class `,看到确实是基于栈的指令

![image-20200531165305377](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200531165305377.png)



## JVM生命周期

**虚拟机的启动**

Java虚拟机的启动是通过引导类加载器（bootstrap class loader）创建个初始类（initial class）来完成的，这个类是由虚拟机的具体实现指定的。

**虚拟机的执行**

- 一个运行中的Java虚拟机有着一个清晰的任务：执行Java程序。（也就是一个java程序对应一个JVM实例）
- 程序开始执行时他才运行，程序结束时他就停止。
- **执行一个所谓的Java程序的时候，真真正正在执行的是一个叫做Java虚拟机的进程**

**虚拟机的退出**

有如下的几种情况：

- 程序正常执行结束

- 程序在执行过程中遇到了异常或错误而异常终止
- 由于操作系统出现错误而导致Java虚拟机进程终止
- 某线程调用 **Runtime类或 System类的exit**方法，或 **Runtime类的halt**方法，并且Java安全管理器也允许这次exit或halt操作
- 除此之外，JNI（Java native interface）规范描述了用JNI Invocation API来加载或卸载Java虚拟机时，Java虚拟机的退出情况



## JVM发展历程（了解）

这里只介绍一个最早的商用虚拟机和三大虚拟机，现在HotSpot和JRockit都被Oracle收购，J9还是IBM公司的

- Sun Classic VM

  世界上第一款商用Java虚拟机，内部只提供解释器（每次逐行翻译，不会生成编译文件）

- ==**HotSpot**==

  目前 Hotspot占有绝对的市场地位，称霸武林

  不管是现在仍在广泛使用的JDK6，还是使用比例较多的JDK8中，默认的虚拟机都是Hotspot sun/Oracle JDK和 OpenJDK的默认虚拟机。因此介绍虚拟机就按HotSpot讲即可。

  从服务器、桌面到移动端、嵌入式都有应用。采用**热点代码探测**技术，在最优化的程序响应时间与最佳执行能中取得平衡。

- **JRockit**

  专注于服务器端应用，不关注程序启动速度，因此。JRockit内部**不包含解释器实现**，全靠即时编译器编译后执行。JRockit JVM是世界上**最快的JVM**。Oracle进行了收购，希望整合HotSpot和JRockit两大优秀虚拟机的工作，大致在JDK8中完成。

- **J9**

  市场定位与 Hotspot接近，服务器端、桌面应用、嵌入式等多用途VM，基本只在自家的产品用。