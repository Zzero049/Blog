# 牛客sql练习

## 1、查找最晚入职员工的所有信息

查找最晚入职员工的所有信息，为了减轻入门难度，目前所有的数据里员工入职的日期都不是同一天

(sqlite里面的注释为--,mysql为comment)

```sql
 CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL, -- '员工编号'
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
```

**输出描述:**

| emp_no | birth_date | first_name | last_name | gender | hire_date  |
| ------ | ---------- | ---------- | --------- | ------ | ---------- |
| 10008  | 1958-02-19 | Saniya     | Maliniak  | M      | 1994-09-15 |

**sql语句**

```mysql
# 解法1：排序加挑选一个
select * from employees
order by hire_date desc
limit 1;

# 使用limit 与 offset关键字,注意记录数从1开始计数，即0向后偏移1位
select * from employees
order by hire_date desc
limit 1 offset 0;

 
# 使用limit关键字 从第0条记录 向后读取一个，也就是第一条记录
select * from employees
order by hire_date desc
limit 0,1;


# 解法2：使用子查询，最后一天的时间如果有多个员工信息
select * from employees
where hire_date = (select max(hire_date) from employees);
```



## 2、查找入职员工时间排名倒数第三的员工所有信息

**题目描述**

查找入职员工时间排名倒数第三的员工所有信息，为了减轻入门难度，目前所有的数据里员工入职的日期都不是同一天

```sql
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
```

**输出描述:**

| emp_no | birth_date | first_name | last_name | gender | hire_date  |
| ------ | ---------- | ---------- | --------- | ------ | ---------- |
| 10005  | 1955-01-21 | Kyoichi    | Kalloufi  | M      | 1989-09-12 |

**sql语句**

```mysql
# 使用limit 与 offset关键字
select * from employees
order by hire_date desc
limit 1 offset 2;

 
# 使用limit关键字 从第0条记录 向后读取一个，也就是第一条记录 */
select * from employees
order by  hire_date desc
limit 2,1;

# 如果入职时间倒数第三排倒数第三的员工不止一个，那么用子查询找出排倒数第三的日期即可
select * from employees
where hire_date = (
    select distinct hire_date 
    from employees
    order by hire_date desc       -- 倒序
    limit 1 offset 2;              -- 去掉排名倒数第一第二的时间，取倒数第三
);    
```



## 3、查找各个部门当前领导当前薪水详情以及其对应部门编号

查找各个部门当前(dept_manager.to_date='9999-01-01')领导当前(salaries.to_date='9999-01-01')薪水详情以及其对应部门编号dept_no

(注:请以salaries表为主表进行查询，输出结果以salaries.emp_no升序排序，并且请注意输出结果里面dept_no列是最后一列)

```sql
CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL, -- '员工编号',
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));

CREATE TABLE `dept_manager` (
`dept_no` char(4) NOT NULL, -- '部门编号'
`emp_no` int(11) NOT NULL, -- '员工编号'
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));
```

**输出描述:**

| emp_no | salary | from_date  | to_date    | dept_no |
| :----- | :----- | :--------- | :--------- | :------ |
| 10002  | 72527  | 2001-08-02 | 9999-01-01 | d001    |
| 10004  | 74057  | 2001-11-27 | 9999-01-01 | d004    |
| 10005  | 94692  | 2001-09-09 | 9999-01-01 | d003    |
| 10006  | 43311  | 2001-08-02 | 9999-01-01 | d002    |
| 10010  | 94409  | 2001-11-23 | 9999-01-01 | d006    |

**sql语句**

注意了，题目条件要求了，**部门当前**和**领导当前**，也就是to_date都有要求的，最后salaries.emp_no是默认升序排序的，不需要设置

```mysql
# 内连接写法
select s.* ,d.dept_no
from salaries s
join dept_manager d							# 默认内连接inner join
on s.emp_no = d.emp_no 
where s.to_date='9999-01-01' and d.to_date='9999-01-01';

# select拼接
select s.* ,d.dept_no
from salaries s,dept_manager d
where  s.emp_no = d.emp_no and s.to_date='9999-01-01' and d.to_date='9999-01-01';
```



## 4、查找所有已经分配部门的员工的最新名字和首次用名和部门号

**题目描述**

查找所有**已经分配部门**的员工的last_name和first_name以及dept_no(请注意输出描述里各个列的前后顺序)

```sql
 CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
```

**输出描述:**

| last_name | first_name | dept_no |
| :-------- | :--------- | :------ |
| Facello   | Georgi     | d001    |
| 省略      | 省略       | 省略    |
| Piveteau  | Duangkaew  | d006    |

**sql语句**

```mysql
# 内连接
select e.last_name,e.first_name,d.dept_no
from employees e
(inner) join dept_emp d on e.emp_no = d.emp_no;		 # 括号内为可补全内容            

# select拼接
select e.last_name,e.first_name,d.dept_no
from employees e,dept_emp d
where e.emp_no = d.emp_no;
```



## 5、查找包括暂时没有分配的所有员工的最新名字和首次用名和部门号

查找所有员工的last_name和first_name以及对应部门编号dept_no，也包括暂时没有分配具体部门的员工(请注意输出描述里各个列的前后顺序)

```sql
CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
```

**输出描述:**

| last_name | first_name | dept_no                              |
| :-------- | :--------- | :----------------------------------- |
| Facello   | Georgi     | d001                                 |
| 省略      | 省略       | 省略                                 |
| Piveteau  | Duangkaew  | NULL(在sqlite中此处为空,MySQL为NULL) |

**sql语句**

```mysql
# 左外连接
select e.last_name,e.first_name,d.dept_no
from employees e
left (outer) join dept_emp d on e.emp_no = d.emp_no;   # 括号内为可补全内容
```



## 6、查找所有员工入职时候的薪水情况

查找所有员工入职时候的薪水情况，给出emp_no以及salary， 并按照emp_no进行逆序(请注意，一个员工可能有多次涨薪的情况)

```sql
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));

CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
```

**输出描述:**

| emp_no | salary |
| :----- | :----- |
| 10011  | 25828  |
| 省略   | 省略   |
| 10001  | 60117  |

注意是入职时候的薪水情况，工资表里为同个员工不同时期的多条记录

**sql语句**

```sql
-- hire_data时间和from_data时间一致

-- 内连接
select s.emp_no,s.salary
from salaries s
join employees e on e.emp_no = s.emp_no
where s.from_date = e.hire_date
order by s.emp_no desc;

-- where拼接
select s.emp_no,s.salary
from salaries s ,employees e  
where  e.emp_no = s.emp_no and s.from_date = e.hire_date
order by s.emp_no desc;


-- group by分组，from_data肯定最小
select emp_no,salary
from salaries
group by emp_no
having min(from_date)
order by emp_no desc;
```



## 7、查找薪水变动超过15次的员工号以及其对应的变动次数

查找薪水变动超过15次的员工号emp_no以及其对应的变动次数t

```sql
CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
```

**输出描述:**

| emp_no | t    |
| :----- | :--- |
| 10001  | 17   |
| 10004  | 16   |
| 10009  | 18   |

**sql语句**

```sql
-- 通过group by聚合，having条件筛选
select emp_no,count(emp_no) as t
from salaries
group by emp_no
having count(emp_no)>15;
```



## 8、找出所有员工当前薪水情况

找出所有员工当前(to_date='9999-01-01')具体的薪水salary情况，对于相同的薪水只显示一次,并按照逆序显示

```sql
CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
```

**输出描述:**

| salary |
| :----- |
| 94692  |
| 94409  |
| 88958  |
| 88070  |
| 74057  |
| 72527  |
| 59755  |
| 43311  |
| 25828  |

**sql语句**

```sql
-- 通过group by聚合
select salary
from salaries
where to_date='9999-01-01'
group by salary
order by salary desc;

-- distinct去重
select distinct salary
from salaries
where to_date='9999-01-01'
order by salary desc;
```



## 9、获取所有部门当前管理者的当前薪水情况，给出相应信息

获取所有部门当前(dept_manager.to_date='9999-01-01')manager的当前(salaries.to_date='9999-01-01')薪水情况，给出dept_no, emp_no以及salary(请注意，同一个人可能有多条薪水情况记录)

```sql
CREATE TABLE `dept_manager` (
`dept_no` char(4) NOT NULL,
`emp_no` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
```

**输出描述:**

| dept_no | emp_no | salary |
| :------ | :----- | :----- |
| d001    | 10002  | 72527  |
| d004    | 10004  | 74057  |
| d003    | 10005  | 94692  |
| d002    | 10006  | 43311  |
| d006    | 10010  | 94409  |

**sql语句**

```sql
-- 通过where
select d.dept_no,d.emp_no,s.salary
from dept_manager d, salaries s
where d.emp_no = s.emp_no and d.to_date='9999-01-01' and s.to_date='9999-01-01';

-- 通过inner join
select d.dept_no,d.emp_no,s.salary
from dept_manager d
join salaries s on d.emp_no = s.emp_no 
where d.to_date='9999-01-01' and s.to_date='9999-01-01';
```



## 10、获取所有非管理层的员工编号

获取所有非manager的员工emp_no

```sql
CREATE TABLE `dept_manager` (
`dept_no` char(4) NOT NULL,
`emp_no` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
 PRIMARY KEY (`emp_no`));
 
 
-- 如插入为:
INSERT INTO dept_manager VALUES('d001',10002,'1996-08-03','9999-01-01');
INSERT INTO dept_manager VALUES('d002',10006,'1990-08-05','9999-01-01');
INSERT INTO dept_manager VALUES('d003',10005,'1989-09-12','9999-01-01');
INSERT INTO dept_manager VALUES('d004',10004,'1986-12-01','9999-01-01');
INSERT INTO dept_manager VALUES('d005',10010,'1996-11-24','2000-06-26');
INSERT INTO dept_manager VALUES('d006',10010,'2000-06-26','9999-01-01');

INSERT INTO employees VALUES(10001,'1953-09-02','Georgi','Facello','M','1986-06-26');
INSERT INTO employees VALUES(10002,'1964-06-02','Bezalel','Simmel','F','1985-11-21');
INSERT INTO employees VALUES(10003,'1959-12-03','Parto','Bamford','M','1986-08-28');
INSERT INTO employees VALUES(10004,'1954-05-01','Chirstian','Koblick','M','1986-12-01');
INSERT INTO employees VALUES(10005,'1955-01-21','Kyoichi','Maliniak','M','1989-09-12');
INSERT INTO employees VALUES(10006,'1953-04-20','Anneke','Preusig','F','1989-06-02');
INSERT INTO employees VALUES(10007,'1957-05-23','Tzvetan','Zielinski','F','1989-02-10');
INSERT INTO employees VALUES(10008,'1958-02-19','Saniya','Kalloufi','M','1994-09-15');
INSERT INTO employees VALUES(10009,'1952-04-19','Sumant','Peac','F','1985-02-18');
INSERT INTO employees VALUES(10010,'1963-06-01','Duangkaew','Piveteau','F','1989-08-24');
INSERT INTO employees VALUES(10011,'1953-11-07','Mary','Sluis','F','1990-01-22');
```

**输出描述:**

| emp_no |
| :----- |
| 10001  |
| 10003  |
| 10007  |
| 10008  |
| 10009  |
| 10011  |

**sql语句**

```sql
-- not in 子查询
select e.emp_no
from employees e
where e.emp_no not in(select emp_no from dept_manager);

-- 左外连接 ，因为只有dept_manager有dept_no字段，因此左外连接只保留该字段为null的就是非管理层
select e.emp_no
from employees e left join dept_manager d
on d.emp_no = e.emp_no
where d.dept_no is null
```



##  11、获取所有员工当前的管理者

获取所有员工当前的(dept_manager.to_date='9999-01-01')manager，如果员工是manager的话不显示(也就是如果当前的manager是自己的话结果不显示)。输出结果第一列给出当前员工的emp_no,第二列给出其manager对应的emp_no。

```sql
CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL, -- '所有的员工编号'
`dept_no` char(4) NOT NULL, -- '部门编号'
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE `dept_manager` (
`dept_no` char(4) NOT NULL, -- '部门编号'
`emp_no` int(11) NOT NULL, -- '经理编号'
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

-- 如插入：
INSERT INTO dept_emp VALUES(10001,'d001','1986-06-26','9999-01-01');
INSERT INTO dept_emp VALUES(10002,'d001','1996-08-03','9999-01-01');
INSERT INTO dept_emp VALUES(10003,'d004','1995-12-03','9999-01-01');
INSERT INTO dept_emp VALUES(10004,'d004','1986-12-01','9999-01-01');
INSERT INTO dept_emp VALUES(10005,'d003','1989-09-12','9999-01-01');
INSERT INTO dept_emp VALUES(10006,'d002','1990-08-05','9999-01-01');
INSERT INTO dept_emp VALUES(10007,'d005','1989-02-10','9999-01-01');
INSERT INTO dept_emp VALUES(10008,'d005','1998-03-11','2000-07-31');
INSERT INTO dept_emp VALUES(10009,'d006','1985-02-18','9999-01-01');
INSERT INTO dept_emp VALUES(10010,'d005','1996-11-24','2000-06-26');
INSERT INTO dept_emp VALUES(10010,'d006','2000-06-26','9999-01-01');

INSERT INTO dept_manager VALUES('d001',10002,'1996-08-03','9999-01-01');
INSERT INTO dept_manager VALUES('d002',10006,'1990-08-05','9999-01-01');
INSERT INTO dept_manager VALUES('d003',10005,'1989-09-12','9999-01-01');
INSERT INTO dept_manager VALUES('d004',10004,'1986-12-01','9999-01-01');
INSERT INTO dept_manager VALUES('d005',10010,'1996-11-24','2000-06-26');
INSERT INTO dept_manager VALUES('d006',10010,'2000-06-26','9999-01-01');
```

**输出描述:**

| emp_no | manager_no |
| :----- | :--------- |
| 10001  | 10002      |
| 10003  | 10004      |
| 10009  | 10010      |

**sql语句**

```sql
-- 内连接，去掉自己是管理层即可，注意当前时间
select de.emp_no as emp_no,dm.emp_no as manager_no 
from dept_emp de
inner join dept_manager dm on  dm.dept_no=de.dept_no
where de.emp_no!= dm.emp_no and dm.to_date='9999-01-01';
```



## 12、获取每个部门中当前员工薪水最高的相关信息（==易错题==）

获取所有部门中当前(dept_emp.to_date = '9999-01-01')员工当前(salaries.to_date='9999-01-01')薪水最高的相关信息，给出dept_no, emp_no以及其对应的salary，按照部门升序排列。

```sql
CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));

--- 如插入：
INSERT INTO dept_emp VALUES(10001,'d001','1986-06-26','9999-01-01');
INSERT INTO dept_emp VALUES(10002,'d001','1996-08-03','9999-01-01');
INSERT INTO dept_emp VALUES(10003,'d001','1996-08-03','1997-08-03');

INSERT INTO salaries VALUES(10001,90000,'1986-06-26','1987-06-26');
INSERT INTO salaries VALUES(10001,88958,'2002-06-22','9999-01-01');
INSERT INTO salaries VALUES(10002,72527,'1996-08-03','1997-08-03');
INSERT INTO salaries VALUES(10002,72527,'2000-08-02','2001-08-02');
INSERT INTO salaries VALUES(10002,72527,'2001-08-02','9999-01-01');
INSERT INTO salaries VALUES(10003,90000,'1996-08-03','1997-08-03');
```

**输出描述:**

| dept_no | emp_no | salary |
| ------- | ------ | ------ |
| d001    | 10001  | 88958  |

**sql语句**

