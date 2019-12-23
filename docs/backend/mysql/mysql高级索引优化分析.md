# 索引优化分析

## sql查询出现的问题：
- 性能下降SQL慢
- 执行时间长
- 等待时间长

可能的原因：
- 查询语句写的烂
- 索引失效（建了索引，没用上）
    - 单值
    - 复合
- 关联查询太多join（设计缺陷或不得已的需求）- 服务器调优及各个参数设置（缓冲、线程数等）

----
## 常见通用的Join查询
### SQL执行顺序

人写的sql语句：
```sql
SELECT DISTINCT
    <select list>
FROM
<left_table>
<join_type>JOIN<right table>
ON<join condition>
WHERE<where condition>
GROUP BY
<group_by_list>
HAVING
<having_condition>
ORDER BY
<order by_condition>
LIMIT<limit number>
```

机器解析：（从from开始读）
```sql
FROM<left table>
ON<join condition>
<join_type>JOIN<right_table>
WHERE <where condition>
GROUP BY <group by_list>
HAVING <having_condition>
SELECT DISTINCT <select list>
ORDER BY <order by_condition>
LIMIT<limit number>
```
<img src="./pictures/Annotation 2019-12-23 163813.png"  div align=center />

## 7种Join连接

### 内连接
<img src="./pictures/Annotation 2019-12-23 170425.png"  div align=center />

```sql
SELECT <select_list>
FROM TableA A
INNER JOIN TableB B
ON A.key = B.key;
```

### 左外连接
<img src="./pictures/Annotation 2019-12-23 170300.png"  div align=center />


<br>例子：查找女神表对应的男朋友表中的男朋友信息,没有男朋友时信息为NULL

```sql
SELECT <select_list>
FROM TableA A
LEFT JOIN TableB B
ON A.key = B.key;
```

<img src="./pictures/Annotation 2019-12-23 170718.png"  div align=center />

<br>例子：查找女神表中的有男朋友的对应信息,没有男朋友的女神不显示


### 右外连接
右外连接和左外连接是对称的

<img src="./pictures/Annotation 2019-12-23 171202.png"  div align=center />


```sql
SELECT <select_list>
FROM TableA A
RIGHT JOIN TableB B
ON A.key = B.key;
```

<img src="./pictures/Annotation 2019-12-23 171237.png"  div align=center />


```sql
SELECT <select_list>
FROM TableA A
RIGHT JOIN TableB B
ON A.key = B.key
WHERE A.key IS NULL；
```

### 全外连接
**mysql 不支持全外连接**
<img src="./pictures/Annotation 2019-12-23 171313.png"  div align=center />

```sql
SELECT <select_list>
FROM TableA A
FULL OUTER JOIN TableB B
ON A.key = B.key

```

<img src="./pictures/Annotation 2019-12-23 202538.png"  div align=center />
```sql
SELECT <select_list>
FROM TableA A
FULL OUTER JOIN TableB B
ON A.key = B.key
WHERE A.key IS NULL OR B.key IS NULL;
```



## 索引(Index)
MySQL官方对索引的定义为：索引（Index）是帮助MySQL高效获取数据**的 <span style='color:red'>数据结构</span>。**

可以简单理解为 **“排好序的快速查找数据结构”**

索引的目的在于提高查询效率，可以类比字典，如果要查“mysql”这个单词，我们肯定需要定位到m字母，然后从下往下找到y字母，再找到剩下的sql。如果没有索引（数据在数据库杂乱排序），那么你可能需要a----z，如果我想找到Java开头的单词呢？或者Oracle开头的单词呢？那么每次都要全表扫描。

在数据之外，数据库系统还维护着满足特定查找算法的数据结构，这些数据结构以某种方式引用（指向）数据，这样就可以在这些数据结构上实现高级查找算法。这种数据结构，就是索引。下图就是一种可能的索引方式示例：（二叉查找树）
<img src="./pictures/Annotation 2019-12-23 212647.png"  div align=center />

为了加快Col2的查找，可以维护一个右边所示的二叉查找树，每个节点分别包含索引键值和一个指向对应数据记录物理地址的指针，这样就可以运用二叉查找在一定的复杂度内获取到相应数据，从而快速的检索出符合条件的记录。

一般来说索引本身也很大，不可能全部存储在内存中，因此索引往往以索引文件的形式存储的磁盘上。

我们平常所说的索引，如果没有特别指明，都是指**B树**（多路搜索树，并不一定是二叉的）结构组织的索引。其中聚集索引，次要索引复合索引，前缀索引，唯一索引默认都是使用**B+树**索引，统称索引。当然，除了B+树这种类型的索引之外，还有哈希索引（hash index）等。

### 优点
- **查找：** 类似大学图书馆建书目索引，提高数据检索的效率，降低数据库的IO成本（成本是树高）
- **排序：** 通过索引列对数据进行排序，降低数据排序的成本，降低了CPU的消耗
### 缺点

- **占用空间：** 实际上索引也是一张表，该表保存了主键与索引字段，并指向实体表的记录，所以索引列也是要占用空间的

-  **更新慢：** 虽然索引大大提高了查询速度，同时却会降低更新表的速度，如对表进行INSERT、UPDATE和DELETE。因为更新表时，MySQL不仅要保存数据，还要保一下索引文件每次更新添加了索引列的字段，都会调整因为更新所带来的键值变化后的索引信息
-  **数据量庞大时，索引结构需要研究：** 索引只是提高效率的一个因素，如果你的MySQL有大数据量的表，就需要花时间研究建立最优秀的索引，或优化查询

### 索引分类
#### 单值索引
即一个索引只包含单个列，一个表可以有多个单列索引


- 性能分析
- 索引优化