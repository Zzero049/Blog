# 主从复制
主机做的操作，从机从主机那里复制过去。


MySQL复制过程分成三步：
1 master将改变记录到二进制日志（binary log）。这些记录过程叫做二进制日志事件，binary log events；
2 slave将master的binary log events拷贝到它的中继日志（relaylog）；
3 slave重做中继日志中的事件，将改变应用到自己的数据库中。MySQL复制是异步的且串行化的
<img src="https://gitee.com/zero049/MyNoteImages/raw/master/Annotation 2019-12-25 212224.png"  div align=center />

### 复制的原则
每个slave只有一个master
每个slave只能有一个唯一的服务器ID
每个master可以有多个salve

具体操作配置的时候再一步步弄