```sql
-- 错误示例
SELECT d.dept_no, d.emp_no, s.salary
FROM dept_emp as d
INNER JOIN salaries as s
ON d.emp_no=s.emp_no
WHERE d.to_date='9999-01-01'
AND s.to_date='9999-01-01'
GROUP BY d.dept_no
HAVING salary=MAX(s.salary);
```

错误点1：d.emp_no是非聚合字段，不能出现在SELECT。因为一个聚合字段(dept_no)对应多个非聚合字段(emp_no)，所以选择的时候，会随机选择非聚合字段中的一个，不一定能对应上，于是出错。参考https://www.cnblogs.com/hoojjack/p/7460574.html
错误点2：根据错误点1，如果强行写上述代码，当**多人同时拥有最高薪水时也无法查出。**

语法：

```sql
SELECT column_1, column_2, … column_n, aggregate_function(expression), constant
FROM tables
WHERE predicates
GROUP BY column_1, column_2, … column_n
HAVING condition_1 … condition_n;
```

注意：因为聚合函数通过作用一组值而只返回一个单一值，因此，在SELECT语句中出现的字段要么为一个聚合函数的输入值，如COUNT(course)，要么为GROUP BY语句中指定的字段，要么是常数，否则会出错。
简而言之：使用GROUP BY子句时，SELECT子句中只能有聚合键、聚合函数、常数。

正确答案：关联子查询，外表固定一个部门，内表进行子查询

```sql
select d1.dept_no, d1.emp_no,s1.salary
from dept_emp d1
join salaries s1 on d1.emp_no = s1.emp_no and d1.to_date='9999-01-01' and s1.to_date='9999-01-01'
where s1.salary in (select max(s2.salary)
                   from dept_emp d2
                   join salaries s2
                   on d2.emp_no=s2.emp_no
                   where d2.dept_no = d1.dept_no         -- 必须满足是该部门，锁定部门
                   and d2.to_date='9999-01-01' and s2.to_date='9999-01-01' )-- 否则可能找到不是当前时间的最大值
order by d1.dept_no;
```

这里的逻辑是，先内连接形成一个表，再判断表中salary必须是该部门最大，找最大的方法是另起一个内连接，锁定部门，再查当前员工薪水最高的数是多少即可



## 13、从titles表获取按照title进行分组

从titles表获取按照title进行分组，每组个数大于等于2，给出title以及对应的数目t。

```sql
CREATE TABLE IF NOT EXISTS `titles` (
`emp_no` int(11) NOT NULL,
`title` varchar(50) NOT NULL,
`from_date` date NOT NULL,
`to_date` date DEFAULT NULL);
```

**如插入：**

```sql
INSERT INTO titles VALUES(10001,'Senior Engineer','1986-06-26','9999-01-01');
INSERT INTO titles VALUES(10002,'Staff','1996-08-03','9999-01-01');
INSERT INTO titles VALUES(10003,'Senior Engineer','1995-12-03','9999-01-01');
INSERT INTO titles VALUES(10004,'Engineer','1986-12-01','1995-12-01');
INSERT INTO titles VALUES(10004,'Senior Engineer','1995-12-01','9999-01-01');
INSERT INTO titles VALUES(10005,'Senior Staff','1996-09-12','9999-01-01');
INSERT INTO titles VALUES(10005,'Staff','1989-09-12','1996-09-12');
INSERT INTO titles VALUES(10006,'Senior Engineer','1990-08-05','9999-01-01');
INSERT INTO titles VALUES(10007,'Senior Staff','1996-02-11','9999-01-01');
INSERT INTO titles VALUES(10007,'Staff','1989-02-10','1996-02-11');
INSERT INTO titles VALUES(10008,'Assistant Engineer','1998-03-11','2000-07-31');
INSERT INTO titles VALUES(10009,'Assistant Engineer','1985-02-18','1990-02-18');
INSERT INTO titles VALUES(10009,'Engineer','1990-02-18','1995-02-18');
INSERT INTO titles VALUES(10009,'Senior Engineer','1995-02-18','9999-01-01');
INSERT INTO titles VALUES(10010,'Engineer','1996-11-24','9999-01-01');
INSERT INTO titles VALUES(10010,'Engineer','1996-11-24','9999-01-01');
```

**输出**

| title              | t    |
| :----------------- | :--- |
| Assistant Engineer | 2    |
| Engineer           | 4    |
| 省略               | 省略 |
| Staff              | 3    |

**sql语句**

```sql
-- group by + having搞定
select title,count(emp_no) as t					-- 统计同一title下记录数目
from titles
group by title
having count(emp_no)>=2
```



## 14、从titles表获取按照title进行分组，注意对于重复的emp_no进行忽略。

从titles表获取按照title进行分组，每组个数大于等于2，给出title以及对应的数目t。

注意**对于重复的emp_no进行忽略**(即emp_no重复的title不计算，title对应的数目t不增加)。

```sql
CREATE TABLE IF NOT EXISTS `titles` (
`emp_no` int(11) NOT NULL,
`title` varchar(50) NOT NULL,
`from_date` date NOT NULL,
`to_date` date DEFAULT NULL);
```

**如插入：**

```sql
INSERT INTO titles VALUES(10001,'Senior Engineer','1986-06-26','9999-01-01');
INSERT INTO titles VALUES(10002,'Staff','1996-08-03','9999-01-01');
INSERT INTO titles VALUES(10003,'Senior Engineer','1995-12-03','9999-01-01');
INSERT INTO titles VALUES(10004,'Engineer','1986-12-01','1995-12-01');
INSERT INTO titles VALUES(10004,'Senior Engineer','1995-12-01','9999-01-01');
INSERT INTO titles VALUES(10005,'Senior Staff','1996-09-12','9999-01-01');
INSERT INTO titles VALUES(10005,'Staff','1989-09-12','1996-09-12');
INSERT INTO titles VALUES(10006,'Senior Engineer','1990-08-05','9999-01-01');
INSERT INTO titles VALUES(10007,'Senior Staff','1996-02-11','9999-01-01');
INSERT INTO titles VALUES(10007,'Staff','1989-02-10','1996-02-11');
INSERT INTO titles VALUES(10008,'Assistant Engineer','1998-03-11','2000-07-31');
INSERT INTO titles VALUES(10009,'Assistant Engineer','1985-02-18','1990-02-18');
INSERT INTO titles VALUES(10009,'Engineer','1990-02-18','1995-02-18');
INSERT INTO titles VALUES(10009,'Senior Engineer','1995-02-18','9999-01-01');
INSERT INTO titles VALUES(10010,'Engineer','1996-11-24','9999-01-01');
INSERT INTO titles VALUES(10010,'Engineer','1996-11-24','9999-01-01');
```

**输出描述:**

| title              | t    |
| :----------------- | :--- |
| Assistant Engineer | 2    |
| Engineer           | 3    |
| 省略               | 省略 |
| Staff              | 3    |

**sql语句**

```sql
-- 解法1：和上题一样的思路，这里count的时候去重
select title, count(distinct emp_no) t
from titles
group by title
having t>=2;

-- 解法2：子查询，先去重再计数
select title, count(emp_no) t
from (select distinct emp_no,title from titles)
group by title
having t>=2;

```

## 15、查找employees表的奇数id（==奇偶查询方法与正则知识点==）

查找employees表所有emp_no为奇数，且last_name不为Mary(注意大小写)的员工信息，并按照hire_date逆序排列（**题目不能使用mod函数**）

```sql
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
```

**如插入：**

```sql
INSERT INTO employees VALUES(10001,'1953-09-02','Georgi','Facello','M','1986-06-26');
INSERT INTO employees VALUES(10002,'1964-06-02','Bezalel','Simmel','F','1985-11-21');
INSERT INTO employees VALUES(10003,'1959-12-03','Parto','Bamford','M','1986-08-28');
INSERT INTO employees VALUES(10004,'1954-05-01','Chirstian','Koblick','M','1986-12-01');
INSERT INTO employees VALUES(10005,'1955-01-21','Kyoichi','Maliniak','M','1989-09-12');
INSERT INTO employees VALUES(10006,'1953-04-20','Anneke','Preusig','F','1989-06-02');
INSERT INTO employees VALUES(10007,'1957-05-23','Tzvetan','Zielinski','F','1989-02-10');
INSERT INTO employees VALUES(10008,'1958-02-19','Saniya','Kalloufi','M','1994-09-15');
INSERT INTO employees VALUES(10009,'1952-04-19','Sumant','Peac','F','1985-02-18');
INSERT INTO employees VALUES(10010,'1963-06-01','Duangkaew','Piveteau','F','1989-08-24');
INSERT INTO employees VALUES(10011,'1953-11-07','Mary','Sluis','F','1990-01-22');
```

**输出描述:**

| emp_no | birth_date | first_name | last_name | gender | hire_date  |
| :----- | :--------- | :--------- | :-------- | :----- | :--------- |
| 10011  | 1953-11-07 | Mary       | Sluis     | F      | 1990-01-22 |
| 10005  | 1955-01-21 | Kyoichi    | Maliniak  | M      | 1989-09-12 |
| 10007  | 1957-05-23 | Tzvetan    | Zielinski | F      | 1989-02-10 |
| 10003  | 1959-12-03 | Parto      | Bamford   | M      | 1986-08-28 |
| 10001  | 1953-09-02 | Georgi     | Facello   | M      | 1986-06-26 |
| 10009  | 1952-04-19 | Sumant     | Peac      | F      | 1985-02-18 |

**sql语句**

```sql
-- 使用%，底层应该是不调mod
select *
from employees
where emp_no%2=1 and last_name!='Mary'
order by hire_date desc;

-- 使用&，不需要=
select *
from employees
where emp_no&1 and last_name!='Mary'						-- 查询偶数可以用(emp_no>>1)<<1
order by hire_date desc;

-- 使用正则表达式
select *
from employees
where emp_no regexp '[13579]$' and last_name!='Mary'			-- $表示结尾，以13579任意一个结尾
order by hire_date desc;
```

补充：emp_no % 2=1也可以改成MOD(emp_no, 2)=1，但是某些sql版本可能不支持后者(比如题库就不支持)

补充：不相等有三种表示方式：<>、!=、IS NOT

补充：sql中/表示标准除法，如101/2得到50.5，而DIV表示整数除法，如101 DIV 2得到50

查询奇数的一般方法：如上(最好是位运算&)

查询偶数的一般方法：emp_no=(emp_no>>1)<<1

注意：last_name是varchar类型，所以对它的判断需要加上单引号

**顺便说一下正则化表达式：**

但是，前两种办法，针对的是字段全是数字的情况，如果对于身份证这种中间隐藏了一部分的，无法使用数字计算

所以更好的方法是使用正则化表达式(当然题库这里无法使用正则化表达式，可能是版本或设置问题)

```
^aa：以aa开头
aa$：以aa结尾
.：匹配任何字符
[abc]：[字符集合]，包含中括号内的字符
[^abc]或[!abc]：[字符集合]，不包含中括号内的字符
a|b|c：匹配a或b或c，如(中|美)国
*：匹配前面的子表达式0次或者多次。如，zo*能匹配’z’以及’zoo’。*等价于[0,+∞)
+：匹配前面的子表达式1次或者多次。如，’zo+’能匹配’zo’，但不能匹配’z’。+等价于[1,+∞)
{n}：n是一个非负整数，匹配前面的子表达式2次。如，o{2} 能匹配’food’中的两个o，但不能匹配’Bob’中的o
{n, m}：m和n均为非负整数，其中n<=m。最少匹配n次且最多匹配m次。
```



## 16、统计出当前各个title类型对应的员工当前薪水对应的平均工资

统计出当前(titles.to_date='9999-01-01')各个title类型对应的员工当前(salaries.to_date='9999-01-01')薪水对应的平均工资。结果给出title以及平均工资avg。

```sql
CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
CREATE TABLE IF NOT EXISTS "titles" (
`emp_no` int(11) NOT NULL,
`title` varchar(50) NOT NULL,
`from_date` date NOT NULL,
`to_date` date DEFAULT NULL);
```

**如插入：**

```sql
INSERT INTO salaries VALUES(10001,88958,'1986-06-26','9999-01-01');
INSERT INTO salaries VALUES(10003,43311,'2001-12-01','9999-01-01');
INSERT INTO salaries VALUES(10004,70698,'1986-12-01','1995-12-01');
INSERT INTO salaries VALUES(10004,74057,'1995-12-01','9999-01-01');
INSERT INTO salaries VALUES(10006,43311,'2001-08-02','9999-01-01');
INSERT INTO salaries VALUES(10007,88070,'2002-02-07','9999-01-01');

INSERT INTO titles VALUES(10001,'Senior Engineer','1986-06-26','9999-01-01');
INSERT INTO titles VALUES(10003,'Senior Engineer','2001-12-01','9999-01-01');
INSERT INTO titles VALUES(10004,'Engineer','1986-12-01','1995-12-01');
INSERT INTO titles VALUES(10004,'Senior Engineer','1995-12-01','9999-01-01');
INSERT INTO titles VALUES(10006,'Senior Engineer','2001-08-02','9999-01-01');
INSERT INTO titles VALUES(10007,'Senior Staff','1996-02-11','9999-01-01');
```

**输出：**

| title           | avg      |
| --------------- | -------- |
| Senior Engineer | 62409.25 |
| Senior Staff    | 88070.0  |

**sql语句**

```sql
-- 内连接
select t.title,avg(s.salary) as avg
from titles t,salaries s
where s.emp_no = t.emp_no and s.to_date='9999-01-01' and t.to_date='9999-01-01'
group by t.title;

-- where
select t.title,avg(s.salary) as avg
from titles t
join salaries s 
on s.emp_no = t.emp_no and s.to_date='9999-01-01' and t.to_date='9999-01-01'
group by t.title;
```



## 17、获取当前薪水第二多的员工的编号以及其对应的薪水

获取当前（to_date='9999-01-01'）薪水第二多的员工的emp_no以及其对应的薪水salary

```sql
CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
```

**输出描述:**

| emp_no | salary |
| :----- | :----- |
| 10009  | 94409  |

**sql语句**

由于工资第二高的可能不止一个，因此不能单纯只找到一个

```sql
-- 子查询group by+limit找到第二小的值
select emp_no,salary
from salaries
where to_date='9999-01-01' and salary=(select salary
                                       from salaries
                                       where to_date='9999-01-01'
                                       order by salary desc
                                       limit 1 offset 1);

-- 还可以用max先找最大，再用<找第二大
select emp_no,salary
from salaries
where to_date='9999-01-01' and salary=(select max(salary)								-- 最外层等
                                       from salaries
                                       where to_date='9999-01-01' 
                                       and salary < (select max(salary)					-- 找第二大	
                                                     from salaries
                                                     where to_date='9999-01-01'));		-- 找最大
```



## 18、获取当前薪水第二多的员工的emp_no以及其对应的薪水salary

查找当前薪水(to_date='9999-01-01')排名第二多的员工编号emp_no、薪水salary、last_name以及first_name，你可以不使用order by完成吗

```sql
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));

CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
```

**输出描述：**

| emp_no | salary | last_name | first_name |
| :----- | :----- | :-------- | :--------- |
| 10009  | 94409  | Peac      | Sumant     |

**sql语句**

```sql
-- 方法一：和上题一样max和<找第二小
select e.emp_no,s.salary,e.last_name,e.first_name
from employees e,salaries s
where e.emp_no = s.emp_no 
and s.to_date='9999-01-01'
and s.salary=(select max(salary)
             from salaries
             where to_date='9999-01-01' 
              and salary<(select max(salary)
                          from salaries
                          where to_date='9999-01-01'));
                          
-- 方法二：自连接查询
select e.emp_no,s.salary,e.last_name,e.first_name
from employees e,salaries s
where e.emp_no = s.emp_no 
and s.to_date='9999-01-01'
and s.salary=(select s1.salary
              from salaries s1
              join salaries s2
              on s1.salary<=s2.salary					--- 也可以用where筛选连接
              where s1.to_date = '9999-01-01' and s2.to_date = '9999-01-01'
              group by s1.salary
              having count(s2.salary)=2 );
```

