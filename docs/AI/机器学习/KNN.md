<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<script type="text/x-mathjax-config">
    MathJax.Hub.Config({ tex2jax: {inlineMath: [['$', '$']]}, messageStyle: "none" });
</script>

# KNN(K-Nearest Neighbor)最近邻规则分类
* 为了判断未知实例的类别，以所有已知类别的实例作为参照选择参数K
* 计算未知实例与所有已知实例的距离
* 选择最近K个已知实例
* 根据少数服从多数的投票法则（majority-voting），让未知实例归类为K个最邻近样本中最多数的类别
![欧氏距离](https://gitee.com/zero049/MyNoteImages/raw/master/ou.png)
http://www.cnblogs.com/beltuture/p/5871452.html
## k的取值
![k](https://gitee.com/zero049/MyNoteImages/raw/master/k.png)

## 缺点
* 算法复杂度较高（需要比较所有已知实例与要分类的实例）
* 当其样本分布不平衡时，比如其中一类样本过大（实例数量过多）占主导的时候，新的未知实例容易被归类为这个主导样本，因为这类样本实例的数量过大，但这个新的未知实例实际并没有接近目标样本
![defect](https://gitee.com/zero049/MyNoteImages/raw/master/knndefect.png)

## 算法流程
* 先计算出与各点间距离
* 根据这些点距离排序
* 取距离小的前K个点
* 统计k个点中其最多的标签

```python
def knn(x_test, x_data, y_data, k):
    # 计算样本数量
    x_data_size = x_data.shape[0]
    # 计算x_test与每个点之间的欧几里得距离
    diffMat = np.tile(x_test, (x_data_size, 1)) - x_data 
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    # 根据距离排序
    sortedDistances = distances.argsort()
    classCount = {}
    # 统计出距离最近的点的标签数量
    for i in range(k):
        votelabel = y_data[sortedDistances[i]]
        classCount[votelabel] = classCount.get(votelabel, 0) + 1
    # 统计并排序出现最多的标签
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    
    return sortedClassCount[0][0]
        
```
