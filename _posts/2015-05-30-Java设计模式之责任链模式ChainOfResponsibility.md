---
layout: post
title: "Java设计模式之责任链模式ChainOfResponsibility"
date: 2015-05-30 12:00:01 +0800
categories: Java
--- 

对于一个复杂请求的处理，我们可以这样做，**为避免请求发送者与请求处理者之间的耦合，将请求的处理分派给多个对象，这些对象连成一条链，请求沿着链条传递**，这个就是责任链模式(Chain of responsibility)。 Java servlet的Filter以及Structs中的拦截器都可以看作是这种模式；现实中，对于某些申请一般也是层层审批，也可以看作这种模式。

我们依旧以某种web请求的处理来举例。如果对请求的处理十分复杂，或者经常改变，那采用责任链模式就是非常恰当的。

比如，对一个请求，假设是请求食品或者饮料的列表，我们首先进行鉴权Authentication(是否有权限)和授权Authorization检查(拥有的权限是否可以当前操作)，再检查请求参数是否有效等，最终才是处理。

![pic](/images/2015-05-30-chain1.png)

* Handler: 请求处理者的接口，核心是setNextHandler 和 handleRequest 方法，每个具体的处理者在实现handleRequest方法时，里面还要调用nextHandler.handleRequest
* HandlerAuth / HandlerRequest: 具体的请求处理者，实现Handler接口 
* Request: 请求对象的封装
* ChainOfResponsibilityDemo: 测试类

![pic](/images/2015-05-30-chain2.png)


{% highlight java %}
public interface Handler {
    void handleRequest(Request request);
    void setNextHandler(Handler handler);
}
{% endhighlight %}

{% highlight java %}
public class AuthHandler implements Handler{
    private Handler nextHandler;

    public void handleRequest(Request request){
        System.out.println("Start to process " + request);
        if (request.getRequestAuthCode() > 0) {
            System.out.println("Authentication Pass!");
            nextHandler.handleRequest(request);
        } else {
            System.out.println("Authentication Failed!");
        }
    }

    @Override
    public void setNextHandler(Handler nextHandler) {
        this.nextHandler = nextHandler;
    }
}
{% endhighlight %}

{% highlight java %}
public class RequestHandler implements Handler{
    private Handler nextHandler;

    private static final String DRINKS = "drinks";
    private static final String FOOD = "food";

    public void handleRequest(Request request){
        if(request.getRequestType().equalsIgnoreCase(DRINKS)){
            System.out.println("Drinks: Water, Milk, Coffee, Red Tea");
        } else if(request.getRequestType().equalsIgnoreCase(FOOD)){
            System.out.println("Food: Baozi, Hamburger, Salad");
        } else {
            System.out.println("Incorrect request type");
        }
    }

    @Override
    public void setNextHandler(Handler nextHandler) {
        this.nextHandler = nextHandler;
    }
}
{% endhighlight %}

{% highlight java %}
public class Request {
    private int requestAuthCode;
    private String requestType;

    public int getRequestAuthCode() {
        return requestAuthCode;
    }

    public void setRequestAuthCode(int requestAuthCode) {
        this.requestAuthCode = requestAuthCode;
    }

    public String getRequestType() {
        return requestType;
    }

    public void setRequestType(String requestType) {
        this.requestType = requestType;
    }

    @Override
    public String toString() {
        return "Request{" +
                "requestAuthCode=" + requestAuthCode +
                ", requestType='" + requestType + '\'' +
                '}';
    }
}
{% endhighlight %}

{% highlight java %}
public class ChainOfResponsibilityDemo {
    public static void main(String[] args) {
        Handler authHandler = new AuthHandler();
        Handler requestHandler = new RequestHandler();

        authHandler.setNextHandler(requestHandler);

        Request request1 = new Request();
        request1.setRequestType("drinks");
        authHandler.handleRequest(request1);

        request1.setRequestAuthCode(1);
        authHandler.handleRequest(request1);
    }
}
{% endhighlight %}
 
程序输出如下： 
```
Start to process Request{requestAuthCode=0, requestType='drinks'}
Authentication Failed!
Start to process Request{requestAuthCode=1, requestType='drinks'}
Authentication Pass!
Drinks: Water, Milk, Coffee, Red Tea
```
  
附：  

创建型模式
====================
  * [Java设计模式之抽象工厂模式AbstractFactory](https://metaphy.github.io/java/2015/05/09/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E6%8A%BD%E8%B1%A1%E5%B7%A5%E5%8E%82%E6%A8%A1%E5%BC%8FAbstractFactory.html)
  * [Java设计模式之创建者Builder](https://metaphy.github.io/java/2015/05/10/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E5%88%9B%E5%BB%BA%E8%80%85Builder.html)
  
结构型模式
====================
  * [Java设计模式之外观模式Facade](https://metaphy.github.io/java/2015/05/20/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E5%A4%96%E8%A7%82%E6%A8%A1%E5%BC%8FFacade.html)
  * [Java设计模式之组合模式Composite](https://metaphy.github.io/java/2015/05/20/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E7%BB%84%E5%90%88%E6%A8%A1%E5%BC%8FComposite.html)
  * [Java设计模式之享元模式Flyweight](https://metaphy.github.io/java/2015/05/20/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E4%BA%AB%E5%85%83%E6%A8%A1%E5%BC%8FFlyweight.html)
  * [Java设计模式之代理模式Proxy](https://metaphy.github.io/java/2015/05/20/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E4%BB%A3%E7%90%86%E6%A8%A1%E5%BC%8FProxy.html)
  * [Java设计模式之桥接模式Bridge](https://metaphy.github.io/java/2015/05/20/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E6%A1%A5%E6%8E%A5%E6%A8%A1%E5%BC%8FBridge.html)


行为型模式
====================  
  * [Java设计模式之策略模式Strategy](https://metaphy.github.io/java/2015/05/30/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E7%AD%96%E7%95%A5%E6%A8%A1%E5%BC%8FStrategy.html)
  * [Java设计模式之状态模式State](https://metaphy.github.io/java/2015/05/30/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E7%8A%B6%E6%80%81%E6%A8%A1%E5%BC%8FState.html)
  * [Java设计模式之访问者Visitor](https://metaphy.github.io/java/2015/05/30/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E8%AE%BF%E9%97%AE%E8%80%85Visitor.html)
  * [Java设计模式之观察者Observer](https://metaphy.github.io/java/2015/05/30/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E8%A7%82%E5%AF%9F%E8%80%85Observer.html) 
  * [Java设计模式之中介者Mediator](https://metaphy.github.io/java/2015/05/30/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E4%B8%AD%E4%BB%8B%E8%80%85Mediator.html)
  * [Java设计模式之命令模式Command](https://metaphy.github.io/java/2015/05/30/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E5%91%BD%E4%BB%A4%E6%A8%A1%E5%BC%8FCommand.html)  
  * [Java设计模式之责任链模式ChainOfResponsibility](https://metaphy.github.io/java/2015/05/30/Java%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E8%B4%A3%E4%BB%BB%E9%93%BE%E6%A8%A1%E5%BC%8FChainOfResponsibility.html)  
  

  