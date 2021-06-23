首先需要介绍元老级别的Google开源的项目： [Dapper](http://bigbully.github.io/Dapper-translation/)

### 1. 介绍

[www.cnblogs.com/xiaoqi/p/ap…](https://www.cnblogs.com/xiaoqi/p/apm.html), 这篇文章介绍的不错

其实对于现在 APM（Application Performance Management）系统，以下三点都包含了，不管是系统指标（[Prometheus](https://prometheus.io/)），还是日志（ELK），还是链路追踪（Skywalking，zipkin，jeager），都逐步向中间靠拢

![image-20201029132759719](https:////p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/32f93415154641f687f67f86c186778c~tplv-k3u1fbpfcp-zoom-1.image)

这个是目前市场上主流的开源的 链路追踪系统，我们可以看一下大致的区别，目前比较火的其实是后三者，他们其实都可以互相兼容，因为实现了 opentracing 规范！

其中比较推荐的是：[Jeager](https://www.jaegertracing.io/docs/1.20/getting-started/)（17年孵化的项目），原因就是作为 [CNCF毕业项目](https://www.cncf.io/projects/) ，成长空间和云原声的系统架构比较兼容性好。

下面还有很多没有介绍到的，比如美团的[CAT](https://github.com/dianping/cat)，fb的 [xhprof](https://github.com/phacility/xhprof) ， 阿里的[鹰眼](https://www.cnblogs.com/gzxbkk/p/9600263.html)

![image-20201029132943685](https:////p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/84f2695e70aa47d1914b1045fb04deaa~tplv-k3u1fbpfcp-zoom-1.image)

### 2. opentracing 规范

[官网链接](https://opentracing.io/guides/java/)  [opentracing.io/guides/java…](https://opentracing.io/guides/java/)

[规范链接 ](https://github.com/opentracing-contrib/opentracing-specification-zh/blob/master/specification.md)  [github.com/opentracing…](https://github.com/opentracing-contrib/opentracing-specification-zh/blob/master/specification.md)

[链路追踪（二）-分布式链路追踪系统数据采集](https://www.cnblogs.com/hama1993/p/10713747.html)  ,这两篇文章都比较不错， 这个是基于 open tracing规范开发的。

## 1、架构

官方给的设计图在这里 :   这个就是整体的设计架构图.

- 1、Trace，其实就是收集器
- 2、Metric，就是系统监控，比如JVM的一些信息，但是并没有提供Go的信息
- 3、核心还是他的 可观测分析平台，提供了分析和查询的功能，是很多loging/trace框架没有的(所以我也想像借助它以最小的成本整合到业务中去，我们这边开发语言是Go，但是go-sdk提供的埋点编码太多，并不适合直接使用，其次是和我们业务耦合太重，所以我这里不推荐直接使用，介意进一步封装API)

![img](https:////p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b9828316b37d4f4dabadd6aad63ba09e~tplv-k3u1fbpfcp-zoom-1.image)

## 2. 快速开始

- 1、安装 skywalking 8.0.1 ， [www.apache.org/dyn/closer.…](https://www.apache.org/dyn/closer.cgi/skywalking/8.0.1/apache-skywalking-apm-8.0.1.tar.gz)
- 2、阅读 8.0的文档， [skyapm.github.io/document-cn…](https://skyapm.github.io/document-cn-translation-of-skywalking/zh/8.0.0/)
- 3、下载Go-SDK ，[github.com/SkyAPM/go2s…](https://github.com/SkyAPM/go2sky/archive/v0.4.0.zip) ，其中 v0.4.0 才支持了 8.0 版本，所以需要注意。

基于上诉准备，我们就可以快速的开发Go的探针

- 1、启动skywalking

```shell
➜  bin ./startup.sh
SkyWalking OAP started successfully!
SkyWalking Web Application started successfully!
```

## 3、Go的跨服务调用的探针埋点

> ​	对于Java开发者使用SkyWalking来说，简单来说常用的开发框架他都做了自动埋点，但是对于Go来说啥都需要手动埋点，需要我们自己写代码，而不是官方的人去写代码。
>
> 目前来说Go这边支持了Gin框架，但是切记，这只是一个Demo

```go
import (
	"fmt"
	"github.com/SkyAPM/go2sky"
	"github.com/SkyAPM/go2sky/multi_server/common"
	"github.com/SkyAPM/go2sky/reporter"
	"github.com/gin-gonic/gin"
	"net/http"
	"time"

	gg "github.com/SkyAPM/go2sky/plugins/gin"
)

const (
	server_name_2 = "server-2"
	server_port_2 = 8082
)

func main() {
	r := gin.New()
  // SkyAddr 是skywaling的grpc地址，默认是localhost:11800 ， 默认心跳检测时间是1s
	rp, err := reporter.NewGRPCReporter(common.SkyAddr, reporter.WithCheckInterval(time.Second))
	common.PanicError(err)
  // 初始化一个 tracer，一个服务只需要一个tracer，其含义是这个服务名称
	tracer, err := go2sky.NewTracer(server_name_2, go2sky.WithReporter(rp))
	common.PanicError(err)
  // gin 使用 sky自带的middleware， 说实话0.4代码比0.3强太多了！
	r.Use(gg.Middleware(r, tracer))

  // 自定义一个接口
	r.POST("/user/info", func(context *gin.Context) {
    // LocalSpan可以理解为本地日志的tracer，一般用户当前应用
		span, ctx, err := tracer.CreateLocalSpan(context.Request.Context())
		common.PanicError(err)
    // 每一个span都有一个名字去标实操作的名称！
		span.SetOperationName("UserInfo")
    // 记住重新设置一个ctx，再其次这个ctx不是gin的ctx，而是httprequest的ctx
		context.Request = context.Request.WithContext(ctx)
    
    // 。。。。
    params := new(common.Params)
		err = context.BindJSON(params)
		common.PanicError(err)

		span.Log(time.Now(), "[UserInfo]", fmt.Sprintf(server_name_2+" satrt, req : %+v", params))
		local := gin.H{
			"msg": fmt.Sprintf(server_name_2+" time : %s", time.Now().Format("15:04:05")),
		}
		context.JSON(200, local)
		span.Log(time.Now(), "[UserInfo]", fmt.Sprintf(server_name_2+" end, resp : %s", local))
    // 切记最后要设置span - end，不然就是一个非闭环的
		span.End()
	})

	common.PanicError(http.ListenAndServe(fmt.Sprintf(":%d", server_port_2), r))
}
复制代码
```

server-1 调用 server -2

```go
import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/SkyAPM/go2sky"
	"github.com/SkyAPM/go2sky/multi_server/common"
	"github.com/SkyAPM/go2sky/propagation"
	"github.com/SkyAPM/go2sky/reporter"
	v3 "github.com/SkyAPM/go2sky/reporter/grpc/language-agent"
	"github.com/gin-gonic/gin"
	"io/ioutil"
	"net/http"
	"time"

	gg "github.com/SkyAPM/go2sky/plugins/gin"
)

const (
	server_name        = "server-1"
	server_port        = 8081
	remote_server_name = "server-2"
	remote_server_addr = "localhost:8082"
	remoto_path        = "/user/info"
)

func main() {

  // 这些都一样
	r := gin.New()
	rp, err := reporter.NewGRPCReporter(common.SkyAddr, reporter.WithCheckInterval(time.Second))
	common.PanicError(err)
	tracer, err := go2sky.NewTracer(server_name, go2sky.WithReporter(rp))
	common.PanicError(err)
	r.Use(gg.Middleware(r, tracer))

  // 调用接口
	r.GET("/trace", func(context *gin.Context) {
		span, ctx, err := tracer.CreateLocalSpan(context.Request.Context())
		common.PanicError(err)
		span.SetOperationName("Trace")

		context.Request = context.Request.WithContext(ctx)
		span.Log(time.Now(), "[Trace]", fmt.Sprintf(server_name+" satrt, params : %s", time.Now().Format("15:04:05")))

		result := make([]map[string]interface{}, 0)

    //1、请求一次
		{
			url := fmt.Sprintf("http://%s%s", remote_server_addr, remoto_path)

			params := common.Params{
				Name: server_name + time.Now().Format("15:04:05"),
			}
			buffer := &bytes.Buffer{}
			_ = json.NewEncoder(buffer).Encode(params)
			req, err := http.NewRequest(http.MethodPost, url, buffer)
			common.PanicError(err)

			// op_name 是每一个操作的名称
			reqSpan, err := tracer.CreateExitSpan(context.Request.Context(), "invoke - "+remote_server_name, fmt.Sprintf("localhost:8082/user/info"), func(header string) error {
				req.Header.Set(propagation.Header, header)
				return nil
			})
			common.PanicError(err)
			reqSpan.SetComponent(2)                         //HttpClient,看 https://github.com/apache/skywalking/blob/master/docs/en/guides/Component-library-settings.md ， 目录在component-libraries.yml文件配置
			reqSpan.SetSpanLayer(v3.SpanLayer_RPCFramework) // rpc 调用

			resp, err := http.DefaultClient.Do(req)
			common.PanicError(err)
			defer resp.Body.Close()

			reqSpan.Log(time.Now(), "[HttpRequest]", fmt.Sprintf("开始请求,请求服务:%s,请求地址:%s,请求参数:%+v", remote_server_name, url, params))
			body, err := ioutil.ReadAll(resp.Body)
			common.PanicError(err)
			fmt.Printf("接受到消息： %s\n", body)
			reqSpan.Tag(go2sky.TagHTTPMethod, http.MethodPost)
			reqSpan.Tag(go2sky.TagURL, url)
			reqSpan.Log(time.Now(), "[HttpRequest]", fmt.Sprintf("结束请求,响应结果: %s", body))
			reqSpan.End()
			res := map[string]interface{}{}
			err = json.Unmarshal(body, &res)
			common.PanicError(err)
			result = append(result, res)
		}

    //2 、再请求一次
		{
			url := fmt.Sprintf("http://%s%s", remote_server_addr, remoto_path)

			params := common.Params{
				Name: server_name + time.Now().Format("15:04:05"),
			}
			buffer := &bytes.Buffer{}
			_ = json.NewEncoder(buffer).Encode(params)
			req, err := http.NewRequest(http.MethodPost, url, buffer)
			common.PanicError(err)

			// 出去必须用这个携带header
			reqSpan, err := tracer.CreateExitSpan(context.Request.Context(), "invoke - "+remote_server_name, fmt.Sprintf("localhost:8082/user/info"), func(header string) error {
				req.Header.Set(propagation.Header, header)
				return nil
			})
			common.PanicError(err)
			reqSpan.SetComponent(2)                         //HttpClient,看 https://github.com/apache/skywalking/blob/master/docs/en/guides/Component-library-settings.md ， 目录在component-libraries.yml文件配置
			reqSpan.SetSpanLayer(v3.SpanLayer_RPCFramework) // rpc 调用

			resp, err := http.DefaultClient.Do(req)
			common.PanicError(err)
			defer resp.Body.Close()

			reqSpan.Log(time.Now(), "[HttpRequest]", fmt.Sprintf("开始请求,请求服务:%s,请求地址:%s,请求参数:%+v", remote_server_name, url, params))
			body, err := ioutil.ReadAll(resp.Body)
			common.PanicError(err)
			fmt.Printf("接受到消息： %s\n", body)

			reqSpan.Tag(go2sky.TagHTTPMethod, http.MethodPost)
			reqSpan.Tag(go2sky.TagURL, url)
			reqSpan.Log(time.Now(), "[HttpRequest]", fmt.Sprintf("结束请求,响应结果: %s", body))
			reqSpan.End()
			res := map[string]interface{}{}
			err = json.Unmarshal(body, &res)
			common.PanicError(err)
			result = append(result, res)
		}

    // 设置响应结果
		local := gin.H{
			"msg": result,
		}
		context.JSON(200, local)
		span.Log(time.Now(), "[Trace]", fmt.Sprintf(server_name+" end, resp : %s", local))
		span.End()
		{
			span, ctx, err := tracer.CreateEntrySpan(context.Request.Context(), "Send", func() (s string, e error) {
				return "", nil
			})
			context.Request = context.Request.WithContext(ctx)
			common.PanicError(err)
			span.SetOperationName("Send")
			//span.Error(time.Now(), "[Error]", "time is too long")
			span.Log(time.Now(), "[Info]", "send resp")
			span.End()
		}
	})

	common.PanicError(http.ListenAndServe(fmt.Sprintf(":%d", server_port), r))

}
复制代码
```

最终调用效果如下：是一个简单的时序图

![image-20200913165902725](https:////p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/52e9ff48b63e40ffb2e6ee8e80e95b37~tplv-k3u1fbpfcp-zoom-1.image)

这就是一个跨进程的简单调用。

## 4、需要知道的一些细节

go-sky 的 sdk，0.4 对于 0.3的改动很大，其中很大一部分在于个性化的功能设置更多了，再其次就是支持v3协议，后面再说。

### 1、reporter

> ​	就是用来发送数据的

这个就是一个初始化的过程，很简单

```go
reporter.NewGRPCReporter(common.SkyAddr, reporter.WithCheckInterval(time.Second))
复制代码
```

主要就三个核心方法！

![image-20200913170324887](https:////p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d58da3ccb24b4a21ba7b2dcb07878e76~tplv-k3u1fbpfcp-zoom-1.image)

启动，发送，关闭，三个方法。。。很简单和方便

### 2、tracer

> ​	tracer 就是用来追踪的，遵守open trace 规范。

```go
// NewTracer return a new go2sky Tracer
func NewTracer(service string, opts ...TracerOption) (tracer *Tracer, err error) {
	if service == "" {
		return nil, errParameter
	}
	t := &Tracer{
		service:  service,
		initFlag: 0,
	}
	for _, opt := range opts {
		opt(t)
	}

	if t.reporter != nil {
		if t.instance == "" {
			id, err := idgen.UUID()
			if err != nil {
				return nil, err
			}
			t.instance = id + "@" + tool.IPV4()
		}
    // 调用了reporter的启动方法，所以对于需要创建tracer的是不需要自己启动reporter的
		t.reporter.Boot(t.service, t.instance)
		t.initFlag = 1
	}
	return t, nil
}
```

### 3、span(核心)

> ​	span 就是我们主要关注的核心，可以理解为就是全部的核心

#### 1、方法介绍

```go
type Span interface {
   SetOperationName(string) // 每一个span唯一的id就是OperationName，这个最好创建的时候有规范
   GetOperationName() string
   SetPeer(string) // 这个是设置兄弟节点，不知道是干啥了。。。。
   SetSpanLayer(v3.SpanLayer) // 这个主要是设置类型，比如你是RPC，DB，MQ？
   SetComponent(int32)// 这个是设置 Span的类型，比如HTTP客户端/MYSQL客户端，相对于上面的，这个类型更加具体
   Tag(Tag, string)// tag是标签
   Log(time.Time, ...string) // 日志功能
   Error(time.Time, ...string)
   End()// 每一个span都需要设置一个结尾标识符
   IsEntry() bool
   IsExit() bool
}
```

span 其实就是这种key - value 结构。

![image-20200913173309904](https:////p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/02b48c07edf7453c80323e1258575214~tplv-k3u1fbpfcp-zoom-1.image)

#### 2、EntrySpan

一般是进入哪个服务了就使用`EntrySpan`

这里一般指的是比如进入 `server-1`或者`server-2` ， 就去创建一个 entry span

```go
//Middleware gin middleware return HandlerFunc  with tracing.
func Middleware(engine *gin.Engine, tracer *go2sky.Tracer) gin.HandlerFunc {
	if engine == nil || tracer == nil {
		return func(c *gin.Context) {
			c.Next()
		}
	}
	m := new(middleware)

	return func(c *gin.Context) {
		m.routeMapOnce.Do(func() {
			routes := engine.Routes()
			/// 。。。 不用care
		})
		var operationName string
		handlerName := c.HandlerName()
		if routeInfo, ok := m.routeMap[c.Request.Method][handlerName]; ok {
			operationName = routeInfo.operationName
		}
		if operationName == "" {
			operationName = c.Request.Method
		}
    // 创建
    //1、参数是ctx
    //2、每一个span都有一个id，比如一般是以路由名称为id的
    //3、会掉函数，主要是获取header(这个头的介绍：https://github.com/apache/skywalking/blob/master/docs/en/protocols/Skywalking-Cross-Process-Propagation-Headers-Protocol-v3.md )
		span, ctx, err := tracer.CreateEntrySpan(c.Request.Context(), operationName, func() (string, error) {
			return c.Request.Header.Get(propagation.Header), nil
		})
		if err != nil {
			c.Next()
			return
		}
    // 设置该span的类型，这里一般是根据：这个文件确定的，默认也没提供几个id，go-sdk里
		span.SetComponent(httpServerComponentID)
		span.Tag(go2sky.TagHTTPMethod, c.Request.Method)
		span.Tag(go2sky.TagURL, c.Request.Host+c.Request.URL.Path)
		span.SetSpanLayer(v3.SpanLayer_Http)

    // 这里值得注意，没有使用gin的ctx
		c.Request = c.Request.WithContext(ctx)

		c.Next()

		if len(c.Errors) > 0 {
			span.Error(time.Now(), c.Errors.String())
		}
    // end，设置code
		span.Tag(go2sky.TagStatusCode, strconv.Itoa(c.Writer.Status()))
		// end
    span.End()
	}
}

复制代码
```

其实这个API相当好理解哇，就是拿到头，设置trace_id，然后继续打log

#### 3、ExitSpan

其实也不能叫做退出Span，他只是服务调用，可以理解为 我A服务调用B服务，A需要使用`ExitSpan`发送探针，去创建一个儿子，然后B服务收到后，使用`EntrySpan`去接受，它认了认个父亲。这样就有关系了

```go
url := fmt.Sprintf("http://%s%s", remote_server_addr, remoto_path)
params := common.Params{
  Name: server_name + time.Now().Format("15:04:05"),
}
buffer := &bytes.Buffer{}
_ = json.NewEncoder(buffer).Encode(params)
// 创建一个http.Request
req, err := http.NewRequest(http.MethodPost, url, buffer)
common.PanicError(err)

// 创建一个Tracer
reqSpan, err := tracer.CreateExitSpan(context.Request.Context(), "invoke - "+remote_server_name, fmt.Sprintf("localhost:8082/user/info"), func(header string) error {
  req.Header.Set(propagation.Header, header)
  return nil
})
common.PanicError(err)
// 设置为HttpClient类型
reqSpan.SetComponent(2)
// rpc 调用
reqSpan.SetSpanLayer(v3.SpanLayer_RPCFramework) 

reqSpan.Tag(go2sky.TagHTTPMethod, http.MethodPost)
reqSpan.Tag(go2sky.TagURL, url)

// 记录开始日志
reqSpan.Log(time.Now(), "[HttpRequest]", fmt.Sprintf("开始请求,请求服务:%s,请求地址:%s,请求参数:%+v", remote_server_name, url, params))
// 直接去调用请求
resp, err := http.DefaultClient.Do(req)
common.PanicError(err)
defer resp.Body.Close()

body, err := ioutil.ReadAll(resp.Body)
common.PanicError(err)
// 记录响应日志
reqSpan.Log(time.Now(), "[HttpRequest]", fmt.Sprintf("结束请求,响应结果: %s", body))
// 结束。其实还应该记录状态码
reqSpan.End()
res := map[string]interface{}{}
err = json.Unmarshal(body, &res)
common.PanicError(err)
result = append(result, res)
复制代码
```

其实看树状图很简单的就看出来了。

![image-20200913174055349](data:image/svg+xml;utf8,<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="800" height="600"></svg>)

#### 4、LocalSpan

`LocalSpan`可以理解为进程/线程内部的Span，它如果没有指定，父亲，是没有父子交互的，也就是这个链路串不起来。

```go
span, ctx, err := tracer.CreateLocalSpan(context.Request.Context())
common.PanicError(err)
// 设置id
span.SetOperationName("UserInfo")
context.Request = context.Request.WithContext(ctx)
params := new(common.Params)
err = context.BindJSON(params)
common.PanicError(err)

span.Log(time.Now(), "[UserInfo]", fmt.Sprintf(server_name_2+" satrt, req : %+v", params))
local := gin.H{
  "msg": fmt.Sprintf(server_name_2+" time : %s", time.Now().Format("15:04:05")),
}
context.JSON(200, local)
span.Log(time.Now(), "[UserInfo]", fmt.Sprintf(server_name_2+" end, resp : %s", local))
span.End()
复制代码
```

#### 5、源码分析

```go
// CreateLocalSpan creates and starts a span for local usage
func (t *Tracer) CreateLocalSpan(ctx context.Context, opts ...SpanOption) (s Span, c context.Context, err error) {
  // ctx为空 异常
	if ctx == nil {
		return nil, nil, errParameter
	}
  // 是否是一个不需要操作的ctx，这个意思就是这个ctx的是一个NoopSpan，需要儿子不需要任何操作
	if s, c = t.createNoop(ctx); s != nil {
		return
	}
  // 初始化一个
	ds := newLocalSpan(t)
	for _, opt := range opts {
		opt(ds)
	}
  // 这个就是去获取ctx的一个segmentSpan，主要就是trace_id
	parentSpan, ok := ctx.Value(ctxKeyInstance).(segmentSpan)
	if !ok {
		parentSpan = nil
	}
  // 核心步骤
	s, err = newSegmentSpan(ds, parentSpan)
	if err != nil {
		return nil, nil, err
	}
	return s, context.WithValue(ctx, ctxKeyInstance, s), nil
}
复制代码
s, err = newSegmentSpan(ds, parentSpan)
type segmentSpanImpl struct {
	defaultSpan // span
	SegmentContext // 上下文信息
}
复制代码
func newSegmentSpan(defaultSpan *defaultSpan, parentSpan segmentSpan) (s segmentSpan, err error) {
	ssi := &segmentSpanImpl{
		defaultSpan: *defaultSpan,
	}
  // span 其实所有的都是segmentSpan，除了noop，所以核心逻辑在这里
	err = ssi.createSegmentContext(parentSpan)
	if err != nil {
		return nil, err
	}
  // 创建父亲节点，一个进程内的一个链路只能创建一次
	if parentSpan == nil || !parentSpan.segmentRegister() {
		rs := newSegmentRoot(ssi)
		err = rs.createRootSegmentContext(parentSpan)
		if err != nil {
			return nil, err
		}
		s = rs
	} else {
		s = ssi
	}
	return
}
复制代码
err = ssi.createSegmentContext(parentSpan)
func (s *segmentSpanImpl) createSegmentContext(parent segmentSpan) (err error) {
	if parent == nil {// 父亲为空
    // 创建一个新的上下文
		s.SegmentContext = SegmentContext{}
		if len(s.defaultSpan.Refs) > 0 {// ref>0，后面解释
			s.TraceID = s.defaultSpan.Refs[0].TraceID// 获取第一个trace_id
		} else {
			s.TraceID, err = idgen.GenerateGlobalID()// 通过id生成器，生产一个id
			if err != nil {
				return err
			}
		}
	} else {
    // 上下文信息传递
		s.SegmentContext = parent.context()
		s.ParentSegmentID = s.SegmentID
		s.ParentSpanID = s.SpanID
		s.SpanID = atomic.AddInt32(s.Context().spanIDGenerator, 1)
	}
	if s.SegmentContext.FirstSpan == nil {
		s.SegmentContext.FirstSpan = s
	}
	return
}
复制代码
```

所以我想说的是所有的都是`LocalSpan`

```go
// CreateEntrySpan creates and starts an entry span for incoming request
func (t *Tracer) CreateEntrySpan(ctx context.Context, operationName string, extractor propagation.Extractor) (s Span, nCtx context.Context, err error) {
	if ctx == nil || operationName == "" || extractor == nil {
		return nil, nil, errParameter
	}
	if s, nCtx = t.createNoop(ctx); s != nil {
		return
	}
	header, err := extractor()
	if err != nil {
		return
	}
	var refSc *propagation.SpanContext
	if header != "" {
    //解析头部
		refSc = &propagation.SpanContext{}
		err = refSc.DecodeSW8(header)
		if err != nil {
			return
		}
	}
  // 设置WithContext，申明父亲的trace_id
	s, nCtx, err = t.CreateLocalSpan(ctx, WithContext(refSc), WithSpanType(SpanTypeEntry))
	if err != nil {
		return
	}
	s.SetOperationName(operationName)
	return
}
复制代码
```

## 5、Go和Java应用一起Happy

上面的Server-1和Server-2代码不变，新增一个Java的请求

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.Collections;
import java.util.Map;

@SpringBootApplication
public class SpringSkywalkingApplication {
    public static void main(String[] args) {
        SpringApplication.run(SpringSkywalkingApplication.class, args);
    }
    @Bean
    public RestTemplate rt() {
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.setRequestFactory(new SimpleClientHttpRequestFactory());
        return restTemplate;
    }
    @RestController
    @RequestMapping("/rpc")
    public static class DemoRpcController {
        @Autowired
        private RestTemplate template;
        @GetMapping("/go")
        public Map invoke() {
            return template.getForObject("http://localhost:8081/trace", Map.class);
        }
    }
}
复制代码
```

启动的时候，加上JVM参数

```java
-javaagent:/Users/dong/software/apache-skywalking-apm-bin/agent/skywalking-agent.jar
-Dskywalking.agent.service_name=java-api
-Dskywalking.collector.backend_service=localhost:11800
复制代码
```

然后就可以愉快的使用了

```shell
➜  java curl http://localhost:8888/rpc/go
{"msg":[{"msg":"server-2 time : 18:36:30"},{"msg":"server-2 time : 18:36:30"}]}
复制代码
```

可以发现成功调用！！！！！！！

![image-20200913183754478](https:////p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b278b8ee13614282bd5ec1dc3d6b7300~tplv-k3u1fbpfcp-zoom-1.image)

调用图：

![image-20200913184145812](https:////p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/28acbe31d777476fac21e68e1c359021~tplv-k3u1fbpfcp-zoom-1.image)

## 6、改造Go-Skywalking

​      我们这边主要的编程语言是Go，业务中并未使用op-tracing 规范，只是通过请求头携带trace_id。大致逻辑就是 server-1 调用 server-2 会携带一个请求头，trace_id=1, 当server-2收到的时候创建一个并且append server-2的trace_id，此时trace_id=2_1 ，我们所有的func都传递了ctx，所以很轻松的在日志里记录trace_id。

```shell
logger.Infoc(ctx, "[GetCityMonthlyXXXXList] start,params=%+v", &request.Params)
复制代码
2020/07/25 11:28:35 service_request.go:119: [INFO] [trace_id=xxxxxx] [HttpRequest] start,server_name=xxxxx,url=http://xxxx:13071/ucenter/v1/user/black_detail,params=map[type:2 user_id:907744]
复制代码
```

但是我们业务只有一个简单的依靠elk进行的过滤，并没有调用图，全链路图，并不能找到出现了哪些问题。最主要的是，你都不知道哪个服务调用你，因此造成业务问题追查起来比较难。

因此想依靠skywalking的收集器将日志收集起来，做统一的展示！

### 1、基于异步模式

1、业务的Logger不变，启动一个服务消费Logger的日志(业务中是kafka)，采用sky-walking的go客户端

2、我们只需要改造reporter即可，也就是只需要将reporter改造成logger方式

3、看官方提供的简单的reporter， `NewLogReporter()`

还是上面的程序，我们改成日志

```go
rp, err := reporter.NewLogReporter()
common.PanicError(err)
复制代码
```

然后再看一下我们的输出

```go
go2sky-log2020/09/13 19:17:45 Segment-bfd2097af5b211eab1203c15c2d23e34: [
    {
        "Refs": null,
        "StartTime": "2020-09-13T19:17:45.942056+08:00",
        "EndTime": "2020-09-13T19:17:45.968277+08:00",
        "OperationName": "invoke - server-2",
        "Peer": "localhost:8082/user/info",
        "Layer": 2,
        "ComponentID": 2,
        "Tags": [
            {
                "key": "http.method",
                "value": "POST"
            },
            {
                "key": "url",
                "value": "http://localhost:8082/user/info"
            }
        ],
        "Logs": [
            {
                "time": 1599995865968,
                "data": [
                    {
                        "key": "[HttpRequest]",
                        "value": "开始请求,请求服务:server-2,请求地址:http://localhost:8082/user/info,请求参数:{Name:server-119:17:45}"
                    }
                ]
            },
            {
                "time": 1599995865968,
                "data": [
                    {
                        "key": "[HttpRequest]",
                        "value": "结束请求,响应结果: {\"msg\":\"server-2 time : 19:17:45\"}"
                    }
                ]
            }
        ],
        "IsError": false,
        "SpanType": 1,
        "TraceID": "bfd2093ef5b211eab1203c15c2d23e34",
        "SegmentID": "bfd2097af5b211eab1203c15c2d23e34",
        "SpanID": 2,
        "ParentSpanID": 1,
        "ParentSegmentID": "bfd2097af5b211eab1203c15c2d23e34"
    },
 // ... 
]
复制代码
```

如果我们能解析出来，发送给sky就可以了，简单试试

```go
复制代码
```

但是，实际上是不可以的，需要对其进行二次加工。。。。。。。。。。。

## 7、报警模块

[报警官方文档](https://github.com/apache/skywalking/blob/master/docs/en/setup/backend/backend-alarm.md#list-of-all-potential-metrics-name)

[juejin.im/post/684490…](https://juejin.im/post/6844903954770313224)

## 参考

[github.com/apache/skyw…](https://github.com/apache/skywalking)

[skyapm.github.io/document-cn…](https://skyapm.github.io/document-cn-translation-of-skywalking/zh/8.0.0/)

## Demo地址

[gitee.com/Anthony-Don…](https://gitee.com/Anthony-Dong/skywalking-demo)


