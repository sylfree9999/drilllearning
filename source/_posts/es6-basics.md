---
title: ES6 基础知识
date: 2019-04-09 12:48:23
tags: [es6]
---

## `let`  vs.  `var`

先来看一个`var`的典型错误，主要原因是`var`没有块级作用域

```javascript
window.onload = function(){
    var aBtn = document.getElementByTagName('input');
    
    for(var i=0; i<aBtn.length; i++){
        aBtn[i].onclick = function(){
            alert(i);
        }
    }
}
//下面有四个<input>button
```

如果是用`var`来声明`i`，由于没有块级作用域，所以每次循环不会新建一个`i`，用的都是老的`i`，所以不管哪个button，**alert的全都是4**

要修改这个问题，可以声明`i`的时候用`let`，因为`let`是有块级作用域的，在`for`循环就是一个块级作用域，所以每循环一次会新建一个`i`

<!--more-->

## 解构赋值

```javascript
let {a,b,c} = {a:12,b:5,c:7};
let [a,b,c] = [12,5,8];
console.log(a,b,c);

let {a,b,c} = {12,5,8};//这个就会报错，右边必须要写全，如果是json
let {a,b,c} = {d:5,e:8,f:0}; //这个也会报错，因为右边没有a,b,c
```

## 箭头函数

本质上就是一个简写

```	javascript
function(para){
    
}

//等同于
(para)=>{}

//如果有且仅有一个参数，()可省略，如果有且仅有一条语句且这个语句为return，{}也可以省略
let sum = (a,b)=>a+b;
```

箭头函数另一个重要的功能就是修复了**this**

先来看一下`this`的问题，在别的语言里面`this`指向的是当前对象，但在JS里面会变。如果用箭头函数的话，这个`this`会牢牢绑定在当前的环境之下

```javascript
let json = {
    a:5,
    b:7,
    show:function(){
        alert(this.a+this.b);
    }
}
//json.show(); //这个时候能够正确弹出12

document.onclick = json.show; //但是这个时候却弹出的是NaN，因为这个时候你把json把绑到了document上面，this指向了document而不是json了！！
```

如果这个时候你把`json	`里面的`show`函数改成了箭头函数，<p style="color:red">则这个时候会指向`window`,因为`json`就是声明在全局里面的，这个时候全局是`window`,这个时候其实要用`class`才能把`this`绑定在`json`上面</p>

## 系统对象

- Array

  - `map` 映射， 1对1，每个元素都变个样子

  - ```javascript
    let arr = [100,78,89,45,80];
    let res = arr.map(function(item,index){
        if(item>=60){
            return 'Pass';
        }else{
            return 'Fail';
        }
    });
    ```

    

  - `reduce` 减少,多对一，多个进去，出来一个

  - ```javascript
    let arr = [34,234,56,123,76];
    //tmp是两个数相加的结果，第一个tmp的值为第一个数，即34
    arr.reduce(function(tmp,item,index){
        return tmp+item; //第一次tmp=34,item=234;第二次tmp=34+234,item=56
    });
    
    //求平均数
    arr.reduce(function(tmp,item,index){
        if(index < arr.length - 1){
            return tmp+item;
        }else{
            return (tmp+item)/arr.length;
        }
    })
    ```

    

  - `forEach` 遍历， 循环一遍，与`for`循环一样

  - ```javascript
    let arr = [12,78,455,80];
    arr.forEach((item,index)=>{
        alert('第'+index+'个是'+item);
        alert(`第${index}个是{item}`);//也可以写成这种string拼接的形式
    })
    ```

  - `filter` 过滤

  - ```javascript
    let arr = [12,67,8,3,4,78];
    arr.filter(item=>item%2==0).filter(item=>item>=8);
    ```

## 异步操作

- `promise`, 对异步操作进行了一个封装

- ```javascript
  let p = new Promise(function(resolve,reject){
      $.ajax({
          url:'1.json',
          dataType:'json',
          success(data){
              resolve(data);
          },
          error(res){
              reject(res);
          }
      })
  });
  
  p.then(function(data){
      alert(data);
  },function(res){
      alert(res);
  }); //function(data){}其实就是resolve,function(res){}就是reject
  ```

  `promise`可以有`all`操作，只有里面的东西都完成了才能到`then`, `all`里面的执行是并行的，**只要有一个有错，就全错**

  ```javascript
  Promise.all([
     $.ajax({url:'1.json', dataType:'json'}), 
     $.ajax({url:'2.json', dataType:'json'}),
     $.ajax({url:'3.json', dataType:'json'}),
  ]).then([data1,data2,data3]=>{ //解构赋值可以直接放在参数里面
      console.log(data1,data2,data3);
  },res=>{
      alert("Fail");
  })
  ```

  如果第二个异步请求需要用到第一个异步请求的结果呢？用`async/await`

