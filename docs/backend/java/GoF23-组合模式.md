## 组合模式
* 使用组合模式的场景：
把部分和整体的关系用树形结构来表示，从而使客户端可以使用统一的方式处理部分对象和整体对象。
* 组合模式核心：
-抽象构件（Component）角色：定义了叶子和容器构件的共同点
-叶子（Leaf）构件角色：无子节点
-容器（Composite）构件角色：有容器特征，可以包含子节点

组合模式为处理树形结构提供了完美的解决方案，描述了如何将容器和叶子进行递归组合，使得用户在使用时可以一致性的对待容器和叶子。
当容器对象的指定方法被调用时，将遍历整个树形结构，寻找也包含这个方法的成员，并调用执行。其中，使用了递归调用的机制对整个结构进行处理。

```java
package GOF23.Composite;

import java.util.ArrayList;
import java.util.List;

class Test{
    public static void main(String[] args) {
        AbstractFile f2, f3, f4;

        f2 = new ImageFile("迪丽热巴.jpg");
        f3 = new VideoFile("上海堡垒.mp4");

        Folder f1 = new Folder("我的收藏");
        f1.add(f2);
        f1.add(f3);
        f1.killVirus();
    }
}

public interface AbstractFile {
    void killVirus();
}

class ImageFile implements AbstractFile{

    private  String name;

    public ImageFile(String name) {
        this.name = name;
    }

    @Override
    public void killVirus() {
        System.out.println("----图像文件："+name+",进行查杀！");

    }
}

class VideoFile implements AbstractFile{

    private  String name;

    public VideoFile(String name) {
        this.name = name;
    }

    @Override
    public void killVirus() {
        System.out.println("----视频文件："+name+",进行查杀！");

    }
}

class Folder implements AbstractFile{

    private String name;
    private List<AbstractFile> list = new ArrayList<AbstractFile>();

    public Folder(String name) {
        this.name = name;
    }

    public void add(AbstractFile file){
        list.add(file);
    }

    public void remove(AbstractFile file){
        list.remove(file);
    }

    public AbstractFile getChild(int index){
        return list.get(index);
    }
    @Override
    public void killVirus() {
        System.out.println("----文件夹："+name+",进行查杀！");
        for(AbstractFile file:list){
            file.killVirus();
        }
    }
}
```

叶子结点和容器有相同的操作（继承同一接口），不同的是容器有更多功能

开发中的应用场景：
-操作系统的资源管理器-GUI中的容器层次图
-XML文件解析
-OA系统中，组织结构的处理
-Junit单元测试框架
-----底层设计就是典型的组合模式，TestCase（叶子）、TestUnite（容器）、Test接口（抽象）