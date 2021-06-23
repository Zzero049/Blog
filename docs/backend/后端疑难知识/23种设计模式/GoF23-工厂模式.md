## 工厂模式
实现了创建者和调用者的分离。
实例化对象，用工厂方法代替new操作。
将选择实现类、创建对象统一管理和控制。从而将调用者跟我们的实现类解耦。

应用场景
1. JDK中Calendar的getinstance方法
1. JDBC中Connection对象的获取
1. Hibernate中SessionFactory创建Session
1. spring中IOC容器创建管理bean对象
1. XML解析时的DocumentBuilderFactory创建解析器对象
1. 反射中Class对象的newlInstance0

详细分类：
* 简单工厂模式（静态工厂）：用来生产同一等级结构中的任意产品。（对于增加新的产品，需要修改已有代码）
特点：虽然某种程度不符合设计原则，但实际使用最多。

* 工厂方法模式：用来生产同一等级结构中的固定产品。（支持增加任意产品）
特点：不修改已有类的前提下，通过增加新的工厂类实现扩展。

* 抽象工厂模式：用来生产不同产品族的全部产品。（对于增加新的产品，无能为力；支持增加产品族）
特点：不可以增加产品，可以增加产品族！

面向对象设计的基本原则：
* OCP（开闭原则，Open-Closed Principle）：一个软件的实体应当对扩展开放，对修改关闭。
* DIP（依赖倒转原则，Dependence Inversion Principle）：要针对接口编程，不要针对实现编程。
* LoD（迪米特法则，Law of Demeter）：只与你直接的朋友通信，而避免和陌生人通信。

### 简单工厂
简单工厂模式也叫静态工厂模式，就是工厂类一般是使用静态方法，通过接收的参数的不同来返回不同的对象实例。

对于增加新产品无能为力！不修改代码的话，是无法扩展的。

在没有工厂模式之前，面向接口调用方法
```java
public class EasyFactory {
    public static void main(String[] args) {
        car c1 = new Benz();
        car c2 = new Audi();
        c1.run();
        c2.run();
    }
}

interface car{
    public void run();
}

class Audi implements car{
    @Override
    public void run() {
        System.out.println("奥迪跑起来");
    }
}

class Benz implements car{
    @Override
    public void run() {
        System.out.println("奔驰跑起来");
    }
}
```
显然当车品牌多起来，主函数的依赖使得代码看上去复杂繁琐，如果使用工厂模式思想把这些依赖关系简单封装起来如下(方便调用和阅读)：
```java
class Factory01{
    //或者对每种车写一种创建方法，如createAudi()、createBC()
    public static car createCar(String type){
        if("奥迪".equals(type)){
            return new Audi();
        }else if("奔驰".equals(type)){
            return new Benz();
        }else{
            return null;
        }
    }
}

public class EasyFactory {
    public static void main(String[] args) {
        car c1 = Factory01.createCar("奥迪");
        car c2 = Factory01.createCar("奔驰");
        c1.run();
        c2.run();
    }
}
```



### 工厂方法模式
简单工厂一个工厂可以生产多个产品，而工厂方法则是通过新建工厂来实现产出固定的产品。

```java
class BenzFactory implements carFactory{
    @Override
    public car createCar() {
        return new Benz();
    }
}

class AudiFactory implements carFactory{
    @Override
    public car createCar() {
        return new Audi();
    }
}
public class EasyFactory {
    public static void main(String[] args) {
        car c1 = new BenzFactory().createCar();
        car c2 = new AudiFactory().createCar();
        c1.run();
        c2.run();
    }
}

```

简单工厂模式和工厂方法模式PK：
* 结构复杂度
从这个角度比较，显然简单工厂模式要占优。简单工厂模式只需一个工厂类，而工厂方法模式的工厂类随着产品类个数增加而增加，这无疑会使类的个数越来越多，从而增加了结构的复杂程度。

* 代码复杂度
代码复杂度和结构复杂度是一对矛盾，既然简单工厂模式在结构方面相对简洁，那么它在代码方面肯定是比工厂方法模式复杂的了。简单工厂模式的工厂类随着产品类的增加需要墙加很多方法（或代码），而工厂方法模式每个具体工厂类只完成单一任务，代码简洁。

* 客户端编程难度
工厂方法模式虽然在工厂类结构中引入了接口从而满足了OCP，但是在客户端编码中需要对工厂类进行实例化，而简单工厂模式的工厂类是个静态类，在客户端无需实例化，这无凝是个吸引人的优点。

* 管理上的难度
我们先谈扩展，众所周知，工厂方法模式完全满足OCP，即它有非常良好的扩展性，那是否就说明了简单工厂模式就没有扩属性呢？答案是否定的，简单工厂模式同样具备良好的扩属性——扩展的时候仅需要修改少量的代码（修改工厂类的代码）就可以满足扩展性的要求了。尽管这没有完全满足OCP，但我们不需要太拘泥于设计理论，要知道，sun提供的java官方工具包中也有想到多没有满足OCP的例子啊，然后我们从维护性的角度分析下，假如某个具体产品类需要进行一定的修改，很可能需要修改对应的工厂类，当同时希要%改多个产品然的时候，对工厂然的修改会变得相当麻烦（对号入座已经是个问题了），反而简单工厂没有这？麻烦，当多个产品类需要修改是，简单工厂模式仍然仅仅需要修改唯一的工厂类（无论怎样都能改到满足要求吧？大不了把这个类重写）。

根据设计理论建议：工厂方法模式。但实际上，我们一般都用简单工厂模式。

### 抽象工厂模式
用来生产不同产品族的全部产品。（对于增加新的产品，无能为力；支持增加产品族）
抽象工厂模式像是工厂方法模式的升级版本（就根据不同产品，新增接口和工厂方法即可），在有多个业务品种、业务分类时，通过抽象工厂模式产生需要的对象是一种非常好的解决方式。

<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-07 210455.png"  div align=center />
