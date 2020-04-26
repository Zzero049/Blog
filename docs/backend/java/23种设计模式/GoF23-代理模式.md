## 代理模式
通过代理，控制对对象的访问！
可以详细控制访问某个（某类）对象的方法，在调用这个方法前做前置处理，调用这个方法后做后置处理。（即：AOP[面向切面编程]的微观实现！）

核心角色：
* 抽象角色
-定义代理角色和真实角色的公共对外方法
* 真实角色
-实现抽象角色，定义真实角色所要实现的业务逻辑，供代理角色调用。
-关注真正的业务逻辑！
* 代理角色
-实现抽象角色，是真实角色的代理，通过真实角色的业务逻辑方法来实现抽象方法，并可以附加自己的操作。
-将统一的流程控制放到代理角色中处理！
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-08 140828.png"  div align=center />

应用场景：
-安全代理：屏蔽对真实角色的直接访问。
-远程代理：通过代理类处理远程方法调用（RMI）
-延迟加载：先加载轻量级的代理对象，真正需要再加载真实对象。
* 比如你要开发一个大文档查看软件，太文档中有大的图片，有可能一个图片有100MB，在打开文件时不可能将所有的图片都显示出来，这样就可以使用代理模式，当需要查看图片时，用proxy来进行大图片的打开。

分类：
-静态代理（静态定义代理类）
-动态代理（动态生成代理类）
·JDK自带的动态代理
·javaassist字节码操作库实现
·CGLIB
·ASM（底层使用指令，可维护性较差）

### 静态代理
```java
package GOF23.Proxy;

public class StaticProxy {
    public static void main(String[] args) {
        Star real = new RealStar();
        Star proxy = new Proxy01(real);
        proxy.sing();
        proxy.bookTicket();
        proxy.signContract();
    }
}

interface Star{

    /**
     * 面谈
     */
    void confer();

    /**
     * 签合同
     */
    void signContract();
    void bookTicket();
    void sing();
    void collectMoney();

}

class RealStar implements Star{

    @Override
    public void confer() {
        System.out.println("明星本人面谈...");
    }

    @Override
    public void signContract() {
        System.out.println("明星本人签合同...");
    }

    @Override
    public void bookTicket() {
        System.out.println("明星本人订票...");
    }

    @Override
    public void sing() {
        System.out.println("明星本人唱歌...");
    }

    @Override
    public void collectMoney() {
        System.out.println("明星本人收钱...");
    }
}

class Proxy01 implements Star{

    private Star star;

    public Proxy01(Star star) {
        this.star = star;
    }

    @Override
    public void confer() {
        System.out.println("代理面谈...");
    }

    @Override
    public void signContract() {
        System.out.println("代理本人签合同...");
    }

    @Override
    public void bookTicket() {
        System.out.println("代理本人订票...");
    }

    @Override
    public void sing() {
        star.sing();
    }

    @Override
    public void collectMoney() {
        System.out.println("代理本人收钱...");
    }
}
```

### 动态代理
抽象角色中（接口）声明的所以方法都被转移到调用处理器一个集中的方法中处理，这样，我们可以更加灵活和统一的处理众多的方法。

#### JDK自带的动态代理
* jaya.lang.reflest.Proxy
作用：动态生成代理类和对象
* java.lang.reflect.InyocationHandler（处理器接口）
可以通过invoke方法实现对享实角色的代理访问。
每次通过Proxy生成代理类对象对象时都要指定对应的处理器对象

```java
public class DynamicProxy {
    public static void main(String[] args) {
        Star realStar = new RealStar();
        StarHandler handler = new StarHandler(realStar);

        Star proxy = (Star) Proxy.newProxyInstance(ClassLoader.getSystemClassLoader(),new Class[]{Star.class},handler);
        proxy.sing();
        
    }
}


class StarHandler implements InvocationHandler{

    Star  realStar;

    public StarHandler(Star realStar) {
        this.realStar = realStar;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {

        System.out.println("订票、签合同、唱歌");
        if(method.getName().equals("sing")){
            method.invoke(realStar, args);
        }

        return null;
    }
}
```
输出结果：
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-08 144514.png"  div align=center />

method.invoke里因为传的是realStar所以调用的是realStar的方法。只需要改造这个方法就可以进行动态控制代理能做的，真实角色要做的


开发框架中应用场景：
-struts2中拦截器的实现
-数据库连接池关闭处理Hibernate中延时加载的实现
-mybatis中实现拦截器插件
-Aspes！的实现
-spring中AOP的实现
·日志拦哉
·声明式事务处理
-web service
-RMI远程方法调用
...
