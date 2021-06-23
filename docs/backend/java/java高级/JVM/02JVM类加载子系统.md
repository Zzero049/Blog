# 类加载器子系统

idea安装插件`jclasslib Bytecode viewer`，能方便查看字节码

## 什么是类的加载？

虚拟机把描述类的数据从class文件加载到内存，并对数据进行校验转换解析和初始化最终形成可以被虚拟机直接使用的java类这就是虚拟机的类加载机制，这个过程通过类加载器子系统完成。

与那些在编译时需要进行连接工作的语言不同在java语言中类型的加载连接和初始化过程都是在程序运行期间完成的这种策略虽然会令类加载时稍微增加一些性能开销，但是为java感用程序提供高度的灵活性java里天生可以**动态扩展**的语言特性就是依赖**运行时期动态加载和动态链接**的这个特点实现的

一个class文件是通过类加载器子系统加载到内存的，一个类加载过程包括了加载、验证、准备、解析、初始化、使用和卸载七个阶段。

一个类的生命周期包括了加载、验证、准备、解析、初始化、使用和卸载七个阶段。其中**类加载的过程包括了加载、验证、准备、解析、初始化五个阶段**。在这五个阶段中，加载、验证、准备和初始化这四个阶段发生的顺序是确定的，而解析阶段则不一定，它在某些情况下可以在初始化阶段之后开始。另外注意这里的几个阶段是**按顺序开始**，而**不是按顺序进行或完成**，因为这些阶段通常都是互相交叉地混合进行的，通常在一个阶段执行的过程中调用或激活另一个阶段。

![image-20200531175808319](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200531175808319.png)

- 类加载器子系统负责从文件系统或者网中加载class文件，class文件在文件开头有特定的文件标识。
- ClassLoader只负责class文件的加载，至于它是否可以运行，则由 Execution Engine 执行引擎决定。
- 加载的类信息存放于一块称为方法区的内存空间。除了类的信息外，方法区中还会存放运行时常量池信息，可能还包括字符串字面量和数字常量（这部分常量信息是Class文件中常量池部分的内存映射）

![image-20200531180057191](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200531180057191.png)

## 类的加载过程

### 加载阶段（Loading）

1、通过一个类的全限定名获取定义此类的<font color="#DC143C">**二进制字节流**</font>

2、将这个字节流所代表的静态**存储结构**转化为方法区的运行时数据结构

3、在JVM内存中生成一个代表这个类的<font color="red">**java.lang.Class**对象</font>，作为方法区这个类的各种数据的访问入口

![image-20200603165108662](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200603165108662.png)

补充：加载.class文件的方式

- 从本地系统中直接加载
- 通过网络获取，典型场景：Web Applet
- 从zip压缩包中读取，成为日后jar、war格式的基础
- 运行时计算生成，使用最多的是：动态代理技术由其他文件生成，典型场景：JSP应用
- 从专有数据库中提取.class文件，比较少见
- 从加密文件中获取，典型的防Class文件被反编译的保护措施



### 链接阶段（Linking）

#### 验证（Verification）

目的在于**确保class文件的字节流中包含信息符合当前虚拟机要求**，保证被加载类的正确性，不会危害虚拟机自身安全。

如果使用纯粹的 java 代码，做到诸如将一个对象转型为它并未实现的类型，编译器将拒绝编译(编译报错)。但是在前文中提到，Class文件并不一定要求是 Java 源码编译而来的。虚拟机如果不检查输入的字节码流,对其完全信任的话,很可能会因为载入了有害的字节码流而导致系统崩溃。  

验证阶段大致需要下面四个阶段来验证，文件格式验证，元数据验证，字节码验证，符号引用验证。

1. **文件格式验证：**
   验证字节流是否符合<font color="#DC143C">**Class 文件格式**</font>的规范,并且能被当前版本的虚拟机处理.

   比如,是否以**魔数 0xCAFEBABE 开头**(字节码头四个字节,用来表示一个可以接受的字节码文件).

   主要目的是保证输入的字节流能正确的解析并存储于方法区之内,格式上符合描述一个 java 类型信息的要求.  

2. **元数据验证：**
   对字节码描述的信息进行语义分析，以保证其<font color="#DC143C">**描述的信息**</font>符合 Java 语言规范的要求。

   比如，是否有父类，是否继承了不允许被继承的类等等。（比如确保是该类是Object子类）

   主要目的是对类的元数据信息进行语义校验，保证不存在不符合 java 语言规范的元数据信息.  

