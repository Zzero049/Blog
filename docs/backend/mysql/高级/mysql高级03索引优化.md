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
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-23 163813.png"  div align=center />

## 7种Join连接

### 内连接
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-23 170425.png"  div align=center />

```sql
SELECT <select_list>
FROM TableA A
INNER JOIN TableB B
ON A.key = B.key;
```

### 左外连接
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-23 170300.png"  div align=center />


<br>例子：查找女神表对应的男朋友表中的男朋友信息,没有男朋友时信息为NULL

```sql
SELECT <select_list>
FROM TableA A
LEFT JOIN TableB B
ON A.key = B.key;
```

<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-23 170718.png"  div align=center />

<br>例子：查找女神表中的有男朋友的对应信息,没有男朋友的女神不显示


### 右外连接
右外连接和左外连接是对称的

<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-23 171202.png"  div align=center />


```sql
SELECT <select_list>
FROM TableA A
RIGHT JOIN TableB B
ON A.key = B.key;
```

<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-23 171237.png"  div align=center />


```sql
SELECT <select_list>
FROM TableA A
RIGHT JOIN TableB B
ON A.key = B.key
WHERE A.key IS NULL；
```

### 全外连接
**mysql 不支持全外连接**
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-23 171313.png"  div align=center />

```sql
SELECT <select_list>
FROM TableA A
FULL OUTER JOIN TableB B
ON A.key = B.key

```

<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-23 202538.png"  div align=center />
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
mysql中会自动为主键（PRIMARY KEY），唯一值（UNIQUE）建立索引。（还有一种FULLTEXT全文索引）
- 单值索引
即一个索引只包含单个列，一个表可以有多个单列索引
- 唯一索引
索引列的值必须唯一，但允许有空值
- 复合索引
即一个索引包含多个列

#### 索引基本语法
**创建索引**
写法一：
``` sql
# 唯一索引带UNIQUE，单值则为表中只选一列
CREATE [UNIQUE] INDEX indexName ON mytable(columnname(length));
```
写法二：
```sql
ALTER mytable ADD [UNIQUE] INDEX [indexName] ON(columnname(length));
```

**删除**
```sql
DROP INDEX [indexName]ON mytable;
```

**查看**
```sql
SHOW INDEX FROM tbl_emp;
```

**修改**
有四种方式来添加数据表的索引：
```sql
# 该语句添加一个主键，这意味着索引值必须是唯一的，且不能为NULL。(主键是唯一索引)
ALTER TABLE tbl_name ADD PRIMARY KEY(column_list);

# 这条语气创建索引的值必须是唯一的（除了NULL外，NULL可能会出现多次）。
ALTER TABLE tbl_name ADD UNIQUE index_name(column_list);

# 添加普通索引，索引值可出现多次。
ALTER TABLE tbl_ame ADD INDEX index_name(column_list);

# 该语指定了索引为FULLTEXT，用于全文索引。
ALTER TABLE tbl_name ADD FULLTEXT index name(column list);
```

### mysql索引结构
这里简要举B树的例子
1. B树
<img src="./pictures/Annotation 2019-12-23 221000.png"  div align=center />

【初始化介绍】
一颗b+树，浅蓝色的块我们称之为一个磁盘块，可以看到每个磁盘块包含几个数据项（深蓝色所示）和指针（黄色所示），如磁盘块1包含数据项17和35，包含指针P1、P2、P3，P1表示小于17的磁盘块，P2表示在17和35之间的磁盘块，P3表示大于35的磁盘块。

**真实的数据存在于叶子结点即3、5、9、10、13、15、28、29、36、60、75、79、90、99。**

<span style='color: red'>非叶子节点只不存储真实的数据，只存储指引搜素方向的数据项</span>，如17、35并不真实存在于数据表中

【查找过程】
如果要查找数据项29，那么首先会把磁盘块1由磁盘加载到内存，此时发生一次IO，在内存中用二分查找确定29在17和35之间，锁定磁盘块1的P2指针，内存时间因为非常短（相比磁盘的IO）可以忽略不计，通过磁盘块1的P2指针的磁盘地址把磁盘块3由磁盘加载到内存，发生第二次IO，29在26和30之间，锁定磁盘块3的P2指针，通过指针加载磁盘块8到内存，发生第三次IO，同时内存中做二分查找找到29，结束查询，总计三次IO。

真实的情况是，3层的b+树可以表示上百万的数据，如果上百万的数据查找只需要三次IO，性能提高将是巨大的，如果没有索引，每个数据项都要发生一次IO，那么总共需要百万次的IO，显然成本非常非常高。

