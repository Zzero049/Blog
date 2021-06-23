# 399、除法求值

给出方程式 A / B = k, 其中 A 和 B 均为用字符串表示的变量， k 是一个浮点型数字。根据已知方程式求解问题，并返回计算结果。如果结果不存在，则返回 -1.0。

输入总是有效的。你可以假设除法运算中不会出现除数为 0 的情况，且不存在任何矛盾的结果。

 

**示例 1：**

```
输入：equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
输出：[6.00000,0.50000,-1.00000,1.00000,-1.00000]
解释：
给定：a / b = 2.0, b / c = 3.0
问题：a / c = ?, b / a = ?, a / e = ?, a / a = ?, x / x = ?
返回：[6.0, 0.5, -1.0, 1.0, -1.0 ]

```

**示例 2：**

```
输入：equations = [["a","b"],["b","c"],["bc","cd"]], values = [1.5,2.5,5.0], queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]
输出：[3.75000,0.40000,5.00000,0.20000]
```

**示例 3：**

```
输入：equations = [["a","b"]], values = [0.5], queries = [["a","b"],["b","a"],["a","c"],["x","y"]]
输出：[0.50000,2.00000,-1.00000,-1.00000]
```

**提示：**

- 1 <= equations.length <= 20
- equations[i].length == 2
- 1 <= `equations[i][0].length, equations[i][1].length` <= 5
- values.length == equations.length
- 0.0 < values[i] <= 20.0
- 1 <= queries.length <= 20
- queries[i].length == 2
- 1 <= `queries[i][0].length`, `queries[i][1].length` <= 5
- `equations[i][0] `, `equations[i][1]`, `queries[i][0]`, `queries[i][1]` 由小写英文字母与数字组成



## 题解

### 方法一：带权并查集

1、先构造并查集

- 如果进来的两个字符串在同一个集合，不需要合并
- 如果进来两个字符串不在同一个集合，需要合并

- 判断在不在一个集合里，通过判断根是不是相同的确定

![image-20201004164106682](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201004164106682.png)

![image-20201004164158320](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201004164158320.png)

2、通过并查集去判断，询问的方程的结果

- 如果不在并查集中，为-1.0
- 如果在不同的两个并查集，为-1.0
- 如果在并查集且为自己，为1.0
- 如果在同一个并查集，如果上面求b/f，那么就是 p(f)/p(b)

不带路径压缩版本，总的来说这个方案比较好想，代码如下

```java
class Solution {
    private Map<String, String> parMap;				// key是子节点，value是父节点
    private Map<String, Double> valMap;				// 不带路径压缩，每个节点存的是父节点到子节点的权值

    public double[] calcEquation(List<List<String>> equations, double[] values, List<List<String>> queries) {
        parMap = new HashMap<>();
        valMap = new HashMap<>();

        int n = equations.size();
        int len = queries.size();
        double[] ans = new double[len];
        for (int i = 0; i < n; ++i) {
            String parent = equations.get(i).get(0);
            String child = equations.get(i).get(1);
            unoin(parent, child, values[i]);
        }

        for (int i = 0; i < len; ++i) {
            String parent = queries.get(i).get(0);
            String child = queries.get(i).get(1);
            if (!parMap.containsKey(parent) || !parMap.containsKey(child)) {
                ans[i] = -1.0;
                continue;
            }
            if (parent.equals(child)) {
                ans[i] = 1.0;
                continue;
            }
            String root1 = getRoot(parent);
            String root2 = getRoot(child);
            if (!root1.equals(root2)) {
                ans[i] = -1.0;
                continue;
            }
            ans[i] = calToRoot(child) / calToRoot(parent);

        }
        return ans;
    }


    private void unoin(String parent, String child, double value) {
        // 如果parent和child不存在创建一个，以自己为根
        if (!parMap.containsKey(parent)) {					
            parMap.put(parent, parent);
            valMap.put(parent, 1.0);
        }
        if (!parMap.containsKey(child)) {
            parMap.put(child, child);
            valMap.put(child, 1.0);
        }
        String root1 = getRoot(parent);
        String root2 = getRoot(child);
        if (!root1.equals(root2)) {								// 进行合并，root2合并到root1的集合
            parMap.put(root2, root1);
            valMap.put(root2, value * calToRoot(parent) / calToRoot(child));		
        }
    }

    private String getRoot(String s) {							// 查找自己集合的根节点
        String root = parMap.get(s);
        while (!s.equals(root)) {
            s = root;
            root = parMap.get(s);
        }
        return root;
    }

    private double calToRoot(String s) {				// 非路径压缩，需要不断的往上乘找到自己这条路径的权值乘积结果
        String root = parMap.get(s);
        double val = 1.0;
        while (!s.equals(root)) {
            val *= valMap.get(s);
            s = root;
            root = parMap.get(s);
        }
        return val;
    }
}
```

带路径压缩的，valMap最后存的是根到自己的权值

![image-20201004173118557](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201004173118557.png)

![image-20201004173130468](https://gitee.com/zero049/MyNoteImages/raw/master/image-20201004173130468.png)

```java
class Solution {
    private HashMap<String,String> parent=new HashMap<>();

    private HashMap<String,Double> quotient=new HashMap<>();

    //带路径压缩的
    public String find(String p){
        if (!parent.get(p).equals(p)) {
            //需要先保存父亲的值,因为后面压缩后树只有两层,后面*的就是根节点的权值1,是不对的
            //这里可以看看上面的并茶几的方向和值来判断
            String f=parent.get(p);
            parent.put(p,find(f));
            //这样压缩后的子节点才是正确的
            quotient.put(p,quotient.get(p)*quotient.get(f));
        }
        return parent.get(p);
    }

    public void init(String s){
        if (!parent.containsKey(s)) {
            parent.put(s,s);
            quotient.put(s,1.0);
        }
    }

    public void merge(String a,String b,Double value){
        init(a);init(b);
        String fa=find(a); // a/fa=val[a], b/fb=val[b]
        String fb=find(b);
        if (fa.equals(fb)) {
            return;
        }
        parent.put(fa,fb);
        quotient.put(fa,value*(quotient.get(b)/quotient.get(a)));
    }

    public double[] calcEquation(List<List<String>> equations, double[] values, List<List<String>> queries) {
        for (int i=0;i<equations.size();i++) {
            List<String> equation=equations.get(i);
            merge(equation.get(0),equation.get(1),values[i]);
        }
        double[] res=new double[queries.size()];
        int index=0;
        for (List<String> query:queries) {
            String a=query.get(0);
            String b=query.get(1);
            if (!parent.containsKey(a) || !parent.containsKey(b)) {
                res[index++]=-1;
            }else{
                //先做路径压缩
                res[index++]=find(a).equals(find(b))?quotient.get(a)/quotient.get(b):-1;
            }
        }
        return res;
    }
}
```

