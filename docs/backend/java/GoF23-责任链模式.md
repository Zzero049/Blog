## 责任链模式

行为型模式汇总：
①责任链模式 chain of responsibility
②命令模式command
③解释器模式 interpreter
④迭代器模式 iterator
⑤中介者模式 mediator
⑥备忘录模式 memento
⑦观察者模式observer
⑧状态模式state
⑨策略模式strategy
⑩模板方法式 template method
11.访问者模式 visitor


定义：
-将能够处理同一类请的对象连成一条链所提交的请求沿着链传递，链上的对象逐个判断是否有能力处理该请求，如果能则处理，如果不能则传递给链上的下一个对象。

场景：
-打牌时，轮流出牌
-接力赛跑
-大学中，奖学金审批
-公司中，公文审批

比如
公司里面，报销个单据需要经过流程：
·申请人填单申请，申请给经理-->小于1000，经理审查-->超过1000，交给总经理审批-->总经理审批通过

公司里面，请假条的审批过程：
如果请假天数小于5天，主任审批-->如果请假天数大于等于5天，小于15天，经理审批-->如果大于等于15天，小于30天，总经理审批-->如果大于等于30天，提示拒绝

```java
public class Test {
    public static void main(String[] args) {
        Request zhang  = new Request("张三",35,"回家休息");
        Leader a = new Director("主管");
        Leader b = new Manager("经理");
        Leader c = new Boss("老板");

        a.setLeader(b);
        b.setLeader(c);
        a.handle(zhang);
    }
}

class Request{
    String name;
    int leaveDay;
    String reason;

    public Request(String name, int leaveDay, String reason) {
        this.name = name;
        this.leaveDay = leaveDay;
        this.reason = reason;
    }

    public int getLeaveDay() {
        return leaveDay;
    }
}

class Leader{
    Leader nextLeader;
    void handle(Request request){}
    public void setLeader(Leader leader){
        this.nextLeader = leader;
    }
}

class Director extends Leader{
    String name;
    public Director(String name) {
        this.name = name;
    }

    @Override
    public void handle(Request request) {
        if(request.getLeaveDay()<5){
            System.out.println(this.name+"同意请假");
        }else{
            super.nextLeader.handle(request);
        }
    }
}

class Manager extends Leader{
    String name;
    public Manager(String name) {
        this.name = name;
    }


    @Override
    public void handle(Request request) {
        if(request.getLeaveDay()<15){
            System.out.println(this.name+"同意请假");
        }else{
            super.nextLeader.handle(request);
        }
    }
}

class Boss extends Leader{
    String name;
    public Boss(String name) {
        this.name = name;
    }

    @Override
    public void handle(Request request) {
        if(request.getLeaveDay()<30){
            System.out.println(this.name+"同意请假");
        }else{
            System.out.println("不想干了？");
        }
    }
}
```

开发中常见的场景：
-Java中，异常机制就是一种责任链模式。一个try可以对应多个catch，当第一个catch不匹配类型，则自动跳到第二个catch.
-Javascript语言中，事件的冒泡和捕获机制。Java语言中，事件的处理采用观察者模式。
-Servlet开发中，过滤器的链式处理
-Struts2中，拦截器的调用也是典型的责任链模式