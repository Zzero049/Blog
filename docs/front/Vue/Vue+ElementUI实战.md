# Vue+ElementUI

1、创建工程，创建一个名为hello-vue的工程

```shell
vue init webpack hello-vue
```

2、安装依赖，我们需要安装vue-router、element-ui、sass-loader和node-sass四个插件

```shell
# 进入工程目录
cd he11o-vue 
# 安装vue-router
npm install vue-router --save --only=dev
# 安装e1ement-ui 
npm i element-ui -S
# 安装依赖
npm install
# 安装SASS加载器
cnpm install sass-loader node-sass --save --only=dev
# 启动测试
npm run dev
```

**Npm命令解释**

- `npm install moduleName`：安装模块到项目目录下
- `npm insta11 -g moduleName`:-g的意思是将模块安装到全局，具体安装到磁盘哪个位置要看 npm config prefix的位置
- `npm install -save moduleName:`-save的意思是将模块安装到项目目录下，并在package文件的 dependencies节点写入依赖，-S为该命令的缩写
- `npm insta1l-save --only=dev moduleName`:--save --only=dev的意思是将模块安装到项目目录下，并在 package文件的 dev Dependencies节点写入依赖，-D为该命令的缩写



3、创建一个login.vue页面，并在官网上找到一个想要展示的内容，修改`<template>`和`<script>`的内容，输入账号密码不为空后，跳转到Main.vue

```vue
<template>
  <div class="login-box">

    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
      <h3 class="login-title">欢迎登录</h3>
      <el-form-item label="账号" prop="account">
        <el-input type="text" placeholder="请输入帐号" v-model="ruleForm.account" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="pass">
        <el-input type="password" placeholder="请输入密码" v-model="ruleForm.pass" autocomplete="off"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
        <el-button @click="resetForm('ruleForm')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>

</template>

<script>
  export default {
    data() {
      var validateAccount = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入帐号'));
        }else{
          callback();
        }
      };
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        }else{
          callback();
        }
      };

      return {
        ruleForm: {
          account: '',
          pass: '',

        },
        rules: {
          pass: [
            { validator: validatePass, trigger: 'blur' }
          ],
          account: [
            { validator: validateAccount, trigger: 'blur' }
          ]
        },


      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$router.push("/main");
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      }
    }
  }
</script>

<style>
  .login-box{
    border: 1px solid #DCDFE6;
    width: 350px;
    margin: 100px auto;
    padding: 35px 35px 15px 35px;

  }
</style>

```

4、创建路由配置index.js，并在主页的App.vue配置跳转

```js
// index.js
import Vue from 'vue'
import VueRouter from 'vue-router'
import login from "../view/login";
import Main from "../view/Main";
Vue.use(VueRouter);

export default new VueRouter({
  routes:[{
    // 路由路径
    path: '/login',
    name: 'login',
    // 跳转的组件
    component: login
  },{
    // 路由路径
    path: '/main',
    name: 'main',
    // 跳转的组件
    component: Main
  }
  ]
})

```

```vue
<!--App.vue-->
<template>
  <div id="app">
    <!--    控制路由-->
    <router-link to="/login"></router-link>

    <!--    控制展示-->
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'App',
}
</script>
```

5、按照elementUi官网上入门，配置main.js，导入和使用ElementUI

```js
import Vue from 'vue';
import App from './App';
// 使用路由
import router from './router';

//导入elementUI
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
// 使用elementUI
Vue.use(router);
Vue.use(ElementUI);


/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App),
  router
});


```

![image-20200527155554669](https://gitee.com/zero049/MyNoteImages/raw/master/image-20200527155554669.png)