3. **字节码验证：**

   在元数据验证之后，这个阶段将对类的方法体进行校验分析，保证被校验的类的方法在运行时不会做出危害虚拟机安全的事。

   目的是通过数据流和控制流分析确定程序语义是合法的符合逻辑的

4. **符号引用验证：**

    该校验是发生在虚拟机将符号引用转化为直接引用的时候，这个转化动作将在解析阶段中发生，目的是确保解析动作能正常执行。

    比如校验符号引用中的全限定名是否能找到对应的类，是否具备访问权限等等。

对于虚拟机的类加载机制来说，验证阶段是一个非常重要的，但不是一定必要（对程序运行期没有影响）的阶段。如果所运行的全部代
 码都已经被反复使用和验证过，那么在实施阶段可以考虑使用 <font color="red">**-Xverify:none 参数来关闭大部分的类验证措施**</font>，以缩短虚拟机类加载的
时间



#### 准备（Preparation）

**为类变量（static变量）分配内存并且设置该类变量的默认初始值**，即 0、null、fasle。

进行赋值声明的变量，在初始化阶段才被正确赋值。这里不包含用final修饰的 static，因为final在编译的时候就会分配了，调用时不会触发类的加载；

这里不会为<font color="#DC143C">**实例变量（非静态）**</font>分配初始化，类变量会分配在方法区中，而实例变量是会随着对象实例化一起分配到Java堆中



#### 解析（Resolution）

**将<font color="#DC143C">常量池</font>内的符号引用转换为直接引用**的过程。

事实上，**解析操作往往会伴随着JVM在执行完初始化之后**再执行。

**符号引用（Symbolic References）：**以一组符号来描述所引用的目标，符号可以是任何形式的字面量，只要使用时能够无歧义的定位到目标即可。符号引用与虚拟机的内存布局无关，引用的目标并不一定加载到内存中。在 Java 中，一个 java 类将会编译成一个class 文件。在编译时，java 类并不知道所引用的类的实际地址，因此只能使用符号引用来代替 。

**直接引用：**就是直接指向目标的指针、相对偏移量或一个间接定位到目标的句柄（句柄就是个数字，一般和当前系统下的整数的位数一样，比如32bit系统下就是4个字节。这个数字是一个对象的唯一标识，和对象一一对应）。

解析动作主要针对类或接口、字段、类方法、接口方法、方法类型等。对应常量池中的CONSTANT_Class_info，CONSTANT_Fieldref_info，CONSTANT_Methodref_infor等



### 初始化阶段（Initialize）

初始化阶段,才真正开始执行类中定义的 java 程序代码。

初始化阶段是执行类构造器<font color="red">	**`<clinit>()`方法**</font>的过程。此方法不需定义，是 Javac编译器自动收集类中的所有类变量的赋值动作和静态代码块中的语句合并而来。

类构造器`<clinit>()`方法规则：

1. 类构造器`<clinit>()`方法是有编译器自动收集类中的所有类变量的赋值动作和 `static `语句块中的语句合并产生的。编译器收集的顺序是由语句在**源文件中出现的顺序所决定的**。静态语句块中只能访问到定义在静态语句块之前的变量，定义在其之后的变量，在静态语句块中可以赋值，但是不能访问。如：

   ![image-20200603183543458](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200603183543458.png)

   1、能够前向赋值，是因为在准备阶段，就已经对 i 这个变量分配空间和赋 0 的操作了

   2、前向引用报错，至于为什么不能调用后面的变量，这其实是一个JVM语法规定，对于静态变量，你可以在它的声明前面赋值，但是不允许你在它的声明前面访问。

2. `类构造器<clinit>()`方法与`类的构造器<init>()`方法不同，JVM会保证子类的`<c1init>()`执行前，父类的`< clinit>()`已经执行完毕，即**父类`<c1init>()`先执行**。因此，在虚拟机中第一个被执行的`<clinit>()`方法的类肯定是 Object。

3.  由于父类的`<clinit>()`方法先执行，也就意味着父类中定义的静态语句块要优于子类的变量赋值。

4. 类构造器`<clinit>`()方法对于类或者接口来说并不是必需的，如果一个类中没有静态语句块，编译器就不会为这个类生成` <clinit>()`方法。

