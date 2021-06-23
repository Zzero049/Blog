- ElasticSearch 是个开源分布式搜索引擎，它的特点有：分布式，零配置，自动发现，索引自动分片，索引副本机制，restful风格接口，多数据源，自动搜索负载等。它可以快速地、近实时的存储，搜索和分析大规模的数据。一般被用作底层引擎/技术，为具有复杂搜索功能和要求的应用提供强有力的支撑。Elasticsearch 至少需要Java 8

  Kibana 是一个开源分析和可视化平台，旨在可视化操作 Elasticsearch 。Kibana可以用来搜索，查看和与存储在 ElasticSearch 索引中的数据进行交互。可以轻松地进行高级数据分析，并可在各种图表，表格和地图中显示数据。Kibana 可以轻松理解海量数据。其简单的基于浏览器的界面使您能够快速创建和共享动态仪表板，实时显示 Elasticsearch 查询的更改。

  官网下载

  ElasticSearch下载：https://www.elastic.co/cn/downloads/elasticsearch，这里我们选择的是WINDOWS版本

  Kibana下载：https://www.elastic.co/cn/downloads/kibana，这里我们选择的是WINDOWS版本


  百度网盘下载

  链接: https://pan.baidu.com/s/19hD88pViPrbW3LUwENgOlg 提取码: cfpa

  ElasticSearch安装

  解压下载好的ZIP包，将它放在常用的安装目录下面，elasticsearch-6.5.4.zip，如下图：

  双击bin目录下面的elasticsearch.bat，即可运行，如下图

  访问：http://127.0.0.1:9200，出现JSON数据，即代表ES安装成功，如下图：

  Kibana安装

  解压下载下来的kibana-6.5.4-windows-x86_64.zip，放到常用的安装盘目录下面，将文件夹名字修改的简洁一点，kibana-6.5.4，如下图

  CMD打开命令窗口，切换到kibana所安装的目录的bin下面，然后执行kibana回车；或者直接双击bin目录下面的kibana.bat执行文件即可，如下图

  在浏览器中访问 http://127.0.0.1:5601，出现“Kibana server is not ready yet”的话，证明你没有启动ES服务。如果出现如下类似界面，即表示

  