# 索引优化例题

```sql
# 建表
CREATE TABLE test03(
id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
c1 CHAR(10),
c2 CHAR(10),
c3 CHAR(10),
c4 CHAR(10),
c5 CHAR(10)
);
# 插入数据
INSERT INTO test03(c1,c2,c3,c4,c5) VALUES('a1','a2','a3','a4','a5');
INSERT INTO test03(c1,c2,c3,c4,c5) VALUES('b1','b2','b3','b4','b5');
INSERT INTO test03(c1,c2,c3,c4,c5) VALUES('c1','c2','c3','c4','c5');
INSERT INTO test03(c1,c2,c3,c4,c5) VALUES('d1','d2','d3','d4','d5');
INSERT INTO test03(c1,c2,c3,c4,c5) VALUES('e1','e2','e3','e4','e5');
# 建立索引
CREATE INDEX idx_test03_c1234 ON  test03(c1,c2,c3,c4);

# 1243顺序索引一样有效，原因是mysql有优化器
# 但还是推荐按顺序写，避免底层翻译和转换
EXPLAIN SELECT * FROM test03 
WHERE c1='a1' AND c2='a2' AND c4='a4' AND c3='a3';

# 范围之后全失效，ref为NULL，type为ref
# 用到了索引4个键,c1,c2,c3用于查找c4用于排序
EXPLAIN SELECT * FROM test03 
WHERE c1='a1' AND c2='a2'  AND c3='a3' AND c4>'a4';

# like 与> <产生的范围是不同的
# like ***%索引依旧生效，而>后面索引不生效
# c3索引生效
EXPLAIN SELECT * FROM test03
WHERE c1='a1'AND c2 LIKE 'a2%' AND c3='a3';
# c3不生效
EXPLAIN SELECT * FROM test03
WHERE c1='a1'AND c2 > 'a2%' AND c3='a3';

# c1，c2用于查找，c3用于排序
EXPLAIN SELECT * FROM test03
WHERE c1='a1' AND c2='a2'  AND c4='a4'
ORDER BY c3;
# 一样
EXPLAIN SELECT * FROM test03
WHERE c1='a1' AND c2='a2' 
ORDER BY c3;

# 缺失c3，出现using filesort
EXPLAIN SELECT * FROM test03
WHERE c1='a1' AND c2='a2' 
ORDER BY c4;

# c1用于索引查找，c2，c3用于排序，没有filesort
EXPLAIN SELECT * FROM test03
WHERE c1='a1'AND c5='a5'
ORDER BY c2,c3;
# 有filesort
EXPLAIN SELECT * FROM test03
WHERE c1='a1'AND c5='a5'
ORDER BY c3,c2;

# c1,c2用于查找，c3用于排序，没有filesort
EXPLAIN SELECT * FROM test03
WHERE c1='a1'AND c2='a2'
ORDER BY c2,c3;
# 由于c2用于查找一个常量了，不会出现filesort
EXPLAIN SELECT * FROM test03
WHERE c1='a1'AND c2='a2'
ORDER BY c3,c2;

# group by与order by分析相似，c1查找，c2排序
EXPLAIN SELECT * FROM test03
WHERE c1='a1'AND c4='a4'
ORDER BY c2,c3;

# 注意：
# group by 基本上都需要进行排序，会有临时表产生
# 出现using filesort和temporary
EXPLAIN SELECT * FROM test03
WHERE c1='a1'AND c4='a4'
ORDER BY c3,c2;
```

## 建议

1. 对于单键索引，尽量选择针对当前query过滤性更好的索引
1. 在选择组合索引的时候，当前Query中过滤性最好的字段在索引字段顺序中，位置越靠前越好。
1. 在选择组合索引的时候，尽量选择可以能够包含当前query中的where字句中更多字段的索引
1. 尽可能通过分析统计信息和调整query的写法来达到选择合适索引的目的
1. group by 基本上都需要进行排序，会有临时表产生,order by一般是个范围