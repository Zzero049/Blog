### sql语句定义的顺序

```sql
(1) SELECT (2)DISTINCT<select_list>
(3) FROM <left_table>
(4) <join_type> JOIN <right_table>
(5)         ON <join_condition>
(6) WHERE <where_condition>
(7) GROUP BY <group_by_list>
(8) WITH {CUBE|ROLLUP}
(9) HAVING <having_condition>
(10) ORDER BY <order_by_condition>
(11) LIMIT <limit_number>

```

### sql语句执行顺序

```sql
(8) SELECT (9)DISTINCT<select_list>
(1) FROM <left_table>
(3) <join_type> JOIN <right_table>
(2)         ON <join_condition>
(4) WHERE <where_condition>
(5) GROUP BY <group_by_list>
(6) WITH {CUBE|ROLLUP}
(7) HAVING <having_condition>
(10) ORDER BY <order_by_list>
(11) LIMIT <limit_number>

```

**可以看到，一共有十一个步骤，最先执行的是FROM操作，最后执行的是LIMIT操作。每个操作都会产生一个虚拟表，该虚拟表作为一个处理的输入，看下执行顺序：**

(1) FROM:对FROM子句中的左表`<left_table>`和右表`<right_table>`执行笛卡儿积，产生虚拟表VT1;
(2) ON: 对虚拟表VT1进行ON筛选，只有那些符合`<join_condition>`的行才被插入虚拟表VT2;
(3) JOIN: 如果指定了`OUTER JOIN`(如LEFT OUTER JOIN、RIGHT OUTER JOIN)，那么保留表中未匹配的行作为外部行添加到虚拟表VT2，产生虚拟表VT3。如果FROM子句包含两个以上的表，则对上一个连接生成的结果表VT3和下一个表重复执行步骤1~步骤3，直到处理完所有的表;
(4) WHERE: 对虚拟表VT3应用WHERE过滤条件，只有符合`<where_condition>`的记录才会被插入虚拟表VT4;
(5) GROUP By: 根据GROUP BY子句中的列，对VT4中的记录进行分组操作，产生VT5;
(6) CUBE|ROllUP: 对VT5进行CUBE或ROLLUP操作，产生表VT6;
(7) HAVING: 对虚拟表VT6应用HAVING过滤器，只有符合`<having_condition>`的记录才会被插入到VT7;
(8) SELECT: 第二次执行SELECT操作，选择指定的列，插入到虚拟表VT8中;
(9) DISTINCT: 去除重复，产生虚拟表VT9;
(10) ORDER BY: 将虚拟表VT9中的记录按照`<order_by_list>`进行排序操作，产生虚拟表VT10;
(11) LIMIT: 取出指定街行的记录，产生虚拟表VT11，并返回给查询用户