单纯连接以后:

|  s1  |  s2  |
| :--: | :--: |
| 100  | 100  |
|  98  |  98  |
|  98  |  98  |
|  95  |  95  |

但以**s1<=s2**条件链接，注意无法用where完成，下表98是第二大的

|  s1  |  s2  |
| :--: | :--: |
| 100  | 100  |
|  98  | 100  |
|      |  98  |
|      |  98  |
|  95  | 100  |
|      |  98  |
|      |  98  |
|      |  95  |

**以**s1.salary**分组时一个s1会对应多个s2，对s2进行去重统计数量, 就是s1对应的排名**



## 19、查找所有员工的last_name和first_name以及对应的dept_name

查找所有员工的last_name和first_name以及对应的dept_name，也包括暂时没有分配部门的员工

```sql
CREATE TABLE `departments` (
`dept_no` char(4) NOT NULL,
`dept_name` varchar(40) NOT NULL,
PRIMARY KEY (`dept_no`));

CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
```

如插入：

```sql
-- 插入记录到departments
INSERT INTO departments VALUES('d001','Marketing');
INSERT INTO departments VALUES('d002','Finance');
INSERT INTO departments VALUES('d003','Human Resources');
INSERT INTO departments VALUES('d004','Production');
INSERT INTO departments VALUES('d005','Development');
INSERT INTO departments VALUES('d006','Quality Management');

-- 插入记录到dept_emp
INSERT INTO dept_emp VALUES(10001,'d001','1986-06-26','9999-01-01');
INSERT INTO dept_emp VALUES(10002,'d001','1996-08-03','9999-01-01');
INSERT INTO dept_emp VALUES(10003,'d004','1995-12-03','9999-01-01');
INSERT INTO dept_emp VALUES(10004,'d004','1986-12-01','9999-01-01');
INSERT INTO dept_emp VALUES(10005,'d003','1989-09-12','9999-01-01');
INSERT INTO dept_emp VALUES(10006,'d002','1990-08-05','9999-01-01');
INSERT INTO dept_emp VALUES(10007,'d005','1989-02-10','9999-01-01');
INSERT INTO dept_emp VALUES(10008,'d005','1998-03-11','2000-07-31');
INSERT INTO dept_emp VALUES(10009,'d006','1985-02-18','9999-01-01');
INSERT INTO dept_emp VALUES(10010,'d005','1996-11-24','2000-06-26');
INSERT INTO dept_emp VALUES(10010,'d006','2000-06-26','9999-01-01');

-- 插入记录到employees
INSERT INTO employees VALUES(10001,'1953-09-02','Georgi','Facello','M','1986-06-26');
INSERT INTO employees VALUES(10002,'1964-06-02','Bezalel','Simmel','F','1985-11-21');
INSERT INTO employees VALUES(10003,'1959-12-03','Parto','Bamford','M','1986-08-28');
INSERT INTO employees VALUES(10004,'1954-05-01','Chirstian','Koblick','M','1986-12-01');
INSERT INTO employees VALUES(10005,'1955-01-21','Kyoichi','Maliniak','M','1989-09-12');
INSERT INTO employees VALUES(10006,'1953-04-20','Anneke','Preusig','F','1989-06-02');
INSERT INTO employees VALUES(10007,'1957-05-23','Tzvetan','Zielinski','F','1989-02-10');
INSERT INTO employees VALUES(10008,'1958-02-19','Saniya','Kalloufi','M','1994-09-15');
INSERT INTO employees VALUES(10009,'1952-04-19','Sumant','Peac','F','1985-02-18');
INSERT INTO employees VALUES(10010,'1963-06-01','Duangkaew','Piveteau','F','1989-08-24');
INSERT INTO employees VALUES(10011,'1953-11-07','Mary','Sluis','F','1990-01-22');
```

**输出描述:**

| last_name | first_name | dept_name |
| :-------- | :--------- | :-------- |
| Facello   | Georgi     | Marketing |
| 省略      | 省略       | 省略      |
| Sluis     | Mary       | NULL      |

**sql语句**

```sql
-- 显然要包括暂时没有分配部门的员工，需要左外连接
select e.last_name,e.first_name,dee.dept_name
from  employees e
left join (select de.*,d.dept_name
          from departments d, dept_emp de
          where d.dept_no=de.dept_no) dee
on e.emp_no = dee.emp_no;
```



## 20、查找员工编号emp_no为10001其自入职以来的薪水salary涨幅

查找员工编号emp_no为10001其自入职以来的薪水salary涨幅(总共涨了多少)growth(可能有多次涨薪，没有降薪)

```sql
CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
```

**输出**

| growth |
| :----- |
| 28841  |

**sql语句**

```sql
-- 由于薪水只有涨，那么可以用emp_no=10001的最大工资减最小工资就是入职以来的薪水salary涨幅，但如果薪水会波动，此法不行
select max(salary)-min(salary) as growth
from salaries
where emp_no=10001;

-- 找现在的工资-入职时候的时间的工资
-- 方法一：用max和min等聚合函数，注意where不能用聚合函数，select、having可以
select (select salary
       from salaries
       where emp_no=10001 and to_date=(select max(to_date)				--- 最大日期
                                      from salaries
                                      where emp_no=10001))
        - 																--- 减
       (select salary
       from salaries
       where emp_no=10001 and from_date=(select min(from_date)			--- 最小日期，即入职以来
                                        from salaries
                                        where emp_no=10001))
as growth;

-- 也可以用order by和limit去找，最大日期和最小日期
select (select salary
       from salaries
       where emp_no=10001 and to_date=(select to_date
                                      from salaries
                                      where emp_no=10001 
                                      order by to_date desc
                                      limit 1 offset 0))
        - 
       (select salary
       from salaries
       where emp_no=10001 and from_date=(select from_date
                                        from salaries
                                        where emp_no=10001
                                        order by from_date asc
                                        limit 1 offset 0))
as growth;
```



## 21、查找所有员工自入职以来的薪水涨幅情况（==ON与where区别==）

查找所有员工自入职以来的薪水涨幅情况，给出员工编号emp_no以及其对应的薪水涨幅growth，并按照growth进行升序

（注:可能有employees表和salaries表里存在记录的员工，有对应的员工编号和涨薪记录，但是已经离职了，离职的员工salaries表的最新的to_date!='9999-01-01'，这样的数据不显示在查找结果里面）

```sql
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL, -- '入职时间'
PRIMARY KEY (`emp_no`));

CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL, -- '一条薪水记录开始时间'
`to_date` date NOT NULL, -- '一条薪水记录结束时间'
PRIMARY KEY (`emp_no`,`from_date`));
```

**输出描述**

| emp_no | growth |
| :----- | :----- |
| 10011  | 0      |
| 省略   | 省略   |
| 10010  | 54496  |
| 10004  | 34003  |

**sql语句**

```sql
select s1.emp_no,(s1.salary-s2.salary) as growth			
from (select e.emp_no,s.salary
     from employees e
     join salaries s on e.emp_no = s.emp_no		-- 采用内连接即可，新员工就算刚入职，salary也不应该有记录
     where s.to_date = '9999-01-01'
     ) s1,												--- s1找对应员工最新工资
    (select e.emp_no,s.salary
     from employees e
     join salaries s on e.emp_no = s.emp_no
     where s.from_date = e.hire_date
     ) s2												--- s2找对应员工入职工资
where s1.emp_no = s2.emp_no
order by growth;
```

本题用left join和inner join都是可以的，但where条件不能放在on里

**过滤条件放在ON和WHERE是否一致的问题：**

当我们使用关联操作时，关联两张表或多张表来返回记录时，数据库就会生成一张临时表，最后将这张临时表返回给用户。以LEFT JOIN为例：在使用LEFT JOIN时，ON和WHERE的过滤条件的区别如下：

**ON条件是在生成临时表时使用的条件，它不管ON中的条件是否为真，都会返回左边表中的记录**
**WHERE条件是在临时表已经生成后，对临时表进行的过滤条件。**如果WHERE条件不为真的记录就会被过滤掉。

由于LEFT JOIN(以及RIGHT JOIN，FULL JOIN)的特殊性，不管ON条件是否为真，数据库都会返回左侧(或右侧、左右两侧)表中的全部记录。由于INNER JOIN没有这样的特殊性，所以过滤条件放在ON中或WHERE中，其返回的结果是一样的。
这是使用的是LEFT JOIN，而s.to_date=‘9999-01-01’是连接表之后需要进行的过滤条件，所以必须放在WHERE里面。





## 22、统计各个部门的工资记录数

统计各个部门的工资记录数，给出部门编码dept_no、部门名称dept_name以及部门在salaries表里面有多少条记录sum

```sql
CREATE TABLE `departments` (
`dept_no` char(4) NOT NULL,
`dept_name` varchar(40) NOT NULL,
PRIMARY KEY (`dept_no`));

CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
```

**输出描述**

| dept_no | dept_name          | sum  |
| ------- | ------------------ | ---- |
| d001    | Marketing          | 24   |
| d002    | Finance            | 14   |
| d003    | Human Resources    | 13   |
| d004    | Production         | 24   |
| d005    | Development        | 25   |
| d006    | Quality Management | 25   |

**sql语句**

```sql
-- 方法一：直接三表联查，用WHERE过滤，即通通连起来，再按部门分组
select de.dept_no,d.dept_name,count(de.emp_no) as sum
from departments d,salaries s,dept_emp de
where d.dept_no = de.dept_no and s.emp_no = de.emp_no
group by de.dept_no;

-- 方法二：嵌套查询，查出一个dept_no，就进行子查询的到对应数目COUNT(*)
select d.dept_no, d.dept_name,(select count(*)
                               from dept_emp de
                               join salaries s
                               on de.emp_no = s.emp_no
                               and de.dept_no = d.dept_no) as sum
from departments d;

-- 方法三：思想同方法一，多次内连接
select de.dept_no, de.dept_name, count(*) as sum
from (select *
      from departments
      join dept_emp
      on departments.dept_no=dept_emp.dept_no) as de
join salaries as s
on de.emp_no=s.emp_no
group by de.dept_no;
-- 这里要提的是，多次内连接可以省略内层的内连接SELECT (因为内连接自己会生成临时表)：
select de.dept_no, de.dept_name, count(*) as sum
from (departments						-- 省略select
      join dept_emp
      on departments.dept_no=dept_emp.dept_no) as de
join salaries as s
on de.emp_no=s.emp_no
group by de.dept_no;
-- 还可以用连续内连接进一步省略
select de.dept_no, d.dept_name, count(*) as sum
from (departments d
      join dept_emp de
      on d.dept_no=de.dept_no
      join salaries as s					--	连续两次内连接
      on de.emp_no=s.emp_no
     ) 
group by de.dept_no;
```

注意：连续内连接中一定不要出现WHERE



## 23、对所有员工的薪水按照salary进行按照1-N的排名（==易错题==）

对所有员工的当前(to_date='9999-01-01')薪水按照salary进行按照1-N的排名，相同salary并列且按照emp_no升序排列

```sql
CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
```

**输出描述：**

| emp_no | salary | rank |
| :----- | :----- | :--- |
| 10005  | 94692  | 1    |
| 10009  | 94409  | 2    |
| 10010  | 94409  | 2    |
| 10001  | 88958  | 3    |
| 10007  | 88070  | 4    |
| 10004  | 74057  | 5    |
| 10002  | 72527  | 6    |
| 10003  | 43311  | 7    |
| 10006  | 43311  | 7    |
| 10011  | 25828  | 8    |

**sql语句**

```sql
-- 方法一，固定s的一条记录，利用关联查询的到它的rank
select s.emp_no,s.salary,(select count(distinct salary) 		-- 注意这里用where比较好，内连接写太费劲
                          from salaries 						-- 不需要group，s.salary可重复
                          where salary >= s.salary 
                          and to_date='9999-01-01') as rank		--- s.to_date = '9999-01-01'已经满足
from salaries s
where s.to_date = '9999-01-01'
order by salary desc ,s.emp_no asc;

-- 方法二，先构建不含salary的rank表，再将rank表和salaries表内接，然后排序得到结果
select a.emp_no,a.salary,b.rank
from salaries a
join (select s1.emp_no,count(distinct s2.salary) as rank		-- 要计数的是salary而不是emp_no，因为salry会重复
     from salaries s1
     join salaries s2 
     on s1.salary<=s2.salary 
     where s1.to_date='9999-01-01' and s2.to_date='9999-01-01'
     group by s1.emp_no) b										-- 最后按编号分组（不是工资），才能统计出正确的排名
on a.emp_no = b.emp_no and a.to_date='9999-01-01'
order by a.salary desc, a.emp_no asc;

-- 方法三，SQL编程，在题库中不能运行，在mysql中可以运行（了解）
select emp_no, salary,
@rankno := @rankno + (@pre <> (@pre := salary)) as rank
from salaries, (select @rankno := 0, @pre := -1) as r
where to_date = '9999-01-01'
order by salary desc, emp_no asc;
/*
这里的逻辑是根据salary排序后，通过两个变量，一个变量记录工资，一个变量记录排名，当工资变动则排名+1（有序了已经），不变说明是相同排名则排名不变

解析：变量使用前要加@，:=表示赋值，(SELECT @rankno := 0, @pre := -1) r是进行初始化，r是推导表的别名，
@rankno代表排名，@pre代表工资，@rankno := @rankno + (@pre <> (@pre := salary)) rank是推导公式，rank是别名
@pre <> (@pre := salary)的执行顺序是：
@pre是上一次的值
@pre:=salary是进行新一次赋值给pre
判断<>，如果左右不想等，则返回1，否则(相等)返回0
*/
```



## 24、获取所有非manager员工当前的薪水情况

获取所有非manager员工当前的薪水情况，给出dept_no、emp_no以及salary ，当前表示to_date='9999-01-01'

```sql
CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE `dept_manager` (
`dept_no` char(4) NOT NULL,
`emp_no` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));

CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
```

**输出描述**

| dept_no | emp_no | salary |
| :------ | :----- | :----- |
| d001    | 10001  | 88958  |
| d004    | 10003  | 43311  |
| d005    | 10007  | 88070  |
| d006    | 10009  | 95409  |

**sql语句**

```sql
select de.dept_no, e.emp_no, s.salary
from dept_emp de, employees e, salaries s
where s.to_date='9999-01-01' 							-- 当前薪水
and s.emp_no = e.emp_no 
and e.emp_no = de.emp_no 
and e.emp_no not in (select emp_no from dept_manager)

-- 实际上可以省略employees表
select de.dept_no,de.emp_no,s.salary
from dept_emp de,salaries s
where s.to_date='9999-01-01'
and de.emp_no = s.emp_no 
and de.emp_no not in (select dm.emp_no
                      from dept_manager dm);
```



## 25、获取员工其当前的薪水比其manager当前薪水还高的相关信息

获取员工其当前的薪水比其manager当前薪水还高的相关信息，当前表示to_date='9999-01-01',

结果第一列给出员工的emp_no，

第二列给出其manager的manager_no，

第三列给出该员工当前的薪水emp_salary,

第四列给该员工对应的manager当前的薪水manager_salary

```sql
CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE `dept_manager` (
`dept_no` char(4) NOT NULL,
`emp_no` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
```

**输出描述：**

| emp_no | manager_no | emp_salary | manager_salary |
| :----- | :--------- | :--------- | :------------- |
| 10001  | 10002      | 88958      | 72527          |
| 10009  | 10010      | 95409      | 94409          |

**sql语句**