5. 接口中也可以定义 static 变量，生成的`<clinit>()`方法不需要先执行父接口中的`<clinit>()`方法，同理，接口的实现类在初始化的时候也一样不会执行接口中的`<clinit>()`方法。

6. 虚拟机会保证一个类的`<clinit>()`方法在多线程环境中被正确的加锁，同步，如果多线程同时去初始化一个类，只会有一个线程去初始化，其他线程都阻塞。

![image-20200603190647809](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200603190647809.png)

**初始化时机**

虽然对于加载时机，java 虚拟机规范中并没有进行强制约束。这点可以交给虚拟机的具体实现来自有把握。但是对于初始化阶段，虚拟机规范则严格规定了有且只有五种情况必须立即对类进行"初始化"(加载,验证,准备自然需要在初始化之前开始)。

1. 遇到 **new 指令**(使用关键字 new 来实例化对象)，**getstatic，putstatic**(读取或设置一个类的静态字段的时候,除了 final 修饰,在编译时期就已经把结果放在常量池的静态字段)或invokestatic(调用类的静态方法)这4条字节码指令时,如果类没有进行初始化,则需要先
   触发其初始化.
2. 使用 java.lang.reflect 包的方法**对类进行反射调用的时候,如果类没有进行过初始化**,则需要先触发其初始化.
3. 当**初始化一个类的时候,如果发现其父类还没有进行初始化**,则需要先触发其父类的初始化(接口初始化例外,不要求所有父接口全部都初始化,只有在真正调用到父接口的时候才会初始化).
4. 当启动虚拟机时,用户需要**指定一个需要执行的主类（main方法所在）**,虚机先初始化这个主类.
5. 当使用java7的动态语言支持时,如果一个MethodHandle实例在解析时,该方法对应的类没有进行初始化,则需要先触发其初始化。

这五种场景中的行为称之为对一个类进行主动引用。除此之外，所有引用类型的方式都**不会触发初始化**，叫做被动引用.

1.通过**子类引用父类的静态字段（静态变量或静态方法）**,不会导致子类初始化(此时的静态资源不是属于子类父类的,底层还是使用的是 SuperClass.value去访问的,所以只初始化 SuperClass,而不初始化 SubClass)  

![image-20200603170113465](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200603170113465.png)

2.通过**数组定义来引用类**,不会触发此类的初始化  

![image-20200603170127775](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200603170127775.png)

3.**final定义的常量在编译阶段会存入调用类的常量池**中,本质上并没有直接引用到定义常量的类,因此不会触发定义常量的类的初始化.  

![image-20200603170420154](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200603170420154.png)



**例题：**

![image-20200603191235250](H:\Desktop\新建文件夹\Blog\docs\backend\java高级知识\JVM\pictures\image-20200603191235250.png)

首先,当有代码调用了类中的静态方法 getSingleTon,会触发类的初始化.

![image-20200603191416021](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200603191416021.png)

**对于情况一:**

- 连接阶段,为静态变量赋初始值.count1=0, count2=0, singltTon=null.
- 初始化阶段,从上到下依次执行赋值操作和静态代码块.
- count1=0, count2=0,创建对象之后,对两个数值进行递增.结果 count1=1,count2=1.

**对于情况二:**

- 连接阶段,为静态变量赋初始值.singltTon=null.count1=0, count2=0,.
- 初始化阶段,从上到下依次执行赋值操作和静态代码块.
- 先创建对象,对两个数值进行递增.结果 count1=1,count2=1.
- 再是赋值,count1 没有赋值,count2 重新赋值.count1=1, count2=0.  



## 类加载器

虚拟机设计团队把类加载阶段中的“通过一个类的全限定名来获取描述此类的二进制字节流”这个动作放到了 java 虚拟机外部去实现(意思就是说,如何把字节码文件变成流的过程,不仅仅属于虚拟机中的功能).以便**让应用程序自己决定如何去获取所需要的类**。这个动作的代码模块成为"类加载器".

**类加载器可以说是 java 语言的一项创新.也是 java 语言流行的重要原因之一**.它在类层次划分,OSGi,热部署,代码加密等领域大放异彩。成为 java 体系中一块重要的基石。

JVM支持两种类型的类加载器，分别为：

