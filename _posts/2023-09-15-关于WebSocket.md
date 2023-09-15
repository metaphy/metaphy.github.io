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

**较低的延迟**：WebSocket通过建立持久连接，避免了每次请求都需要重新建立连接的开销，从而减少了通信的延迟。

**更高的性能**：由于WebSocket减少了HTTP头的传输，减少了通信的数据量，使得数据传输更加高效。

**与HTTP兼容**：WebSocket使用HTTP协议进行握手，握手成功后会升级协议，转换为WebSocket协议。因此，WebSocket可以与现有的基于HTTP的应用和基础设施兼容。
WebSocket常用于实时聊天、在线游戏、股票行情等需要实时数据传输的场景。

------------
下文使用Node.js来演示WebSocket的使用




{% highlight javascript %} 
{% endhighlight %}
