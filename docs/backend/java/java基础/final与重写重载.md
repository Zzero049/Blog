
### final
final关键字的作用：
1. 修饰变量：被他修饰的变量不可改变。一旦赋了初值，就不能被重新赋值。
>final int MAX_SPEED = 120；

2. 修饰方法：该方法不可被子类重写。但是可以被重载！
>final void study(){}

3. 修饰类：修饰的类不能被继承。比如：Math、String等。
>final class A{}

### 关于重写和重载
1. 重写(Override)
从字面上看，重写就是 重新写一遍的意思。其实就是在子类中把父类本身有的方法重新写一遍。子类继承了父类原有的方法，但有时子类并不想原封不动的继承父类中的某个方法，所以在方法名，参数列表，返回类型(除过子类中方法的返回值是父类中方法返回值的子类时)都相同的情况下， 对方法体进行修改或重写，这就是重写。但要注意子类函数的访问修饰权限不能少于父类的。
例如：
```java
public class Father {

    public static void main(String[] args) {
        // TODO Auto-generated method stub
        Son s = new Son();
        s.sayHello();
    }

    public void sayHello() {
        System.out.println("Hello");
    }
}

class Son extends Father{

    @Override
    public void sayHello() {
        // TODO Auto-generated method stub
        System.out.println("hello by ");
    }

}
```
#### 重写 总结：
1.发生在父类与子类之间
2.方法名，参数列表，返回类型（除过子类中方法的返回类型是父类中返回类型的子类）必须相同
3.访问修饰符的限制一定要大于被重写方法的访问修饰符（public>protected>default>private)
4.重写方法一定不能抛出新的检查异常或者比被重写方法申明更加宽泛的检查型异常

2.重载(Overload)
在一个类中，同名的方法如果有不同的参数列表（参数类型不同、参数个数不同甚至是参数顺序不同）则视为重载。同时，重载对返回类型没有要求，可以相同也可以不同，但不能通过返回类型是否相同来判断重载。
例如：
```java
public class Father {

    public static void main(String[] args) {
        // TODO Auto-generated method stub
        Father s = new Father();
        s.sayHello();
        s.sayHello("wintershii");

    }

    public void sayHello() {
        System.out.println("Hello");
    }

    public void sayHello(String name) {
        System.out.println("Hello" + " " + name);
    }
}
```
#### 重载 总结：
1.重载Overload是一个类中多态性的一种表现
2.重载要求同名方法的参数列表不同(参数类型，参数个数甚至是参数顺序)
3.重载的时候，返回值类型可以相同也可以不相同。无法以返回型别作为重载函数的区分标准

#### 重写和重载区别
方法的重载和重写都是实现多态的方式，区别在于前者实现的是编译时的多态性，而后者实现的是运行时的多态性。重载发生在一个类中，同名的方法如果有不同的参数列表（参数类型不同、参数个数不同或者二者都不同）则视为重载；重写发生在子类与父类之间，重写要求子类被重写方法与父类被重写方法有相同的参数列表，有兼容的返回类型，比父类被重写方法更好访问，不能比父类被重写方法声明更多的异常（里氏代换原则）。重载对返回类型没有特殊的要求，不能根据返回类型进行区分。

