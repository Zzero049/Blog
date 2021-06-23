**1.动态代理模式有哪几种 怎么实现的**

Spring AOP中的动态代理主要有两种方式，JDK动态代理和CGLIB动态代理：

（1）JDK动态代理**只提供接口的代理，不支持类的**代理。

核心InvocationHandler接口和Proxy类，InvocationHandler 通过invoke()方法反射来获取真实对象从而回调目标类中的代码，动态地将横切逻辑和业务编织在一起；接着，Proxy利用 InvocationHandler动态创建一个符合某一接口的实例, 生成目标类的代理对象。

（2）如果代理类没有实现 InvocationHandler 接口（这个应该不是这样吧，没有实现普通接口吧），那么Spring AOP会选择使用CGLIB来动态代理目标类。CGLIB（Code Generation Library），是一个代码生成的类库，可以在运行时动态的生成指定类的一个**子类对象**，**并覆盖其中特定方法并添加增强代码**，从而实现AOP。CGLIB是通过**继承**的方式做的动态代理，因此如果某个类被标记为final，那么它是无法使用CGLIB做动态代理的。

静态代理与动态代理区别在于生成AOP代理对象的时机不同，相对来说AspectJ的静态代理方式具有更好的性能，但是AspectJ需要特定的编译器进行处理，而Spring AOP则无需特定的编译器处理。

**动态代理的底层执行过程？**

参考API，JDK提供了实现动态代理的相关组件。包括如下：

```
接口 InvocationHandler；
类 Proxy；
它们都在java.lang.reflect包中。
```

InvocationHandler是代理实例的调用处理程序 实现的接口。 该接口只有一个方法：Object invoke(Object proxy,Method method,Object[] args)throwsThrowable。

直接的理解为：**当调用被代理对象的某个方法时，实际上会在该接口的实现类上调用invoke方法**。也就是说，**invoke方法就是代替原来执行的方法。**

Proxy 提供用于**创建动态代理类和实例**的静态方法，创建出来的代理类实例都是Proxy的子类。它的这两个方法是比较重要的：getProxyClass动态生成代理类，newProxyInstance整合了getProxyClass方法并通过构造方法反射获得代理类的实例。

实际上JDK的动态代理实现是比较容易的，例如下面的例子：

1、一个接口

```
public interface IUserDao {
    void save();
}
```

2、接口的实现类（真实对象）

```
ublic class UserDaoImpl implements IUserDao {

    @Override
    public void save() {
        System.out.println("真实对象的say方法");
    }
}
```

3、处理类（继承invocationHandler）

```
public class Handler implements InvocationHandler {

    /**
     * 需要持有真实对象的接口
     */
    private IUserDao userDao;

    public Handler(IUserDao userDao) {
        this.userDao = userDao;
    }

    /**
     *
     * @param proxy
     * @param method
     * @param args
     * @return
     * @throws Throwable
     */
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        System.out.println("调用真实对象方法前的处理");
        //通过method方法传入真实对象
        method.invoke(userDao,args);
        System.out.println("调用真实对象方法后的处理");
        return "执行完成";
    }
}
```

4、测试的时候使用proxy类获取实例

```
public class TestProxy {
    public static void main(String[] args) {
        IUserDao userDao=new UserDaoImpl();
        //1、获取处理类
        Handler handler = new Handler(userDao);
        //2、获取代理对象
        IUserDao proxyInstance = (IUserDao) Proxy.newProxyInstance(
        userDao.getClass().getClassLoader(),
        new Class[]{IUserDao.class}, handler);
        //3、代理对象调用方法
        proxyInstance.save();
    }
}
```

![img](H:\Desktop\新建文件夹\Blog\docs\backend\SSM\Spring\pictures\38895)

结合上述的代码，有几点需要注意：

1、在invoke方法中，不能在该方法中调用proxy对象的方法，因为在proxy对象中实现的任何一个方法内部都是回调InvocationHandler的invoke方法，如果这样就会造成递归死循环。如：proxy.save();

2、JDK方式产生的所有代理实例都是Proxy类的子类，然后实现代理类实现的接口的方法，如上面的UserDao，在代理类的内部通过对原始调用的方法命名，如m1,m2,m3，save命名为m3，然后在替代方法中调用这些原始方法。

