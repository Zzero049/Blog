

# DBUtils

DBUtils 可以帮助开发者完成数据的封装（结果集到Java对象的映射）

使用时，Java实体类的所有字段名要与数据库一致，否则不一致的字段名无法完成封装（Mybatis起别名可以解决）

导入jar包

![image-20200426131341410](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200426131341410.png)

传统方式，需要自己在结果集封装到实体类

```java
String sql="select * from student where id=30";
preparedStatement=connection.prepareStatement(sql); 
resultSet=preparedStatement. executeQuery();
while(resultSet.next()){
    Integer id=resultSet.getInt(1); 
    String name=resultSet. getString(2); 
    Double score=resultSet. getDouble(3);
    Student student = new Student(id,name,score);
}
```

DBUtils 通过 ResultHandler 接口是用来处理结果集，可以将查询到的结果集转换成Java对象，提供了4种实现类。

- BeanHandler                                   将结果集映射成Java对象Student

```java
String sql="select * from student where id=30";
QueryRunner queryRunner= new QueryRunner(); 
Student student =queryRunner.query(connection, sql,new BeanHandler<>(Student.class));
```

- BeanListHandler                             将结果集映射成List集合List<Student>
- MapHandler                                    将结果集映射成Map对象（属性与值全部变为map对象的键值对）

```java
String sql="select * from student where id=30";
QueryRunner queryRunner= new QueryRunner(); 
Map<String, Object> map =queryRunner.query(connection, sql,new MapHandle());
```

- MapListHandler                              将结果集映射成MapList集合

```java
String sql="select * from student";
QueryRunner queryRunner= new QueryRunner(); 
List<Map<String, Object>> list =queryRunner.query(connection, sql,new MapListHandler());
```

