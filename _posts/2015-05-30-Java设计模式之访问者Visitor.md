---
layout: post
title:  "Java设计模式之访问者Visitor"
date:   2015-05-30 16:20:00 +0800
categories: java
--- 

访问者（Visitor）是一种行为型模式，它表示**一个作用于某对象结构中各元素的操作**。它主要目的是在不修改现有对象结构的前提下，对对象添加新的操作。

譬如我们已经有了一个成熟的2D图形系统，里面包含父类Shape和它的子类Rectangle, Circle等，在这个系统中我们自然已经定义好了求面积求周长等各种操作。突然有一天，一个新的业务需求提出来了：各个类型都需要加一种优美的打印自己的方法。

由于既有代码工作良好，我们不想在各个子类分别去添加这么个方法实现，所以我们新建一个Visitor，让它去做这个事情。尽管我们不会对Shape及其子类有大的改动，但是还是需要稍微改一下，即添加accept方法，方法具体的实现交给具体的Vistor来做。

整个实现过程还是比较简单的，核心是把新加操作封装到Visitor和它具体的实现类里面，再对既有code增加一个打印方法。

* Shape, Rectangle, Circle 是图形类，它们需要改的是增加accept方法，但这个方法参数是Viistor, 并且具体的实现使用的是visitor的beautifulPrint方法
* Visitor, 接口，定义优美打印的方法，其中方法参数为各个Shape子类
* PrintVisitor, 实现Visitor接口，里面的打印方法，参数是各个Shape 子类
* VisitorDemo, 测试类

{% highlight java %}
public abstract class Shape{
    public abstract void accept (Visitor visitor);

    // other old and stable codes ...
}
{% endhighlight %}

{% highlight java %}
public class Rectangle extends Shape {
    private int length, width;

    public Rectangle(){}

    public Rectangle(int length, int width) {
        this.length = length;
        this.width = width;
    }

    public int getLength() {
        return length;
    }
 
    public int getWidth() {
        return width;
    }

    @Override
    public void accept(Visitor visitor) {
        visitor.beautifulPrint(this);
    }
}
{% endhighlight %} 

{% highlight java %}
public class Circle extends Shape {
    private int radius;

    public Circle(){}
    public Circle(int radius) {
        this.radius = radius;
    }


    public int getRadius() {
        return radius;
    }

    public void setRadius(int radius) {
        this.radius = radius;
    }

    @Override
    public void accept(Visitor visitor) {
        visitor.beautifulPrint(this);
    }
}
{% endhighlight %} 

{% highlight java %}
public interface Visitor {
    void beautifulPrint(Rectangle rectangle);
    void beautifulPrint(Circle circle);
}
{% endhighlight %} 

{% highlight java %}

public class PrintVisitor implements Visitor {
    @Override
    public void beautifulPrint(Rectangle rectangle) {
        int length = rectangle.getLength();
        int width = rectangle.getWidth();

        for (int i = 0; i <= width; i++) {
            for (int j = 0;j <= length; j++) {
                System.out.print(".  ");
            }
            System.out.println();
        }
    }

    @Override
    public void beautifulPrint(Circle circle) {
        int radius = circle.getRadius();

        for (int y = -radius; y <= radius; y++) {
            for (int x = -radius; x <= radius; x++) {
                if (x * x + y * y <= radius * radius) {
                    // 点(x,y)在圆内
                    System.out.print(".  ");
                } else {
                    System.out.print("   ");
                }
            }
            System.out.println();
        }

    }
}
{% endhighlight %} 

{% highlight java %}
public class VisitorDemo {
    public static void main(String[] args) {
        Rectangle rectangle = new Rectangle(12, 5);
        Circle circle = new Circle(5);

        Visitor printer = new PrintVisitor();
        System.out.println("\nPrint the rectangle:");
        printer.beautifulPrint(rectangle);

        System.out.println("\nPrint the circle:");
        printer.beautifulPrint(circle);
    }
}
{% endhighlight %} 
 
 
结果如下
{% highlight java %}

Print the rectangle:
.  .  .  .  .  .  .  .  .  .  .  .  .  
.  .  .  .  .  .  .  .  .  .  .  .  .  
.  .  .  .  .  .  .  .  .  .  .  .  .  
.  .  .  .  .  .  .  .  .  .  .  .  .  
.  .  .  .  .  .  .  .  .  .  .  .  .  
.  .  .  .  .  .  .  .  .  .  .  .  .  

Print the circle:
               .                 
      .  .  .  .  .  .  .        
   .  .  .  .  .  .  .  .  .     
   .  .  .  .  .  .  .  .  .     
   .  .  .  .  .  .  .  .  .     
.  .  .  .  .  .  .  .  .  .  .  
   .  .  .  .  .  .  .  .  .     
   .  .  .  .  .  .  .  .  .     
   .  .  .  .  .  .  .  .  .     
      .  .  .  .  .  .  .        
               .                 
{% endhighlight %} 