```sql
-- 四表联查
select de.emp_no,dm.emp_no as manager_no,s1.salary as emp_salary,s2.salary as manager_salary
from dept_emp de,dept_manager dm,salaries s1,salaries s2
where de.emp_no = s1.emp_no
and de.dept_no = dm.dept_no and de.emp_no != dm.emp_no
and dm.emp_no = s2.emp_no
and s1.salary > s2.salary
and s1.to_date='9999-01-01' and s2.to_date='9999-01-01';

-- 构建员工工资表和管理工资表，然后两表联查
select a.emp_no, b.manager_no, a.emp_salary, b.manager_salary
from (select de.dept_no,de.emp_no,s.salary as emp_salary
     from dept_emp de,salaries s
     where de.emp_no=s.emp_no and s.to_date='9999-01-01') a,
     (select dm.dept_no,dm.emp_no as manager_no,s.salary as manager_salary
     from dept_manager dm,salaries s
      where dm.emp_no=s.emp_no and s.to_date='9999-01-01') b
where a.dept_no = b.dept_no and a.emp_salary > b.manager_salary;
```



## 26、汇总各个部门当前员工的title类型

汇总各个部门当前员工的title类型的分配数目，即结果给出部门编号dept_no、dept_name、其部门下所有的当前(dept_emp.to_date = '9999-01-01')员工的当前(titles.to_date = '9999-01-01')title以及该类型title对应的数目count

(注：因为员工可能有离职，所有dept_emp里面to_date不为'9999-01-01'就已经离职了，不计入统计，而且员工可能有晋升，所以如果titles.to_date 不为 '9999-01-01'，那么这个可能是员工之前的职位信息，也不计入统计)

```sql
CREATE TABLE `departments` (
`dept_no` char(4) NOT NULL,
`dept_name` varchar(40) NOT NULL,
PRIMARY KEY (`dept_no`));

CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE IF NOT EXISTS `titles` (
`emp_no` int(11) NOT NULL,
`title` varchar(50) NOT NULL,
`from_date` date NOT NULL,
`to_date` date DEFAULT NULL);
```

**输出描述**

| dept_no | dept_name          | title           | count |
| :------ | :----------------- | :-------------- | :---- |
| d001    | Marketing          | Senior Engineer | 1     |
| d001    | Marketing          | Staff           | 1     |
| d002    | Finance            | Senior Engineer | 1     |
| d003    | Human Resources    | Senior Staff    | 1     |
| d004    | Production         | Senior Engineer | 2     |
| d005    | Development        | Senior Staff    | 1     |
| d006    | Quality Management | Engineer        | 2     |
| d006    | Quality Management | Senior Engineer | 1     |

**sql语句**

```sql
-- 将de.dept_no,title作为键进行分组
select de.dept_no, d.dept_name, t.title, count(*) as count
from departments d, dept_emp de, titles t
where t.emp_no = de.emp_no and d.dept_no = de.dept_no
and t.to_date = '9999-01-01' and de.to_date = '9999-01-01'
group by de.dept_no,title;
```



## 27、给出每个员工每年薪水涨幅超过5000的员工编号

给出每个员工每年薪水涨幅超过5000的员工编号emp_no、薪水变更开始日期from_date以及薪水涨幅值salary_growth，并按照salary_growth逆序排列。

提示：在sqlite中获取datetime时间对应的年份函数为strftime('%Y', to_date)

(数据保证每个员工的每条薪水记录to_date-from_date=1年，而且同一员工的下一条薪水记录from_data=上一条薪水记录的to_data)

```sql
CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));

--- 如：插入
INSERT INTO salaries VALUES(10001,52117,'1986-06-26','1987-06-26');
INSERT INTO salaries VALUES(10001,62102,'1987-06-26','1988-06-25');
INSERT INTO salaries VALUES(10002,72527,'1996-08-03','1997-08-03');
INSERT INTO salaries VALUES(10002,72527,'1997-08-03','1998-08-03');
INSERT INTO salaries VALUES(10002,72527,'1998-08-03','1999-08-03');
INSERT INTO salaries VALUES(10003,43616,'1996-12-02','1997-12-02');
INSERT INTO salaries VALUES(10003,43466,'1997-12-02','1998-12-02');
```

**输出：**

| emp_no | from_date  | salary_growth |
| ------ | ---------- | ------------- |
| 10001  | 1987-06-26 | 9985          |

**sql语句**

```sql
-- 不用strftime函数，凭借同一员工的下一条薪水记录from_data=上一条薪水记录的to_data的条件确定年份关系
select s2.emp_no,s2.from_date,(s2.salary-s1.salary) as salary_growth
from salaries s2, salaries s1
where s2.emp_no = s1.emp_no 
and s2.from_date = s1.to_date 
and s2.salary-s1.salary>5000
order by salary_growth desc;

-- 用strftime函数，修改限定条件即可
select s2.emp_no,s2.from_date,(s2.salary-s1.salary) as salary_growth
from salaries s2, salaries s1
where s2.emp_no = s1.emp_no 
and  strftime('%Y',s2.from_date) - strftime('%Y',s1.from_date)=1
and s2.salary-s1.salary>5000
order by salary_growth desc;
```



## 28、查找描述信息中包含robot的电影（题目奇奇怪怪的）

查找描述信息(film.description)中包含robot的电影对应的分类名称(category.name)以及电影数目(count(film_id))，而且还需要该分类包含电影总数量(count(film_category.film_id))>=5部

film表

| 字段        | 说明         |
| ----------- | ------------ |
| film_id     | 电影id       |
| title       | 电影名称     |
| description | 电影描述信息 |

category表

| 字段        | 说明                 |
| ----------- | -------------------- |
| category_id | 电影分类id           |
| name        | 电影分类名称         |
| last_update | 电影分类最后更新时间 |

film_category表

| 字段        | 说明                                 |
| ----------- | ------------------------------------ |
| film_id     | 电影id                               |
| category_id | 电影分类id                           |
| last_update | 电影id和分类id对应关系的最后更新时间 |

```sql
CREATE TABLE IF NOT EXISTS film (
film_id smallint(5)  NOT NULL DEFAULT '0',
title varchar(255) NOT NULL,
description text,
PRIMARY KEY (film_id));

CREATE TABLE category  (
category_id  tinyint(3)  NOT NULL ,
name  varchar(25) NOT NULL, `last_update` timestamp,
PRIMARY KEY ( category_id ));

CREATE TABLE film_category  (
film_id  smallint(5)  NOT NULL,
category_id  tinyint(3)  NOT NULL, `last_update` timestamp);
```



**如：输入为:**

```sql
--- 插入到film的记录
INSERT INTO film VALUES(1,'ACADEMY DINOSAUR','A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies');
INSERT INTO film VALUES(2,'ACE GOLDFINGER','A Astounding Epistle of a Database Administrator And a Explorer who must Find a Car in Ancient China');
INSERT INTO film VALUES(3,'ADAPTATION HOLES','A Astounding Reflection of a Lumberjack And a Car who must Sink a Lumberjack in A Baloon Factory');
INSERT INTO film VALUES(4,'AFFAIR PREJUDICE','A Fanciful Documentary of a Frisbee And a Lumberjack who must Chase a Monkey in A Shark Tank');
INSERT INTO film VALUES(5,'AFRICAN EGG','A Fast-Paced Documentary of a Pastry Chef And a Dentist who must Pursue a Forensic Psychologist in The Gulf of Mexico');
INSERT INTO film VALUES(6,'AGENT TRUMAN','A Intrepid Panorama of a robot And a Boy who must Escape a Sumo Wrestler in Ancient China');
INSERT INTO film VALUES(7,'AIRPLANE SIERRA','A Touching Saga of a Hunter And a Butler who must Discover a Butler in A Jet Boat');
INSERT INTO film VALUES(8,'AIRPORT POLLOCK','A Epic Tale of a Moose And a Girl who must Confront a Monkey in Ancient India');
INSERT INTO film VALUES(9,'ALABAMA DEVIL','A Thoughtful Panorama of a Database Administrator And a Mad Scientist who must Outgun a Mad Scientist in A Jet Boat');
INSERT INTO film VALUES(10,'ALADDIN CALENDAR','A Action-Packed Tale of a Man And a Lumberjack who must Reach a Feminist in Ancient China');

--- 插入到category的记录
INSERT INTO category VALUES(1,'Action','2006-02-14 20:46:27');
INSERT INTO category VALUES(2,'Animation','2006-02-14 20:46:27');
INSERT INTO category VALUES(3,'Children','2006-02-14 20:46:27');
INSERT INTO category VALUES(4,'Classics','2006-02-14 20:46:27');
INSERT INTO category VALUES(5,'Comedy','2006-02-14 20:46:27');
INSERT INTO category VALUES(6,'Documentary','2006-02-14 20:46:27');
INSERT INTO category VALUES(7,'Drama','2006-02-14 20:46:27');
INSERT INTO category VALUES(8,'Family','2006-02-14 20:46:27');
INSERT INTO category VALUES(9,'Foreign','2006-02-14 20:46:27');
INSERT INTO category VALUES(10,'Games','2006-02-14 20:46:27');
INSERT INTO category VALUES(11,'Horror','2006-02-14 20:46:27');
INSERT INTO category VALUES(12,'Music','2006-02-14 20:46:27');
INSERT INTO category VALUES(13,'New','2006-02-14 20:46:27');
INSERT INTO category VALUES(14,'Sci-Fi','2006-02-14 20:46:27');
INSERT INTO category VALUES(15,'Sports','2006-02-14 20:46:27');
INSERT INTO category VALUES(16,'Travel','2006-02-14 20:46:27');

--- 插入到film_category的记录
INSERT INTO film_category VALUES(1,6,'2006-02-14 21:07:09');
INSERT INTO film_category VALUES(2,11,'2006-02-14 21:07:09');
INSERT INTO film_category VALUES(3,6,'2006-02-14 21:07:09');
INSERT INTO film_category VALUES(4,11,'2006-02-14 21:07:09');
INSERT INTO film_category VALUES(5,6,'2006-02-14 21:07:09');
INSERT INTO film_category VALUES(6,6,'2006-02-14 21:07:09');
INSERT INTO film_category VALUES(7,5,'2006-02-14 21:07:09');
INSERT INTO film_category VALUES(8,6,'2006-02-14 21:07:09');
INSERT INTO film_category VALUES(9,11,'2006-02-14 21:07:09');
INSERT INTO film_category VALUES(10,15,'2006-02-14 21:07:09');
```

**如输出为:**

| 分类名称category.name | 电影数目count(film_id) |
| --------------------- | ---------------------- |
| Documentary           | 1                      |

**sql语句**

简而言之，输出需要包含robot的电影对应的分类名称和其中包含robot的电影的数量，而且这个分类必须包含5个电影及以上

```sql
select c.name,count(fc.film_id)
from film f,category c,film_category fc
where f.description like '%robot%' 
and f.film_id = fc.film_id and fc.category_id = c.category_id
and c.category_id in (select category_id from film_category			-- 挑选出分类满足大于等于5的category_id
                     group by category_id
                     having count(film_id)>=5)
group by c.category_id;												-- 最后再从剩下的记录统计下
```



## 29、使用join查询方式找出没有分类的电影id以及名称

使用join查询方式找出没有分类的电影id以及名称

表信息同上题

```sql
CREATE TABLE IF NOT EXISTS film (
film_id smallint(5)  NOT NULL DEFAULT '0',
title varchar(255) NOT NULL,
description text,
PRIMARY KEY (film_id));

CREATE TABLE category  (
category_id  tinyint(3)  NOT NULL ,
name  varchar(25) NOT NULL, `last_update` timestamp,
PRIMARY KEY ( category_id ));

CREATE TABLE film_category  (
film_id  smallint(5)  NOT NULL,
category_id  tinyint(3)  NOT NULL, `last_update` timestamp);
```

**如输入为：**

```sql
INSERT INTO film VALUES(1,'ACADEMY DINOSAUR','A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies');
INSERT INTO film VALUES(2,'ACE GOLDFINGER','A Astounding Epistle of a Database Administrator And a Explorer who must Find a Car in Ancient China');
INSERT INTO film VALUES(3,'ADAPTATION HOLES','A Astounding Reflection of a Lumberjack And a Car who must Sink a Lumberjack in A Baloon Factory');

INSERT INTO category VALUES(1,'Action','2006-02-14 20:46:27');
INSERT INTO category VALUES(2,'Animation','2006-02-14 20:46:27');
INSERT INTO category VALUES(3,'Children','2006-02-14 20:46:27');
INSERT INTO category VALUES(4,'Classics','2006-02-14 20:46:27');
INSERT INTO category VALUES(5,'Comedy','2006-02-14 20:46:27');
INSERT INTO category VALUES(6,'Documentary','2006-02-14 20:46:27');
INSERT INTO category VALUES(7,'Drama','2006-02-14 20:46:27');
INSERT INTO category VALUES(8,'Family','2006-02-14 20:46:27');
INSERT INTO category VALUES(9,'Foreign','2006-02-14 20:46:27');
INSERT INTO category VALUES(10,'Games','2006-02-14 20:46:27');
INSERT INTO category VALUES(11,'Horror','2006-02-14 20:46:27');

INSERT INTO film_category VALUES(1,6,'2006-02-14 21:07:09');
INSERT INTO film_category VALUES(2,11,'2006-02-14 21:07:09');
```

**输出为：**

| 电影id | 名称             |
| ------ | ---------------- |
| 3      | ADAPTATION HOLES |

**sql语句**

```sql
-- 子查询加内连接
select film_id,title
from film 
where film_id not in (select f.film_id from film f
                     join film_category fc on fc.film_id=f.film_id);
 
-- 左外连接，找null，注意用is
select f.film_id, f.title
from film f
left join film_category fc on f.film_id=fc.film_id
where fc.category_id is null;
```



## 30、使用子查询的方式找出属于Action分类的所有电影对应的title,description

你能使用子查询的方式找出属于Action分类的所有电影对应的title,description吗

```sql
CREATE TABLE IF NOT EXISTS film (
film_id smallint(5)  NOT NULL DEFAULT '0',
title varchar(255) NOT NULL,
description text,
PRIMARY KEY (film_id));

CREATE TABLE category  (
category_id  tinyint(3)  NOT NULL ,
name  varchar(25) NOT NULL, `last_update` timestamp,
PRIMARY KEY ( category_id ));

CREATE TABLE film_category  (
film_id  smallint(5)  NOT NULL,
category_id  tinyint(3)  NOT NULL, `last_update` timestamp);
```

**输入如：**

```sql
INSERT INTO film VALUES(1,'ACADEMY DINOSAUR','A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies');
INSERT INTO film VALUES(2,'ACE GOLDFINGER','A Astounding Epistle of a Database Administrator And a Explorer who must Find a Car in Ancient China');
INSERT INTO film VALUES(3,'ADAPTATION HOLES','A Astounding Reflection of a Lumberjack And a Car who must Sink a Lumberjack in A Baloon Factory');

INSERT INTO category VALUES(1,'Action','2006-02-14 20:46:27');
INSERT INTO category VALUES(2,'Animation','2006-02-14 20:46:27');
INSERT INTO category VALUES(3,'Children','2006-02-14 20:46:27');
INSERT INTO category VALUES(4,'Classics','2006-02-14 20:46:27');
INSERT INTO category VALUES(5,'Comedy','2006-02-14 20:46:27');
INSERT INTO category VALUES(6,'Documentary','2006-02-14 20:46:27');

INSERT INTO film_category VALUES(1,1,'2006-02-14 21:07:09');
INSERT INTO film_category VALUES(2,1,'2006-02-14 21:07:09');
INSERT INTO film_category VALUES(3,6,'2006-02-14 21:07:09');
```

**输出：**

