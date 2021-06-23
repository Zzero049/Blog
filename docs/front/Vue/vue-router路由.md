# vue-router路由

学习的时候，尽量的打开官方的文档 https://router.vuejs.org/zh/

Vue router是vue.js官方的路由管理器。它和 Vue.js的核心深度集成，让构建单页面应用变得易如反掌。包含的功能有

- 嵌套的路由/视图表
- 模块化的、基于组件的路由配置
- 路由参数、查询、通配符
- 基于uejs过渡系统的视图过渡效果
- 细粒度的导航控制
- 带有自动激活的 CSS class的链接
- HTML5历史模式或hash模式，在|E9中自动降级
- 自定义的滚动条行为

## 安装

基于第一个vue-cli进行测试学习先查看 node modules中是否存在vue-router 

vue-router是一个插件包，所以我们还是需要用npm/cnpm来进行安装的。打开命令行工具，进入你的项目目录，输入下面命令。

```shell
npm install vue-router --save --only=dev
```



## 第一个路由Demo

1、创建两个Vue Component文件，做跳转页面

```vue
<template>
  <h1>内容页</h1>
</template>

<script>
    export default {
        name: "Content1"
    }
</script>

<style scoped>

</style>
```

```vue
<template>
    <h1>首页</h1>
</template>

<script>
    export default {
        name: "Main"
    }
</script>

<style scoped>

</style>

```

2、创建路由配置（也是js文件），如果命名为index，则只需要扫描包，自动识别

```js
import Vue from 'vue'
import VueRouter from 'vue-router'
import Content1 from "../components/Content1";
import Main from "../components/Main";

// 安装路由
Vue.use(VueRouter);

// 配置导出路由

export default new VueRouter({	//导入的VueRouter
  routes: [
    {
      // 路由路径
      path: '/content',
      name: 'content',
      // 跳转的组件
      component: Content1
    },
    {
      // 路由路径
      path: '/main',
      name: 'main',
      // 跳转的组件
      component: Main
    }
  ]
});

```

3、 再在main.js声明使用配置的路由

```js

import Vue from 'vue'
import App from './App'

import router from './router'   // 自动扫描里面的路由配置，注意名字必须叫router


Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  //配置路由
  router,
  components: { App },
  template: '<App/>'
});

```

4、在主页App.vue配置跳转页面 router-link相当于a标签，to标签相当于href

```vue
<template>
  <div id="app">
    <h1>Vue-Router</h1>
<!--    控制路由-->
    <router-link to="/main">首页</router-link>
    <router-link to="/content">内容页</router-link>
<!--    控制展示-->
    <router-view></router-view>
  </div>
</template>

<script>
import Content1 from "./components/Content1";

export default {
  name: 'App',
  components: {
    Content1
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

```

![image-20200527115411725](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200527115411725.png)

## router-link和a标签区别

### a标签

**点击a标签从当前页面跳转到另一个页面**
通过a标签跳转，页面就会重新加载，相当于重新打开了一个网页

### router-link

**通过router-link进行跳转不会跳转到新的页面**，不会重新渲染，它会选择路由所指的组件进行渲染

通过a标签和router-link对比，router-link避免了重复渲染，不像a标签一样需要重新渲染减少了DOM性能的损耗



## vue-router和express-router

一个是前端路由 一个是后端路由

前端路由的意思就是 http://example.com/home, 当这个链接出现在浏览器中时，其实并没有真正发送请求到服务器。而是前端路由自己处理了这个路径(hash 事件，history 事件), vue-router 找到注册的组件，然后渲染到页面中

