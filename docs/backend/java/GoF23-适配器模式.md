## 适配器模式
什么是适配器模式？
将一个类的接口转换成客户希望的另外一个接口。Adapter模式使得原本由于接口不兼容而不能一起工作的那些类可以在一起工作。

模式中的角色
* 目标接口（Target）：用户所期待的接口。目标可以是具体的或抽象的类，也可以是接口。
* 需要适配的类（Adaptee）：需要适配的类或适配者类。
* 适配器（Adapter）：通过包装一个需要适配的对象，把原接口转换成目标接口。
```java
public class AdapterModule {

    public void test(Target target){
        target.hanlde();
    }
    public static void main(String[] args) {
        AdapterModule am = new AdapterModule();
        Adaptee adaptee = new Adaptee();
        Adapter adapter = new Adapter(adaptee);
        am.test(adapter);
    }
}

interface Target{
    void hanlde();
}
class Adaptee{
    public void reponse(){
        System.out.println("可以完成客户请求");
    }
}
//class Adapter extends Adaptee implements Target则为类适配器
class Adapter implements Target{
    //对象适配器
    Adaptee a;
    public Adapter(Adaptee a) {
        this.a = a;
    }
    @Override
    public void hanlde() {
        a.response();
    }
}
```

应用场景
1. 经常用来做旧系统改造和升级
2. 如果我们的系统开发之后再也不需要维护，那么很多模式都是没必要的，但是不幸的是，事实却是维护一个系统的代价往往是开发一个系统的数倍。

3. 我们学习中见过的场景(字节流转换为字符流)
-java.io.InputStreamReader(InputStream)
-java.io.OutputStreamWriter(OutputStream)