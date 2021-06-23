

# Javap与Jclasslib的使用

首先得知道：

我们在idea看到的class文件是经过解析的，根本不是真正意义的class文件上所存储的内容（直接打开class文件跟乱码一样，切换16进制显示即可）

```java
package RunningDateArea.PCRegister;

public class PCRegisterTest {
    public PCRegisterTest() {
    }

    public static void main(String[] args) {
        int i = 10;
        int j = 20;
        int k = i + j;
        String s = "abc";
        System.out.println(i);
        System.out.println(k);
    }
}
```

实际上的class文件是二进制流文件

```java
// 截取部分
00000000: cafe babe 0000 0033 001d 0a00 0600 0f09  .......3........
00000010: 0010 0011 0800 120a 0013 0014 0700 1507  ................
00000020: 0016 0100 063c 696e 6974 3e01 0003 2829  .....<init>...()
00000030: 5601 0004 436f 6465 0100 0f4c 696e 654e  V...Code...LineN
00000040: 756d 6265 7254 6162 6c65 0100 046d 6169  umberTable...mai
00000050: 6e01 0016 285b 4c6a 6176 612f 6c61 6e67  n...([Ljava/lang
00000060: 2f53 7472 696e 673b 2956 0100 0a53 6f75  /String;)V...Sou
00000070: 7263 6546 696c 6501 000f 4865 6c6c 6f57  rceFile...HelloW
00000080: 6f72 6c64 2e6a 6176 610c 0007 0008 0700  orld.java.......
00000090: 170c 0018 0019 0100 0c48 656c 6c6f 2057  .........Hello W
000000a0: 6f72 6c64 2107 001a 0c00 1b00 1c01 000a  orld!...........
000000b0: 4865 6c6c 6f57 6f72 6c64 0100 106a 6176  HelloWorld...jav
000000c0: 612f 6c61 6e67 2f4f 626a 6563 7401 0010  a/lang/Object...
000000d0: 6a61 7661 2f6c 616e 672f 5379 7374 656d  java/lang/System
000000e0: 0100 036f 7574 0100 154c 6a61 7661 2f69  ...out...Ljava/i
000000f0: 6f2f 5072 696e 7453 7472 6561 6d3b 0100  o/PrintStream;..
00000100: 136a 6176 612f 696f 2f50 7269 6e74 5374  .java/io/PrintSt
00000110: 7265 616d 0100 0770 7269 6e74 6c6e 0100  ream...println..
00000120: 1528 4c6a 6176 612f 6c61 6e67 2f53 7472  .(Ljava/lang/Str
00000130: 696e 673b 2956 0021 0005 0006 0000 0000  ing;)V.!........
00000140: 0002 0001 0007 0008 0001 0009 0000 001d  ................
00000150: 0001 0001 0000 0005 2ab7 0001 b100 0000  ........*.......
00000160: 0100 0a00 0000 0600 0100 0000 0100 0900  ................
00000170: 0b00 0c00 0100 0900 0000 2500 0200 0100  ..........%.....
00000180: 0000 09b2 0002 1203 b600 04b1 0000 0001  ................
00000190: 000a 0000 000a 0002 0000 0003 0008 0004  ................

```

javap是jdk自带的**反解析（也说反编译，java的编译分为前端和后端，前端的java编译是java到class文件，后端的编译是字节码到机器码）**工具。它的作用就是根据class字节码文件，反解析出当前类对应的code区（汇编指令）、本地变量表、异常表和代码行偏移量映射表、常量池等等信息。

Jclasslib能实现javap的效果，对class文件进行解析，源码可以可读的查看。使用只需要在idea搜索这个插件，安装重启后，在view-》Show Bytecode With Jclasslib即可使用

![image-20200604173341769](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200604173341769.png)

![image-20200604173128549](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200604173128549.png)

![image-20200604173525317](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200604173525317.png)

Length是指变量有效到PC指令的那一条（对应Code中的指令地址）



上手一下就会了，这里就不多作记录了，先提及这两个工具

