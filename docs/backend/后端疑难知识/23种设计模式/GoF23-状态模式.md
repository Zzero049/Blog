## 状态模式
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-08 204325.png"  div align=center />
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-08 204540.png"  div align=center />

·核心：
-用于解决系统中复杂对象的状态转换以及不同然态下行为的封装问题

·结构：
Context环境类
·环境类中维护一个State对象，他是定义了当前的状态。
-State抽象状态类
ConcreteState具体状态类
·每一个类封装了一个状态对应的行为

```java
class Test{
    public static void main(String[] args) {
        Context c  =new Context();
        c.setState(new FreeSate());
        c.setState(new BookedState());
    }

}

interface State {
    void handle();
}


class FreeSate implements State{

    @Override
    public void handle() {
        System.out.println("房间空闲");
    }
}

class CheckedInState implements State{

    @Override
    public void handle() {
        System.out.println("房间已入住");
    }
}

class BookedState implements State{

    @Override
    public void handle() {
        System.out.println("房间已预订");
    }
}

class Context{
    private State state;

    public void setState(State state) {
        System.out.println("修改状态");
        this.state = state;
        this.state.handle();
    }
}
```

开发中常见的场景：
-银行系统中账号状态的管理
-OA系统中公文状态的管理
-酒店系统中，房间状态的管理
-线程对象各状态之间的切换