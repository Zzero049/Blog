## 模版方法模式
模板方法模式介绍：
-模板方法模式是编程中经常用得到模式。它定义了一个操作中的算法骨架，将某些步骤延迟到子类中实现。这样，新的子类可以在不改变一个算法结构的前提下重新定义该算法的某些特定步骤。
核心：
-处理某个流程的代码已经都具备，但是其中某个节点的代码暂时不能确定。因此，我们采用工厂法模式，将这个节点的代码实现转移给子类完成。**即：处理步骤父类中定义好，具体实现延迟到子类中定义（父类定义抽象方法）**

```java
public class Method {
    public static void main(String[] args) {
        BankTemplateMethod bankTemplateMethod = new DrawMoney();
        bankTemplateMethod.process();

        //匿名内部类
        BankTemplateMethod bankTemplateMethod2 = new DrawMoney(){
            @Override
            public void transact(){
                System.out.println("我要存钱");
            }
        };
        bankTemplateMethod2.process();
    }
}

abstract class BankTemplateMethod{
    public void takeNumber(){
        System.out.println("排队取号");
    }
    //具体业务
    public abstract void transact();

    public void evaluate(){
        System.out.println("反馈评分");
    }

    public final void process(){
        this.takeNumber();
        this.transact();
        this.evaluate();
    }
}

class DrawMoney extends BankTemplateMethod{

    @Override
    public void transact() {
        System.out.println("要取钱");
    }
}
```

子类不能调用父类，而通过父类调用子类。这些调用步骤已经在父类中写好了，完全由父类控制整个过程。


什么时候用到模板方法模式：
-实现一个算法时，整体步骤很固定。但是，某些部分易变。易变部分可以抽象成出来，供子类实现。
开发中常见的场景：
-非常频繁。各个框架、类库中都有他的影子。比如常见的有：
·数据库访问的封装
·Junit单元测试
·servlet中关于doGet/doPost方法调用
·Hibernate中模板程序
·spring中JDBCTemplate、HibernateTemplate等。