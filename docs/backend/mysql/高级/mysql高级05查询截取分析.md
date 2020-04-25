# 查询截取分析

### 内容
1. 查询优化
1. 慢查询日志
1. 批量数据脚本
1. show Profile
1. 全局查询日志

### 出现sql执行慢的调整流程

1. 观察，至少跑1天，看看生产的慢SQL情况。
1. 开启慢查询日志，设置阈值，比如超过5秒钟的就是慢SQL，并将它抓取出来。
1. explain+慢SQL分析
1. show profile
1. 运维经理or DBA，进行SQL数据库服务器的参数调优。

## 查询优化
### 小表驱动大表
优化原则：小表驱动大表，即小的数据集驱动大的数据集。

当B表的数据集必须小于A表的数据集时，用in优于exists。
```sql
select * from A  where id in
(select id from B);
```
当A表的数据集系小于B表的数据集时，用exists优于in。
```sql
select * from A where id exists
(select 1 from B
where A.id = B.id
);
```

- EXISTS 
SELECT..FROM table WHERE EXISTS(subquery)
该语法可以理解为：**将主查询的数据，放到子查询中做条件验证，根据验证结果（TRUE或FALSE）来决定主查询的数据结果是否得以保留。**
    - EXISTS（subquery）只返回TRUE 或FALSE，因此子查询中的SELECT*也可以是SELECT 1或Select 'x'，官方说法是实际执行时会忽略SELECT清单，因此没有区别
    - EXISTS子查询的实际执行过程可能经过了忧化而不是我们理解上的逐条对比，如果担忧效率问题，可进行实际检验以确定是否有效率问题。
    - EXISTS子查询往往也可以用条件表达式、其他子查询或者JOIN来替代，何种最优需要具体问题具体分析

### Order by优化
MySql能为排序与查询使用相同的索引
MySql两种排序方式：文件排序或扫描有序索引排序
ORDER BY子句，尽量使用Index方式排序，避免使用FileSort方式排序。

```sql
#建表
CREATE TABLE tblA(
id INT PRIMARY KEY AUTO_INCREMENT,
age INT,
birth TIMESTAMP NOT NULL
);

# 插入数据
INSERT INTO tblA(age,birth) VALUES(22,NOW());
INSERT INTO tblA(age,birth) VALUES(23,NOW());
INSERT INTO tblA(age,birth) VALUES(24,NOW());
# 建立索引（此表3个字段都有索引，后面才用的了select *）
CREATE INDEX idx_A_ageBirth ON tblA(age, birth);

# 不产生filesort
EXPLAIN SELECT * FROM tblA WHERE age>20
ORDER BY age;
EXPLAIN SELECT * FROM tblA WHERE age>20
ORDER BY age,birth;

# 产生filesort
EXPLAIN SELECT * FROM tblA WHERE age>20
ORDER BY birth;
# 索引默认是升序的，现在一升一降，产生内排序filesort
EXPLAIN SELECT * FROM tblA
ORDER BY age ASC, birth DESC;

# 同升同降，不产生filesort
EXPLAIN SELECT * FROM tblA
ORDER BY age DESC, birth DESC;
```

<br>
尽可能在索引列上完成排序操作，遵照索引建的最佳左前缀

如果不在索引列上，filesort有两种算法：mysql就要启动双路排序和单路排序

#### filesort 双路排序
1. MySQL4.1之前是使用双路排序，字面意思就是两次扫描磁盘，最终得到数据，读取行指针和order by列，对他们进行排序，然后扫描已经排序好的列表，按照列表中的值重新从列表中读取对应的数据输出
2. 从磁盘取排序字段，在buffer进行排序，再从磁盘取其他字段。
#### filesort 单路排序
从磁盘读取查询需要的所有列，按照order by列在buffer对它们进行排序，然后扫描排序后的列表进行输出，它的效率更快一些，避免了第二次读取数据。并且把随机IO变成了顺序IO，但是它会使用更多的空间，因为它把每一行都保存在内存中了。
总体上单路优于双路，但是还是有缺陷的
#### filesort 单路排序的缺陷
在sort_buffer中，单路排序比双路排序要多占用很多空间，因为单路排序是把所有字段都取出，所以有可能取出的数据的总大小超出了sort_buffer的容量，导致每次只能取sort_buffer容量大小的数据，进行排序（创建tmp文件，多路合并），排完再取取sort_buffer容量大小，再排……从而多次I/O。

