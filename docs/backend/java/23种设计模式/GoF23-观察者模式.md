## 观察者模式
·场景：
-聊天室程序的创建。服务器创建好后，A，B，C三个客户端连上来公开聊天。A向服务器发送数据，服务器端聊天数据改变。我们希望将这些聊天数据分别发给其他在线的客户。也就是说，每个客户端需要更新服务器端得数据。
-网站上，很多人订阅了"java主题”的新闻。当有这个主题新闻时，就会将这些新闻发给所有订阅的人。
-大家一起玩CS游戏时，服务器需要将每个人的方位变化发给所有的客户。
上面这些场景，我们都可以使用观察者模式来处理。我们可以把多个订阅者、客户称之为观察者（被动接受）；需要同步给多个订阅者的数据封装到对象中，称之为目标。

<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-09 161736.png"  div align=center />

```java
public class Test {
    public static void main(String[] args) {
        ConcreteSubject subject = new ConcreteSubject();

        ObserverA observer1 = new ObserverA();
        ObserverA observer2 = new ObserverA();
        ObserverA observer3 = new ObserverA();

        subject.registerObserver(observer1);
        subject.registerObserver(observer2);
        subject.registerObserver(observer3);

        subject.setState(300);

        System.out.println(observer1.getMyState());
        System.out.println(observer2.getMyState());

        subject.setState(5000);

        System.out.println(observer1.getMyState());
        System.out.println(observer2.getMyState());



    }
}


class Subject{

    protected List<Observer> list = new ArrayList<>();

    public void registerObserver(Observer obs){
        list.add(obs);
    }

    public void removeObeserver(Observer obs){
        list.remove(obs);
    }

    public void notifyAllObservers(){
        for(Observer obs:list){
            obs.update(this);
        }
    }
}

class ConcreteSubject extends Subject{
    private int state;

    public void setState(int state) {
        this.state = state;
        this.notifyAllObservers();
    }

    public int getState() {
        return state;
    }

}

interface Observer{
    //更新的是容器内的观察者
    void update(Subject subject);
}

class ObserverA implements Observer{
    private int myState;

    @Override
    public void update(Subject subject) {
        myState = ((ConcreteSubject)subject).getState();

    }

    public void setMyState(int myState) {
        this.myState = myState;
    }

    public int getMyState() {
        return myState;
    }
}
```

可以把State想象成游戏的服务器，状态发生变化时，就把观察者（玩家）与自己的状态更新成一致。
