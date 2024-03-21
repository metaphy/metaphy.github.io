---
layout: post
title: "Java设计模式之享元模式Flyweight"
date: 2015-05-20 12:00:01 +0800
categories: java
--- 

享元模式(Flyweight Pattern)是一种结构型设计模式，**用于优化内存使用，它通过共享尽可能多的对象来减少内存占用**。 

在有大量对象时，我们就把其中共同的部分抽象出来，有相同的业务请求，直接返回在内存中已有的对象，避免重新创建，那这个就是享元模式，它适应以下场景：

* 系统有大量相似的对象
* 需要缓存池的场景

p.s. Flyweight是指拳击或UFC的蝇量级，最小的体重级别。

下面例子，是我们需要创建许多Circle的时候，使用Flyweight: 

* Shape: 图形类的接口
* Circle: 圆形，实现Shape接口
* ShapeFactory: 生成Shape的工厂，目前主要是生成Circle, 对生成的Circle按特征值（此例是color）进行缓存。存到static的HashMap里
* FlyweightDemo: 测试类
 
{% highlight java %}
public interface Shape {
    void draw();
}
{% endhighlight %}

{% highlight java %}
public class Circle implements Shape {
    private String color;

    public Circle(String color) {
        this.color = color;
    }

    @Override
    public void draw() {
        System.out.println("Drawing Circle with color " + color);
    }
}
{% endhighlight %}

{% highlight java %}
public class ShapeFactory {
    private static final Map<String, Shape> cached = new HashMap<>();

    public static Shape getCircle(String color) {
        Shape circle = cached.get(color);

        if (circle == null) {
            circle = new Circle(color);
            cached.put(color, circle);
            System.out.println("-- Creating circle of color " + color);
        }

        return circle;
    }
}
{% endhighlight %}

程序输出：
{% highlight java %}
-- Creating circle of color Green
Drawing Circle with color Green
-- Creating circle of color Red
Drawing Circle with color Red
Drawing Circle with color Red
-- Creating circle of color Blue
Drawing Circle with color Blue
Drawing Circle with color Red
Drawing Circle with color Green
Drawing Circle with color Green
Drawing Circle with color Red
Drawing Circle with color Blue
Drawing Circle with color Blue
{% endhighlight %}