| title            | description                                                  |
| ---------------- | ------------------------------------------------------------ |
| ACADEMY DINOSAUR | A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies |
| ACE GOLDFINGER   | A Astounding Epistle of a Database Administrator And a Explorer who must Find a Car in Ancient China |

**sql语句**

```sql
-- 子查询
select f.title,f.description 
from film f
where f.film_id in (select fc.film_id 
                    from film_category fc, category c
                   where fc.category_id=c.category_id and c.name='Action');
                   
-- 直接构建表   
select f.title, f.description
from (select c.category_id , f.film_id
      from film_category fc , category c , film f
      where f.film_id =fc.film_id
      and fc.category_id = c.category_id
      and c.name = 'Action') a ,
      film f
where f.film_id = a.film_id
```



## 31、将employees表的所有员工的last_name和first_name拼接起来作为Name(==Concat函数介绍==)

将employees表的所有员工的last_name和first_name拼接起来作为Name，中间以一个空格区分

(注：该数据库系统是sqllite,字符串拼接为 || 符号，不支持concat函数)

```sql
CREATE TABLE `employees` ( `emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
```

**输出描述：**

| Name               |
| :----------------- |
| Facello Georgi     |
| Simmel Bezalel     |
| Bamford Parto      |
| Koblick Chirstian  |
| Maliniak Kyoichi   |
| Preusig Anneke     |
| Zielinski Tzvetan  |
| Kalloufi Saniya    |
| Peac Sumant        |
| Piveteau Duangkaew |
| Sluis Mary         |

**sql语句**

```sql
select (last_name||' '||first_name) as Name
from employees
```

**concat函数拓展：**

mysql不支持||，||作为或处理，字符串拼接用concat函数

SQL CONCAT函数用于将多个字符串（不止两个）连接起来，形成一个单一的字符串。

```sql
SELECT CONCAT('FIRST ', 'SECOND'); 	-- 'FIRST '后有个空格的
-- 输出
+----------------------------+
| CONCAT('FIRST ', 'SECOND') |
+----------------------------+
| FIRST SECOND               |
+----------------------------+

SELECT CONCAT('Hello ', 'World!','Hello ','mysql');
-- 输出
+---------------------------------------------+
| CONCAT('Hello ', 'World!','Hello ','mysql') |
+---------------------------------------------+
| Hello World!Hello mysql                     |
+---------------------------------------------+
```

MySQL中concat_ws函数

使用方法：contcat_ws(separator,str1,str2,...)

contcat_ws() 代表 CONCAT With Separator ，是CONCAT()的特殊形式。第一个参数是其它参数的分隔符。分隔符的位置放在要连接的两个字符串之间。分隔符可以是一个字符串，也可以是其它参数。注意：如果分隔符为 NULL，则结果为 NULL。函数会忽略任何分隔符参数后的 NULL 值。

和MySQL中concat函数不同的是, concat_ws函数在执行的时候,不会因为NULL值而返回NULL 

```sql
mysql> select concat_ws(',','11','22','33');
-- 输出
+-------------------------------+
| concat_ws(',','11','22','33') |
+-------------------------------+
| 11,22,33                      |
+-------------------------------+


mysql> select concat_ws(',','11','22',NULL);
+-------------------------------+
| concat_ws(',','11','22',NULL) |
+-------------------------------+
| 11,22                         |
+-------------------------------+
```



## 32、创建一个actor表，包含如下列信息

创建一个actor表，包含如下列信息(注：sqlite获取系统默认时间是datetime('now','localtime'))

| 列表        | 类型        | 是否为NULL | 含义                               |
| :---------- | :---------- | :--------- | :--------------------------------- |
| actor_id    | smallint(5) | not null   | 主键id                             |
| first_name  | varchar(45) | not null   | 名字                               |
| last_name   | varchar(45) | not null   | 姓氏                               |
| last_update | timestamp   | not null   | 最后更新时间，默认是系统的当前时间 |

**sql语句**

```sql
create table if not exists `actor`(											-- 建议加 if not exists 字段
`actor_id` smallint(5) not null,											-- primary key写在这也行
`first_name` varchar(45) not null ,											-- ``尖冒号是可选的，不加也行
`last_name` varchar(45)	not null  ,
`last_update` timestamp not null default(datetime('now','localtime')),		--- 注意是default(...)
primary key(`actor_id`));
```

注意点：

1、建表建议加上 if not exists 字段

2、default值写在括号里

## 33、批量插入数据（==给表加行列==）

对于表actor批量插入如下数据(不能有2条insert语句哦!)

```sql
CREATE TABLE IF NOT EXISTS actor (
actor_id smallint(5) NOT NULL PRIMARY KEY,
first_name varchar(45) NOT NULL,
last_name varchar(45) NOT NULL,
last_update timestamp NOT NULL DEFAULT (datetime('now','localtime')))
```

| actor_id | first_name | last_name | last_update         |
| :------- | :--------- | :-------- | :------------------ |
| 1        | PENELOPE   | GUINESS   | 2006-02-15 12:34:33 |
| 2        | NICK       | WAHLBERG  | 2006-02-15 12:34:33 |

**sql语句**

```sql
insert into actor(actor_id,first_name,last_name,last_update) 
values(1,'PENELOPE','GUINESS','2006-02-15 12:34:33'),
      (2,'NICK','WAHLBERG','2006-02-15 12:34:33');				-- values不需要(),记录要()
```

拓展：

1、给表加行

- insert into 表名(列名) values (行内容),(行内容);

2、给表加列

- alter table 表名 add column 列名 列约束，列名 列约束；



## 34、批量插入数据，不使用replace操作（==插入忽略==）

对于表actor批量插入如下数据,如果数据已经存在，请忽略(不支持使用replace操作)
CREATE TABLE IF NOT EXISTS actor (
actor_id smallint(5) NOT NULL PRIMARY KEY,
first_name varchar(45) NOT NULL,
last_name varchar(45) NOT NULL,
last_update timestamp NOT NULL DEFAULT (datetime('now','localtime')))

| actor_id | first_name | last_name | last_update           |
| :------- | :--------- | :-------- | :-------------------- |
| '3'      | 'ED'       | 'CHASE'   | '2006-02-15 12:34:33' |

sql语句

```sql
-- 牛客判题系统是sqlite3，以下是sqlit3的写法
insert or ignore into actor(actor_id,first_name,last_name,last_update)
values (3,'ED','CHASE','2006-02-15 12:34:33');

-- 如果是mysql，那么把or去掉
insert ignore into actor(actor_id,first_name,last_name,last_update)
values (3,'ED','CHASE','2006-02-15 12:34:33');
```

拓展：

insert into:插入数据,如果主键重复，则报错

insert repalce:插入替换数据,如果存在主键或unique数据则替换数据

insert ignore:如果存在数据,则忽略。



**1、如果不存在则插入，如果存在则忽略**

```
INSERT OR IGNORE INTO tablename VALUES(...);
```

**2、 如果不存在则插入，如果存在则替换**

```
INSERT OR REPLACE INTO tablename VALUES(...);
```



## 35、创建一个actor_name表

对于如下表actor，其对应的数据为:

| actor_id | first_name | last_name | last_update         |
| :------- | :--------- | :-------- | :------------------ |
| 1        | PENELOPE   | GUINESS   | 2006-02-15 12:34:33 |
| 2        | NICK       | WAHLBERG  | 2006-02-15 12:34:33 |

请你创建一个actor_name表，并且将actor表中的所有first_name以及last_name导入该表.

actor_name表结构如下：

| 列表       | 类型        | 是否为NULL | 含义 |
| :--------- | :---------- | :--------- | :--- |
| first_name | varchar(45) | not null   | 名字 |
| last_name  | varchar(45) | not null   | 姓氏 |

**sql语句**

```sql
-- 方法一：先建表，再插入
create table if not exists actor_name(
first_name varchar(45) not null,
last_name varchar(45) not null
);
insert into actor_name select first_name,last_name from actor;

-- 方法二：建表直接选择字段
create table actor_name as						-- 如果是mysql，as可去
select first_name,last_name from actor;
```



## 36、对first_name创建唯一索引uniq_idx_firstname

针对如下表actor结构创建索引：

(注:在 SQLite 中,除了重命名表和在已有的表中添加列,ALTER TABLE 命令不支持其他操作)

CREATE TABLE IF NOT EXISTS actor (
actor_id smallint(5) NOT NULL PRIMARY KEY,
first_name varchar(45) NOT NULL,
last_name varchar(45) NOT NULL,
last_update timestamp NOT NULL DEFAULT (datetime('now','localtime')))

对first_name创建唯一索引uniq_idx_firstname，对last_name创建普通索引idx_lastname

(请先创建唯一索引，再创建普通索引)

```sql
-- 创建唯一索引
create unique index uniq_idx_firstname on actor(first_name);
-- 创建普通索引
create index idx_lastname on actor(last_name)
```



## 37、针对actor表创建视图actor_name_view

针对actor表创建视图actor_name_view，只包含first_name以及last_name两列，并对这两列重新命名，first_name为first_name_v，last_name修改为last_name_v：

```sql
CREATE TABLE IF NOT EXISTS actor (
actor_id smallint(5) NOT NULL PRIMARY KEY,
first_name varchar(45) NOT NULL,
last_name varchar(45) NOT NULL,
last_update timestamp NOT NULL DEFAULT (datetime('now','localtime')))
```

**sql语句**

```sql
-- 方法一：正常语法创建，注意 CREATE VIEW ... AS ... 的 AS 是创建视图语法中的一部分
create view actor_name_view as 
select 
first_name as first_name_v,
last_name as last_name_v
from actor;

-- 方法二：直接在视图名的后面用小括号创建视图中的字段名
create view actor_name_view(first_name_v,last_name_v) as 
select first_name,last_name
from actor;
```



## 38、针对上面的salaries表emp_no字段创建索引idx_emp_no

针对salaries表emp_no字段已经创建索引idx_emp_no，查询emp_no为10005, **使用强制索引**。

```sql
CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
create index idx_emp_no on salaries(emp_no);
```

**sql语句**

```sql
-- SQLite:用indexed by
select *
from salaries
indexed by idx_emp_no
where emp_no = 10005;

--MySQL:用force index
select *
from salaries
force index(idx_emp_no)				--- 有括号
where emp_no = 10005;
```

SQLite中，使用` INDEXED BY INDEX_NAME `语句进行强制索引查询

MySQL中，使用 `FORCE INDEX(INDEX_NAME) `语句进行强制索引查询



## 39、在last_update后面新增加一列名字为create_date

存在actor表，包含如下列信息：

```sql
CREATE TABLE IF NOT EXISTS actor (
actor_id smallint(5) NOT NULL PRIMARY KEY,
first_name varchar(45) NOT NULL,
last_name varchar(45) NOT NULL,
last_update timestamp NOT NULL DEFAULT (datetime('now','localtime')));
```


现在在last_update后面新增加一列名字为create_date, 类型为datetime, NOT NULL，默认值为'0000-00-00 00:00:00'

**sql语句**

```sql
-- 下面add column可省略column
alter table actor add column create_date datetime not null default '0000-00-00 00:00:00';	-- 不需要括号
```

如33题拓展所见，给表加列的语法为

- alter table 表名 add [column] 列名 列约束，列名 列约束；

其中不加column也可以



## 40、构造一个触发器audit_log（==触发器==）

构造一个触发器audit_log，在向employees_test表中插入一条数据的时候，触发插入相关的数据到audit中。

```sql
CREATE TABLE employees_test(
ID INT PRIMARY KEY NOT NULL,
NAME TEXT NOT NULL,
AGE INT NOT NULL,
ADDRESS CHAR(50),
SALARY REAL
);

CREATE TABLE audit(
EMP_no INT NOT NULL,
NAME TEXT NOT NULL
);
```

**sql语句**

```sql
create trigger audit_log after insert on employees_test				-- 没有into了
begin
    insert into audit values(NEW.ID,NEW.NAME);						-- 完整语句，每条带分号
end;
```

注意点：

1.创建触发器使用语句：CREATE TRIGGER trigname;

2.指定触发器触发的事件在执行某操作之前还是之后，使用语句：BEFORE/AFTER [INSERT/UPDATE/ADD] ON tablename

3.触发器触发的事件写在BEGIN和END之间，且语句是完整的，以分号结束

4.触发器中可以通过**NEW获得触发事件之后2对应的tablename的相关列的值**，**OLD获得触发事件之前的2对应的tablename的相关列的值（比如要修改employees_test，能拿到修改前的值）**



## 41、删除emp_no重复的记录，只保留最小的id对应的记录。

删除emp_no重复的记录，只保留最小的id对应的记录。

```sql
CREATE TABLE IF NOT EXISTS titles_test (
id int(11) not null primary key,
emp_no int(11) NOT NULL,
title varchar(50) NOT NULL,
from_date date NOT NULL,
to_date date DEFAULT NULL);

insert into titles_test values ('1', '10001', 'Senior Engineer', '1986-06-26', '9999-01-01'),
('2', '10002', 'Staff', '1996-08-03', '9999-01-01'),
('3', '10003', 'Senior Engineer', '1995-12-03', '9999-01-01'),
('4', '10004', 'Senior Engineer', '1995-12-03', '9999-01-01'),
('5', '10001', 'Senior Engineer', '1986-06-26', '9999-01-01'),
('6', '10002', 'Staff', '1996-08-03', '9999-01-01'),
('7', '10003', 'Senior Engineer', '1995-12-03', '9999-01-01');
```

删除后titles_test表为

| id   | emp_no | title           | from_date  | to_date    |
| ---- | ------ | --------------- | ---------- | ---------- |
| 1    | 10001  | Senior Engineer | 1986-06-26 | 9999-01-01 |
| 2    | 10002  | Staff           | 1996-08-03 | 9999-01-01 |
| 3    | 10003  | Senior Engineer | 1995-12-03 | 9999-01-01 |
| 4    | 10004  | Senior Engineer | 1995-12-03 | 9999-01-01 |

**sql语句**

本题思路如下：

1、正向思维，就找id比最小的还大的记录，删除

2、反向思维，找最小id，不是删除

都要用到group去找最小id

```sql
-- 方法一：找出所有emp_no组中最小的那些id，删掉不是最小id的即可
delete from titles_test
where id not in(select min(id) as id 
                from titles_test t
               group by emp_no);

-- 方法二：找出所有出现的频次>1的emp_no，而且id还比最小的id大的记录，删除掉
delete from titles_test where id in (
    select id from(select a.id from titles_test a ,
                   (select min(id) as id, emp_no 
                    from titles_test
                    group by emp_no 
                    having count(emp_no) > 1) AS b
                where a.emp_no = b.emp_no and a.id > b.id ) as t);
```

值得注意的是，在mysql中无法通过第一种写法，报错信息

```
You can't specify target table for update in FROM clause
```

大致意思是：不能先select出同一表中的某些值，再update这个表(在同一语句中)，那么需要他们不是同一个表即可，再嵌一层即可

```mysql
delete from titles_test 
where id not in (select a.id 
                 from((select min(id) as id
                       from titles_test t
                       group by emp_no))as a);
```

细心的同学可以发现，第二个sql from 的表还特地起了别名t，否则也是无法通过



## 42、将所有to_date为9999-01-01的全部更新为NULL

将所有to_date为9999-01-01的全部更新为NULL,且 from_date更新为2001-01-01。

```sql
CREATE TABLE IF NOT EXISTS titles_test (
id int(11) not null primary key,
emp_no int(11) NOT NULL,
title varchar(50) NOT NULL,
from_date date NOT NULL,
to_date date DEFAULT NULL);

