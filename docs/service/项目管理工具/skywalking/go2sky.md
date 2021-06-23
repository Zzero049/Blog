1、背景介绍git

​    因为在微服务架构中，服务之间的调用关系多而复杂，因此有必要对它们之间的调用链路进行追踪、分析，判断是哪里出了问题，或者哪里耗时过多。github

​    最近接到了这个需求，添加全链路追踪，因此研究并实践了一下，还不太深入，如有错误的地方欢迎指正。数据库

2、OpenTracing相关概念介绍架构

​    首先，要实现全链路追踪，必须先理解OpenTracing的一些基本概念。OpenTracing为分布式链路追踪制定了一个统一的标准。只要是按照此标准实现的服务，就可以完整的进行分布式追踪。分布式

  \1. Span函数

​    Span能够被翻译为跨度，能够理解为一次方法调用，一个程序块的调用，或者一次RPC/数据库访问。微服务

​    Span之间是有关系的，child of 和 follow of。好比一次RPC的调用，RPC客户端和服务端的span就造成了父子关系。spa

  \2. Trace翻译

​    Trace表示一个调用链，好比在分布式服务中，一个客户端的请求，在后台可能通过了层层的调用，那么每一次调用就至关于一个span，而这一整条调用链路，能够理解成一个trace。3d

​    Trace有一个全局惟一的ID。

3、Go2sky简介

​    Go2sky是Golang提供给开发者实现SkyWalking agent探针的包，能够经过它来实现向SkyWalking Collector上报数据。

