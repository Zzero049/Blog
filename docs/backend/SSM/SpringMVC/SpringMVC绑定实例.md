```java
public class Account implements Serializable {
    private String username;
    private String password;
    private Double money;

    private List<User> list;
    private Map<String, User> map;

    public List<User> getList() {
        return list;
    }

    public void setList(List<User> list) {
        this.list = list;
    }

    public Map<String, User> getMap() {
        return map;
    }

    public void setMap(Map<String, User> map) {
        this.map = map;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    @Override
    public String toString() {
        return "Account{" +
                "username='" + username + '\'' +
                ", password='" + password + '\'' +
                ", money=" + money +
                '}';
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public Double getMoney() {
        return money;
    }

    public void setMoney(Double money) {
        this.money = money;
    }
}

```

jsp文件
```jsp
 <form action="param/saveAccount" method="post">
        姓名： <input type="text" name="username" /><br/>
        密码： <input type="text" name="password" /><br/>
        金额： <input type="text" name="money" /><br/>

        用户姓名： <input type="text" name="list[0].uname" /><br/>
        用户年龄： <input type="text" name="list[0].age" /><br/>

        用户姓名： <input type="text" name="map['one'].uname" /><br/>
        用户年龄： <input type="text" name="map['one'].age" /><br/>
         <input type="submit" value="提交" />
```
返回封装到Account里

<img src="pictures/Annotation 2020-04-12 143352.png">