insert into titles_test values ('1', '10001', 'Senior Engineer', '1986-06-26', '9999-01-01'),
('2', '10002', 'Staff', '1996-08-03', '9999-01-01'),
('3', '10003', 'Senior Engineer', '1995-12-03', '9999-01-01'),
('4', '10004', 'Senior Engineer', '1995-12-03', '9999-01-01'),
('5', '10001', 'Senior Engineer', '1986-06-26', '9999-01-01'),
('6', '10002', 'Staff', '1996-08-03', '9999-01-01'),
('7', '10003', 'Senior Engineer', '1995-12-03', '9999-01-01');
```

更新后的值:

titles_test 表的值：

| id   | emp_no | title           | from_date  | to_date |
| ---- | ------ | --------------- | ---------- | ------- |
| 1    | 10001  | Senior Engineer | 2001-01-01 | NULL    |
| 2    | 10002  | Staff           | 2001-01-01 | NULL    |
| 3    | 10003  | Senior Engineer | 2001-01-01 | NULL    |
| 4    | 10004  | Senior Engineer | 2001-01-01 | NULL    |
| 5    | 10001  | Senior Engineer | 2001-01-01 | NULL    |
| 6    | 10002  | Staff           | 2001-01-01 | NULL    |
| 7    | 10003  | Senior Engineer | 2001-01-01 | NULL    |

**sql语句**

```sql
-- 注意不是设置成字符串的'NULL',而是直接设置为NULL，还有设置多个值用逗号连接
update titles_test 
set from_date='2001-01-01' , to_date=NULL			-- 逗号连接
where to_date='9999-01-01';
```



## 43、将id=5以及emp_no=10001的行数据替换成id=5以及emp_no=10005（==replace==）

将id=5以及emp_no=10001的行数据替换成id=5以及emp_no=10005,其他数据保持不变，**使用replace实现**。

```sql
CREATE TABLE IF NOT EXISTS titles_test (
id int(11) not null primary key,
emp_no int(11) NOT NULL,
title varchar(50) NOT NULL,
from_date date NOT NULL,
to_date date DEFAULT NULL);

insert into titles_test values ('1', '10001', 'Senior Engineer', '1986-06-26', '9999-01-01'),
('2', '10002', 'Staff', '1996-08-03', '9999-01-01'),
('3', '10003', 'Senior Engineer', '1995-12-03', '9999-01-01'),
('4', '10004', 'Senior Engineer', '1995-12-03', '9999-01-01'),
('5', '10001', 'Senior Engineer', '1986-06-26', '9999-01-01'),
('6', '10002', 'Staff', '1996-08-03', '9999-01-01'),
('7', '10003', 'Senior Engineer', '1995-12-03', '9999-01-01');
```

**sql语句**

```sql
-- 使用replace
-- 解法一：replace字段更新替换，用的是into
-- 由于 REPLACE 的新记录中 id=5，与表中的主键 id=5 冲突，故会替换掉表中 id=5的记录，否则会插入一条新记录
replace into titles_test values(5, 10005, 'Senior Engineer', '1986-06-26', '9999-01-01');

-- 也可以不写死其他值
replace into titles_test
select 5, 10005, title, from_date, to_date
from titles_test
where id = 5;

-- 解法二：运用REPLACE(X,Y,Z)函数。
-- 其中X是要处理的字段，Y是X中将要被替换的字符串，Z是用来替换Y的字符串，最终返回替换后的字符串。
update titles_test set emp_no = replace(emp_no,10001,10005) where id = 5


-- 不使用replace
update titles_test
set emp_no=10005
where id=5 and emp_no=10001;
```



## 44、将titles_test表名修改为titles_2017

将titles_test表名修改为titles_2017。

```sql
CREATE TABLE IF NOT EXISTS titles_test (
id int(11) not null primary key,
emp_no int(11) NOT NULL,
title varchar(50) NOT NULL,
from_date date NOT NULL,
to_date date DEFAULT NULL);

insert into titles_test values ('1', '10001', 'Senior Engineer', '1986-06-26', '9999-01-01'),
('2', '10002', 'Staff', '1996-08-03', '9999-01-01'),
('3', '10003', 'Senior Engineer', '1995-12-03', '9999-01-01'),
('4', '10004', 'Senior Engineer', '1995-12-03', '9999-01-01'),
('5', '10001', 'Senior Engineer', '1986-06-26', '9999-01-01'),
('6', '10002', 'Staff', '1996-08-03', '9999-01-01'),
('7', '10003', 'Senior Engineer', '1995-12-03', '9999-01-01');
```

**sql语句**

```sql
-- mysql下面to可省，sqlite3不可
alter table titles_test rename to titles_2017  

-- mysql还可以直接这么写
rename table titles_test to titles_2017 
```

拓展：

修改数据库名

RENAME DATABASE books TO 新库名;



## 45、在audit表上创建外键约束，其emp_no对应employees_test表的主键id

在audit表上创建外键约束，其emp_no对应employees_test表的主键id。

(audit已经创建，需要先drop)

```sql
CREATE TABLE employees_test(
ID INT PRIMARY KEY NOT NULL,
NAME TEXT NOT NULL,
AGE INT NOT NULL,
ADDRESS CHAR(50),
SALARY REAL
);

CREATE TABLE audit(
EMP_no INT NOT NULL,
create_date datetime NOT NULL
);
```

(注：创建表的时候，字段的顺序不要改变)



**sql语句**

注意，外键要设置为表级约束

```sql
-- 没必要删表再建，但本题是这么要求的
drop table if exists audit;
CREATE TABLE audit(
EMP_no INT NOT NULL ,
create_date datetime NOT NULL,
foreign key(EMP_no) references employees_test(ID)
);

-- 如果是mysql，可以直接增加表级约束
alter table audit
add foreign key(emp_no) references employees_test(id)
```



## 46、将所有获取奖金的员工当前的薪水增加10%

请你写出更新语句，将所有获取奖金的员工当前的(salaries.to_date='9999-01-01')薪水增加10%。(emp_bonus里面的emp_no都是当前获奖的所有员工)

```sql
create table emp_bonus(
emp_no int not null,
btype smallint not null);

CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL, PRIMARY KEY (`emp_no`,`from_date`));
```

如：

```sql
INSERT INTO emp_bonus VALUES (10001,1);
INSERT INTO salaries VALUES(10001,85097,'2001-06-22','2002-06-22');
INSERT INTO salaries VALUES(10001,88958,'2002-06-22','9999-01-01');
```

更新后的结果:

salaries:

| emp_no | salary  | from_date  | to_date    |
| ------ | ------- | ---------- | ---------- |
| 10001  | 85097   | 2001-06-22 | 2002-06-22 |
| 10001  | 97853.8 | 2002-06-22 | 9999-01-01 |

**sql语句**

这道题的意思是，获取奖金的员工，工资增加10%，而且是当前工资，读不清题意，很容易翻车

```sql
update salaries
set salary = 1.1 * salary 
where to_date='9999-01-01' 
and emp_no in (select emp_no 
               from emp_bonus);
```



## 47、针对库中的所有表生成select count(*)对应的SQL语句(==如何获取数据库的所有表==）

针对库中的所有表生成select count(*)对应的SQL语句，如数据库里有以下表，

(注:在 SQLite 中用 “||” 符号连接字符串，无法使用concat函数)

employees

departments

dept_emp

dept_manage

salaries

titles

emp_bonus

那么就会输出以下的样子:

| cnts                               |
| :--------------------------------- |
| select count(*) from employees;    |
| select count(*) from departments;  |
| select count(*) from dept_emp;     |
| select count(*) from dept_manager; |
| select count(*) from salaries;     |
| select count(*) from titles;       |
| select count(*) from emp_bonus;    |

**sql语句**

```sql
-- sqlite
select "select count(*) from" || name ||";" as cnts
from sqlite_master
where type='table';

-- mysql
select concat("select count(*) from ", table_name,";") as cnts
from (select table_name from information_schema.tables where table_schema='sql_q') as tables_from_db;
```

**SQLite**

在 SQLite 系统表 sqlite_master 中可以获得所有表的索引，其中字段 name 是所有表的名字，而且对于自己创建的表而言，字段 type 永远是 'table'

**MySQL**

mysql中针对某个库,获取所有表名字代码为

```mysql
select table_name from information_schema.tables where table_schema='shop' ;  # 其中shop为数据库名字
```



## 48、将employees表中的所有员工的last_name和first_name通过引号连接起来

将employees表中的所有员工的last_name和first_name通过(')连接起来。(不支持concat，请用||实现)

```sql
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`)); 
```

**输出格式:**

| name               |
| :----------------- |
| Facello'Georgi     |
| Simmel'Bezalel     |
| Bamford'Parto      |
| Koblick'Chirstian  |
| Maliniak'Kyoichi   |
| Preusig'Anneke     |
| Zielinski'Tzvetan  |
| Kalloufi'Saniya    |
| Peac'Sumant        |
| Piveteau'Duangkaew |
| Sluis'Mary         |

**sql语句**

```sql
-- sqlite：不能用'\''没转义
select last_name ||"'"||first_name as name
from employees;

-- mysql：可以用'\''
select CONCAT(last_name,'\'',first_name) as name
from employees;
```



## 49、查找字符串 10,A,B 中逗号,出现的次数cnt

查找字符串'10,A,B' 中逗号','出现的次数cnt。

**sql语句**

①巧用length函数和replace，length函数计算字符串的长度，length("10,A,B")算出整个字符串的长度。

②使用replace将 , 替换为空，那么整个字符串减少的长度等于 , 的长度，两者相减就是 , 出现的次数。

```sql
select (length("10,A,B") - length(replace("10,A,B", ",", "")))  as cnt;
```



## 50、获取Employees中的first_name

获取Employees中的first_name，查询按照first_name最后两个字母，按照升序进行排列

```sql
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
```

**输出格式：**

| first_name |
| :--------- |
| Chirstian  |
| Tzvetan    |
| Bezalel    |
| Duangkaew  |
| Georgi     |
| Kyoichi    |
| Anneke     |
| Sumant     |
| Mary       |
| Parto      |
| Saniya     |

**sql语句**

本题考查 substr(X,Y,Z) 或 substr(X,Y) 函数的使用。其中**X是要截取的字符串**。**Y是字符串的起始位置**（注意第一个字符的位置为1，而不为0），取值范围是±(1~length(X))，当Y等于length(X)时，则截取最后一个字符；当Y等于负整数-n时，则从倒数第n个字符处截取。**Z是要截取字符串的长度**，取值范围是正整数，若Z省略，则从Y处一直截取到字符串末尾；若Z大于剩下的字符串长度，也是截取到字符串末尾为止。

```sql
select first_name
from employees
order by substr(first_name,length(first_name)-1,2);
```



## 51、按照dept_no进行汇总（==group_concat==）

按照dept_no进行汇总，属于同一个部门的emp_no按照逗号进行连接，结果给出dept_no以及连接出的结果employees

```sql
CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));
```

**输出格式:**

| dept_no | employees         |
| :------ | :---------------- |
| d001    | 10001,10002       |
| d002    | 10006             |
| d003    | 10005             |
| d004    | 10003,10004       |
| d005    | 10007,10008,10010 |
| d006    | 10009,10010       |

**sql语句**

```sql
-- sqlite
select dept_no, group_concat(emp_no) as employees
from dept_emp
group by dept_no;

-- mysql
-- 三种方式，1、emp_no 2、emp_no SEPARATOR ',' 3、emp_no, ',' 注意前两种写法都是正常输出，3会打印多很多','，不可取
select dept_no,group_concat(emp_no SEPARATOR ',') as employees	
from dept_emp 
group by dept_no;
```

本题要用到聚合函数group_concat(X,Y)，其中**X是要连接的字段，Y是连接时用的符号**，可省略，默认为逗号。**此函数必须与 GROUP BY 配合使用。**此题以 dept_no 作为分组，将每个分组中不同的emp_no用逗号连接起来（即可省略Y）。

**group_concat()函数返回X的非null值的连接后的字符串。如果给出了参数Y，将会在每个X之间用Y作为分隔符。如果省略了Y，“，”将作为默认的分隔符。每个元素连接的顺序是随机的。**



## 52、查找排除当前最大、最小salary之后的员工的平均工资avg_salary

查找排除最大、最小salary之后的当前(to_date = '9999-01-01' )员工的平均工资avg_salary。

```sql
CREATE TABLE `salaries` ( `emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
```

如：

```sql
INSERT INTO salaries VALUES(10001,85097,'2001-06-22','2002-06-22');
INSERT INTO salaries VALUES(10001,88958,'2002-06-22','9999-01-01');
INSERT INTO salaries VALUES(10002,72527,'2001-08-02','9999-01-01');
INSERT INTO salaries VALUES(10003,43699,'2000-12-01','2001-12-01');
INSERT INTO salaries VALUES(10003,43311,'2001-12-01','9999-01-01');
INSERT INTO salaries VALUES(10004,70698,'2000-11-27','2001-11-27');
INSERT INTO salaries VALUES(10004,74057,'2001-11-27','9999-01-01');
```

**输出格式:**

| avg_salary |
| :--------- |
| 73292      |

**sql语句**

```sql
-- 可以用 != 、<> 、 not in
select avg(salary)
from salaries
where salary!=(select max(salary)
               from salaries
               where to_date='9999-01-01')
and salary!=(select min(salary)
             from salaries
             where to_date='9999-01-01')
and to_date='9999-01-01';

-- 也可以用比最大值小，比最小值大
select avg(salary)
from salaries
where salary<(select max(salary)
               from salaries
               where to_date='9999-01-01')
and salary>(select min(salary)
             from salaries
             where to_date='9999-01-01')
and to_date='9999-01-01';
```



## 53、分页查询employees表，每5行一页，返回第2页的数据

分页查询employees表，每5行一页，返回第2页的数据

```sql
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
```

**sql语句**

```sql
-- 两种写法
-- 法一：offset代表偏移，limit代表展示数量
select * from employees limit 5 offset 5;

-- 法二：前面数字代表偏移，后面数字代表展示数量
select * from employees limit 5,5;
```



## 54、获取所有员工的emp_no

获取所有员工的emp_no、部门编号dept_no以及对应的bonus类型btype和received，没有分配奖金的员工不显示对应的bonus类型btype和received

```sql
CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

CREATE TABLE `emp_bonus`(
emp_no int(11) NOT NULL,
received datetime NOT NULL,
btype smallint(5) NOT NULL);

CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
```

返回的结果格式如下:

| e.emp_no | dept_no | btype | received   |
| :------- | :------ | :---- | :--------- |
| 10001    | d001    | 1     | 2010-01-01 |
| 10002    | d001    | 2     | 2010-10-01 |
| 10003    | d004    | 3     | 2011-12-03 |
| 10004    | d004    | 1     | 2010-01-01 |
| 10005    | d003    |       |            |
| 10006    | d002    |       |            |
| 10007    | d005    |       |            |
| 10008    | d005    |       |            |
| 10009    | d006    |       |            |
| 10010    | d005    |       |            |
| 10010    | d006    |       |            |

**sql语句**

考虑到新员工可能没分配部门，员工可能没奖金，应该采用左外连接

```sql
select e.emp_no,e.dept_no ,eb.btype,eb.received
from (select em.emp_no,de.dept_no
     from employees em
     join dept_emp de on em.emp_no=de.emp_no) e
left join emp_bonus eb on e.emp_no=eb.emp_no;
```



## 55、使用含有关键字exists查找未分配具体部门的员工的所有信息(==exists用法==)

使用含有关键字exists查找未分配具体部门的员工的所有信息。

```sql
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));

CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));
```

输出格式:

| emp_no | birth_date | first_name | last_name | gender | hire_date  |
| :----- | :--------- | :--------- | :-------- | :----- | :--------- |
| 10011  | 1953-11-07 | Mary       | Sluis     | F      | 1990-01-22 |

**sql语句**

```sql
select * 
from employees e
where not exists(select emp_no 
                 from dept_emp de
                 where de.emp_no=e.emp_no);
