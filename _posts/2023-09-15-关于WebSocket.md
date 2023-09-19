---
layout: post
title: "关于WebSocket"
date: 2023-09-15 15:10:00 +0800
categories: javascript
--- 

WebSocket是一种在单个TCP连接上进行全双工通信的网络协议。它提供了一个持久的连接，允许服务器主动向客户端推送数据，并且可以支持双向通信，使得客户端和服务器之间可以实时地进行数据交换。

WebSocket协议通过在 HTTP 握手请求中使用特殊的头部信息来进行握手。一旦握手成功，连接就建立起来了，服务器可以主动向客户端发送消息。WebSocket协议的详细内容可以查阅 [RFC6455](https://datatracker.ietf.org/doc/html/rfc6455)

相比于传统的基于HTTP的请求-响应模式，WebSocket具有以下特点：

**实时性**：WebSocket能够在客户端和服务器之间进行实时的双向数据传输，实现了真正的实时通信。

**高效性**：WebSocket通过建立持久连接，避免了每次请求都需要重新建立连接的开销，减少了HTTP头的传输，减少了通信的数据量，从而减少了通信的延迟。

**与HTTP兼容**：WebSocket使用HTTP协议进行握手，握手成功后会升级协议，转换为WebSocket协议。因此，WebSocket可以与现有的基于HTTP的应用和基础设施兼容。
WebSocket常用于实时聊天、在线游戏、股票行情等需要实时数据传输的场景。


**下文使用Node.js来演示WebSocket的使用，例子是服务器以一定频率向客户端推送某种商品成交额的信息。**

首先创建项目文件夹，并使用npm初始化（npm init时，使用默认选项就好）:
```
cd WebSocketDealAmountDemoServer
npm init
```

我们还需要引入WebSocket lib 'ws'，使用npm安装，--save 表示这个库会添加到package.json打包文件中：
```
npm install ws --save
```

我们使用deals.json作为数据源，还要使用一个HTML5页面来作为client去测试它。项目的文件结构如下：

```
WebSocketDealAmountDemoServer
  node_modules
    ws
  deals.json
  index.js
  package-lock.json
  package.json
  test-client.html
```

着重分析一下作为服务器程序的index.js. 引入和初始化WebSocketServer之后，该server自动监控connection事件，connection的响应可以非常简单，譬如：

```
const WebSocketServer = require('ws').Server
const wss = new WebSocketServer({port: 8080})

wss.on('connection', (ws) => {
  ws.send('Hello, world!')
})
```

在建立连接后，除了初始的'Hello, world'，还可以监听message事件，响应Client发过来的信息：
```
wss.on('connection', (ws) => {
  ws.send(getConnectedEvent())
 
  ws.on('message', (message) => {
    console.log('Received the message from client: ' + message)
  })
})
```

最终，我们使用setInterval以一定频率，比如每5秒一次向client 发送消息，并且在connection关闭时，清理这个interval:
```
ws.dealUpdateInterval = setInterval(() => {
  if (connectionInfo.productsToMonitor.length > 0) {
    ws.send(getDealsUpdateEvent(connectionInfo))
    connectionInfo.productsUpdateCount += 1
  }
}, 5000)

ws.on('close', () => {
  clearInterval(ws.dealUpdateInterval)
})
```

为了确保在网络出问题时，server端不会长时间持有这个连接，server端使用定期ping 客户端的方式，在多次ping而无响应时，server将会关闭这个connection，下面的演示只是一次ping不通就断开的情况：
```
ws.pingInterval = setInterval(() =>{
  if(connectionInfo.isActive) {
    //set it to false, once ping get a pong, set it back to true
    connectionInfo.isActive = false
    ws.ping() 
  } else {
    disconnect(ws, 'connection inactive: Ping without Pong')
  }
}, 17000)

ws.connectionTimeout = setTimeout(() => {
  disconnect(ws, 'Automatically disconnected after some time')
}, 300000)
```

That's it! 这个就是server部分的核心代码了。client端使用一个HTML5页面，code非常简单，比当年手写Ajax要简单，所以不再解释。值的注意的是，在测试前，我们需要先检查浏览器是否支持WebSocket对象，好在目前新版本的Chrome, Firefox, Edge 均支持：
```
if(!window.WebSocket) {   
  console.log('WebSocket is NOT supported!')   
}
```

为了更清晰的打印带有timestamp的log，使用下面debug函数代替console.log
```
function debug(info) {
  console.log(new Date().toISOString() + ': ' + info)
}
```

然后我们设计整个测试流程。首先启动server:
```
node index
```
然后在浏览器中打开test-client.html, 并打开console. 

第0秒：客户端连接服务器，连接成功后收到服务器返回的'connected'信息；之后，服务器会以5秒的频率发送商品的交易额信息

第1秒: 客户端发送subscribe event ["WLQ","QDLHT"]，服务器将发送指定的商品的交易信息

第5秒：服务器发回["WLQ","QDLHT"] 的交易信息

第10秒：服务器发回["WLQ","QDLHT"] 的交易信息

第12秒：客户端发送unsubscribe event ["WLQ"]

第15秒：服务器发回["QDLHT"] 的交易信息

第20秒：服务器发回["QDLHT"] 的交易信息

第25秒：服务器发回["QDLHT"] 的交易信息

第30秒：服务器主动断开连接，客户端显示close信息：Server disconnected! Bye~~

整个log显示出的相应信息，与我们的测试设计完全符合：
```
2023-09-16T04:01:00.373Z: WebSocket object is created
2023-09-16T04:01:00.385Z: ****Connection Successfully****
2023-09-16T04:01:00.387Z: Received: {"event":"connected","products":["WLQ","QDLHT"],"message":"Connected to the server"}
2023-09-16T04:01:01.381Z: Send data to Server: {"event":"subscribe","products":["WLQ","QDLHT"]}
2023-09-16T04:01:05.409Z: Received: {"event":"deal-update","deals":{"WLQ":120,"QDLHT":556}}
2023-09-16T04:01:10.412Z: Received: {"event":"deal-update","deals":{"WLQ":186.3,"QDLHT":532.82}}
2023-09-16T04:01:12.382Z: Send data to Server: {"event":"unsubscribe","products":["WLQ"]}
2023-09-16T04:01:15.426Z: Received: {"event":"deal-update","deals":{"QDLHT":480.29}}
2023-09-16T04:01:20.427Z: Received: {"event":"deal-update","deals":{"QDLHT":462.99}}
2023-09-16T04:01:25.430Z: Received: {"event":"deal-update","deals":{"QDLHT":417.63}}
2023-09-16T04:01:30.400Z: Server disconnected! Bye~~
```

最后代码附下，需要注意的是为了保持代码简洁，必要的输入信息检测和错误处理都省略了，实际开发中不能省。

deals.json
```
[
    {
        "productId": "WLQ",
        "productName": "握力器",
        "dealsData": [
            {
                "minute": 0,
                "price": 120
            },
            {
                "minute": 1,
                "price": 186.3
            },
            {
                "minute": 2,
                "price": 283.5
            },
            {
                "minute": 3,
                "price": 560.1
            },
            {
                "minute": 4,
                "price": 1000.2
            },
            {
                "minute": 5,
                "price": 1063.29
            },
            {
                "minute": 6,
                "price": 1222.32
            },
            {
                "minute": 7,
                "price": 1379.10
            },
            {
                "minute": 8,
                "price": 1900.91
            },
            {
                "minute": 9,
                "price": 2200.05
            }
        ]
    },
    {
        "productId": "QDLHT",
        "productName": "青岛老火腿",
        "dealsData": [
            {
                "minute": 0,
                "price": 556.1
            },
            {
                "minute": 1,
                "price": 932.82
            },
            {
                "minute": 2,
                "price": 1480.28
            },
            {
                "minute": 3,
                "price": 2662.00
            },
            {
                "minute": 4,
                "price": 3417.63
            },
            {
                "minute": 5,
                "price": 5008.00
            },
            {
                "minute": 6,
                "price": 7938.27
            },
            {
                "minute": 7,
                "price": 8351.75
            },
            {
                "minute": 8,
                "price": 11378.3
            },
            {
                "minute": 9,
                "price": 15298.04
            }
        ]
    }
]
```

index.js
```
const fs = require('fs')
const WebSocketServer = require('ws').Server

const wss = new WebSocketServer({port: 8080})
debug('Server is up and listening on port: 8080')

const deals = JSON.parse(fs.readFileSync('deals.json'))
const products = deals.map(_ => _.productId)

const getConnectedEvent = () => {
  const event = {
      event: 'connected',
      products: products,
      message: 'Connected to the server'
  }
  return JSON.stringify(event)
}

const getErrorEvent = (reason) => {
  const event = {
    event: 'error',
    message: reason
  }
  return JSON.stringify(event)
}

const handleSubscribe = (ws, parsedMessage, connectionInfo) => {
  parsedMessage.products.forEach(productId => {
    if (deals.some(deal => deal.productId === productId)) {
      if (!connectionInfo.productsToMonitor.includes(productId)) {
        connectionInfo.productsToMonitor.push(productId)
      }
    } else {
      ws.send(getErrorEvent('invalid product Id'))
    }
  })  
}

const handleUnsubscribe = (ws, parsedMessage, connectionInfo) => {
  parsedMessage.products.forEach(productId => {
    const i = connectionInfo.productsToMonitor.indexOf(productId)
    if (i > -1) {
      connectionInfo.productsToMonitor.splice(i, 1)
    } else {
      ws.send(getErrorEvent('invalid product Id'))
    }
  })
}

const disconnect = (ws, reason) => {
  debug('Disconnected: ' + reason)
  ws.terminate()
}

const getDealsUpdateEvent = (connectionInfo) => {
  let event = {
    event: 'deal-update',
    deals: {}
  }

  connectionInfo.productsToMonitor.forEach(productId => {
    let deal = deals.find(e => e.productId === productId)
    if (deal) {
      const dealsDataLength = deal.dealsData.length
      if (connectionInfo.productsUpdateCount >= dealsDataLength) {
        connectionInfo.productsUpdateCount = 0
      }
      event.deals[productId] = deal.dealsData[connectionInfo.productsUpdateCount].price
    }
  })
  return JSON.stringify(event)
}

wss.on('connection', (ws) => {
  ws.send(getConnectedEvent())

  let connectionInfo = {
    isActive: true,
    productsToMonitor: [],
    productsUpdateCount: 0,
  }

  ws.on('message', (message) => {
    debug('Received message from client: ' + message)

    connectionInfo.isActive = true
    let parsedMessage = JSON.parse(message) 
    /*
      {
        event: 'subscribe',
        products: ['WLQ', 'QDLHT']
      }
    */
    if (parsedMessage.event === 'subscribe') {
      handleSubscribe(ws, parsedMessage, connectionInfo)
    } else if (parsedMessage.event === 'unsubscribe') {
      handleUnsubscribe(ws, parsedMessage, connectionInfo)
    }
  })

  ws.dealUpdateInterval = setInterval(() => {
    if (connectionInfo.productsToMonitor.length > 0) {
      ws.send(getDealsUpdateEvent(connectionInfo))
      connectionInfo.productsUpdateCount += 1
    }
  }, 5000)

  ws.pingInterval = setInterval(() =>{
    if(connectionInfo.isActive) {
      //set it to false, once ping get a pong, set it back to true
      connectionInfo.isActive = false
      ws.ping() 
    } else {
      disconnect(ws, 'connection inactive: Ping without Pong')
    }
  }, 17000)

  ws.connectionTimeout = setTimeout(() => {
    disconnect(ws, 'automatically disconnected after a while')
  }, 30000)

  ws.on('pong', () => {
    connectionInfo.isActive = true
  })

  ws.on('close', () => {
    clearInterval(ws.dealUpdateInterval)
    clearInterval(ws.pingInterval)
    clearTimeout(ws.connectionTimeout)
  })
})


function debug(info) {
  console.log(new Date().toISOString() + ': ' + info)
}
```

test-client.html
```
<!DOCTYPE html>
<html>
<head> 
<title>WebSocket Test Client</title>
</head>

<body> 
<h1>Open console for details</h1>
<script> 

if(!window.WebSocket) {   
  debug('WebSocket is NOT supported!')   
}

const  ws = new WebSocket("ws://127.0.0.1:8080/")
debug('WebSocket object is created')
  
ws.addEventListener('open', (e) => {
  debug('****Connection Successfully****')
})

setTimeout(() => {
  const subscribeEvent = {
    'event': 'subscribe', 
    products: ['WLQ', 'QDLHT'],
  } 
  debug('Send data to Server: ' + JSON.stringify(subscribeEvent))
  ws.send(JSON.stringify(subscribeEvent))  
}, 1000)


setTimeout(() => {
  const subscribeEvent = {
    'event': 'unsubscribe', 
    products: ['WLQ'],
  } 
  debug('Send data to Server: ' + JSON.stringify(subscribeEvent))
  ws.send(JSON.stringify(subscribeEvent))  
}, 12000)
 
ws.addEventListener('message', (e) => {
  debug('Received: ' + e.data);
})

ws.addEventListener('close', (e) => {
  debug('Server disconnected! Bye~~')
})
 
ws.addEventListener('error', (e) => {
  debug('Connection Error')
})

window.onbeforeunload = function () {
  ws.close()
}

function debug(info) {
  console.log(new Date().toISOString() + ': ' + info)
}
</script>
</body>

</html>
```

