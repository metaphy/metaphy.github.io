---
layout: post
title:  "Java设计模式之观察者Observer"
date:   2015-05-05 13:15:00 +0800
categories: Java
--- 

观察者模式（Observer Pattern）是行为型模式中非常典型的一种设计模式，它定义**对象间的一对多的关系，当一个对象发生改变时，所有依赖它的对象都会得到通知**。它的这一解耦方式非常像发布Publish/订阅Subscribe模式，或者生产者Producer/消费者Consumer模式。

实际开发中这一模式应用非常广泛，java.util库中已经封装好Observable和Observer，所以使用Java来实现这一模式也很简单。下面演示天气信息的发布，以及关注天气的各方：本地电视台，机场和Moji App自动接收到天气信息的例子。

* Weather, 继承Observable，是天气信息的发布者。
* WeatherObserver, 实现Observer，天气信息的关注者，他们会自动接收到天气信息。

{% highlight java %}
import java.util.Observable;

public class Weather extends Observable {
    public void publishMessage(String msg) {
        setChanged();
        notifyObservers(msg);
    }
}

{% endhighlight %}
{% highlight java %}

import java.util.Observable;
import java.util.Observer;

public class WeatherObserver implements Observer {
    private String name;

    public WeatherObserver(String name){
        this.name = name;
    }

    @Override
    public void update(Observable o, Object arg) {
        System.out.println("Observer " + name + " receives message: " + arg);
    }

    public static void main(String[] args) {
        Weather weather = new Weather();

        WeatherObserver tv = new WeatherObserver("Local TV Station");
        WeatherObserver airport = new WeatherObserver("Airport");
        WeatherObserver mojiApp = new WeatherObserver("Moji App");

        weather.addObserver(tv);
        weather.addObserver(airport);
        weather.addObserver(mojiApp);

        weather.publishMessage("It will heavily rain tomorrow");
        weather.publishMessage("Lowest temperatures will be 12 degrees Celsius");
    }
}
{% endhighlight %}
 
结果如下
{% highlight java %}
Observer Moji App receives message: It will heavily rain tomorrow
Observer Airport receives message: It will heavily rain tomorrow
Observer Local TV Station receives message: It will heavily rain tomorrow
Observer Moji App receives message: Lowest temperatures will be 12 degrees Celsius
Observer Airport receives message: Lowest temperatures will be 12 degrees Celsius
Observer Local TV Station receives message: Lowest temperatures will be 12 degrees Celsius
{% endhighlight %} 