```

**Exists的用法：**

**exists对外表用loop逐条查询**，每次查询都会查看exists的条件语句，当 exists里的条件语句能够返回记录行时(**无论记录行是的多少，只要能返回**)，条件就为真，**返回当前loop到的这条记录**；反之如果exists里的条件语句不能返回记录行，则当前loop到的这条记录被丢弃，**exists的条件就像一个bool条件，当能返回结果集则为true，不能返回结果集则为 false。**

总的来说，如果外表有n条记录，那么exists查询就是将这n条记录逐条取出，然后判断n遍 exists内部的条件是否能满足

**什么时候用EXISTS，什么时候用IN？**

主表为employees，从表为dept_emp，在主表和从表都对关联的列emp_no建立索引的前提下：

- 当主表比从表大时，IN查询的效率较高；      
- 当从表比主表大时，EXISTS查询的效率较高；


原因如下：

- in是**先执行子查询，得到一个结果集**，将结果集代入外层谓词条件执行主查询，**子查询只需要执行一次** 
- exists是**先从主查询中取得一条数据，再代入到子查询中**，执行一次子查询，判断子查询是否能返回结果，**主查询有多少条数据，子查询就要执行多少次**



## 56、获取employees中的行数据，且这些行也存在于emp_v中

存在如下的视图：

```sql
create view emp_v as select * from employees where emp_no >10005;

CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
```

获取employees中的行数据，且这些行也存在于emp_v中。注意不能使用intersect关键字。

(你能不用select * from employees where emp_no >10005 这条语句完成吗，挑战一下自己对视图的理解)

输出格式:

| emp_no | birth_date | first_name | last_name | gender | hire_date  |
| :----- | :--------- | :--------- | :-------- | :----- | :--------- |
| 10006  | 1953-04-20 | Anneke     | Preusig   | F      | 1989-06-02 |
| 10007  | 1957-05-23 | Tzvetan    | Zielinski | F      | 1989-02-10 |
| 10008  | 1958-02-19 | Saniya     | Kalloufi  | M      | 1994-09-15 |
| 10009  | 1952-04-19 | Sumant     | Peac      | F      | 1985-02-18 |
| 10010  | 1963-06-01 | Duangkaew  | Piveteau  | F      | 1989-08-24 |
| 10011  | 1953-11-07 | Mary       | Sluis     | F      | 1990-01-22 |

**sql语句**

有点智障

```sql
select * from emp_v;
```



## 57、获取有奖金的员工相关信息(==CASE条件判断==)

获取有奖金的员工相关信息。

```sql
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));

CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));

create table emp_bonus(
emp_no int not null,
received datetime not null,
btype smallint not null);

CREATE TABLE `salaries` (
`emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL, PRIMARY KEY (`emp_no`,`from_date`));
```


给出emp_no、first_name、last_name、奖金类型btype、对应的当前薪水情况salary以及奖金金额bonus。 bonus类型btype为1其奖金为薪水salary的10%，btype为2其奖金为薪水的20%，其他类型均为薪水的30%。 当前薪水表示to_date='9999-01-01'

输出格式:

| emp_no | first_name | last_name | btype | salary | bonus   |
| :----- | :--------- | :-------- | :---- | :----- | :------ |
| 10001  | Georgi     | Facello   | 1     | 88958  | 8895.8  |
| 10002  | Bezalel    | Simmel    | 2     | 72527  | 14505.4 |
| 10003  | Parto      | Bamford   | 3     | 43311  | 12993.3 |
| 10004  | Chirstian  | Koblick   | 1     | 74057  | 7405.7  |

**sql语句**

本题主要考查  CASE 表达式的用法。即当 btype = 1 时，得到 salary * 0.1；当 btype = 2 时，得到 salary * 0.2；其他情况得到 salary * 0.3。

```sql
select e.emp_no,e.first_name,e.last_name,eb.btype,s.salary,(case eb.btype
                                                           when 1 then s.salary*0.1
                                                           when 2 then s.salary*0.2
                                                           else s.salary*0.3 end) as bonus
from employees e,emp_bonus eb,salaries s
where e.emp_no=eb.emp_no and e.emp_no = s.emp_no
and s.to_date='9999-01-01';
```

case 条件表达式语法如下

```sql
1) CASE x WHEN w1 THEN r1 WHEN w2 THEN r2 ELSE r3 END
2) CASE WHEN x=w1 THEN r1 WHEN x=w2 THEN r2 ELSE r3 END
```

对于第一种情况，条件表达式x只需计算一次，然后分别和WHEN关键字后的条件逐一进行比较，直到找到相等的条件，其比较规则等价于等号(=)表达式。如果找到匹配的条件，则返回其后THEN关键字所指向的值，如果没有找到任何匹配，则返回ELSE关键字之后的值，如果不存在ELSE分支，则返回NULL。对于第二种情况，和第一种情况相比，唯一的差别就是表达式x可能被多次执行，比如第一个WHEN条件不匹配，则继续计算后面的WHEN条件，其它规则均与第一种完全相同。最后需要说明的是，**以上两种形式的CASE表达式均遵守短路原则，即第一个表达式的条件一旦匹配，其后所有的WHEN表达式均不会再被执行或比较。**



## 58、统计salary的累计和running_total

按照salary的累计和running_total，其中running_total为前N个当前( to_date = '9999-01-01')员工的salary累计和，其他以此类推。 具体结果如下Demo展示。

```sql
CREATE TABLE `salaries` ( `emp_no` int(11) NOT NULL,
`salary` int(11) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`from_date`));
```

**输出格式:**

| emp_no | salary | running_total |
| :----- | :----- | :------------ |
| 10001  | 88958  | 88958         |
| 10002  | 72527  | 161485        |
| 10003  | 43311  | 204796        |
| 10004  | 74057  | 278853        |
| 10005  | 94692  | 373545        |
| 10006  | 43311  | 416856        |
| 10007  | 88070  | 504926        |
| 10009  | 95409  | 600335        |
| 10010  | 94409  | 694744        |
| 10011  | 25828  | 720572        |

**sql语句**

本题的思路为复用 salaries 表进行子查询，最后以 s1.emp_no 排序输出求和结果。

1、输出的第三个字段，是由一个 SELECT 子查询构成。将子查询内复用的 salaries 表记为 s2，主查询的 salaries 表记为 s1，当主查询的 s1.emp_no 确定时，对子查询中不大于 s1.emp_no 的 s2.emp_no 所对应的薪水求和

2、注意是对员工当前的薪水求和，所以在主查询和子查询内都要加限定条件 to_date = '9999-01-01'

```sql
select s.emp_no,s.salary,(select sum(tmp_s.salary)
                          from salaries tmp_s
                          where tmp_s.emp_no<=s.emp_no
                          and tmp_s.to_date='9999-01-01')as running_total
                          
from salaries s
where s.to_date = '9999-01-01'
order by s.emp_no;
```



## 59、对于employees表中，给出奇数行的first_name

对于employees表中，输出first_name排名（按first_name升序排序的排名）为奇数的first_name，输出不需要排序

```sql
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));
```

如，输入为：

```sql
INSERT INTO employees VALUES(10001,'1953-09-02','Georgi','Facello','M','1986-06-26');
INSERT INTO employees VALUES(10002,'1964-06-02','Bezalel','Simmel','F','1985-11-21');
INSERT INTO employees VALUES(10005,'1955-01-21','Kyoichi','Maliniak','M','1989-09-12');
INSERT INTO employees VALUES(10006,'1953-04-20','Anneke','Preusig','F','1989-06-02');
```

**输出格式:**

| first_name |
| :--------- |
| Georgi     |
| Anneke     |

因为Georgi按first_name排名为3，Anneke按first_name排名为1，所以会输出这2个，且输出时不需排序。

**sql语句**

本题关键是，如何获取排名，字符串也是可以做不等式操作的那么获取排名之后，如何绑定到当前的emp_no和first_name，这里用子查询的方式，每拿最外层的一条记录，去子表查他的排名，最后取排名为奇数的即可

```sql
-- 可以创建临时表，并写在临时表的子查询中（select）
select e1.first_name
from (select e2.first_name,(select count(*)
                           from employees e3
                           where e2.first_name>=e3.first_name) as rank
     from employees e2) e1
where e1.rank&1;


-- 也可以写在子查询中（where）
select e1.first_name
from employees e1
where (select count(*)
       from employees e2
       where e2.first_name<=e1.first_name)&1;
```



## 60、出现三次以上相同积分的情况

在牛客刷题的小伙伴们都有着牛客积分，积分(grade)表简化可以如下:

![image-20200829013311203](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829013311203.png)

id为用户主键id，number代表积分情况，让你写一个sql查询，积分表里面出现三次以上的积分，查询结果如下:

![image-20200829013550157](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829013550157.png)

id为用户主键id，number代表积分情况，让你写一个sql查询，积分表里面出现三次以上的积分，查询结果如下:

![image-20200829013418031](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829013418031.png)

**sql语句**

```sql
-- 写复杂了，直接写在having即可
select g1.number 
from grade g1
where (select count(g2.id)
     from grade g2
     where g1.number=g2.number)>=3
group by g1.number;

-- 正确解法
select number
from grade 
group by number
having count(id)>=3;
```



## 61、刷题通过的题目排名（==rank函数，mysql8.0以上才支持==）

在牛客刷题有一个通过题目个数的(passing_number)表，id是主键，简化如下:

![image-20200829013450094](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829013450094.png)

第1行表示id为1的用户通过了4个题目;.....第6行表示id为6的用户通过了4个题目;请你根据上表，输出通过的题目的排名，通过题目个数相同的，排名相同，此时按照id升序排列，数据如下:

![image-20200829013615063](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829013615063.png)

id为5的用户通过了5个排名第1，id为1和id为6的都通过了2个，并列第2

**sql语句**

```sql
-- 传统做法
select pn1.id,pn1.number, (select count(distinct pn2.number)
                          from passing_number pn2
                          where pn1.number<=pn2.number)as rank
from passing_number pn1
order by rank,pn1.id;

-- 运用dense_rank()函数，mysql8.0以下不支持
select id, number, dense_rank() over (order by number desc) as rank
from passing_number
order by number desc, id asc;
```

**这里来看看MySQL中rank()、row_number()、dense_rank()排序**

查看一下插入的数据：

```sql
select * from students;
```

![image-20200829015159948](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829015159948.png)

 

开始使用三种不同的方法进行排序：

```sql
select id, name, rank() over(order by score desc) as r,
	dense_rank() over(order by score desc) as dense_r,
	row_number() over(order by score desc) as row_r
from students;
```

当然也可以写在同一张表中：

**需要注意的一点是as后的别名，千万不要与前面的函数名重名，否则会报错。**

![image-20200829015215279](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829015215279.png)

rank()：重复则相同排名，挤掉下一个排名

dense_rank()：重复则相同排名，不挤掉下一个排名

row_rank()：没有相同排名，就按大小排，相同则按查找顺序

 

## 62、找到每个人的任务

有一个person表，主键是id，如下:

![](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829015228004.png)

有一个任务(task)表如下，主键也是id，如下:

![image-20200829015303329](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829015303329.png)

请你找到每个人的任务情况，并且输出出来，没有任务的也要输出，而且输出结果按照person的id升序排序，输出情况如下:

![image-20200921162338968](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200921162338968.png)

**sql语句**

```sql
select p.id,p.name,t.content
from person p
left join task t on  p.id=t.person_id
order by p.id;
```



## 63、考试前2分数的学生

牛客每次举办企业笔试的时候，企业一般都会有不同的语言岗位，比如C++工程师，JAVA工程师，Python工程师，每个用户笔试完有不同的分数，现在有一个分数(grade)表简化如下:

![image-20200829020155177](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829020155177.png)

第1行表示用户id为1的选择了language_id为1岗位的最后考试完的分数为12000，
....
第7行表示用户id为7的选择了language_id为2岗位的最后考试完的分数为11000，

不同的语言岗位(language)表简化如下:

![image-20200829020728077](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829020728077.png)

请你找出**每个岗位分数排名前2**的用户，得到的结果先**按照language的name升序排序，再按照积分降序排序**，**最后按照grade的id升序**排序，得到结果如下:

 ![image-20200829021123968](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021123968.png)



**sql语句**

本题难点在于，如何对指定的语言下的分数排序

```sql
-- 先找出符合某语言下的排名前2的id，再排序即可，找排名的方法同前面自连接
select g.id,l.name,g.score
from grade g
join language l on g.language_id=l.id
where g.id in (select g1.id								
               from grade g1,grade g2
               where g1.language_id=g2.language_id		-- 指定为同种语言比较
               and g1.score<=g2.score
               group by g1.id,g1.language_id	-- 严谨一点，对id+language_id分组，若只能考一种语言可省language_id
               having count(distinct g2.score)<3)					-- 注意这里是对score排序，才是排名
order by l.name asc,g.score desc, g.id asc;

-- 运用dense_rank排序，mysql8.0以下不支持，可以用变量去算
select id,name,score from(
    select g.id as id,l.name as name,g.score as score,
    dense_rank() over(partition by g.language_id order by g.score desc) as rank -- 按照语言id分窗各自求rank
    from grade g,language l
    where l.id = g.language_id
)temp
where rank <= 2
order by name asc,score desc,id asc;
```



## 64、异常的邮件概率

现在有一个需求，让你统计正常用户发送给正常用户邮件失败的概率:
有一个邮件(email)表，id为主键， type是枚举类型，枚举成员为(completed，no_completed)，completed代表邮件发送是成功的，no_completed代表邮件是发送失败的。简况如下:

![image-20200829021218709](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021218709.png)

第1行表示为id为2的用户在2020-01-11成功发送了一封邮件给了id为3的用户;
...
第3行表示为id为1的用户在2020-01-11**没有成功**发送一封邮件给了id为4的用户;
...
第6行表示为id为4的用户在2020-01-12成功发送了一封邮件给了id为1的用户;


下面是一个用户(user)表，id为主键，is_blacklist为0代表为正常用户，is_blacklist为1代表为黑名单用户，简况如下:

![image-20200829021307128](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021307128.png)

第1行表示id为1的是正常用户;
第2行表示id为2的不是正常用户，是黑名单用户，如果发送大量邮件或者出现各种情况就会容易发送邮件失败的用户
。。。
第4行表示id为4的是正常用户



现在让你写一个sql查询，每一个日期里面，正常用户发送给正常用户邮件失败的概率是多少，结果最多保留到小数点后面3位(3位之后的四舍五入)，并且按照日期升序排序，上面例子查询结果如下:

![image-20200829021336734](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021336734.png)



结果表示:

2020-01-11失败的概率为0.500，因为email的第1条数据，发送的用户id为2是黑名单用户，所以不计入统计，正常用户发正常用户总共2次，但是失败了1次，所以概率是0.500;

2020-01-12没有失败的情况，所以概率为0.000.
(注意: sqlite 1/2得到的不是0.5，得到的是0，只有1*1.0/2才会得到0.5，sqlite四舍五入的函数为round)



题目啰里吧嗦的，就是要求正常用户发送给正常用户邮件失败的概率，而且输出格式是保留3位小数，因此需要四舍五入

**sql语句**

这里先过滤一遍，挑选出正常用户间的收发记录，再在这个基础上，统计type='no_completed'

由于最后date要进行分组合并，所以统计概率最好放在聚合函数内进行

```sql
-- 一开始是用子查询做的，发现用的是同一张表，select...from不好写，嵌套也很麻烦
-- 这里用的sum+条件判断，简洁明了
-- sqlit写法：
select em.date,round(sum(case
                        when type='no_completed' then 1
                        else 0 end) * 1.0/count(*),3) as p	 		-- 保留3位，round函数四舍五入
from email em,user u1,user u2
where em.send_id = u1.id and em.receive_id=u2.id
and u1.is_blacklist!=1 and u2.is_blacklist!=1
group by em.date
order by em.date;

-- mysql写法
select em.date,round(sum(if(type='no_completed',1,0)) * 1.0/count(*),3) as p	-- 保留3位，round函数四舍五入
from email em,user u1,user u2
where em.send_id = u1.id and em.receive_id=u2.id
and u1.is_blacklist!=1 and u2.is_blacklist!=1
group by em.date
order by em.date;
```



## 65、牛客每个人最近的登录日期(一)（==数据库date格式==）

牛客每天有很多人登录，请你统计一下牛客每个用户最近登录是哪一天。

有一个登录(login)记录表，简况如下:

![image-20200829021356480](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021356480.png)

第1行表示id为2的用户在2020-10-12使用了客户端id为1的设备登录了牛客网
。。。
第4行表示id为3的用户在2020-10-13使用了客户端id为2的设备登录了牛客网


请你写出一个sql语句查询每个用户最近一天登录的日子，并且按照user_id升序排序，上面的例子查询结果如下:

![image-20200829021410187](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021410187.png)

查询结果表明:
user_id为2的最近的登录日期在2020-10-13
user_id为3的最近的登录日期也是2020-10-13

**sql语句**

分组查询即可，并不用排名

```sql
select max(date) as d
from login
group by user_id
order by user_id;
```

**数据库date格式**

**DATETIME**类型用在你需要同时包含日期和时间信息的值时。MySQL检索并且以'YYYY-MM-DD HH:MM:SS'格式显示DATETIME值，支持的范围是'1000-01-01 00:00:00'到'9999-12-31 23:59:59'。（“支持”意味着尽管更早的值可能工作，但不能保证他们可以。）

**DATE**类型用在你仅需要日期值时，没有时间部分。MySQL检索并且以'YYYY-MM-DD'格式显示DATE值，支持的范围是'1000-01-01'到'9999-12-31'。

**TIMESTAMP**列类型提供一种类型，你可以使用它自动地用当前的日期和时间标记INSERT或UPDATE的操作。

**TIME**数据类型表示一天中的时间。MySQL检索并且以"HH:MM:SS"格式显示TIME值。支持的范围是'00:00:00'到'23:59:59'。



## 66、牛客每个人最近的登录日期(二)

牛客每天有很多人登录，请你统计一下牛客每个用户最近登录是哪一天，用的是什么设备.

有一个登录(login)记录表，简况如下:

![image-20200829021424986](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021424986.png)


第1行表示id为2的用户在2020-10-12使用了客户端id为1的设备登录了牛客网
。。。
第4行表示id为3的用户在2020-10-13使用了客户端id为2的设备登录了牛客网

还有一个用户(user)表，简况如下:

![image-20200829021454594](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021454594.png)

还有一个客户端(client)表，简况如下:

![image-20200829021608858](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021608858.png)

请你写出一个sql语句查询每个用户最近一天登录的日子，用户的名字，以及用户用的设备的名字，并且查询结果按照user的name升序排序，上面的例子查询结果如下:

![image-20200829021835716](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021835716.png)

查询结果表明:
fh最近的登录日期在2020-10-13，而且是使用pc登录的
wangchao最近的登录日期也是2020-10-13，而且是使用ios登录的

**sql语句**

```sql
-- where 联查
select u.name as u_n,c.name as c_n,max(l.date) as d
from user u,client c,login l
where u.id=l.user_id and c.id=l.client_id
group by l.user_id
order by u.name;

-- 内连接
select u.name u_n,c.name c_n, max(l.date) d
from login l
inner join user u on u.id=l.user_id
inner join client c on c.id=l.client_id
group by l.user_id
order by u.name asc;
```



## 67、牛客每个人最近的登录日期(三)（==较难==）

牛客每天有很多人登录，请你统计一下牛客**新注册用户的次日成功**的留存率（即第一天注册登录后，第二天登录的概率），

有一个登录(login)记录表，简况如下:

![image-20200829021850054](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021850054.png)

第1行表示id为2的用户在2020-10-12使用了客户端id为1的设备第一次新登录了牛客网
。。。
第4行表示id为3的用户在2020-10-14使用了客户端id为2的设备登录了牛客网


请你写出一个sql语句查询新登录用户次日成功的留存率，即第1天登陆之后，第2天再次登陆的概率,保存小数点后面3位(3位之后的四舍五入)，上面的例子查询结果如下:

![image-20200829021900225](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021900225.png)

查询结果表明:

id为2的用户在2020-10-12第一次新登录了，在2020-10-13又登录了，算是成功的留存

id为3的用户在2020-10-12第一次新登录了，在2020-10-13没登录了，算是失败的留存

故次日成功的留存率为 1/2=0.5

(sqlite里查找某一天的后一天的用法是:date(yyyy-mm-dd, '+1 day')，四舍五入的函数为round，sqlite 1/2得到的不是0.5，得到的是0，只有1*1.0/2才会得到0.5)

**sql语句**

```sql
-- 首先，如何确定留存率，可行的办法是用第二天登录的用户数/总用户数
-- 第二，如何确定第二天该用户登录了呢，我们只需要拿到第一天（最小）登录日期，判断该表中是否有其第二天即可
select round(count (distinct user_id)*1.0/(select count(distinct user_id) from login) ,3) as p
from login
where (user_id, date) in (select user_id,date(min(date), '+1 day')			-- 取注册第二天，判断是否在表中
                          from login
                          group by user_id);
                          
-- 也可以用子表
select round((suc_cnt*1.0/cnt),3)as p
from (select count(*) as suc_cnt
      from login 
      inner join (
          select user_id ,date(min(date), '+1 day') as next_day 
          from login 
          group by user_id)as t 
      on login.user_id=t.user_id and login.date=t.next_day) as t1 
inner join (select count(distinct user_id)as cnt 
            from login) as t2 ; 
```

（第一天登录的新用户并且第二天也登录的用户）/（总用户）即为新登录用户的次日成功的留存率

总用户其实挺好算，如下：

```sql
select count(distinct user_id) from login
```

找到每个用户第一天登陆的日子，其实挺好找，取min:

```sql
select user_id,min(date) from login group by user_id
```

比如上面查找语句是1，2020-10-12；那么要找到一个用户对应id和第二天登录日期，那么可以如下写

```sql
select user_id,date(min(date),'+1 day') from login group by user_id
```

这样就可以找到所有的在第一天登录的新用户并且第二天也登录的用户，以及第二天的日期，只需要主表存在对应id+第二天日期date就说明满足情况，进行计数。



## 68、牛客每个人最近的登录日期(四)（==IFNULL函数==）

牛客每天有很多人登录，请你统计一下牛客每个日期**登录新用户个数，**

有一个登录(login)记录表，简况如下:

![image-20200829021914206](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021914206.png)



第1行表示id为2的用户在2020-10-12使用了客户端id为1的设备登录了牛客网，因为是第1次登录，所以是新用户
。。。
第4行表示id为2的用户在2020-10-13使用了客户端id为2的设备登录了牛客网，因为是第2次登录，所以是老用户
。。
第4行表示id为4的用户在2020-10-15使用了客户端id为1)的设备登录了牛客网，因为是第2次登录，所以是老用户