2. Hash索引
3. full-text全文索引
4. R-Tree索引

### 建立索引的情况
1. 主键自动建立唯一索引
2. 频繁作为查询条件的字段应该创建索引
3. 查询中与其它表关联的字段，外键关系建立索引
4. 频繁更新的字段不适合创建索引。因为每次更新不单单是更新了记录还会更新索引
5. Where条件里用不到的字段不创建索引
6. 单键/组合索引的选择问题，who？（在高并发下倾向创建组合索引）
7. 查询中排序的字段，排序字段若通过索引去访问将大大提高排序速度（order by顺序应与索引建立顺序一致）
8. 查询中统计或者分组字段


### 不要建立索引的情况
1. 表记录太少
2. 经常增删的表
3. 数据重复且分布平均的表字段（该键的值差异不大），因此应该只为最经常查询和最经常排序的数据列建立索引。
注意，如果某个数据列包含许多重复的内容，为它建立索引就没有太大的实际效果。

假如一个表有10万行记录，有一个子段A只有T和F两种值，且每个值的分布概率大约为50%，那么对这种表A字段建索引一般不会提高数据库的查询速度。
索引的选择性是指索引列中不同值的数目与表中记录数的比。如果一个表中有2000条记录，表索引列有1980个不同的值，那么这个索引的选择性就是1980/2000=0.99。
一个索引的选择性越接近于1，这个索引的效率就越高。
## 性能分析
### MySQL Query Optimizer
1、Mysql中有专门负责优化SELECT语句的优化器模块，主要功能：通过计算分析系统中收集到的统计信息，为客户端请求的Query提供他队为最优的执行计划（他认为最优的数据检索方式，但不见得是DBA认为是最优的，这部分最耗费时间）

2、当客户端向MySQL 请求一条Query，命令解析器模块完成请求分类，区别出是SELECT并转发给MySQL Query Optimizer时，MySQL Query Optimizer 首先会对整条Query进行优化，处理掉一些常量表达式的预算，直接换算成常量值。并对Query中的查询条件进行简化和转换，如去掉一些无用或显而易见的条件、结构调整等。然后分析Query中的Hint信息（如果有），看显示Hint信息是否可以完全确定该Query的执行计划。如果没有Hint 或Hint 信息还不足以完全确定执行计划，则会读取所涉及对象的统计信息，根据Query进行写相应的计算分析，然后再得出最后的执行计划。

### MySQL常见瓶颈
- CPU:CPU在饱和的时候一般发生在数据装入内存或从磁盘上读取数据时候
- IO：磁盘I/O瓶颈发生在装入数据远大于内存容量的时候
- 服务器硬件的性能瓶颈：top，free，iostat和vmstat来查看系统的性能状态
- 索引优化

### EXPLAIN
使用EXPLAIN关键字可以模拟优化器执行SQL查询语句，从而知道MySQL是如何处理你的SQL语句的。分析你的查询语句或是表结构的性能瓶颈
#### 功能
- 表的读取顺序(看id)
- 数据读取操作的操作类型(看select_type)
- 哪些索引可以使用(看possible_key)
- 哪些索引被实际使用(看key)
- 表之间的引用(ref)
- 每张表有多少行被优化器查询(rows)
#### 如何使用
- Explain+SQL语句
- 执行计划包含的信息

查询出的表头：
|id|select_type|table|type|possible_keys|key|key_len|ref|rows|extra|
|------------|----|----|----|----|----|----|----|----|----|

表头字段解释：
1. **id**
可以来解析出表的读取顺序，select查询的序列号，包含一组数字，表示查询中执行select子句或操作表的顺序
    - id相同，执行顺序由上至下
    - id不同，如果是子查询，id的序号会递增，id值越大优先级越高，越先被执行
    - id有相同有不同，结合上述两个规则

2. select_type
查询的类型，主要是用于区别普通查询、联合查询、子查询等的复杂查询
    - **SIMPLE:**
    简单的select查询，查询中不包含子查询或者UNION
    - **PRIMARY:**
    查询中若包含任何复杂的子部分，最外层查询则被标记为
    - **SUBQUERY:**
    在SELECT或WHERE列表中包含了子查询
    - **DERIVED:**  
        - 在FROM列表中包含的子查询被标记为DERIVED（衍生）
        - MySQL会递归执行这些子查询，把结果放在临时表里。
    - **UNION:** 
        - 若第二个SELECT出现在UNION之后，则被标记为UNION
        - 若UNION包含在FROM子句的子查询中，外层SELECT将被标记为：DERIVED
    - **UNION RESULT:**
    从UNION表获取结果的SELECT

    示例：
    ```sql
    explain
    select * from tbl_emp a left join tbl_dept b on a.deptId =b.id 
    union 
    select * from tbl_emp a right join tbl_dept b on a.deptId =b.id;
    ```

    <img src="./pictures/Annotation 2019-12-24 155244.png "  div align=center />
    <img src="./pictures/Annotation 2019-12-24 155129.png"  div align=center />

