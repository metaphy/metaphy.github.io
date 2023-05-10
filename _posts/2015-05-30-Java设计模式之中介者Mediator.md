---
layout: post
title:  "Java设计模式之中介者Mediator"
date:   2015-05-30 16:00:00 +0800
categories: Java
--- 

当多个对象之间存在大量关联关系时，这些对象之间很容易出现强耦合，此时我们可以创建一个中间人，来协调各个类之间的联系；这就是中介者模式(Mediator)。 中介者属于行为型模式，**用一个中介对象来封装一系列的对象交互，中介者使各对象不需要显式地相互引用，从而使其耦合松散，而且可以独立地改变它们之间的交互**。

中介者显著降低了对象与对象之间的联系，将1v多变成1v1模式，缺点是中介者自身可能变得非常庞大，而难以维护。

现实世界中的机场调度塔台就是充当了中介者，各飞机与塔台互相联系，而不是与其他飞机直接联系，这样明显提高沟通效率。

![pic](/images/2015-05-30-mediator1.png)

* ControlTower: 控制台接口，只有sendMessage(message, plane) 方法，其中的plan代表Sender
* ControlTowerImpl: 控制台具体实现，需要包含各个AirCraft，其中sendMessage方法将会收到各个sender的消息并做转发等处理
* AirCraft: 飞行器类，包含ControlTower的具体实现，并将自己的sendMessage 交给ControlTower的sendMessage
* MediatorDemo: 测试类

![pic](/images/2015-05-30-mediator2.png)

{% highlight java %}
public interface ControlTower {
    void sendMessage(String message, AirCraft plane);
}
{% endhighlight %}

{% highlight java %}
public class ControlTowerImpl implements ControlTower {
    private AirCraft airBus;
    private AirCraft boeing;

    public void setAirBus(AirCraft airBus) {
        this.airBus = airBus;
    }

    public void setBoeing(AirCraft boeing) {
        this.boeing = boeing;
    }

    @Override
    public void sendMessage(String message, AirCraft plane){
        if(plane == airBus){
            boeing.receiveMessage(message);
        } else {
            airBus.receiveMessage(message);
        }
    }
}

{% endhighlight %}

{% highlight java %}

public class AirCraft {
    private String name;
    private ControlTower controlTower;

    public AirCraft(String name, ControlTower controlTower){
        this.name = name;
        this.controlTower = controlTower;
    }

    public void sendMessage(String message) {
        controlTower.sendMessage(message, this);
    }

    public void receiveMessage(String message) {
        System.out.println(name + " received message: " + message);
    }
}
{% endhighlight %}

{% highlight java %}
public class MediatorDemo {

    public static void main(String[] args) {
        ControlTowerImpl controlTowerImpl = new ControlTowerImpl();

        AirCraft airBus = new AirCraft("AirBus A300", controlTowerImpl);
        AirCraft boeing = new AirCraft("Boeing 737", controlTowerImpl);

        controlTowerImpl.setAirBus(airBus);
        controlTowerImpl.setBoeing(boeing);

        airBus.sendMessage("Hello from Airbus");
        boeing.sendMessage("Good day from Boeing");
    }
}
{% endhighlight %}

程序输出：
```
Boeing 737 received message: Hello from Airbus
AirBus A300 received message: Good day from Boeing
```

  
附：  

创建型模式
====================
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