请你写出一个sql语句查询每个日期登录新用户个数，并且查询结果按照日期升序排序，上面的例子查询结果如下:(输出0，可以用sqlite的ifnull函数尝试实现，select ifnull(null,1)的输出是1)

![image-20200829021956919](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829021956919.png)

查询结果表明:
2020-10-12，有3个新用户(id为2，3，1)登录
2020-10-13，没有新用户登录
2020-10-14，有1个新用户(id为4)登录
2020-10-15，没有新用户登录

**sql语句**

总之，要绑定用户id和最小值，并统计出来

```sql
-- 写法1，子查询
select l1.date,ifnull((select count(distinct user_id)
                       from login l2
                       where l1.date=l2.date										-- 与主表日期对应
                       and (l2.user_id,l2.date) in (select user_id,min(date)		-- 确定最小
                                                   from login
                                                   group by user_id)),0) as new
from login l1
group by l1.date
order by l1.date;


-- 写法2，左连接子表
select login.date,ifnull(n1.new_num,0) as new 
from login 
left join (select l1.date,count(distinct l1.user_id) as new_num		-- 统计该天新用户
           from login l1
           where l1.date =(select min(date) 						-- 筛选出该天新用户记录
                           from login 
                           where user_id=l1.user_id)
           group by l1.date) n1										-- 对date分组
on login.date = n1.date
group by login.date 
order by login.date;
```

首先，获取每个日期对应的登录数，可以由下面的sql得出

```sql
select l1.date,count(distinct l1.user_id)
from login l1
group by l1.date;
```

那么判断哪些是新用户，可以在where里面添加一个条件，判断id相同时，是否是最小日期

```sql
select l1.date,count(distinct l1.user_id)
from login l1
where l1.date =
(select min(date) from login where user_id=l1.user_id)
group by l1.date;
```

但是这样并不能通过用例，因为这样的话，2020-10-13没有新用户登录，应该输出为0的，这个语句却没有输出。但是login表的日期是完整的，所以我们考虑将login表当主表，上面查出来的表左连接到主表，顺序输出，并使用ifnull语句将null变成0。

**IFNULL()函数**

```sql
IFNULL(expression, alt_value)
```

如果第一个参数的表达式 expression 为 NULL，则返回第二个参数的值。

如上面2020-10-13没有查到数据，那么会返回NULL，因此使用第二个参数0



## 69、牛客每个人最近的登录日期(五)（==困难==）

牛客每天有很多人登录，请你统计一下牛客**每个日期新用户的次日留存率。**

有一个登录(login)记录表，简况如下:

![image-20200829022027214](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829022027214.png)

第1行表示id为2的用户在2020-10-12使用了客户端id为1的设备登录了牛客网，因为是第1次登录，所以是新用户
。。。
第4行表示id为2的用户在2020-10-13使用了客户端id为2的设备登录了牛客网，因为是第2次登录，所以是老用户
。。
第4行表示id为4的用户在2020-10-15使用了客户端id为1的设备登录了牛客网，因为是第2次登录，所以是老用户



请你写出一个sql语句查询每个日期新用户的次日留存率，结果保留小数点后面3位数(3位之后的四舍五入)，并且查询结果按照日期升序排序，上面的例子查询结果如下:

![image-20200829022101914](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829022101914.png)

查询结果表明:

2020-10-12登录了3个(id为2，3，1)新用户，2020-10-13，只有2个(id为2,1)登录，故2020-10-12新用户次日留存率为2/3=0.667;

2020-10-13没有新用户登录，输出0.000;

2020-10-14登录了1个(id为4)新用户，2020-10-15，id为4的用户登录，故2020-10-14新用户次日留存率为1/1=1.000;

2020-10-15没有新用户登录，输出0.000;

(注意:sqlite里查找某一天的后一天的用法是:date(yyyy-mm-dd, '+1 day')，sqlite里1/2得到的不是0.5，得到的是0，只有1*1.0/2才会得到0.5)



**SQL语句**

这题是第三、四的升级版，其中对0/0也要用ifnull排查

```sql
select first_login.date, round(ifnull(second_login.second_login_num *1.0/ first_login.first_num,0),3)
from (select login.date,ifnull(n1.new_num,0) as second_login_num	-- 尽可能选左连接的字段，如选n1.date
      from login 													-- 没有的日期不显示
      left join (select l1.date,count(distinct l1.user_id) as new_num
                 from login l1
                 join login l2 on l1.user_id=l2.user_id and l2.date=date((l1.date),'+1 day')
                 where l1.date = (select min(date) from login where user_id=l1.user_id)
                 group by l1.date) n1
      on login.date = n1.date
      group by login.date) second_login								-- 左连接要用左连接的字段排序
join (select login.date,ifnull(n1.new_num,0) as first_num
      from login 
      left join (select l1.date,count(distinct l1.user_id) as new_num
                 from login l1
                 where l1.date =(select min(date) from login where user_id=l1.user_id)
                 group by l1.date) n1
      on login.date = n1.date
      group by login.date) first_login
on second_login.date=first_login.date
```

这里主要是如何确定某天新用户第二天还登录的，这里思路是再联查同张表，确定该用户第二天也在该表中

```sql
	  select login.date,ifnull(n1.new_num,0) as second_login_num	
      from login 													
      left join (select l1.date,count(distinct l1.user_id) as new_num
                 from login l1
                 join login l2 on l1.user_id=l2.user_id and l2.date=date((l1.date),'+1 day') --关键
                 where l1.date = (select min(date) from login where user_id=l1.user_id)
                 group by l1.date) n1
      on login.date = n1.date
      group by login.date) second_login		
```



## 70、牛客每个人最近的登录日期(六)

牛客每天有很多人登录，请你统计一下牛客每个用户每一天的刷题通过数据，包括: 用户的名字，以及用户用的设备的名字，用户刷题通过总数，不存在没有登录却刷题的情况，但是存在登录了没刷题的情况，不会存在刷题表里面，有提交代码没有通过的情况，但是会记录在刷题表里，只不过通过数目是0。
有一个登录(login)记录表，简况如下:

![image-20200829022136050](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829022136050.png)

第1行表示id为2的用户在2020-10-12使用了客户端id为1的设备登录了牛客网
。。。
第5行表示id为3的用户在2020-10-13使用了客户端id为2的设备登录了牛客网


有一个刷题（passing_number)表，简况如下:

![image-20200829022200817](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829022200817.png)

第1行表示id为2的用户在2020-10-12通过了4个题目。
。。。
第3行表示id为1的用户在2020-10-13提交了代码但是没有通过任何题目。
第4行表示id为4的用户在2020-10-13通过了2个题目


还有一个用户(user)表，简况如下:

![image-20200829022215662](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829022215662.png)


还有一个客户端(client)表，简况如下:

![image-20200829022230393](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200829022230393.png)

请你写出一个sql语句查询每一天的刷题通过数据，包括: 用户的名字，以及用户用的设备的名字，以及用户刷题通过的总数，并且查询结果先按照日期升序排序，再按照姓名升序排序，有登录却没有刷题的哪一天的数据不需要输出，上面的例子查询结果如下:

![image-20200829022246533](pictures/image-20200829022246533.png)

查询结果表明:

fh在2020-10-12，使用pc刷题通过4道，总计为4

wangchao在2020-10-12，使用ios刷题通过1道，总计为1

tm在2020-10-12只登陆了没有刷题，故没有显示出来

tm在2020-10-13使用了android刷题，但是却没有通过任何题目，总计为0

wangchao在2020-10-13使用了ios刷题通过1道，但是加上前面2020-10-12通过2道，总计为3



**sql 语句**

注意这里第四列是输出总计刷题数，前三列内连接没啥可讲的

```sql
-- 解法1，传统sum，求累计
select u.name as u_n,c.name as c_n,pn.date as date,(select sum(number) 				-- 不需要分组，求和即可
                              from passing_number 
                              where pn.user_id=user_id
                              and date<= pn.date) as ps_num
from login l,passing_number pn,user u,client c
where l.client_id=c.id and u.id=pn.user_id						-- 拼接语句
and pn.user_id=l.user_id and pn.date=l.date
group by pn.user_id,pn.date
order by pn.date,u.name

-- 解法2，over开窗函数
select user.name as u_n, client.name as c_n, login.date, p1.ps_num
from login 
join (select user_id, date ,sum(number) over(partition by user_id order by date) ps_num 
      from passing_number) p1					-- 这里sum求和，over逻辑是对同一user_id，按date顺序求和
on p1.user_id=login.user_id and p1.date=login.date
join user on login.user_id=user.id
join client on login.client_id=client.id
order by login.date, user.name
```