3. table
显示这一行的数据是关于哪张表的

4. **type**
显示表查询属于哪种类型，常用的有以下八个值:
    |ALL|index|range|ref|eq_ref|const|system|NULL|
    |---|---|---|---|---|---|---|---|
   
    从最好到最差依次是:
system>const>eq_ref>ref>range>index>ALL
一般来说，得保证查询至少达到range级别，最好能达到ref。
    - **system**
    表只有一行记录（等于系统表），这是const类型的特例，平时一般不会出现。
    - **const**
    表示通过索引一次就找到了，const用于比较primary key或者unique索引。因为只匹配一行数据，所以很快如将主键置于where列表中，MySQL就能将该查询转换为一个常量
    - **eq_ref**
    唯一性索引扫描，对于每个索引键，表中只有一条记录与之匹配。常见于主键或唯一索引扫描(查一个公司的ceo，只有一个)
    - **ref**
    非唯一性索引扫描，返回匹配某个单独值的所有行。本质上也是一种索引访问，它返回所有匹配某单独值的行，然而，它可能会找到多个符合条件的行，所以他应该属于查找和扫描的混合。（查一个公司的程序员，有一堆）
    - **range**
    只检索给定范围的行，使用一个索引来选择行。key列显示使用了哪个索引一般就是在你的where语句中出现了between、<、>、in等的查询这种范围扫描索引扫描比全表扫描要好，为它只需要开始于索引的某一点，而结束语另一点，不用扫描全部索引。
    - **index**
    Full Index Scan，index与ALL区别为index类型只遍历索引树。这通常比ALL快，因为索引文件通常比数据文件小（也就是说虽然all和Index都是读全表但index是从索引中读取的，而all是从硬盘中读的）
    - **all** 
    Full Table Scan，将遍历全表以找到匹配的行

5. possible_keys
显示可能应用在这张表中的索引，一个或多个。
查询涉及到的字段上若存在索引，则该索引将被列出，**但不一定被查询实际使用**

6. **key**
实际使用的索引。如果为NULL，则没有使用索引查询中
<span style='color:red'>若使用了覆盖索引，则该索引仅出现在key列表中<span>

7. key_len
    - 表示索引中使用的字节数，可通过该列计算查询中使用的索引的长度。在不损失精确性的情况下，长度越短越好
    - key_len显示的值为索字段的**最大可能长度，并非实际使用长度**，即key_len是根据表定义计算而得，不是通过表内检索出的

8. ref
显示索引的哪一列被使用了，如果可能的话，是一个常数。哪些列或常量被用于查找索引列上的值(注意与type的ref区别)，常见的值有const，某数据库某表的某字段。

9. **rows**
根据表统计信息及索引选用情况，大致估算出找到所需的记录所需要读取的行数（越小越好）

10. **extra**
包含不适合在其他列中显示但十分重要的额外信息
     - **Using filesort**
        - 说明mysql会对数据使用一个外部的索引排序，而不是按照表内的索引顺序进行读取。（慢,尽快优化）
        - MySQL中无法利用索引完成的排序操作称为“文件排序”

    - **Using temporary**
    使了用临时表保存中间结果，MySQL在对查询结果排序时使用临时表。常见于排序order by和分组查询 group by。（更加慢，尽量保持索引和group by顺序相同）

    - **Using index**
        - 表示相应的select操作中使用了覆盖索引（Covering Index），避免访问了表的数据行，效率不错！
        - 如果同时出现using where，表明索引被用来执行索引键值的查找；
        - 如果没有同时出现using where，表明索引用来直接读取数据而不执行查找动作。
        - **覆盖索引**
        select的数据列只用从索引中就能够取得，不必读取数据行，MySQL可以利用索引返回select列表中的字段，而不必根据索引再次读取数据文件，换句话说查询列要被所建的索引覆盖。

    - Using where
    表明使用了Where过滤

    - Using join buffer
    使用了连接缓存

    - impossible where
    where子句的值总是false的，不可能从where中获得元组

    - select table optimized away
    在没有GROUPBY子句的情况下，基手索引优化MIN/MAX操作或者对于MyISAM存储引擎优COUNT（*）操作，不必等到执行阶段再进行计算，查询执行计划生成的阶段即完成优化。
    - distinct
    优化distinct操作，在找到第一匹配的元组后即停止找同样值的动作