### 优化策略
基于filesort排序算法的缺陷，提高Order by速度有以下的策略（索引失效时）

1. 带Order by时，select*是一个大忌只Query需要的字段，这点非常重要。在这里的影响是：
    - 当Query的字段大小总和小于max_length_for_sort_data而且排序字段不是TEXTIBLOB类型时，会用改进后的算法—一单路排序，否则用老算法——多路排序。
    - 两种算法的数据都有可能超出sort_buffer的容量，超出之后，会创建tmp文件进行合并排序，导致多次/O，但是用单路排序算法的风险会更大一些，所以要提高sort_buffer_size。

2. 尝试提高 sort_buffer_size
不管用哪种算法，提高这个参数都会提高效率，当然，要根据系统的能力去提高，因为这个参数是针对每个进程的
3. 尝试提高 max_length_for_sort_data
提高这个参数，会增加用改进算法的概率。但是如果设的太高，数据总容量超出sort_buffer_size的概率就增大，明显症状是高的磁盘/O活动和低的处理器使用率。

总结：  

<img src="./pictures/Annotation 2019-12-25 154548.png"  div align=center />


### Group by优化（与orderby类似）
group by实质是先排序后进行分组，遵照索引建的最佳左前缀
当无法使用索引列，增大max_length for_sort data参数的设置和增大sort buffer_size参数的设置
where高于having，能写在where限定的条件就不要去having限定了。

## 慢查询日志

- MySQL的慢查询日志是MySQL提供的一种日志记录，它用来记录在MySQL中响应时间超过阈值的语句，具体指运行时间超过long_query_time值的SQL，则会被记录到慢查询日志中。

- 具体指运行时间超过long_query_time值的SQL，则会被记录到慢查询日志中。long_query_time的默认值为10，意思是运行10秒以上的语句。

- 由他来查看哪些SQL超出了我们的最大忍耐时间值，比如一条sql执行超过5秒钟，我们就算慢SQL，希望能收集超过5秒的sql，结合之前explain进行全面分析。

MySQL数据库**默认没有开启**慢查询日志，需要我们手动来设置这个参数。
当然，如果不是调优需要的话，一般不建议启动该参数，因为开启慢查询日志会或多或少带来一定的性能影响。慢查询日志支持将日志记录写入文件

#### 设置慢查询日志
默认情况下slow_query_log的值为OFF，表示慢查询日志是禁用的，可以通过设置slow_query_log的值来开启

查询：
```sql
SHOW VARIABLES LIKE '%slow_query_log%';
```
设置开启：
```sql
set global slow_query_log=1;
```
使用set global slow_query_log=1开启了慢查询日志只对当前数据库生效
如果MySQL重启后则会失效。

如果要永久生效，就必须修改配置文件,在[mysqld]下添加

slow_query_log=1
slow_query_log_file=（先查询SHOW VARIABLES LIKE '%slow_query_log%';里面的值）
关于慢查询的参数slow_query_log_file，它指定慢查询日志文件的存放路径，系统默认会给一个缺省的文件host_name-slow.log（如果没有指定参数slow_query_log_file的话）

#### 设置慢查询
查看阈值时间：
```sql
SHOW VARIABLES LIKE '%long_query_time%';
```
修改阈值时间，重新连接mysql修改才可见：
```sql
SET GLOBAL long_query_time=4;
```
输入 sleep(5);进行测试，在日志文件可见

