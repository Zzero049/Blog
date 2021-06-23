## 备忘录模式
场景：
-录入大批人员资料。正在录入当前人资料时，发现上一个人录错了，此时需要恢复上一个人的资料，再进行修改。
-Word文档编辑时，忽然电脑死机或断电，再打开时，可以看到word提示你恢复到以前的文档
-管理系统中，公文撤回功能。公文发送出去后，想撤回来。

核心
-就是保存某个对象内部状态的拷贝，这样以后就可以将该对象恢复到原先的状态。
结构：
-源发器类Originator（需要备忘的类）
-备忘录类Memento（备忘录）
-负责人类CareTake（管理一份或多份（list或stack实现）备忘录）

```java
public class Test {
    public static void main(String[] args) {
        CareTaker taker = new CareTaker();
        EmpOriginator emp = new EmpOriginator(20,50000);
        System.out.println("年龄:"+emp.getAge()+"-->工资:"+emp.getSalary());
        taker.setMemento(emp.memento());//一次备份

        emp.setAge(40);
        emp.setSalary(1000000);
        System.out.println("年龄:"+emp.getAge()+"-->工资:"+emp.getSalary());
        //还原
        emp.recover(taker.getMemento());
        System.out.println("年龄:"+emp.getAge()+"-->工资:"+emp.getSalary());
    }
}

/**
 * 源发器
 */
class EmpOriginator{
    private int age;
    private int salary;

    public EmpOriginator(int age, int salary) {
        this.age = age;
        this.salary = salary;
    }

    public void setSalary(int salary) {
        this.salary = salary;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public int getSalary() {
        return salary;
    }

    public int getAge() {
        return age;
    }

    public Memento memento(){
        return new Memento(this);
    }

    public void recover(Memento memento){
        this.age = memento.getAge();
        this.salary = memento.getSalary();
    }
}
/**
 * 备忘录
* */

class Memento{
    private EmpOriginator originator;
    private int age;
    private int salary;

    public Memento(EmpOriginator originator) {
        this.originator = originator;
        this.age = originator.getAge();
        this.salary = originator.getSalary();
    }

    public int getSalary() {
        return salary;
    }

    public void setSalary(int salary) {
        this.salary = salary;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public int getAge() {
        return age;
    }
}

/**
 * 负责人
 */
class CareTaker{
    private Memento memento;

    public void setMemento(Memento memento) {
        this.memento = memento;
    }

    public Memento getMemento() {
        return memento;
    }
}
```

开发中常见的应用场景：
-棋类游戏中的，悔棋
-普通软件中的，撤销操作
-数据库软件中的，事务管理中的，回滚操作
-Photoshop软件中的，历史记录