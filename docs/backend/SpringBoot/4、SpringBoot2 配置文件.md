# 配置文件

## 1.  文件类型

### properties

同以前的properties用法

### yaml

YAML 是 "YAML Ain't Markup Language"（YAML 不是一种标记语言）的递归缩写。在开发的这种语言时，YAML 的意思其实是："Yet Another Markup Language"（仍是一种标记语言）。 

非常适合用来做以数据为中心的配置文件

**基本语法** 

- key: value；kv之间有空格
- 大小写敏感
- 使用缩进表示层级关系
- 缩进不允许使用tab，只允许空格（也可以设置tab设置成4空格，idea自动设置）
- 缩进的空格数不重要，只要相同层级的元素左对齐即可
- '#'表示注释
- 字符串无需加引号，如果要加，''与""表示字符串内容 会被 转义/不转义

**数据类型**

1. 字面量：单个的、不可再分的值。date、boolean、string、number、null

```
k: v
```

2. 对象：键值对的集合。map、hash、set、object 

```yaml
k: 
  k1: v1
  k2: v2
  k3: v3
  
# 行内写法：  k: {k1:v1,k2:v2,k3:v3}
```

3. 数组：一组按次序排列的值。array、list、queue

```yaml
k:
 - v1
 - v2
 - v3
 
# 行内写法：  k: [v1,v2,v3]
```

**示例**

```java
@Data
@Component
@ConfigurationProperties(prefix = "person")
public class Person {
	
	private String userName;
	private Boolean boss;
	private Date birth;
	private Integer age;
	private Pet pet;
	private String[] interests;
	private List<String> animal;
	private Map<String, Object> score;
	private Set<Double> salarys;
	private Map<String, List<Pet>> allPets;
}

@Data
public class Pet {
	private String name;
	private Double weight;
}
```

在yaml表示以上对象，并填入对应值

```yaml
person:
  userName: zhangsan
  boss: false
  birth: 2019/12/12 20:12:33
  age: 18
  pet: 
    name: tomcat
    weight: 23.4
  interests: [篮球,游泳]
  animal: 
    - jerry
    - mario
  score:
    english: 
      first: 30
      second: 40
      third: 50
    math: [131,140,148]
    chinese: {first: 128,second: 136}
  salarys: [3999,4999.98,5999.99]
  allPets:
    sick:
      - {name: tom}
      - {name: jerry,weight: 47}
      - name: wan
        weight: 77.77
    health: [{name: mario,weight: 47},{name: mario2,weight: 427}]
```

注意要在实体类中添加`@ConfigurationProperties(prefix ="person")`注解，即可配置实例属性

''与""表示字符串内容 会被 转义/不转义，不加则默认单引号

- 双引号

```yaml
person:
  userName: "zhangsan \n 李四"
```

在前端回包中和后端输出可见都没有转义进行了计算机中的原生输出

![image-20210322000018633](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210322000018633.png)

- 单引号

```yaml
person:
  userName: 'zhangsan \n 李四'
```

在前端回包中和后端输出可见都进行了一次转义，将\n作为字符输出

![image-20210322000312970](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210322000312970.png)



## 2. 配置提示

由于自定义的类型yaml没有提示，开发不太方便，springboot提供了配置处理器，有提示补全功能

```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-configuration-processor</artifactId>
            <optional>true</optional>
        </dependency>
```

但该配置处理器打包不应该被包括进去，如果被包括打包后依赖占大概113k（SpringBoot2.4.2自动不打包该依赖）

```xml
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.springframework.boot</groupId>
                            <artifactId>spring-boot-configuration-processor</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </build>
```

