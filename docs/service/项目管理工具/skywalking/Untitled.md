SkyWalking是什么？

SkyWalking是一个可观测性分析平台和应用性能管理系统，提供分布式跟踪、服务网格遥测分析、度量聚合和可视化一体化解决方案，并支持多种开发语言。

官网：http://skywalking.apache.org/ 两天前即2020年8月3号 8.1.0正式发布

![img](https://ask.qcloudimg.com/http-save/7454122/d042ypmxmg.png?imageView2/2/w/1620)

------

#  

# 安装

SkyWalking支持单机与集群部署（默认standalone），并支持多种数据存储（默认H2），如mysql，Elasticsearch，Elasticsearch7等。

本文以SkyWalking8.1.0并使用Elasticsearch来存储数据进行讲解

ElasticSearch搭建请参考我的另外一篇文章

SkyWalking下载地址：http://skywalking.apache.org/downloads/

由于要使用Elasticsearch，下载的时候请注意选择：

![img](https://ask.qcloudimg.com/http-save/7454122/2590qnllw4.png?imageView2/2/w/1620)

 点击tar后选择一个地址即可开始下载

![img](https://ask.qcloudimg.com/http-save/7454122/d7kebvrcht.png?imageView2/2/w/1620)

相关操作命令如下：

```javascript
cd /usr/local/src
wget https://mirror.bit.edu.cn/apache/skywalking/8.1.0/apache-skywalking-apm-es7-8.1.0.tar.gz
tar -xvf apache-skywalking-apm-es7-8.1.0.tar.gz

cd /usr/local/src/apache-skywalking-apm-bin-es7
```

修改相关配置：

1.web访问端口 8080->38080 （本机8080已被其它服务占用）

```javascript
vi /usr/local/src/apache-skywalking-apm-bin-es7/webapp/webapp.yml
#将server.port: 8080 改为38080
#或者使用sed命令
sed -i 's$8080$38080$g' /usr/local/src/apache-skywalking-apm-bin-es7/webapp/webapp.yml
```

2.修改使用Elasticsearch（默认使用h2）

![img](https://ask.qcloudimg.com/http-save/7454122/0jz2ldewri.png?imageView2/2/w/1620)

 注意：nameSpace要和Elasticsearch集群的cluster_name一致

```javascript
name" : "elk02",
  "cluster_name" : "es-cluster",
  "cluster_uuid" : "GnUvYMcGRK2GVJsvkwM7FQ",
  "version" : {
    "number" : "7.2.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "508c38a",
    "build_date" : "2019-06-20T15:54:18.811730Z",
    "build_snapshot" : false,
    "lucene_version" : "8.0.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
```

\#启动

```javascript
/usr/local/src/apache-skywalking-apm-bin-es7/bin/startup.sh
```

\#加入到开机启动

```javascript
cat "/usr/local/src/apache-skywalking-apm-bin-es7/bin/startup.sh" >> /etc/rc.d/rc.local
chmod +x /etc/rc.d/rc.local
```

\#确认应用启动成功端口正常监听

![img](https://ask.qcloudimg.com/http-save/7454122/o0402iqmwp.png?imageView2/2/w/1620)

 \#如果出错可以查看日志并根据错误类型进行处理

![img](https://ask.qcloudimg.com/http-save/7454122/gtnefhcdf.png?imageView2/2/w/1620)

\#然后可以打开浏览器进行查看 ip地址:38080

![img](https://ask.qcloudimg.com/http-save/7454122/tksvgj4121.png?imageView2/2/w/1620)

 一开始是没数据的，待项目集成后再刷新页面就可以看到数据了。

------

# 项目集成

- jar运行

```javascript
java -javaagent:/opt/skywalking/agent/skywalking-agent.jar 
     -Dskywalking.agent.service_name=xiao_test
     -Dskywalking.collector.backend_service=XXX.XXX.XXX.XXX:11800 
     -jar xxxx.jar
#javaagent agent包路径
#skywalking.agent.service_name 服务名称
#skywalking.collector.backend_service 采集信息的服务地址 agent.config配置了就可以不用指定
```

- docker运行

```javascript
#1.在打包插件中增加entrypoint并注意替换最后一部分和mainClass相同，然后打包
<plugin>
	<groupId>com.google.cloud.tools</groupId>
	<artifactId>jib-maven-plugin</artifactId>
	<version>1.7.0</version>
	<configuration>
		<from>
			<!-- 把agent拷贝到基础镜像去/opt/skywalking/agent/skywalking-agent.jar基础镜像去-->
			<image>hub.dev.zycloud.info/cx/oracle-jdk-with-skywalking:8</image>
			<auth>
				<username>xxxxxxxx</username>
				<password>xxxxxxxx</password>
			</auth>
		</from>
		<to>
			<image>hub.dev.zycloud.info/his/${project.artifactId}:${git.commit.id.abbrev}</image>
			<auth>
				<username>xxxxxxxx</username>
				<password>xxxxxxxx</password>
			</auth>
		</to>
		<allowInsecureRegistries>true</allowInsecureRegistries>
		<container>
			<useCurrentTimestamp>true</useCurrentTimestamp>
			<labels>
				<authors>${env.USERNAME}</authors>
				<version>${project.version}</version>
				<git-branch>${git.branch}</git-branch>
				<git-commit-id>${git.commit.id.abbrev}</git-commit-id>
				<git-commit-message>${git.commit.message.short}</git-commit-message>
				<git-commit-user>${git.commit.user.name}</git-commit-user>
			</labels>
			<environment>
				<SPRING_PROFILES_ACTIVE>pro</SPRING_PROFILES_ACTIVE>
				<SW_AGENT_NAME>${project.name}</SW_AGENT_NAME>
				<SW_LOGGING_DIR>/var/log/${project.artifactId}</SW_LOGGING_DIR>
				<SW_LOGGING_MAX_HISTORY_FILES>50</SW_LOGGING_MAX_HISTORY_FILES>
			</environment>
			<mainClass>
				info.zycloud.sass.application.nacos.user.NacosUserApplication
			</mainClass>
			<jvmFlags>
				<jvmFlag>-javaagent:/opt/skywalking/agent/skywalking-agent.jar</jvmFlag>
			</jvmFlags>
		</container>
	</configuration>
	<executions>
		<execution>
			<phase>deploy</phase>
			<goals>
				<goal>build</goal>
			</goals>
		</execution>
	</executions>
</plugin>

#2.docker运行
docker run -d --env SW_AGENT_COLLECTOR_BACKEND_SERVICES="192.168.38.100:11800" -p 29502:9502 hub.dev.zycloud.info/his/user:v1

或者将变量信息统一存放到env文件中
cat config.env
SW_AGENT_COLLECTOR_BACKEND_SERVICES=192.168.38.100:11800

docker run -d --env-file=config.env -p 29502:9502 hub.dev.zycloud.info/his/user:v1
#3.访问应用中服务后访问skywalking UI界面查看相应信息
```

![img](https://ask.qcloudimg.com/http-save/7454122/9td32cbq2a.png?imageView2/2/w/1620)

![img](https://ask.qcloudimg.com/http-save/7454122/4tttd05ps3.png?imageView2/2/w/1620)

本文参与[腾讯云自媒体分享计划](https://cloud.tencent.com/developer/support-plan)，欢迎正在阅读的你也加入，一起分享。