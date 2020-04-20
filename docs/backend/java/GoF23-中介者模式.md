## 中介模式

与代理和外观模式不相同，既不是只代理并保留源对象的某些功能，也不是完全封装

场景（中介大家熟悉吗？房产中介？）：
-假如没有总经理。下面三个部门：财务部、市场部、研发部。财务部要发工资，让大家核对公司需要跟市场部和研发部都通气；市场部要接个新项目，需要研发部处理技术、需要财务部出资金。市场部跟各个部门打交道。虽然只有三个部门，但是关系非常乱。
<img src="./pictures/Annotation 2019-12-08 193110.png"  div align=center />


实际上，公司都有总经理。各个部门有什么事情都通报到总经理这里，总经理再通知各个相关部门。

这就是一个典型的“中介者模式"，总经理起到一个中介、协调的作用
<img src="./pictures/Annotation 2019-12-08 193023.png"  div align=center />

如果一个系统中对象之间的联系呈现为网状结构，对象之间存在大量多对多关系，将导致关系及其复杂，这些对象称为“**同事对象**”我们可以引入一个**中介者对象**，使各个同事对象只跟中介者对象打交道，将复杂的网络结构化解为如下的星形结构。
<img src="./pictures/Annotation 2019-12-08 193841.png"  div align=center />

```java
public class Test {
    public static void main(String[] args) {
        Mediator president = new President();
        Department development = new Development(president);
        Department financial = new Financial(president);

        development.selfAction();
        development.outAction();

    }
}


interface Mediator{
    //中介持有同事信息,根据名字，丢入部门信息对象
    void register(String dname,Department d);
    //中介间接执行的操作
    void command(String dname);
}

interface Department{
    //做本部门的事情
    void selfAction();
    //向总经理发出申请
    void outAction();
}

class Development implements Department{
    Mediator m;

    public Development(Mediator m) {
        this.m = m;
        m.register("development", this);
    }
    @Override
    public void selfAction() {
        System.out.println("专心科研");
    }
    @Override
    public void outAction() {
        System.out.println("研发经费不够，申请经费");
        m.command("financial");
    }
}

class Financial implements Department{
    Mediator m;

    public Financial(Mediator m) {
        this.m = m;
        m.register("financial", this);
    }
    @Override
    public void selfAction() {
        System.out.println("下发经费....");
    }
    @Override
    public void outAction() {
        System.out.println("请各部门统计经费需求");
        m.command("development");
    }
}

class President implements Mediator{
    Map<String, Department> map = new HashMap<>();
    @Override
    public void register(String dname, Department d) {
        map.put(dname, d);
    }

    @Override
    public void command(String dname) {
        map.get(dname).selfAction();
    }
}
```
简单的说，每个部门都持有一个共同的中介，通过中介间接调用各部门之间的交互方法

中介者模式的本质：
-解耦多同事对象之间的交互关系。每个对象都持有中介者对象的引用，只跟中介者对象打交道。我们通过中介者对象统一管理这些交互关系
开发中常见的场景：
-MVC模式（其中的C，控制器就是一个中介者对象。M和V都和他打交道）
-窗口游戏程序，窗口软件开发中窗口对象也是一个中介者对象
-图形界面开发GUI中，多个组件之间的交互，可以通过引入一个中介者对象来解决，可以是整体的窗口对象或者DOM对象
-Java.lang.reflect.Method#invoke()