## `async`/`await`

`await`后面跟的是一个`promise`, 注意，这里只是方便了书写，但内部编译后还会是异步的 ,<p style="color:red">用`async`和`await`可以解决需要等待上一个异步操作结果的情况</p>

```javascript
async function show(){
    let data1 = await $.ajax({url:'1.json',dataType:'json'});
    if(data1.a < 10){
        let data2 = await $.ajax({url:'2.json',dataType:'json'});
        alert(data2);
    }else{
        let data3 = await $.ajax({url:'3.json',dataType:'json'});
        alert(data3);
    }
    console.log(data1, data2, data3);
} //写的样子像是同步的，但其实内部编译后还是异步的
```

## ES6兼容性解决-babel

- 安装`nodejs`

- 安装`babel`

- ```shell
  npm init -y //生成package.json项目文件
  npm i @babel/core @babel/cli @babel/preset-env -D
  ```

- 修改`package.json`中的`scripts`

- ```json
  {
    "name": "Frontend",
    "version": "1.0.0",
    "description": "",
    "main": "index.js",
    "scripts": {
      "build": "babel src -d dest"
    }, //用babel 编译src目录下的文件，到dest目标文件夹中
    "keywords": [],
    "author": "",
    "license": "ISC"
  }
  ```

- 建立预设环境`.babelrc`，比方说默认编译成什么版本

- ```json
  {
      "presets":["@babel/preset-env"]
  }
  ```

- 运行脚本

- ```shell
  npm run build
  ```

## 面向对象

class对象

```javascript
class Person{
    constructor(name,age){
        this.name = name;
        this.age = age;
    }
    
    show(){
        alert(this.name);
        alert(this.age);
    }
}
let p = new Person('hi',28);
p.show();
```

继承

```javascript
class Worker extends Person{
    constructor(name,age,job){
        super(name,age);
        this.job = job;
    }
    
    showJob(){
        alert(this.job);
    }
}

let w = new Worker('ho',23,'farmer');
w.show();
w.showJob();
```

## 闭包=留着别删

每调用一个函数，就会为这个函数分配一个空间，这个空间就是栈。一般函数执行完了以后，这个空间就需要回收，但是闭包可以做到不让这个栈被回收。闭包底层是栈，其把整个函数封装到一个对象里面，这个对象就是栈，所以可以保存这个对象。

```javascript
function show(){
    let a = 19;
    document.onclick = function(){
        alert(a);
    }
}
show();//按理来说，这个a在执行外show以后需要被回收，但是document.onclick一直在用这个a，所以a就不会被回收
```

## ES6模块化-webpack

<em>mod1.js</em>

```javascript
//声明模块,需要输出什么就要export什么
export let a = 12;
```

<em>index.js</em>

```javascript
//引用模块
import * as mod1 from './mod1'; //当前目录要加./
alert(mod1.a);
```

- 安装webpack

- ```shell
  npm i webpack -g
  ```

- 配置`webpack.config.js`

- ```javascript
  const path =  require('path');
  //node的模块化
  module.exports={
      mode: 'production',
      entry: './index.js', //nodejs里面同级目录必须要加./
      output: { //output必须是个object
          path: path.resolve(__dirname,'build'), //必须是绝对路径
          filename: 'bundle.js'
      }
  };
  ```

- Build `webpack`

- ```shell
  webpack
  ```

### Export/Import

- export
  - `export let a=12;`
  - `export const a  = xx;`
  - `export {a,b,c};`
  - `export function xxx(){};`
  - `export class XXX{};`
  - `export default xx;` 导出默认成员
- import
  - `import * as mod from "./xxx";`
  - `import {a,b,c} from "./xxx";`
  - `import xxx from "./mod";` 模块里面没有xxx,这个时候引入的其实就是export default默认成员
  - `import "./1.css"; import "./1.jpg";` 只是引入模块的代码，不引入内部成员，要配合`webpack loader`用
  - `let promise = import("./mod1");` 异步引用