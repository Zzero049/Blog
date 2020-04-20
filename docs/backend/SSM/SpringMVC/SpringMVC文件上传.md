### 传统文件上传
#### 必要条件
1. form 表单的 enctype取值必须是：multipart/form-data
（默认值是：application/x-www-form-urlencoded）
enctype：是表单请求正文的类型
2. method 属性取值必须是Post
4. 提供一个文件选择域`<input tyge="file"/>`

当form表单的enctype取值不是默认值后，request.getParameter（）将失效。

enctype="application/x-www-form-urlencoded"时，form表单的正文内容是：
key=valueskey=value&key=value当form表单的enctype取值为Mutilpart/form-data时，请求正文内容就变成：
每一部分都是MIME类型描述的正文
-----------7de1a433602ac    &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;分界符
Content-Disposition:form-data；name="userName"&emsp;&emsp;&emsp;&emsp;协议头
pom.xml
```xml
<dependency>
      <groupId>commons-fileupload</groupId>
      <artifactId>commons-fileupload</artifactId>
      <version>1.3.1</version>
    </dependency>
    <dependency>
      <groupId>commons-io</groupId>
      <artifactId>commons-io</artifactId>
      <version>2.4</version>
    </dependency>
```

```java
@RequestMapping("/fileUpload1")
    public String fileUpload1(HttpServletRequest request) throws Exception {
        System.out.println("fileUpload1成功执行");
        //使用fileupload组件完成文件上传
        //上传的位置
        String path = request.getSession().getServletContext().getRealPath("/uploads/");
        //判断，该路径是否存在
        File file=new File(path);
        if(!file.exists()){
            //创建该文件夹
            file.mkdirs();
        }
        //解析request对象，获取上传文件项
        DiskFileItemFactory factory = new DiskFileItemFactory();
        ServletFileUpload upload = new ServletFileUpload(factory);
        //解析request
        List<FileItem> items =  upload.parseRequest(request);
        //遍历
        for(FileItem item:items){
            //进行判断，当前item对象是否是上传文件项
            if(item.isFormField()){
                //说明普通表单向

            }else{
                //说明上传文件项
                //获取上传文件的名称
                String filename=item.getName();
                //把文件的名称设置唯一值，uuid
                String uuid= UUID.randomUUID().toString().replace("-","");
                filename = uuid+"_"+filename;
                //完成文件上传
                item.write(new File(path,filename));
                //删除临时文件
                item.delete();
            }
        }
        return "success";
    }
```
### 跨服务器上传
```xml
<dependency>
<groupId>com.sun.jersey</groupId>
<artifactId>jersey-core</artifactId>
<version>1.18.1</version>
</dependency>
<dependency>
<groupId>com.sun.jersey</groupId>
<artifactId>jersey-client</artifactId>
<version>1.18.1</version>
</dependency>
```
```java
 @RequestMapping("/fileUpload2")
    public String fileUpload2(MultipartFile upload) throws Exception {
        System.out.println("跨服务器上传。。。");
        //定义上传文件服务器路径
        String path="http://1ocalhost:9090/uploads/";
        //获取上传文件的名称
        String filename=upload.getOriginalFilename();
        //把文件的名称设置唯一值，uuid
        String uuid= UUID.randomUUID().toString().replace("-","");
        filename = uuid+"_"+filename;
        //创建客户端的对象
        Client client= Client.create();
        //和图片服务器进行连接
        WebResource webResource = client.resource(path+filename);
        //上传文件
        webResource.put(upload.getBytes());
        return "success";
    }
```