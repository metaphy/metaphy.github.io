---
layout: post
title: "Java设计模式之装饰模式Decorator"
date: 2015-05-20 14:30:01 +0800
categories: java
--- 

装饰器模式(Decorator)常见，尤其学习Java I/O部分那些各个类型的转换，就是典型的装饰器，比如：

{% highlight java %}
// 1. 建立连接 (底层的流)
FileInputStream fis = new FileInputStream("game_save.bin");

// 2. 为了高效，套个缓冲区
BufferedInputStream bis = new BufferedInputStream(fis);

// 3. 为了方便读基本类型，套上 DataInputStream
DataInputStream dis = new DataInputStream(bis);

// 有了 DataInputStream 后，可以直接读int，读double等
int level = dis.readInt();      
{% endhighlight %}

那么，装饰器和之前的适配器有什么本质区别？

适配器是做**接口转换**，通常只做一层转换，比如手机充电器的例子；而装饰器是做**行为增强**，添加额外的操作，通常可以支持多层转换，比如上面的读文件流，就经过了两层转换最终到DataInputStream才能直接读int。因此，装饰器就是：不改变原有对象结构，动态给对象增加一些职责。

以咖啡举例子。我们有基础款咖啡，以及在基础款之上加料(装饰)，以实现各种不同种类的咖啡。
{% highlight java %}

public interface Coffee {
    String getDescription();
    double getCost();
}

public class SimpleCoffee implements Coffee {
    @Override
    public String getDescription() {
        return "基础咖啡";
    }

    @Override
    public double getCost() {
        return 10.0;
    }
}


关键点： 它必须实现 Coffee 接口，并持有一个 Coffee 对象的引用。
public abstract class CoffeeDecorator implements Coffee {
    protected final Coffee decoratedCoffee;

    public CoffeeDecorator(Coffee coffee) {
        this.decoratedCoffee = coffee;
    }

    public String getDescription() {
        return decoratedCoffee.getDescription();
    }

    public double getCost() {
        return decoratedCoffee.getCost();
    }
}

通过装饰器，我们可以在不修改 SimpleCoffee 的情况下增加“牛奶”和“糖”。
// 牛奶装饰器
public class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return super.getDescription() + ", 加奶";
    }

    @Override
    public double getCost() {
        return super.getCost() + 5.0;
    }
}

// 糖装饰器
public class SugarDecorator extends CoffeeDecorator {
    public SugarDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return super.getDescription() + ", 加糖";
    }

    @Override
    public double getCost() {
        return super.getCost() + 2.0;
    }
}

public class ArchitectDemo {
    public static void main(String[] args) {
        // 1. 想要一杯纯咖啡
        Coffee coffee = new SimpleCoffee();
        
        // 2. 加点奶 (装饰一次)
        coffee = new MilkDecorator(coffee);
        
        // 3. 再加点糖 (再装饰一次)
        coffee = new SugarDecorator(coffee);

        System.out.println("订单内容: " + coffee.getDescription());
        System.out.println("最终价格: ￥" + coffee.getCost());
    }
}
{% endhighlight %}
输出结果:
```
--- 开始 
```