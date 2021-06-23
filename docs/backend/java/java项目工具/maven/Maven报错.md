# Maven 报错汇总



## 1. 打包

### 1.1  Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.8.1:compile 

具体报错如下

```
[WARNING] Error injecting: org.apache.maven.plugin.compiler.CompilerMojo
java.lang.NoClassDefFoundError: org/codehaus/plexus/compiler/util/scan/mapping/SuffixMapping

...
...

[ERROR] import: Entry[import  from realm ClassRealm[maven.api, parent: null]]
[ERROR] 
[ERROR] -----------------------------------------------------
[ERROR] : org.codehaus.plexus.compiler.util.scan.mapping.SuffixMapping
```

解决方案：

卸载maven3.6.2，安装3.6.3