​    快速入门：[GitHub-Go2Sky](http://www.javashuo.com/link?url=https://github.com/SkyAPM/go2sky)

​    \1. 建立Reporter、Tracer

​      SkyWalking支持http和gRpc两种方式收集数据，在Go2sky中，想要上报数据，先建立一个GRPCReporter.

​      Tracer表明了本程序中的一条调用链路。

​      ![img](https://ewr1.vultrobjects.com/imgur2/000/005/057/838_35a_a75.png)

​      本程序中的全部span都会与服务名为example的服务相关联。

 

​    \2. 建立Span

​      Span有三种类型：LocalSpan、EntrySpan、ExitSpan。

​      LocalSpan：能够用来表示本程序内的一次调用。

​      EntrySpan：用来从下游服务提取context信息。

​      ExitSpan： 用来向上游服务注入context信息。

​      ![img](https://ewr1.vultrobjects.com/imgur2/000/005/057/839_c9e_076.png)

​      在建立span时，上下文参数传入context.Backround() ，就表示它是root span。

 

​    \3. 建立sub span

​      在建立LocalSpan和EntrySpan的时候，返回值会返回一个context信息(ctx)，经过它来建立sub span，来与root span造成父子关系。

​      ![img](https://ewr1.vultrobjects.com/imgur2/000/005/057/840_211_303.png)

​    \4. End Span

​      必需要确保结束span，它们才能够被上传给skywalking。

​      ![img](https://ewr1.vultrobjects.com/imgur2/000/005/057/841_1cb_56f.png)

 

​    \5. 关联Span

​      咱们在程序中建立的span，是怎么关联起来造成一个调用链的呢。

​      在同一个程序中，向上面那样，建立root span 和 sub span便可。

​      在不一样的程序中，下游服务使用ExitSpan向上游注入context信息，上游服务使用EntrySpan从下游提取context信息。Entry和Exit使得skywalking能够分析，从而生成拓扑图和度量指标。

​      ![img](https://ewr1.vultrobjects.com/imgur2/000/005/057/842_9ef_f85.jpg)

 

4、实战 -- 跨程序追踪RPC调用

​    看到这里，有了基本的概念，以及Go2sky的基本用法，可是仍然不可以对RPC进行有效的追踪。

​    由于上图中的例子使用的是http请求，它自己就封装了Get和Set方法，能够很轻松的注入和提取context信息。可是RPC请求并无，想要追踪别的类型跨程序的调用也没有。

​    因此咱们要本身将context信息在进行调用的时候，从下游服务传给上游服务，而后本身定义注入和提取的方法。

​    下面只贴出了链路追踪部分的代码，其它的好比rpc相关的部分代码省略了(否则又臭又长，还难看)。

  \1. Client端 (下游服务)

​    定义请求信息的结构体：

```
type Req struct {
    A       int
    Header  string        // 添加此字段，用于传递context信息
}
```

​    定义context信息的注入方法：

```
func (p *Req) Set(key, value string) error {
    p.Header = fmt.Sprintf("%s:%s", key, value)
    return nil
}
```

​    建立reporter和tracer：

```
r, err = reporter.NewGRPCReporter("192.168.204.130:11800")
if err != nil {
    logs.Info("[New GRPC Reporter Error]: [%v]", err)
    return
}

// 这个程序中全部的span都会跟服务名叫RTS_Test的服务关联起来
tracer, err = go2sky.NewTracer("RTS_Test", go2sky.WithReporter(r), go2sky.WithInstance("RTS_Test_1"))
if err != nil {
    logs.Info("[New Tracer Error]: [%v]", err)
    return
}
tracer.WaitUntilRegister()
```

​    rpc调用以及建立span：

​    在建立ExitSpan的时候，传入了一个函数，函数实现就是咱们定义的如何注入context信息的函数。

​    它会在CreateExitSpan()函数的内部被调用，header的值不须要咱们管，它在CreateExitSpan函数内部生成的。咱们只须要负责在上游服务中把它提取出来便可。

​    我目前的理解是，只须要在下游服务中负责把这个header按必定规则拼接，传给上游服务，而后在上游服务中按照规则将header解析出来，skywalking经过分析，便可将上下游的span关联起来。

```
func OnSnapshot() {
    // client := GetClinet()
    // 表示收到客户端请求，由于只追踪后台服务之间的链路，因此这里不须要提取context信息
    span2, ctx, err := tracer.CreateEntrySpan(context.Background(), "/API/Snapshot", func() (string, error){
        return "", nil
    })
    if err != nil {
        logs.Info("[Create Exit Span Error]: [%v]", err)
        return
    }
    span2.SetComponent(5200)
	
    // 表示rpc调用的span，这里须要向上游服务注入context信息，即参数中的header
    req := Req{3, ""}
    span1, err := tracer.CreateExitSpan(ctx, "/Service/OnSnapshot", "RTS_Server", func(header string) error{
        return req.Set(propagation.Header, header)
    })
    if err != nil {
        logs.Info("[Create Exit Span Error]: [%v]", err)
        return
    }
    span1.SetComponent(5200)    // Golang程序使用范围是[5000, 6000)，还要在skywalking中配置，config目录下的component-libraries.yml文件

    var res Res
    // rpc调用
    err = conn.Call("Req.Snapshot", req, &res)
    if err != nil {
        logs.Info("[RPC Call Snapshot Error]: [%v]", err)
        return
    } else {
        logs.Info("[RPC Call Snapshot Success]: [%s]", res)
    }

    span1.End()
    span2.End()    // 必定要确保span被结束

    // s1 := ReportedSpan(span1)
    // s2 := ReportedSpan(span2)
    // spans := []go2sky.ReportedSpan{s1, s2}
    // r.Send(spans)
}
```

 

  \2. Server端 (上游服务)

​    定义请求信息的结构体：

```
type ReqBody struct {
    A       int
    Header  string
}
```

​    定义context信息的提取方法：

```
func (p *ReqBody) Get(key string) string {
    subs := strings.Split(p.Header, ":")
    if len(subs) != 2 || subs[0] != key {
	    return ""
    }

    return subs[1]
}
```

​    建立reporter和tracer：

```
r, err = reporter.NewGRPCReporter("192.168.204.130:11800")
if err != nil {
    logs.Info("[New GRPC Reporter Error]: [%v]\n", err)
    return
}

tracer, err = go2sky.NewTracer("Service_Test", go2sky.WithReporter(r), go2sky.WithInstance("Service_Test_1"))
if err != nil {
    logs.Info("[New Tracer Error]: [%v]\n", err)
    return
}
tracer.WaitUntilRegister()
```

​    建立span：

​    在建立EntrySpan时，调用Get()方法提取context信息

```
func (p *Req)Snapshot(req ReqBody, res *Res) error {
    // 表示收到 rpc 客户端的请求，这里须要提取context信息
    span1, ctx, err := tracer.CreateEntrySpan(context.Background(), "/Service/OnSnapshot/QueringSnapshot", func() (string, error){
	return req.Get(propagation.Header), nil
    })
    if err != nil {
	    logs.Info("[Create Exit Span Error]: [%v]\n", err)
	    return err
    }
    span1.SetComponent(5200)
    // span1.SetPeer("Service_Test")

    // 表示去请求了一次数据库
    span2, err := tracer.CreateExitSpan(ctx, "/database/QuerySnapshot", "APIService", func(header string) error {
	    return nil
    })
    span2.SetComponent(5200)

    time.Sleep(time.Millisecond * 6)
    *res = "Return Snapshot Info"

    span2.End()
    span1.End()

    // s1 := ReportedSpan(span1)
    // s2 := ReportedSpan(span2)
    // spans := []go2sky.ReportedSpan{s1, s2}
    // r.Send(spans)

    return nil
}
```

 

  \3. 结果展现 

​    链路追踪：

​    ![img](https://ewr1.vultrobjects.com/imgur2/000/005/057/843_52f_0f0.jpg)

​     拓扑图：

​    ![img](https://ewr1.vultrobjects.com/imgur2/000/005/057/844_4fc_ca2.jpg)





```
package main

import (
"flag"
   "github.com/SkyAPM/go2sky/reporter"
   "io/ioutil"
   "log"
   "net/http"
   "time"

   "github.com/SkyAPM/go2sky"
   httpPlugin "github.com/SkyAPM/go2sky/plugins/http"
)

var (
   grpc        bool
   oapServer   string
   upstreamURL string
   listenAddr  string
   serviceName string

   client *http.Client
)

func init() {
flag.BoolVar(&grpc, "grpc", false, "use grpc reporter")
flag.StringVar(&oapServer, "oap-server", "169.254.0.143:11800", "oap server address")  
//169.254.0.143:11800 需替换为 TSW 的私网接入点
flag.StringVar(&upstreamURL, "upstream-url", "upstream-service", "upstream service url")
flag.StringVar(&listenAddr, "listen-addr", ":8081", "listen address")
flag.StringVar(&serviceName, "service-name", "go2sky-server", "service name")
}

func ServerHTTP(writer http.ResponseWriter, request *http.Request) {
time.Sleep(time.Duration(500) * time.Millisecond)

   clientReq, err := http.NewRequest(http.MethodPost, upstreamURL, nil)
if err != nil {
      writer.WriteHeader(http.StatusInternalServerError)
log.Printf("unable to create http request error: %v \n", err)
return
   }
   clientReq = clientReq.WithContext(request.Context())
   res, err := client.Do(clientReq)
if err != nil {
      writer.WriteHeader(http.StatusInternalServerError)
log.Printf("unable to do http request error: %v \n", err)
return
   }
defer res.Body.Close()
   body, err := ioutil.ReadAll(res.Body)
if err != nil {
      writer.WriteHeader(http.StatusInternalServerError)
log.Printf("read http response error: %v \n", err)
return
   }
   writer.WriteHeader(res.StatusCode)
   _, _ = writer.Write(body)
}

func main() {
flag.Parse()

var report go2sky.Reporter
   var err error

   report, err = reporter.NewGRPCReporter(
                        oapServer,
                        reporter.WithAuthentication("tsw_site@xxxxxxxxxxxxxxxxxxxxxxxx")) 
                        //tsw_site@xxxxxxxxxxxxxxxxxxxxxxxx 需替换成您的 Token
//report, err = reporter.NewLogReporter()

   if err != nil {
log.Fatalf("crate grpc reporter error: %v \n", err)
   }

   tracer, err := go2sky.NewTracer(serviceName, go2sky.WithReporter(report))
if err != nil {
log.Fatalf("crate tracer error: %v \n", err)
   }

   client, err = httpPlugin.NewClient(tracer)
if err != nil {
log.Fatalf("create client error %v \n", err)
   }

   route := http.NewServeMux()
   route.HandleFunc("/mack", ServerHTTP)

   sm, err := httpPlugin.NewServerMiddleware(tracer)
if err != nil {
log.Fatalf("create client error %v \n", err)
   }
   err = http.ListenAndServe(listenAddr, sm(route))
if err != nil {
log.Fatal(err)
   }
}
```