3、至于为什么m0,m1,m2没使用，其实是被object的三个方法用了。下面是api的一段描述：

​    在代理实例上的 java.lang.Object 中声明的 hashCode、equals 或 toString 方法的调用将按照与编码和指派接口方法调用相同的方式进行编码，并被指派到调用处理程序的invoke 方法，如上所述。传递到invoke 的 Method 对象的声明类是java.lang.Object。代理类不重写从java.lang.Object 继承的代理实例的其他公共方法，所以这些方法的调用行为与其对java.lang.Object 实例的操作一样。 

4、正如上图所示，jdk方式的代理都是继承proxy类，因此只能代理多个接口，而无法对类进行代理。

原文链接：https://blog.csdn.net/ShewMi/article/details/78108705

**2.循环依赖知道吗  怎么解决 （不懂）**

想彻底弄清楚spring的循环依赖问题，首先得弄清楚，循环依赖是如何发生的，spring又是如何检测循环依赖的发生的。其次再探究spring如何解决循环依赖的问题

最后我们将总结循环依赖解决的2个关键因素，提前曝光和曝光时机，缺一不可

\1. 循环依赖检查（有点像垃圾回收机制里面的循环引用）

```
<bean id="a" class="A">
	<property name="b" ref="b">
<bean/>
<bean id="b" class="B">
	<property name="a" ref="a">
<bean/>

```

无论单例还是原型模式(下文①代表图中步骤1)，spring都有对应的集合保存当前正在创建的beanName，标识该beanName正在被创建。在bean创建前，①检测当前bean是否在创建中，如果不在创建中则②将beanName加入集合，往下创建bean。在bean创建前，检测到当前的bean正在创建，则说明发生循环依赖，抛出异常。最后记得当bean创建完时将beanName移出集合。

![img](H:\Desktop\新建文件夹\Blog\docs\backend\SSM\Spring\pictures\32452)

\2. 循环依赖的处理

单例setter循环依赖

spring注入属性的方式有多种，但是只有一种循环依赖能被解决：**setter依赖注入**。前面或多或少都提到了spring解决循环依赖的做法是未等bean创建完就先将实例曝光出去，方便其他bean的引用。同时还提到了三级缓存，最先曝光到第三级缓存singletonFactories中。简单的说，就是spring先将创建好的实例放到缓存中，让其他bean可以提前引用到该对象。不知道三级缓存是什么的可以参考下(不懂问题也不大)：spring从缓存中获取bean

```
// 第一种 注解方式
public class A {
	@Autowired
	private B b;
}

public class B {
	@Autowired
	private A a;
}

// ===========================
// 第二种 xml配置方式
public class A {
	private B b;
	// getter setter
}

public class B {
	private A a;
	// getter setter
}

<bean id="a" class="A">
	<property name="b" ref="b">
<bean/>
<bean id="b" class="B">
	<property name="a" ref="a">
<bean/>

```

![img](H:\Desktop\新建文件夹\Blog\docs\backend\SSM\Spring\pictures\32456)

提前曝光，如果用c语言的说法就是将指针曝光出去，用java就是将引用对象曝光出去。也就是说即便a对象还未创建完成，但是在④实例化过程中new A()动作已经开辟了一块内存空间，只需要将该地址抛出去b就可以引用的到，而不管a后期还会进行初始化等其他操作

已经了解了提前曝光的作用，而相比而言⑤曝光的时机也非常的重要，该时机发生在④实例化之后，⑥填充与⑯ 初始化之前。spring循环依赖之所以不能解决实例化注入的原因正式因为注入时机在曝光之前所导致

⑤中写的带a的工厂是什么东西？先来了解一下ObjectFatory

```
public interface ObjectFactory<T> {
	T getObject() throws BeansException;
}
```

就是一个接口，通过重写getObject()方法返回对应的object

// 将该bean提前曝光，具体做法是创建一个ObjectFactory对象，再将对象加入到singletonFactories缓存中

```
addSingletonFactory(beanName,
 () -> getEarlyBeanReference(beanName, mbd, bean));
```

