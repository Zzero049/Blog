

# Maven查看配置

1. 检查当前Maven环境启用的文件
   mvn help:effective-settings

2. 查看当前项目的pom配置，包括所有依赖
   mvn help:effective-pom

3. 查看当前处于激活状态的profile
   mvn help:active-profiles

4. 指定使用某个配置文件执行Maven命令
   mvn -s <filepath> <goal>
   mvn -s ~/.m2/settings_local.xml clean deploy

5. 查看当前项目的所有mvn配置

   mvn -X

6. 打印所有可用的环境变量和Java系统属性

   mvn help:system
   