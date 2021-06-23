## 值得注意的细节

### 变量

![image-20210116163916229](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210116163916229.png)



并非所有对象都能进行取地址操作，但变量总是能正确返回（addressable）。指针运算符为左值时，我们可更新目标对象状态；而为右值时则是为了获取目标状态。

![image-20210116150225119](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210116150225119.png)



![image-20210116153501826](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210116150225119.png)





### 函数

![image-20210116174238636](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210116153501826.png)

![image-20210116180908862](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210116174238636.png)



**闭包**

![image-20210118102047586](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210118102047586.png)

![image-20210118102055051](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210118102047586.png)

![image-20210118102147906](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210118102055051.png)

应用场景

可以通过闭包的记忆效应来实现设计模式中工厂模式的生成器。下面的代码示例展示了创建游戏玩家生成器的过程。

```go
package main

import "fmt"

// 定义一个玩家生成器，它的返回类型为 func() (string, int)，输入名称，返回新的玩家数据
func genPlayer(name string) func() (string, int)  {
	// 定义玩家血量
	hp := 1000
	// 返回闭包
	return func() (string, int) {
		// 引用了外部的 hp 变量, 形成了闭包
		return name, hp
	}
}

func main()  {
	// 创建一个玩家生成器
	generator := genPlayer("犬小哈")

	// 返回新创建玩家的姓名, 血量
	name, hp := generator()

	// 打印
	fmt.Println(name, hp)
}
```

代码输出如下:

```go
犬小哈 1000
```

从上面代码看出，闭包具有面向对象语言的特性 —— **封装性**，变量 `hp` 无法从外部直接访问和修改。





### 数组类型

定义数组类型时，数组长度必须是非负整型常量表达式，长度是类型组成部分。也就是说，元素类型相同，但长度不同的数组不属于同一类型。

与C数组变量隐式作为指针使用不同，Go数组是值类型，**赋值和传参操作都会复制整个数组数据。**

```
a := [...]int{1,2}
```



### 切片类型

切片（slice）本身并非动态数组或数组指针。它内部通过指针引用底层数组，设定相关属性将数据读写操作限定在指定区域内。

```
type slice struct{
	array unsafe.Pointer
	len int
	cap int
}
```

len是切片长度，cap是真实数组长

![image-20210202193547451](https://gitee.com/zero049/MyNoteImages/raw/master/image-20210202193547451.png)

