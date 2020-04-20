## 建造者模式
分离了对象子组件的单独构造（由Builder来负责）和装配（由Director负责）。从而可以构造出复杂的对象。这个模式适用于：某个对象的构建过程复杂的情况下使用。
由于实现了构建和装配的解耦。不同的构建器，相同的装配，也可以做出不同的对象；相同的构建器，不同的装配顺序也可以做出不同的对象。也就是实现了构建算法、装配算法的解耦，实现了更好的复用。

开发中应用场景：
1. StringBuilder类的append方法
2. SQL中的PreparedStatement
3. JDOM中，DomBuilder、SAXBuilder

## 原型模式prototype
原型模式：
通过new产生一个对象需要非常繁琐的数据准或问权限则可以使用原型模式。

就是java中的克隆技术，以某个对象为原型，复制出新对象。显然，新的对象具备原型对象的特点优势有：**效率高**（直接克隆，避免了重新执行构造过程步骤）。

克隆类似于new，但是不同于new。new创建新的对象属性采用的是默认值。**克隆出的对象的属性值完全和原型对象相同**。并且克隆出的新对家改变会影响原型对象。然后，再修改克隆对象的值。

原型模式实现：
* Cloneable接口和clone方法
* Prototype模式中实现起来最困难的地方就是内存复制操作，所幸在Java中提供了clone()方法替我们做了绝大部分事情。

```java
public class Sheep implements Cloneable {
    private String name;
    private Date birthday;
    public Sheep(){}

    public Sheep(String name, Date birthday) {
        this.name = name;
        this.birthday = birthday;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setBirthday(Date birthday) {
        this.birthday = birthday;
    }

    public String getName() {
        return name;
    }

    public Date getBirthday() {
        return birthday;
    }

    @Override
    protected Object clone() throws CloneNotSupportedException {
        Object obj = super.clone();
        return obj;
    }
    public static void main(String[] args) throws CloneNotSupportedException {
        date = new new Date(1545454545545L);
        Sheep s1 = new Sheep("duoli",date);
        System.out.println(s1);
        Sheep s2 = (Sheep) s1.clone();
        System.out.println(s2);

        System.out.println(s1.getName());
        System.out.println(s1.getBirthday());
        System.out.println("############################################");
        System.out.println(s2.getName());
        System.out.println(s2.getBirthday());
    }
}
```
注意，s1，s2的属性birthday指向的是同一个对象date，如果不通过创建新Date对象，只通过s1修改birthday（clone之后）,s1,s2会同时改变。将属性一起克隆即可。
<img src="./pictures/Annotation 2019-12-07 222537.png"  div align=center />

```java
@Override
    protected Object clone() throws CloneNotSupportedException {
        Object obj = super.clone();

        Sheep s  =(Sheep) obj;
        s.birthday = (Date) this.birthday.clone();
        return s;
    }

```
原型模式很少单独出现，一般是和工厂方法模式一起出现，通i过clone的方法创建一个对象，然后由工厂方法提供给调用者。
* spring中bean的创建实际就是两种：单例模式和原型模式。（当然，原型模式需要和工厂模式搭配起来）