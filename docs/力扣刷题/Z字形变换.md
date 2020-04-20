
<img src="./pictures/Annotation 2020-04-03 200859.png"  div align=center />

我的解：
通过构造numRows个StringBuilder，通过分析知道当
i%（2*numRows -2）>=numRows-1时（弄复杂了），存进Builder之后数组向上存，反之向下存，也可以定义一个变量，其值为1，直接判断当数组为0或numRows-1时取反

```java
public static String solution(String s, int numRows){
        if (numRows == 1) return s;
        List<StringBuilder> stringArray = new ArrayList<>();
        int internal = 2*numRows -2;
        int len = s.length();
        StringBuilder ans = new StringBuilder("");

        for(int i=0;i<numRows;i++){
            StringBuilder sb = new StringBuilder("");
            stringArray.add(sb);
        }
        for(int i=0, k=0;i<len;i++){

            if(i%internal>=numRows-1){
                stringArray.get(k%numRows).append(s.charAt(i));
                k--;
            }else{
                stringArray.get(k%numRows).append(s.charAt(i));
                k++;

            }
        }

        for(StringBuilder sb:stringArray){
            ans.append(sb);
        }
        return ans.toString();
    }
```


## 参考答案：按行排序
<img src="./pictures/Annotation 2020-04-03 202819.png"  div align=center />



显然如果输入numRows不合理会占用更多时间和内存创建StringBuilder，此处可以优化，代码逻辑上判断并不是最优的
```java
class Solution {
    public String convert(String s, int numRows) {

        if (numRows == 1) return s;

        List<StringBuilder> rows = new ArrayList<>();
        for (int i = 0; i < Math.min(numRows, s.length()); i++)
            rows.add(new StringBuilder());

        int curRow = 0;
        boolean goingDown = false;

        for (char c : s.toCharArray()) {
            rows.get(curRow).append(c);
            if (curRow == 0 || curRow == numRows - 1) goingDown = !goingDown;
            curRow += goingDown ? 1 : -1;
        }

        StringBuilder ret = new StringBuilder();
        for (StringBuilder row : rows) ret.append(row);
        return ret.toString();
    }
}
```
时间复杂度O（n），空间O（n）

```java
class Solution {
    public String convert(String s, int numRows) {

        if (numRows == 1) return s;

        StringBuilder ret = new StringBuilder();
        int n = s.length();
        int cycleLen = 2 * numRows - 2;

        for (int i = 0; i < numRows; i++) {
            for (int j = 0; j + i < n; j += cycleLen) {
                ret.append(s.charAt(j + i));
                if (i != 0 && i != numRows - 1 && j + cycleLen - i < n)
                    ret.append(s.charAt(j + cycleLen - i));
            }
        }
        return ret.toString();
    }
}

```
## 按行访问

<img src="./pictures/Annotation 2020-04-03 202849.png"  div align=center />

```java
class Solution {
    public String convert(String s, int numRows) {

        if (numRows == 1) return s;

        StringBuilder ret = new StringBuilder();
        int n = s.length();
        int cycleLen = 2 * numRows - 2;

        for (int i = 0; i < numRows; i++) {
            for (int j = 0; j + i < n; j += cycleLen) {
                ret.append(s.charAt(j + i));
                if (i != 0 && i != numRows - 1 && j + cycleLen - i < n)
                    ret.append(s.charAt(j + cycleLen - i));
            }
        }
        return ret.toString();
    }
}

```
运行速度更快，但坐标和条件语句比较难想出来