- 引导类加载器（Bootstrap ClassLoader）  C/C++ 实现
- 自定义类加载器（User-Defined ClassLoader） java实现。

![image-20200603192042105](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200603192042105.png)

从概念上来讲，自定义类加载器一般指的是程序中由开发人员自定义的一类类加载器，但是Java虚拟机规范却没有这么定义，而是将所有派生于抽象类ClassLoader的类加载器都划分为自定义类加载器。

![image-20200603193020621](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200603193020621.png)

无论类加载器的类型如何划分，在程序中我们最常见的类加载器始终只有3个（不算自定义的），如下所示：

注意上下层之间不是继承关系

![image-20200616101901516](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200616101901516.png)



示例：

```java
public class ClassLoaderTest {
    public static void main(String[] args) throws ClassNotFoundException {
        // 获取系统类加载器
        System.out.println("=============系统类加载器============");
        ClassLoader systemClassLoader1 = ClassLoader.getSystemClassLoader();
        ClassLoader systemClassLoader2 = ClassLoaderTest.class.getClassLoader();    // 获取这个测试类的类加载器
        System.out.println(systemClassLoader1);
        System.out.println(systemClassLoader2); // 一致


        // 获取扩展类加载器（系统类上级） 都是Launcher的静态内部类
        System.out.println("=============扩展类加载器============");
        ClassLoader extClassLoader = systemClassLoader1.getParent();
        System.out.println(extClassLoader);

        // 获取引导类加载器（扩展类上级）
        System.out.println("=============引导类加载器============");
        ClassLoader bootstrapClassLoader1 = Class.forName("java.lang.String").getClassLoader();
        ClassLoader bootstrapClassLoader2 = extClassLoader.getParent();
        System.out.println(bootstrapClassLoader1);
        System.out.println(bootstrapClassLoader2);//null
    }
}
```

![image-20200603194831266](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200603194831266.png)





### 启动类加载器（Bootstrap ClassLoader）

- 这个类加载使用**C/C++语言**实现的，嵌套在JVM内部。
- 它用来加载**Java的核心类库**（<font color="#DC143C">JAVA_HOME/jre/lib/rt.jar</font>、resources.jar或sun.boot.class path路径下的内容），用于提供JVM自身需要的类(也可以配置参数-Xbootclasspath 参数指定的路径中  )
- 并**不继承**自java.lang.**ClassLoader**，没有父加载器。
- 加载扩展类和应用程序类加载器，并指定为他们的父类加载器。
- 出于安全考虑，Bootstrap启动类加载器**只加载包名为java、javax、sun等开头的类**



### 扩展类加载器（Extension ClassLoader）

- **Java语言**编写，由sun.misc.Launcher$ ExtClassLoader实现。
- 派生于**Classloader类**
- **父类加载器为启动类加载器**
- 从java.ext.dirs系统属性所指定的目录中加载类库，或从JDK的安装目录的 <font color="#DC143C">jre/lib/ext</font> 子目录（扩展目录）下加载类库。**如果用户创建的 JAR 放在此目录下，也会自动由扩展类加载器加载**



### 应用程序类加载器（AppClassLoader）

- **java语言**编写，由sun.misc.Launcher$AppClassLoader实现
- 派生于**ClassLoader类**
- **父类加载器为扩展类加载器**
- 它负责加载环境变量 **classpath**或系统属性 java.class.path路径下的类库( java.class.path包括系统启动时的加载所有class的路径)
- 该类加载是**程序中默认的类加载器**，一般来说，Java应用的类都是由它来完成加载
- 通过Classloader.getSystemClassLoader()方法可以获取到该类加载器

