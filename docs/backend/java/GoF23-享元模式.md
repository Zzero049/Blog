## 享元模式
场景：
内存属于稀缺资源，不要随便浪费。如果有很多个完全相同或相似的对象，我们可以通过享元模式，节省内存。

核心：
享元模式以共享的方式高效地支持大量细粒度对象的重用。-享元对象能做到共享的关键是区分了内部状态和外部状态。
* 内部状态：可以共享，不会随环境变化而改变
* 外部状态：不可以共享，会随环境变化而改变
<img src="./pictures/Annotation 2019-12-08 164229.png"  div align=center />

享元模式实现：
* FlyweightFactory享元工厂类
创建并管理享元对象，享元池一般设计成键值对
* FlyWeight 抽象享元类
通常是一个接口或抽象类，声明公共方法，这些方法可以向外界提供对象的内部状态，设置外部状态。
* ConcreteFlyWeight 具体享元类
为内部状态提供成员变量进行存储
* UnsharedConcreteFlyWeight非共享享元类
不能被共享的子类可以设计为非共享享元类

简单的说，就是将内部状态和外部状态分离，外部状态专门有一个自己类，而内部状态通过享员工厂（Map）管理只保证一种内部状态有一个对象即可。

```java
public class Test {
    public static void main(String[] args) {
        ChessFlyWeight chess1 = ChessFlyWeightFactory.getChess("黑色");
        ChessFlyWeight chess2 = ChessFlyWeightFactory.getChess("黑色");
        System.out.println(chess1);
        System.out.println(chess2);

        System.out.println("增加外部状态的处理----------");
        chess1.display(new Coordinate(10, 10));
        chess2.display(new Coordinate(20, 20));
    }
}

/**
 * 抽象享元类
 */
interface ChessFlyWeight{
    void getColor();
    void display(Coordinate c);
}

/**
 * 棋子外部状态UnsharedConcreteFlyWeight
 */

class Coordinate{
    private int x, y;

    public Coordinate(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public void setX(int x) {
        this.x = x;
    }

    public void setY(int y) {
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }
}

/**
 * 具体享元类
*/

class ConcreteFlyWeight implements ChessFlyWeight{
    private String color;

    public ConcreteFlyWeight(String color) {
        this.color = color;
    }

    @Override
    public void getColor() {

    }

    @Override
    public void display(Coordinate c) {
        System.out.println("棋子颜色："+color);
        System.out.println("棋子位置"+c.getX()+"-----"+c.getY());
    }
}

/**
 * 享元工厂类
 * */
class ChessFlyWeightFactory{
    private static Map<String ,ChessFlyWeight> map = new HashMap<>();

    public static ChessFlyWeight getChess(String color){
        if(map.get(color)!=null){
            return map.get(color);
        }else{
            ChessFlyWeight cfw = new ConcreteFlyWeight(color);
            map.put(color, cfw);
            return cfw;
        }
    }
}
```

享元模式开发中应用的场景：
-享元模式由于其共享的特性，可以在任何“池”中操作，比如：线程池数据库连接池。
-String类的设计也是享元模式

优点
* 极大减少内存中对象的数量
* 相同或相似对象内存中只存一份，极大的节约资源，提高系统性能
* 外部状态相对独立，不影响内部状态

缺点
* 模式较复杂，使程序逻辑复杂化
* 为了节省内存，共享了内部状态，分离出外部状态，而读取外部状态使运行时间变长。用时间换取了空间。