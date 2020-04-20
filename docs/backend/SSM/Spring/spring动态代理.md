通过动态代理可以实现方法增强

法1：
```java

public class Client {
    public static void main(String[] args) {
        Producer producer = new Producer();
        /**
         * 动态代理
         * 特点：字节码随用随创建，随用随加载
         * 作用：不修改源码的基础上对方法增强
         * 分类：
         *      基于接口的动态代理
         *      基于子类的动态代理
         * 基于接口的动态代理：
         *      涉及的类：Proxy
         *      提供者：JDk官方
         * 如何创建代理对象：
         *      用Proxy类中的newProxyInstance方法
         * 创建代理对象的要求：
         *      被代理类最少实现一个接口，如果没有则不能使用
         * newProxyInstance方法的参数：
         *      ClassLoader：类加载器
         *          它是用于加载代理对象字节码的。和被代理对象使用相同的类加载器。固定写法
         *      Class[]：字节码数组
         *           他是用于让代理对象和被代理对象有相同的方法。固定写法
         *      InvocationHandler:用于提供增强的代码
         *          它是让我们写如何代理。我们一般都是些一个该接口的实现类，通常情况下都是匿名内部类，但不是必须的。
         *
         */
        Iproducer proxyProducer =(Iproducer) Proxy.newProxyInstance(producer.getClass().getClassLoader(),
                producer.getClass().getInterfaces(),
                new InvocationHandler() {
                    /**
                     * 作用：执行被代理对象的任何接口方法都会经过该方法
                     * @param o         代理对象的引用
                     * @param method    当前执行的方法
                     * @param objects   当执行方法所需时参数
                     * @return          和被代理对象方法有相同的返回值
                     * @throws Throwable
                     */
                    @Override
                    public Object invoke(Object o, Method method, Object[] objects) throws Throwable {
                        //提供增强的代码
                        Object returnValues = null;
                        //1.获取方法执行的参数
                        Float money = (Float) objects[0];
                        //2.判断当前方法是不是销售
                        if("saleProduct".equals(method.getName())){
                            returnValues = method.invoke(producer, money*0.8f);
                        }
                        return returnValues;
                    }
                });
        proxyProducer.saleProduct(10000f);
    }
}

```

法2：需要依赖
```xml
<dependency>
            <groupId>cglib</groupId>
            <artifactId>cglib</artifactId>
            <version>2.1_3</version>
        </dependency>
```
```java
public class Client {
    public static void main(String[] args) {
        Producer producer = new Producer();
        /**
         * 动态代理
         * 特点：字节码随用随创建，随用随加载
         * 作用：不修改源码的基础上对方法增强
         * 分类：
         *      基于接口的动态代理
         *      基于子类的动态代理
         * 基于接口的动态代理：
         *      涉及的类：Enhancer
         *      提供者：第三方cglib库
         * 如何创建代理对象：
         *      被代理类不能是最终类
         * 创建代理对象的要求：
         *      被代理类最少实现一个接口，如果没有则不能使用
         * create方法的参数：
         *      Class：字节码
         *           它是用于被代理对象的字节码
         *      Callback:用于提供增强的代码
         *          我们一般写的都是该接口的子接口实现类：MethodInterceptor
         *
         */
        Producer producer1 = (Producer) Enhancer.create(producer.getClass(), new MethodInterceptor(){
            /**
             作用：执行被代理对象的任何接口方法都会经过该方法
             * @param o         代理对象的引用
             * @param method    当前执行的方法
             * @param objects   当执行方法所需时参数
             * @return          和被代理对象方法有相同的返回值
             * @throws Throwable
             */
            @Override
            public Object intercept(Object o, Method method, Object[] objects, MethodProxy methodProxy) throws Throwable {
                //提供增强的代码
                Object returnValues = null;
                //1.获取方法执行的参数
                Float money = (Float) objects[0];
                //2.判断当前方法是不是销售
                if("saleProduct".equals(method.getName())){
                    returnValues = method.invoke(producer, money*0.8f);
                }
                return returnValues;
            }
        });
        producer1.saleProduct(20000f);

    }
}
```

由此可以通过动态代理来管理方法中一致需要的步骤
```java
package com.itheima.ui.domain.com.itheima.ui.service.Factory;

import com.itheima.ui.domain.com.itheima.ui.service.IAccountService;
import com.itheima.ui.domain.com.itheima.ui.service.impl.AccountserviceImpl;
import com.itheima.ui.domain.com.itheima.ui.service.utils.TransactionMangager;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

public class ProxyService {

    private IAccountService accountService;
    private TransactionMangager trMangager;

    public void setTrMangager(TransactionMangager trMangager) {
        this.trMangager = trMangager;
    }



    public final void setAccountService(IAccountService accountService) {
        this.accountService = accountService;
    }

    /**
     * 获取service代理对象
     * @return
     */
    public IAccountService getAccountService() {
        return (IAccountService) Proxy.newProxyInstance(accountService.getClass().getClassLoader(),
                accountService.getClass().getInterfaces(), new InvocationHandler() {
                    @Override
                    public Object invoke(Object o, Method method, Object[] objects) throws Throwable {
                        Object rtValue =null;
                        try{
                            //1.开启事务
                            trMangager.beginTransaction();
                            //2.执行操作
                            rtValue = method.invoke(accountService,objects);
                            //3.提交事务
                            trMangager.beginTransaction();
                            //4.返回结果
                            return rtValue;
                        }catch (Exception e){
                            //5.回滚操作
                            trMangager.rollback();
                            throw new RuntimeException(e);
                        }finally {
                            //6.释放连接
                            trMangager.release();
                        }

                    }
                });
    }
}

```