![](https://gitee.com/zero049/MyNoteImages/raw/master/u=2247497232,953556131&fm=26&gp=0.jpg)



示例：

```java
public class LoaderPathTest {
    public static void main(String[] args) {
        System.out.println("=======================启动类加载器=======================");
        URL[] urls = sun.misc.Launcher.getBootstrapClassPath().getURLs();
        for(URL url:urls){
            System.out.println(url);
        }

        System.out.println("=======================扩展类加载器=======================");
        String extDirs = System.getProperty("java.ext.dirs");
        for(String path:extDirs.split(";")){        //由于不同的路径会用;隔开
            System.out.println(path);
        }
        System.out.println("=======================应用类加载器=======================");
        String classDirs = System.getProperty("java.class.path");
        for(String path:classDirs.split(";")){        //由于不同的路径会用;隔开
            System.out.println(path);   // 包括系统启动时的加载所有class的路径，并不能说明一定是由
                                        // AppClassLoader加载，经过双亲委托机制，没被加载的才到他加载
        }

    }
}
```

![image-20200603205200902](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200603205200902.png)

### 用户自定义的类加载器

**自定义加载器的应用场景：**

1、隔离加载类

2、修改类加载的方式

3、扩展加载源

4、防止源码泄漏

**实现步骤：**

1、开发人员可以通过继承抽象类java.lang.ClassLoader类的方式，实现自己的类加载器，以满足一些特殊的需求

2、在JDK1.2之前，在自定义类加载器时，总会去继承ClassLoader类并重写`loadClass()`方法，从而实现自定义的类加载类，但是在JDK1.2之后已**不再建议用户去覆盖`loadClass()`方法**，而是**建议**把自定义的类加载逻辑写在 **`findClass()`**方法中

3、在编写自定义类加载器时，如果没有太过于复杂的需求，可以直接继承`URLClassLoader`类，这样就可以避免自己去编写 `findClass()`方法及其获取字节码流的方式，使自定义类加载器编写更加简洁.



### ClassLoader类

ClassLoader类，它是一个抽象类；其后所有的类加载器都继承自ClassLoader（不包括启动类加载器）

| 方法名称                                          | 描述                                                         |
| ------------------------------------------------- | ------------------------------------------------------------ |
| getParent()                                       | 返回该类加载器的父类加载器                                   |
| loadClass(String name)                            | 加载名称为name的类，返回结果为java.lang.Class类的实例        |
| findClass(String name)                            | 查找名称为name的类，返回结果为java.lang.Class类的实例（和defineClass搭配使用） |
| findLoaderClass(String name)                      | 查找名称为name的已经被加载过的类，返回结果为java.lang.Class类的实例 |
| defineClass(String name,byte[] b,int off,int len) | 把字节数组b的内容转换为一个Java类，返回结果为java.lang.Class类的实例 |
| resolveClass(Class<?> c)                          | 连接指定一个Java类                                           |



**在JVM中表示两个class对象是否为同一个类存在两个必要条件：**

1. 类的完整类名必须一致，包括包名
2. 加载这个类的classloader（指ClassLoader实例对象）必须相同。



## 双亲委托机制

Java虚拟机对 class文件采用的是<font color="#DC143C">**按需加载**</font>的方式，也就是说当需要使用该类时才会将它的class文件加载到内存生成class对象。而且加载某个类的class文件时，只需要加载进内存一次就足够了。为了**避免重复加载**，当父 ClassLoader 已经加载了该类的时候，就没有必要子ClassLoader 再加载一次。这种加载器之间的层次关系，就叫做**双亲委派模型(Parents Delegation Model)**  

### 工作原理

1. 如果一个类加载器收到了类加载请求，它并不会自己先去加载，而是把这个请求委托给父类的加载器去执行；
2. 如果父类加载器还存在其父类加载器，则进一步向上委托，依次递归，请求最终将到达顶层的启动类加载器；
3. 如果父类加载器可以完成类加载任务，就成功返回，倘若父类加载器无法完成此加载任务，子加载器才会尝试自己去加载，这就是双亲委派模式

![双亲委托](https://gitee.com/zero049/MyNoteImages/raw/master/u=2247497232,953556131&fm=26&gp=0.jpg)



**优点：**

1. 避免类的重复加载
2. 保护程序安全，防止核心API被随意篡改
   - 比如自定义了一个java.lang.String，同名仍然是加载到核心类库的String
   - 在比如自定义了一个java.lang.xxxx，引导类加载器加载xxxx会直接报错（权限不足）

### 底层原理浅析

查看底层ClassLoader的`loadClass`方法

发现是一个递归的过程，如果有父加载器，取到继续递归，直到到达引导类加载器（null），父加载器无法完成加载，递归退出，到子类尝试加载，直到结束

```java
protected Class<?> loadClass(String name, boolean resolve)
        throws ClassNotFoundException
    {
        synchronized (getClassLoadingLock(name)) {	// 首先检查是否已经加载了这个类
            // First, check if the class has already been loaded
            Class<?> c = findLoadedClass(name);
            if (c == null) {
                long t0 = System.nanoTime();
                try {
                    if (parent != null) {	// 拿到父类加载器
                        c = parent.loadClass(name, false);	// 向上递归
                    } else {
                        c = findBootstrapClassOrNull(name);	// 引导类加载器
                    }
                } catch (ClassNotFoundException e) {	// 拿父类加载器的过程出错则爆出异常
                    // ClassNotFoundException thrown if class not found
                    // from the non-null parent class loader
                }

                if (c == null) {			// 递归到底，开始执行加载，父类不能加载执行完毕，退栈，到子类进行加载
                    // If still not found, then invoke findClass in order
                    // to find the class.
                    long t1 = System.nanoTime();		
                    c = findClass(name);

                    // this is the defining class loader; record the stats
                    sun.misc.PerfCounter.getParentDelegationTime().addTime(t1 - t0);
                    sun.misc.PerfCounter.getFindClassTime().addElapsedTimeFrom(t1);
                    sun.misc.PerfCounter.getFindClasses().increment();
                }
            }
            if (resolve) {
                resolveClass(c);
            }
            return c;
        }
```



### 破坏双亲委托机制

双亲委派模型，并不是一个强制性的约束模型，而是 java 设计者推荐给开发者的类加载实现方式。在 java 的世界中大部分的类加载器都遵循这个模型。但是，在一些应用场景下，由于直接或间接的原因，双亲委派模型被破坏。

1. 在我们**自定义类加载器**的时候，可以**复写父类 ClassLoader 的 `loadClass `方法**，这样就直接破坏了双亲委派模型。到后面 JDK1.2
    之后，为了解决这个问题以及兼容问题，提供了一个 `findClass()`方法。
2. 如果 **API 中的基础类想要调用用户的代码(JNDI/JDBC 等)，此时双亲委派模型就不能完成**。为了解决这个问题，java 设计团队只好使用一个不优雅的设计方案：Thread 的上下文类加载器，默认就是应用程序的类加载器。
3. 由于程序动态性的发展，**希望应用程序不用重启就可以加载最新的字节码文件**。此时就需要破坏双亲委派模型。

 双亲委派模型被破坏，并不包含贬义，只要有足够意义和理由就可以认为这是一种创新，什么方式会打破双亲委派模型呢?

1. 自定义类加载器，复写 loadClass 方法。

2. 使用线程的上下文类加载器对象



## 沙箱安全机制

自定义 string类，但是在加载自定义 string类的时候会率先使用引导类加载器加载，而引导类加载器在加载的过程中会先加载jdk自带的文件（rt，jar包中java\lang\string.class），报错信息说没有main方法，就是因为加载的是rt.jar包中的 string类。这样可以保证对java核心源代码的保护，这就是**沙箱安全机制**。沙箱机制就是将 **Java 代码限定在虚拟机(JVM)特定的运行范围**中，并且严格限制代码对本地系统资源访问，通过这样的措施来保证对代码的有效隔离，防止对本地系统造成破坏。

java沙箱机制的具体内容，可以参考：https://blog.csdn.net/qq_30336433/article/details/83268945

```java
package java.lang;

public class String {
    static {
        System.out.println("我是病毒，嘿嘿嘿");
    }

    public static void main(String[] args) {
        System.out.println("尝试接入");
    }
}
```

![image-20200603221246801](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200603221246801.png)

沙箱机制的作用：

1. 防止不安全代码访问、破坏安全代码。
2. 防止不安全代码冒充安全的类。

这2 方面作用是通过下述方法实现的：

　1. 将代码分放在多个命名空间中，并在不同命名空间的代码之间设置“ 屏障” 。类载入器结构是通过命名空间来防止不安全代码访问、破坏安全代码。命名空 间在载入到不同命名空间中的类之间设置了1 个“ 屏障” 。在JVM 中，同一命名空间中的类可以直接相互作用，不同命名空间中的类甚至不能检测到对方的存在， 除非程序允许它们相互作用。
 　　2. 保护可信任类库( 像JAVA API) 的边界。如果类载入器载入1 个类，这个类用它的名字来冒充是JAVA API 的1 部分( 例如，类名为java.lang.virus) ，类载入器就传递请求给原始类载入器，如果原始类载入器不能载入这个类，类载入器就抛出安 全例外，并拒绝载入这个类。