让我帮大家改写一下，不然可能看了有点懵逼，以上代码等同于

```
addSingletonFactory(beanName, new ObjectFactory<Object>() {
    @Override
	public Object getObject() throws BeansException {
		getEarlyBeanReference(beanName, mbd, bean);
	} 
});
```

但是我们看到，按原计划重写getObject()应该是直接return bean就行了，为什么还有getEarlyBeanReference是什么鬼？（这点非常重要，但是我看了很多博客甚至书本都完全忽视了这点，如果忽视了这点，那三级缓存将失去意义，直接二级缓存就可以解决提前曝光的问题）

getEarlyBeanReference目的就是为了后置处理，给一个在提前曝光时操作bean的机会，具体要怎么操作bean，那就继承SmartInstantiationAwareBeanPostProcessor重写getEarlyBeanReference方法吧。比如你要System.out.print(“啊啊啊啊,我是” + bean + “，我被曝光且提前引用啦”)也是可以的，关键就在于bean被曝光到三级缓存时并没用使用提前曝光的后置处理，而是当三级缓存被提前引用到二级缓存时才触发！（但是在Spring的源码中，真正实现这个方法的只有AbstractAutoProxyCreator这个类，用于提前曝光的AOP代理。当学习完Ioc AOP全部源码之后，我会给出最终章来解释这个问题《当AOP遇上循环依赖》）

```
	protected Object getEarlyBeanReference(String beanName, RootBeanDefinition mbd, Object bean) {
		Object exposedObject = bean;
		if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
			for (BeanPostProcessor bp : getBeanPostProcessors()) {
				if (bp instanceof SmartInstantiationAwareBeanPostProcessor) {
	SmartInstantiationAwareBeanPostProcessor ibp = (SmartInstantiationAwareBeanPostProcessor) bp;
	// 这么一大段就这句话是核心，也就是当bean要进行提前曝光时，
	// 给一个机会，通过重写后置处理器的getEarlyBeanReference方法，来自定义操作bean
	// 值得注意的是，如果提前曝光了，但是没有被提前引用，则该后置处理器并不生效!!!
	// 这也正式三级缓存存在的意义，否则二级缓存就可以解决循环依赖的问题
	exposedObject = ibp.getEarlyBeanReference(exposedObject, beanName);
				}
			}
		}
		return exposedObject;
	}
```

单例构造器注入循环依赖

上面已经剧透了这个方式是不得行的，原因是依赖注入的时间点不对，他的依赖注入发生在构造器阶段，这个时候连实例都没有，内存都还没开辟完，当然也还没有进行提前曝光，因此不得行

```
示例
public class A {
	private B b;

	@Autowired
	public A(B b) {
		this.b = b;
	}
}

public class B {
	private  A a;

	@Autowired
	public B(A a) {
		this.a = a
	}
}
```

![img](H:\Desktop\新建文件夹\Blog\docs\backend\SSM\Spring\pictures\32460)

图上重点地方也用黄色标出了，问题的原因处在④实例化，实例化的过程是调用new A(B b);的过程，这时的A还未创建出来，根本是不可能提前曝光的，正是这个原因导致⑨无法获取到三级缓存，进而导致⑩异常的抛出

原型模式循环依赖

这此没有图了，因为原型模式每次都是重新生成一个全新的bean，根本没有缓存一说。这将导致实例化A完，填充发现需要B，实例化B完又发现需要A，而每次的A又都要不一样，所以死循环的依赖下去。唯一的做法就是利用循环依赖检测，发现原型模式下存在循环依赖并抛出异常

总结

总结一下循环依赖，spring只能解决setter注入单例模式下的循环依赖问题。要想解决循环依赖必须要满足2个条件：

需要用于提前曝光的缓存

属性的注入时机必须发生在提前曝光动作之后，不管是填充还是初始化都行，总之不能在实例化，因为提前曝光动作在实例化之后

理解了这2点就可以轻松驾驭循环依赖了。比如构造器注入是不满足第二个条件，曝光时间不对。而原型模式则是缺少了第一个条件，没有提前曝光的缓存供使用