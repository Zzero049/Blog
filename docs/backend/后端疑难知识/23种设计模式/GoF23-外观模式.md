## 外观模式
迪米特法则（最少知识原则）：
-一个软件实体应当尽可能少的与其他实体发生相互作用。
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-08 162002.png"  div align=center />
外观模式核心：
-子系统提供统一的入口）封装子系统的复杂性，便于客户端调用。

把主代码该用的方法放入一个类的方法中即可


开发中常见的场景
-频率很高。哪里都会遇到。各种技术和框架中，都有外观模式的使用。如：
·JDBC封装后的，commons提供的DBUtils类，Hibernate提供的工具类、SpringJDBC工具类等