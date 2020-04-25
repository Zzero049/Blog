### IOC与DI
**IOC:**（Inversion（反转）Of Control）：控制反转；
控制：资源的获取方式；
* 主动式：（要什么资源都自己创建即可）
    ```java
    BookServlet{
    BookService bs=new BookService();
    AirPlane ap=new AirPlane();//复杂对象的创建是比较庞大的工程；
    }
    ```
* 被动式：资源的获取不是我们自己创建，而是交给一个容器来创建和设置；
    ```java
    BookServlet{
        BookService bs;
        public void test01(){
            bs.checkout();
        }
    }
    ```
容器：管理所有的组件（有功能的类）；假设，BookServlet受容器管理，BookService也受容器管理；容器可以自动的探查出那些组件（类）需要用到另一写组件（类）；容器帮我们创建BookService对象，并把BookService对象赋值过去；
容器：主动的new资源变为被动的接受资源(想要什么资源向容器提出)；

**DI:**（Dependency Injection） 依赖注入；容器能知道哪个组件（类）运行的时候，需要另外一个类（组件）；容器通过反射的形式，将容器中准备好的BookService对象注入（利用反射给属性赋值）到BookServlet中；

### HelloWorld
（通过各种方式给容器中注册对象（注册会员））

以前是自己new对象，现在所有的对象交给容器创建；给容器中注册组件