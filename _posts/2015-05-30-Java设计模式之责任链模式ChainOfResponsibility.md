---
layout: post
title: "Java设计模式之责任链模式ChainOfResponsibility"
date: 2015-05-20 12:00:01 +0800
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
 
```
Start to process Request{requestAuthCode=0, requestType='drinks'}
Authentication Failed!
Start to process Request{requestAuthCode=1, requestType='drinks'}
Authentication Pass!
Drinks: Water, Milk, Coffee, Red Tea
```