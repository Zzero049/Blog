## 装饰器模式(decorator)
职责：
-动态的为一个对象增加新的功能。
-装饰模式是一种用于代替继承的技术，无须通过继承增加子类就能扩展对象的新功能。**使用对象的关联关系代替继承关系**，更加灵活，**同时避免类型体系的快速膨胀。**

实现细节：
* Component抽象构件角色：
·真实对象和装饰对象有相同的接口。这样，客户端对象就能够以与真实对象相同的方式同装饰对象交互。
* ConcreteComponent 具体构件角色（真实对象）：
·io流中的FilelnputStream、FileOutputStream
* Decorator装饰角色：
·持有一个抽象构件的引用。装饰对象接受所有客户端的请求，并把这些请求转发给真实的对象
。这样，就能在真实对象调用前后增加新的功能。
* ConcreteDecorator具体装饰角色：
·负责给构件对象增加新的责任。

组合的方式！
```java
public class Test {
    public static void main(String[] args) {
        Car  car = new Car();
        car.move();
        System.out.println("##############################");
        //增加新的功能
        FlyCar flyCar = new FlyCar(car);
        flyCar.move();
        System.out.println("##############################");
        WaterCar waterCar =new WaterCar(flyCar);
        waterCar.move();
    }
}


interface ICar{
    void move();
}

class Car implements ICar{

    @Override
    public void move() {
        System.out.println("汽车可以发动！");
    }
}

class SuperCar implements ICar{
    private  ICar car;

    public SuperCar(ICar car) {
        this.car = car;
    }

    @Override
    public void move() {
        car.move();
    }
}

class FlyCar extends SuperCar{

    public FlyCar(ICar car) {
        super(car);
    }

    public void fly(){
        System.out.println("天上飞");
    }
    @Override
    public void move(){
        super.move();
        fly();
    }
}

class WaterCar extends SuperCar{

    public WaterCar(ICar car) {
        super(car);
    }

    public void fly(){
        System.out.println("水上漂");
    }
    @Override
    public void move(){
        super.move();
        fly();
    }
}
```
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-08 161016.png"  div align=center />

开发中使用的场景：
* IO中输入流和输出流的设计
* Swing包中图形界面构件功能
* Servlet API 中提供了一个request对象的Decorator设计模式的默认实现类HttpServletRequestWrapper，HttpServletRequestWrapper类，增强了request对象的功能。
* Struts2中，request，response，session对象的处理