## 示例
### 单表优化
```sql
# 建表
CREATE TABLE IF NOT EXISTS article(
id INT(10 ) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
author_id INT(10) UNSIGNED NOT NULL,
category_id INT(10) UNSIGNED NOT NULL,
views INT(10) UNSIGNED NOT NULL,
comments INT(10) UNSIGNED NOT NULL,
title VARBINARY(255) NOT NULL,
content TEXT NOT NULL
);

# 插入数据
INSERT INTO article(author_id, category_id,views, comments, title, content) VALUES
(1,1,1,1,1,1),
(2,2,2,2,2,2),
(1,1,3,3,3,3);

# 查询 category_id为1且comments大于1的情况下，views最多的article_id。
# 没建索引的type是all且extra出现了Using filesort
EXPLAIN SELECT id,author_id FROM article
WHERE category_id=1 AND comments>1
ORDER BY views DESC 
LIMIT 1;

# 建立索引
CREATE INDEX idx_article_ccv ON article(category_id,comments,views);

# 再次查询
# 结果key用上了刚建立的索引，但是依旧有using filesort的问题
# 因为在comments>1处索引失效，尽量用常量的条件得以解决（如comments=1）

# 删除索引
DROP INDEX idx_article_ccv ON article;

```

但是我们已经建立了索引，为啥没用呢？

这是因为按照BTree索引的工作原理，先排序 category_id，如果遇到相同的category_id 则再排序 comments，如果遇到相同的comments 则再排序Views。
当comments字段在联合索引里处于中间位置时，
因comments>1条件是一个范围值（所谓 range），
MySQL 无法利用索引再对后面的views部分进行检索，即range类型查询字段后面的索引无效。

优化：
```sql
# 创建索引
CREATE INDEX idx_article_cv ON article(category_id, views);

# 再次查询，没有Using filesort了
EXPLAIN SELECT id,author_id FROM article
WHERE category_id=1 AND comments>1
ORDER BY views DESC 
LIMIT 1;
```

### 两表优化

```sql
# 建表
CREATE TABLE IF  NOT EXISTS class(
id INT(10) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
card INT(10) UNSIGNED NOT NULL
);

CREATE TABLE IF NOT EXISTS book(
bookid INT(10) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
card INT(10) UNSIGNED NOT NULL
);

# 插入数据 各20条
INSERT INTO class(card) VALUES(FLOOR(1+(RAND()*20)));
INSERT INTO book(card) VALUES(FLOOR(1+(RAND()*20)));

# 查看左外连接，type都是ALL
EXPLAIN SELECT * FROM class LEFT JOIN book ON book.`card`=class.`card`;

# 尝试建立索引，在右表上
ALTER TABLE book ADD INDEX Y(card);

# 再次查询，右表type变为ref，rows变为1，出现Using index，左表与原先一样

# 尝试建立索引，在左表上
ALTER TABLE book ADD INDEX Y(card);

# 再次查询，左表type变为index，出现Using index，rows不变还是20，右表与原先一样
```
结论：
这是由左连接特性决定的。LEFT JOIN条件用于确定如何从右表搜索行，左边一定都有，所以右表是我们的关键点，一定需要建立索引。同理右连接RIGHT JOIN也是一样的

### 三表优化


```sql
# 再建一张表，把刚才的索引全部删除
CREATE TABLE IF NOT EXISTS phone(
phoneId INT(10) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
card INT(10) UNSIGNED NOT NULL
);
# 查询，发现type是3个ALL
EXPLAIN SELECT * FROM class LEFT JOIN book ON book.`card`=class.`card`
LEFT JOIN phone
ON phone.`card`=class.`card`;

# 增加索引，按照两表优化的规则
ALTER TABLE book ADD INDEX Y(card);
ALTER TABLE phone ADD INDEX Z(card);
# 后2行的type都是ref 且总rows优化很好，效果不错。
# 因此索引最好设置在需要经常查询的字段中。
```

Join语句优化
1. <span style='color:red'>尽可能减少Join语句中的NestedLoop的循环总次数；“永远用小结果集驱动大的结果集”。</span>（即，小表驱动大表）
1. 优先优化NestedLoop的内层循环；
1. 保证Join语句中被驱动表上Join条件字段已经被索引
1. 当无法保证被驱动表的Join条件字段被索引且内存资源充足的前提下，不要太吝惜JoinBuffer的词置；