<img src="./pictures/Annotation 2019-12-25 160540.png"  div align=center />

查看一共有多少条慢查询记录
```sql
SHOW GLOBAL STATUS LIKE '%slow_queries';
```

#### 日志分析工具mysqldumpslow
在生产环境中，如果要手工分析日志，查找、分析SQL，显然是个体力活，MySQL提供了日志分析工具mysqldumpsloWs
```bash
-s：是表示按照以下何种方式排序；
    c：访问次数
    1：锁定时间
    r：返回记录
    t：查询时间
    al：平均锁定时间
    ar：平均返回记录数
    at：平均查询时间
-t：即为返回前面多少条的数据；
-g：后边搭配一个正则匹配模式，大小写不敏感的；

```
<img src="./pictures/Annotation 2019-12-25 161331.png"  div align=center />

## 批量数据脚本
假设要插入一千万条的数据。


创建函数，假如报错：This function has none of DETERMINISTIC...
由于开启过慢查询日志，因为我们开启了bin-log，我们就必须为我们的function指定一个参数。设置参数:
```sql

SHOW VARIABLES LIKE 'log_bin_trust_function_creators';
SET global log_bin_trust_function_creators=1;
# 想自动开启也是在配置文件下设置
```

先创建随机函数
```sql
# 创建一个随机生成字符的函数
DELIMITER $$
CREATE FUNCTION rand_string(n INT) RETURNS VARCHAR(255)
BEGIN
DECLARE chars_str VARCHAR(100) DEFAULT 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
DECLARE return_str VARCHAR(255) DEFAULT '';
DECLARE i INT DEFAULT 0;
WHILE i<n DO
SET return_str =CONCAT(return_str, SUBSTRING(chars_str,FLOOR(1+RAND()*52),1));
SET i = i+1;
END WHILE;
RETURN return_str;
END$$

# 创建一个生成随机数字的函数
DELIMITER $$
CREATE FUNCTION rand_num() RETURNS INT(5)
BEGIN
DECLARE i INT DEFAULT 0;
SET i = FLOOR(100+RAND()*10);
RETURN i;
END $$
```
写存储过程
```sql
# 注意until后面没有;
DELIMITER $$
CREATE PROCEDURE insert_test01(IN loop_num INT(10))
BEGIN
DECLARE i INT DEFAULT 0;
SET autocommit=0;
REPEAT
SET i =i+1;
INSERT INTO test01(NAME,testId) VALUES(rand_string(6),rand_num());
UNTIL i= loop_num
END REPEAT;
COMMIT;
END $$

# 插入50万条数据
call insert_test01(500000);
```

## show profile
是mysql提供可以用来分析当前会话中语句执行的资源消耗情况。可以用于SQL的调优的测量
默认情况下，参数处于关闭状态，并保存最近15次的运行结果

查看与开启
```sql
SHOW VARIABLES LIKE 'profiling';
set profiling=on;
```
查看最近的sql语句
```sql
show profiles;
```
诊断sql
```sql
# 看cpu和Io
# 16为QueryId
SHOW PROFILE cpu,block io FOR QUERY 16;
```

可选的参数
<img src="./pictures/Annotation 2019-12-25 171741.png"  div align=center />

#### profile查看的status异常状态
1. converting HEAP to MyISAM查询结果太大，内存都不够用了，往磁盘上搬了。

1. Creating tmp table创建临时表
拷贝数据到临时表，用完再删除
1. Copying to tmp table on disk把内存中临时表复制到磁盘，危险！！！
1. locked

## 全局查询日志
永远不要在生产环境开启这个功能。测试时用

```sql
set global general_log=1;
set global log_output='TABLE';
```
此后，你所编写的sql语句，将会记录到mysql库里的general log表，可以用下面的命令查看

```sql
select * from mysql.general_log;
```