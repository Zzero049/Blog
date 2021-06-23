# Stream流式计算

集合、MySQL本质就是存储东西的；

计算都应该交给流来操作！

![image-20200516223137818](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200516223137818.png)

案例：

```java
/**
 * 题目要求：一分钟内完成此题，只能用一行代码实现！
 * 现在有5个用户！筛选：
 * 1、ID必须是偶数
 * 2、年龄必须大子23岁
 * 3、用户名转为大写字母
 * 4、用户名字母倒着排序
 * 5、只输出一个用户！
 */
public class StreamTest {
    public static void main(String[] args) {
        User u1 = new User(1, "a", 21);
        User u2 = new User(2, "b", 22);
        User u3 = new User(3, "c", 23);
        User u4 = new User(4, "d", 24);
        User u5 = new User(5, "e", 25);
        User u6 = new User(6, "e", 26);
        //集合存储
        List<User> list = Arrays.asList(u1, u2, u3, u4, u5, u6);
        //链式编程+lambda+函数式接口+流式计算
        //计算交给流
        list.stream()
                .filter(user -> {
                    return user.getId() % 2 == 0;
                })
                .filter(user -> {
                    return user.getAge() > 23;
                })
                .map(user -> {
                    user.setName(user.getName().toUpperCase());
                    return user;
                })
                .sorted((user1, user2) -> {
                    return -user1.getName().compareTo(user2.getName());
                })
                .limit(1)
                .forEach(System.out::println);
    }

}
```

