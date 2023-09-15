---
layout: post
title: "关于WebSocket"
date: 2023-09-15 15:10:00 +0800
categories: javascript
--- 

WebSocket是一种在单个TCP连接上进行全双工通信的网络协议。它提供了一个持久的连接，允许服务器主动向客户端推送数据，并且可以支持双向通信，使得客户端和服务器之间可以实时地进行数据交换。

WebSocket协议通过在 HTTP 握手请求中使用特殊的头部信息来进行握手。一旦握手成功，连接就建立起来了，服务器可以主动向客户端发送消息。WebSocket协议的详细内容可以查阅RFC6455:  https://datatracker.ietf.org/doc/html/rfc6455

相比于传统的基于HTTP的请求-响应模式，WebSocket具有以下特点：

**实时性**：WebSocket能够在客户端和服务器之间进行实时的双向数据传输，实现了真正的实时通信。

**高效性**：WebSocket通过建立持久连接，避免了每次请求都需要重新建立连接的开销，减少了HTTP头的传输，减少了通信的数据量，从而减少了通信的延迟。

**与HTTP兼容**：WebSocket使用HTTP协议进行握手，握手成功后会升级协议，转换为WebSocket协议。因此，WebSocket可以与现有的基于HTTP的应用和基础设施兼容。
WebSocket常用于实时聊天、在线游戏、股票行情等需要实时数据传输的场景。

------------
下文使用Node.js来演示WebSocket的使用，譬如客户端想画一条实时更新的关于某件商品的成交额曲线，那么服务器以一定频率向客户端推送该商品成交额的信息。

首先创建项目文件夹，并使用npm初始化（npm init时，使用默认选项就好）:
```
cd WebSocketDealAmountDemoServer
npm init
```

我们还需要引入WebSocket lib 'ws'，使用npm安装，--save 表示这个库会添加到package.json打包文件中：
```
npm install ws --save
```

我们使用deals.json作为数据源，这个文件的内容附在最后面；我们最后还要使用一个HTML5页面来作为client去测试它。目前的文件结构如下：

```
  node_modules
  deals.json
  index.js
  package-lock.json
  package.json
  test-client.html
```