## 索引失效

以下表和索引为例
```sql
# 创建表
CREATE TABLE staffs1(
id INT PRIMARY KEY AUTO_INCREMENT,
NAME VARCHAR(24) NOT NULL DEFAULT '姓名',
age INT NOT NULL DEFAULT 0 ,
pos VARCHAR(20) NOT NULL DEFAULT  '职位',
add_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '入职时间'
)CHARSET utf8 COMMENT'员工记录表';

# 插入数据
INSERT INTO staffs(NAME,age,pos,add_time) VALUES('z3',22,'manager',NOW());
INSERT INTO staffs(NAME,age,pos,add_time) VALUES('July',23,'dev',NOW());
INSERT INTO staffs(NAME,age,pos,add_time) VALUES('kk',23,'dev',NOW());

# 建立索引
ALTER TABLE staffs ADD INDEX idx_staffs_nameAgePos(NAME,age,pos);
```

失效原因:
1. 全值匹配select *
2. 最佳左前缀法则
    如果索引了多列，要遵守最左前缀法则。指的是查询从索引的最左前列开始并且不跳过索引中的列。例子：
    ```sql
    # 索引用不上 type 变成all
    EXPLAIN SELECT* FROM staffs WHERE age=23 AND pos='dev';
    EXPLAIN SELECT* FROM staffs WHERE  pos='dev';

    # 索引用上了，但只用上了name字段的索引ref只有一个const
    EXPLAIN SELECT* FROM staffs WHERE  name = 'July' and pos='dev';
    ```
3. 不在索引列上做任何操作（计算、函数、（自动or手动）类型转换），会导致索引失效而转向全表扫描，例子：
    ```sql
    # 索引用上了
    EXPLAIN SELECT * FROM staffs WHERE NAME='July';
    # 索引没用上，left函数类似substr
    EXPLAIN SELECT * FROM staffs WHERE LEFT(NAME,4)='July';
    ```
4. 存储引擎不能使用索引中范围条件右边的列
    ```sql
    # 索引成功使用
    EXPLAIN SELECT * FROM staffs 
    WHERE NAME='July' AND age=25 AND pos='manageer';
    # type变为range，范围之后全失效（pos）
    EXPLAIN SELECT * FROM staffs 
    WHERE NAME='July' AND age>25 AND pos='manageer';
    ```
5. 尽量使用覆盖索引（只访问索引的查询（索引列和查询列一致）），减少select *
    ```sql
    EXPLAIN SELECT * FROM staffs 
    WHERE NAME='July' AND age=25 AND pos='manageer';
    # 改为
    EXPLAIN SELECT name,age,pos FROM staffs 
    WHERE NAME='July' AND age=25 AND pos='manageer';
    ```
6. mysql在使用不等于（！=或者<>）的时候无法使用索引会导致全表扫描
    ```sql
    #type为ALL，key为NULL
    EXPLAIN SELECT name,age,pos FROM staffs 
    WHERE NAME!='July';
    ```
7. is null，is not null 也无法使用索引
8. like以通配符开头（%abc...）mysql索引失效会变成全表扫描的操作
    ```sql
    # %July,%July%为全表扫描，而July% type为range
    # 尽量避免%开头的搜索，且不能为select *
    EXPLAIN SELECT * FROM staffs 
    WHERE NAME like '%July%';
    # 运用了覆盖索引，type为index
    EXPLAIN SELECT age,pos FROM staffs 
    WHERE NAME like '%July%';
    ```
9. 字符串不加单引号索引失效
    ```sql
    # 正常
    EXPLAIN SELECT age,pos FROM staffs 
    WHERE NAME = '2000';
    # sql会隐式的类型转换，触犯第三条
    EXPLAIN SELECT age,pos FROM staffs 
    WHERE NAME = 2000;
    ```
10. 少用or，用它来连接时会索引失效
    ```sql
    # 索引失效
    EXPLAIN SELECT age,pos FROM staffs 
    WHERE NAME = 'z3' or NAME='July';
    ```

总结表
<img src="./pictures/Annotation 2019-12-25 141441.png "  div align=center />
全值匹配我最爱，最左前缀要遵守；
带头大哥不能死，中间兄弟不能断；
索引列上少计算，范围之后全失效；
LIKE百分写最右，覆盖索引不写星；
不等空值还有or，索引失效要少用；
VAR引号不可丢，SQL高级也不难！