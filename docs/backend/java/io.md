# io
### 数据源
data source。提供原始数据的原始媒介，常见的：数据库、文件、其他程序、内存、网络连接、IO设备。
* 在Java程序中，对于数据的输入/输出操作以“流”
（stream）方式进行；
*  J2SDK提供了各种各样的“流”类，用以获取不同种类的数据：程序中通过标准的方法输入或输出数据。（以程序为中心定义输入，输出流）

* Java的流类型一般位于java.io包中

整个Java.io包中最重要的就是5个类和3个接口
<img src="./pictures/Annotation 2019-11-09 153426.png"  div align=center />

### 流分类
按数据方向划分：
输入流：数据源到程序（InputStream、Reader读进来）
输出流：程序到目的地（OutputStream、Writer写出去）

按功能方向划分：
节点流：可以直接从数据源或目的地读写数据
<img src="./pictures/Annotation 2019-11-09 154043.png"  div align=center />

处理流（包装流）：不直接连接到数据源或目的地，是其他流进行封装。目的主要是简化操作和提高性能。
<img src="./pictures/Annotation 2019-11-09 154112.png"  div align=center />


**节点流和处理流的关系：**
1. 节点流处于io操作的第一线，所有操作必须通过他们进行；
2. 处理流可以对其他流进行处理（提高效率或操作灵活性）。
<img src="./pictures/Annotation 2019-11-09 212504.png"  div align=center />



按数据类型划分
字节流：按照字节读取数据（InputStream、OutputStream）
<img src="./pictures/Annotation 2019-11-09 154646.png"  div align=center />
字符流：按照字符读取数据（Reader、Writer），因为文件编码的不同，从而有了对字符进行高效操作的字符流对象。（GBK，UTF8，Unicode）
<img src="./pictures/Annotation 2019-11-09 154738.png"  div align=center />
原理：底层还是基于字节流操作，自动搜寻了指定的码表。

## File类
#### 文件操作API
<img src="./pictures/Annotation 2019-11-09 163129.png"  div align=center />

注意
1. exist()是否存在,isFile()是否是文件,isDirectory()是否是文件夹，返回true或者false。exist()，isFile()，isDirectory()一般配合if语句去控制对各种文件的操作
2. 若文件不存在isFile()和isDirectory()都返回false
3. 若文件存在，则createNewFile()创建失败，但并不报错，所给路径下文件夹有任一不存在时报错
4. getPath()返回值是基于构建时所给的路径，相对路径则返回相对路径，绝对时则输出绝对路径，而getAbsolutePath获取的是绝对路径
5. islength()返回文件的字节数（文件夹返回0）
6. createNewFile()无法创建文件夹，即便不加文件后缀，createNewFile()和delete()返回值也是true和false，操作成功返回true（con，com为设备名无法这类名称的文件）

#### 文件夹操作API

<img src="./pictures/Annotation 2019-11-09 165307.png"  div align=center />

注意
1. mkdir()需要确保路径上所有文件夹都存在，mkdirs()没有则创建，操作成功true,失败false
2. listFile是仅包含直接下级所有文件和文件夹

#### 文件编码
字符集：Java字符使用16位的双字节存储（Unicode-16），但是在实际文件存储的数据有各种字符集，需要正确操作，否则就有乱码的发生。
<img src="./pictures/Annotation 2019-11-09 204029.png"  div align=center />
utf-8英文字符用1B表示，中文字符用3B表示
UTF-16每个字符都用2B表示，有一定的空间浪费。
GBK（ANSI）中文2B，英文1B。

**乱码问题**
1. 字节数不够

2. 字符集不统一
```java
public static void main(String[] args) throws UnsupportedEncodingException {
        String msg = "性命生命使命";
        byte[] datas = msg.getBytes();
        System.out.println(datas.length);

        //字节数不够
        msg = new String(datas, 0, datas.length-2, "utf8");
        System.out.println(msg);
        //字符集不统一
        msg = new String(datas, 0, datas.length, "GBK");
        System.out.println(msg);
    }
```

输出结果
<img src="./pictures/Annotation 2019-11-09 211918.png"  div align=center />

#### 四个抽象类
熟悉以下的常用方法
<img src="./pictures/Annotation 2019-11-09 212645.png"  div align=center />



</br>涉及的File即计算机文件的都需要通过操作系统间接读取，使用后需要释放资源，而ByteArray是一段内存，java虚拟机可以直接访问，释放也由java回收机制gc释放</br>
<img src="./pictures/Annotation 2019-11-14 210217.png"  div align=center />
ByteArrayOutputStram()  不需要传地址 

### 装饰器（GoF）
1、抽象组件：需要装饰的抽象对象（接口或抽象父类）
2、具体组件：需要装饰的对象
3、抽象装饰类：包含了对抽象组件的引用以及装饰着共有的方法
4、具体装饰类：起具体装饰作用的具体类

```java
public class IoDecorateCoffee181 {
    public static void main(String[] args) {
        //new的是具体类
        Drink coffee = new Coffee();
        Drink sugar = new Sugar(coffee);
        System.out.println(sugar.info()+"-->"+sugar.cost());
        Drink milk = new Milk(coffee);
        System.out.println(milk.info()+"-->"+milk.cost());
        Drink mix = new Milk(sugar);
        System.out.println(mix.info()+"-->"+mix.cost());

    }
}

/**
 * 抽象组件
 */
interface Drink{
    String info();
    double cost();
}

/**
 * 具体组件，需要装饰的对象
 */
class Coffee implements Drink{
    private double price=10;
    private String name = "原味咖啡";
    @Override
    public String info(){
        return name;
    }
    @Override
    public double cost(){
        return price;
    }
}

/**
 * 抽象装饰类
 */

abstract class Decorate implements Drink{
    private Drink drink;
    public Decorate(Drink drink){
        this.drink = drink;
    }
    @Override
    public double cost(){
        return this.drink.cost();
    }
    @Override
    public String info(){
        return this.drink.info();
    }
}
/**
 * 具体装饰类：起具体装饰作用的具体类
 */

class Milk extends Decorate{
    public Milk(Drink drink){
        //调用父类有相同形参的构造方法
        super(drink);
    }
    @Override
    public double cost(){
        return super.cost()*4;
    }
    @Override
    public String info(){
        return super.info()+"加入了牛奶";
    }
}

class Sugar extends Decorate{
    public Sugar(Drink drink){
        //调用父类有相同形参的构造方法
        super(drink);
    }
    @Override
    public double cost(){
        return super.cost()+2;
    }
    @Override
    public String info(){
        return super.info()+"加入了糖";
    }
}
```

输出结果
<img src="./pictures/Annotation 2019-11-15 092928.png"  div align=center />

<br>
IO的装饰类主要有

1. BufferInputStream/BufferOutputStream
2. BufferReader/BufferWriter
3. DataInputStram/DataOutStream（按java类型输入输出）
4. ObjectInputStream（反序列化）/ObjectOutputStream(序列化)对象必须实现Serializable接口
5. PrintStream（System.out是用这个包装类）/PrintWriter（与PrintStream差不多）</br>

#### RamdomAccessFile
随机查找文件位置，seek可指定开始位置

### CommonsIO
是Apache开源的io操作库