而后端路由就是真正请求到后端服务器的 [http://example.com/api/list](https://link.zhihu.com/?target=http%3A//example.com/api/list) 比如这个路径就会通过 ajax 的方式请求后台服务，后端根据在路由中注册的控制器处理掉这条请求

在前后端分离的项目中，前端路由一般体现在 URL 链接在浏览器中的跳转，后端路由则是通过 ajax 这些方式请求服务获取数据。

## 前端路由hash模式和history模式

对于vue这类渐进式前端开发框架，为了构建 SPA（单页面应用），需要引入前端路由系统，这也就是 Vue-Router 存在的意义。前端路由的核心，就在于 —— 改变视图的同时不会向后端发出请求。

**为了达到这一目的，浏览器当前提供了以下两种支持：**

- hash —— 即地址栏 URL 中的 # 符号（此 hash 不是密码学里的散列运算）。比如这个 URL：http://www.abc.com/#/hello，hash 的值为 #/hello。它的特点在于：hash 虽然出现在 URL 中，但**不会被包括在 HTTP 请求中**，对后端完全没有影响，因此改变 hash 不会重新加载页面。由于 **hash 值变化不会导致浏览器向服务器发出请求**，而且 hash 改变会触发 hashchange 事件（hashchange只能改变 # 后面的url片段）；更关键的一点是，因为hash发生变化的url都会被浏览器记录下来，从而你会发现浏览器的前进后退都可以用了，所以人们在 html5 的 history 出现前，基本都是使用 hash 来实现前端路由的。简单的说，**当#后的 URL 改变时，页面不会重新加载，也不会往服务器发送请求**
  

- history —— 在url中不带#号，用的是传统的路由分发模式，即当用户输入一个url时，是由服务器在接受用户的这个输入请求，并由服务器解析url的路径然后做相应逻辑处理。如果要做到**改变url但又不刷新页面**的潮流效果，就需要**前端用上pushState和replaceState两个H5的api**，这两个方法应用于浏览器的历史记录栈，在当前已有的 `back`、`forward`、`go` 的基础之上，它们提供了对历史记录进行修改的功能。只是当它们执行修改时，虽然**改变了当前的 URL，但浏览器不会立即向后端发送请求**。需要后端人员去配置**url重定向**的问题，**不然在访问二级页面时，做刷新操作会报404的错误**。

- 因此可以说，hash 模式和 history 模式都属于浏览器自身的特性，Vue-Router 只是利用了这两个特性（通过调用浏览器提供的接口）来实现前端路由.

  ### 

  **history的问题**

  1：hash 模式下，仅hash符号之前的内容会被包含在请求中，如`http://www.abc.com`,因此对于后端来说，即使没有做到对路由的全覆盖，也不会返回404错误。
  2：history模式下，前端的URL必须和实际向后端发起请求的URL一致。如`htttp://www.abc.com/book/id`。如果后端缺少对/book/id 的路由处理，将返回404错误、

  通过history api，我们丢掉了丑陋的#；但是，它也有个问题：不怕前进，不怕后退，**就怕刷新，f5**（如果后端没有准备的话，会分分钟刷出一个**404**来*）*,因为刷新是实实在在地去请求服务器的,不玩虚的。

  

vue默认是hash模式，可以通过mode修改

```
export default new VueRouter({
	mode: 'history',
	routes:[
	
	]
});
```



## 嵌套路由 

本节为Vue+ElementUI实战后的内容，在Main.vue 加入了一个导航栏

嵌套路由又称子路由，在实际应用中，通常由多层嵌套的组件组合而成。同样地，URL中各段动态路径也按某种结构对应嵌套的各层组件，例如

![image-20200527162001508](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200527162001508.png)



在路由配置的index.js中配置children，可以实现不改变main页面的内容，点击router-link后显示Profile或List的内容

```js
{
  // 路由路径
  path: '/main',
  name: 'main',
  // 跳转的组件
  component: Main,
  //嵌套路由
  children:[
    {
      path: '/user/Profile',
      component: Profile
    },
    {
      path: '/user/List',
      component: List
    }
  ]
}
```

![image-20200527165909411](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200527165909411.png)

## 动态路由

 就是路由url是restful风格，可以在指定url里面再接收一个参数，注意需要绑定

```vue
<router-link v-bind:to="{name: 'profile', params: {id:1}}">个人信息</router-link>
<router-link v-bind:to="{name:'list',params:{id:2}}">列表信息</router-link>

```

路由修改，原有路径下加上:id

```js
children:[
      {
        path: '/user/Profile/:id',
        name: 'profile',
        component: Profile
      },
      {
        path: '/user/List/:id',
        name: 'list',
        component: List
      }
    ]
```

展示传入的id,注意要放到标签内，否则报错

```vue
{{$route.params.id}}
```

![image-20200527173438982](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200527173438982.png)

也可以用props进行解耦

```vue
<template>
  <div>
    <h1>列表</h1>
    {{id}}
  </div>

</template>

<script>
    export default {
      props: ['id'],
        name: "List"
    }
</script>

```

### 重定向

重定向用redirect即可

```js
children:[
      {
        path: '/user/Profile/:id',
        name: 'profile',
        component: Profile,
        props: true
      },
      {
        path: '/user/List/:id',
        name: 'list',
        component: List,
        props: true				// 允许传递参数
      },
      {
        path: '/home',
        redirect: '/main'		// 点击home，重定向回main
      }
    ]
```

### 传递参数

1、登录页面login.vue修改，携带输入的用户名

```vue
this.$router.push("/main/"+this.ruleForm.account);
```

2、路由页面修改

```js
{
    // 路由路径
    path: '/main/:name',	// 取到的参数叫name
    name: 'main',
    props: true,			// 允许传递
    // 跳转的组件
    component: Main,
    //嵌套路由
    children:[
      {
        path: '/user/Profile/:id',
        name: 'profile',
        component: Profile,
        props: true		
      },
      {
        path: '/user/List/:id',
        name: 'list',
        component: List,
        props: true
      },
      {
        path: '/home',
        redirect: '/main'
      }
    ]
  }
```

3、前端页面展示

```vue
<template>
<div>
{{name}}    
</div>
</template>

<script>
  export default {
    props: ['name'],		// 取到name
    methods: {
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>
```

### 404页面

在路由最后加上一个通配所有路径的即可

```js
import Vue from 'vue'
import VueRouter from 'vue-router'
import login from "../view/login";
import Main from "../view/Main";
import List from "../view/user/List";
import Profile from "../view/user/Profile";
import NotFound from "../view/user/NotFound";
Vue.use(VueRouter);

export default new VueRouter({
  mode: 'history',
  routes:[{
    // 路由路径
    path: '/login',
    name: 'login',
    // 跳转的组件
    component: login,

  },{
    // 路由路径
    path: '/main/:name',
    name: 'main',
    props: true,
    // 跳转的组件
    component: Main,
    //嵌套路由
    children:[
      {
        path: '/user/Profile/:id',
        name: 'profile',
        component: Profile,
        props: true
      },
      {
        path: '/user/List/:id',
        name: 'list',
        component: List,
        props: true
      },
      {
        path: '/home',
        redirect: '/main'
      }
    ]
  },{
    path: '*',
    component: NotFound
  }
  ]
})

```





## 路由钩子

类似Spring的AOP，我们在进入路由和退出路由之前，可以进行一系列操作，通过`beforeRouteEnter: (to, from, next)=>{}`和`beforeRouteLeave: (to,from, next)=>{}`，注意执行过后必须执行next方法，类似拦截器的链。

```vue
<template>
  <div>
    <h1>个人信息</h1>
    {{id}}
  </div>


</template>

<script>
    export default {
      props: ['id'],
      name: "Profile",
      beforeRouteEnter: (to, from, next)=>{
        console.log("进入路由之前");
        next();
      },
      beforeRouteLeave: (to,from, next)=>{
        console.log("进入路由之后");
        next();
      }
    }
</script>

<style scoped>

</style>

```

参数信息

- to：路由将要跳转的路径信息

- from：路径跳转前的路径信息
- next：路由的控制参数next（）跳入下一个页面
- next('/path')：改变路由的跳转方向，使其跳到另一个路由
- next(false) ：返回原来的页面
- next((vm)=>{}) ：    仅在 beforeRouteEnter中可用，vm是组件实例



### 路由钩子完成异步请求

1、安装axios

```shell
cnpm install axios
cnpm install --save vue-axis
```

2、根据官网提示，配置main.js

```js
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)
```

3、在路由钩子方法内部，使用next((vm)=>{}) 可以操作vm对象，执行想要实现的方法

```vue
<template>
  <div>
    <h1>个人信息</h1>
    {{id}}
  </div>


</template>

<script>
    export default {
      props: ['id'],
      name: "Profile",
      beforeRouteEnter: (to, from, next)=>{
        console.log("进入路由之前");
        next(vm => {
          vm.getData(); // 进入路由之前，执行改方法
        });
      },
      beforeRouteLeave: (to,from, next)=>{
        console.log("进入路由之后");
        next();
      },

      methods:{
        getData: function () { // 随便取一个数据
            this.axios.get('http://localhost:8080/static/mock/data.json')
                      .then(function (response) {
                            console.log(response.data)
                      });
        }
      }
    }
</script>

<style scoped>

</style>

```

