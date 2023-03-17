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