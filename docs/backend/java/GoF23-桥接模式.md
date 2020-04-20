## 桥接模式
商城系统中常见的商品分类，以电脑为类，如何良好的处理商品分类销售的问题？

<img src="./pictures/Annotation 2019-12-08 145415.png"  div align=center />

**多层继承**
问题：
* 扩展性问题（类个数膨胀问题）：
·如果要增加一个新的电脑类型智能手机，则要增加各个品牌下面的类。
·如果要增加一个新的品牌，也要增加各种电脑类型的类。
* 违反单一职责原则：
·一个类：联想笔记本，有两个引起这个类变化的原因



<img src="./pictures/Annotation 2019-12-08 150137.png"  div align=center />
```java

public class Test {
    public static void main(String[] args) {
        Computer c = new Desktop(new Lenovo());
        c.sale();
    }
}


interface Brand{
    void sale();
}

class Lenovo implements Brand{

    @Override
    public void sale() {
        System.out.println("联想销售");
    }
}
class Dell implements Brand{

    @Override
    public void sale() {
        System.out.println("戴尔销售");
    }
}
class Computer{
    protected Brand brand;

    public Computer(Brand brand) {
        this.brand = brand;
    }
    public void sale(){
        brand.sale();
    }
}

class Desktop extends Computer{

    public Desktop(Brand brand) {
        super(brand);
    }
    @Override
    public void sale(){
        super.sale();
        System.out.println("销售台式机");
    }
}
```

主要是在Computer类加入了brand，不只是用继承方式控制品牌，而是用组合方式，之后添加品牌或产品只需要继承接口/父类即可。

桥接模式可以取代多层继承的方案。多层继承违背了单一职责原则，复用性较差，类的个数也非常多。桥接模式可以极大的减少子类的个数，从而降低管理和维护的成本。

桥接模式极大的提高了系统可扩展性，在两个变化维度中任意扩展一个维度，都不需要修改原有的系统，符合开闭原则。

桥接模式实际开发中应用场景
JDBC驱动程序
AWT中的Peer架构
银行日志管理：
------格式分类：操作日志、交易日志、异常日志
------距离分类：本地记录日志、异地记录日志
人力资源系统中的奖金计算模块：
------奖金分类：个人奖金、团体奖金、激励奖金。
------部门分类：人事部门、销售部门、研发部门。
OA系统中的消息处理：
------业务类型：普通消息、加急消息、特急消息
------发送消息方式：系统内消息、手机短信、邮件