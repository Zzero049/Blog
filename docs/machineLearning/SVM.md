<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<script type="text/x-mathjax-config">
    MathJax.Hub.Config({ tex2jax: {inlineMath: [['$', '$']]}, messageStyle: "none" });
</script>

# 支持向量机SVM（Support Vector Machine）
最早是由Vladimir N.Vapnik和Alexey Ya.Chervonenkis在1963年提出。
目前的版本（soft margin）是由Coninna Cortes和Vapnik在1993年提出，并在1995年发表。

深度学习（2012）出现之前，SVM被认为机器学习中近十几年来最成功，表现最好的算法，在复杂分类情况下如图像识别、人脸识别表现良好，但是深度学习出现之后，其分类效果比SVM好很多，于是现在很多时候SVM被深度学习取代了。

二分类寻找分界线，如图有多条分界线可选，SVM的任务就是很好的找到这样的分界线（超平面）进行分类
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-10-13 095223.png"  div align=center />

SVM寻找超平面原理
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-10-13 095122.png"  div align=center />
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-10-13 095944.png"  div align=center />


### 向量内积
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-10-13 095629.png"  div align=center />
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-10-13 095841.png"  div align=center />


## SVM优点
训练好的模型的算法复杂度是由支持向量的个数决定的，
而不是由数据的维度决定的。所以SVM不太容易产生
overfitting
*  SVM训练出来的模型完全依赖于支持向量(Support
Vectors), 即使训练集里面所有非支持向量的点都被去
除，重复训练过程，结果仍然会得到完全一样的模型。
* 一个SVM如果训练得出的支持向量个数比较小， SVM
* 训练出的模型比较容易被泛化





*todo*：具体细节推导还是不太会
涉及拉格朗日乘数法，对偶问题
又分线性可分，线性问题，非线性问题

**原理、推导参考**
https://www.cnblogs.com/further-further-further/p/9596898.html

https://blog.csdn.net/weixin_34087503/article/details/89549272