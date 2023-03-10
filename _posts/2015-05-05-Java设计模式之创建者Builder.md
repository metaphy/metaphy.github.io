---
layout: post
title:  "Java设计模式之创建者Builder"
date:   2015-05-05 13:11:00 +0800
categories: Java
--- 

创建者模式（Builder Pattern）**将一个复杂对象的构造过程和它的表现方式（representation）分离开来，使得同样的构造过程可以创造出不同的表示**。这里的不同的表现方式---用现实中的例子来讲---可以指：不同类型的电脑，一间房子不同的装修风格，麦当劳套餐不同的搭配方案等等。简而言之，创建者模式是对创建过程的抽象。

下面例子是创建不同的电脑，其核心是对电脑这一具体物件，抽象出了一个IComputerBuilder接口，该接口用来build电脑的不同部件，比如CPU，内存，硬盘，显示器，操作系统等，并最终提供一个产品；不同电脑的创建器都会实现这一接口，从而达到使用同样创建方式创建出不同电脑的目的。

* Computer, 电脑类，实体类，即我们最终需要的各种各样不同的电脑的类。  
* IComputerBuilder, 电脑对象的创建接口，用来创建电脑的不同部件；各个不同的电脑创建器都需要实现它。
* ComputerDirector，使用不同的Computer创建器并构造出不同的Computer实例，并测试。

{% highlight java %}
public class Computer {
    private String name;
    private String cpu;
    private int memory;
    public void setName(String name) {
        this.name = name;
    }
    public void setCpu(String cpu) {
        this.cpu = cpu;
    }

    public void setMemory(int memory) {
        this.memory = memory;
    }
    
    @Override
    public String toString() {
        return "Computer [" + name + "] CPU=" + cpu + ", Memory=" + memory + "GB";
    }
}
{% endhighlight %}
{% highlight java %}
public interface IComputerBuilder {
    void buildName();
    void buildCpu();
    void buildMemory();

    Computer build();
}

{% endhighlight %}
{% highlight java %}
public class MacBookBuilder implements IComputerBuilder {
    private Computer computer = new Computer();

    @Override
    public void buildName() {
        computer.setName("MacBook Pro");
    }
    
    @Override
    public void buildCpu() {
        computer.setCpu("Intel Core i7 2.3GHz");
    }
    
    @Override
    public void buildMemory() {
        computer.setMemory(8);
    }
    
    @Override
    public Computer build() {
        return computer;
    }
}
{% endhighlight %}
{% highlight java %}
public class ThinkPadBuilder implements IComputerBuilder {
    private Computer computer = new Computer();

    @Override
    public void buildName() {
        computer.setName("ThinkPad X1");
    }
    
    @Override
    public void buildCpu() {
        computer.setCpu("Intel i5 2520M");
    }
    
    @Override
    public void buildMemory() {
        computer.setMemory(8);
    }
    
    @Override
    public Computer build() {
        return computer;
    }
}
{% endhighlight %}
{% highlight java %}
public class ComputerDirector {
    public Computer build(IComputerBuilder computerBuilder) {
        computerBuilder.buildName();
        computerBuilder.buildCpu();
        computerBuilder.buildMemory();
    
        return computerBuilder.build();
    }
    
    public static void main(String[] args) {
        ComputerDirector director = new ComputerDirector();
        
        IComputerBuilder macBookBuilder = new MacBookBuilder();
        Computer mac = director.build(macBookBuilder);
        System.out.println(mac);
        
        IComputerBuilder thinkPadBuilder = new ThinkPadBuilder();
        Computer thinkpad = director.build(thinkPadBuilder);
        System.out.println(thinkpad);
    }
}
{% endhighlight %}
最终输出结果：
{% highlight java %}
Computer [MacBook Pro] CPU=Intel Core i7 2.3GHz, Memory=8GB
Computer [ThinkPad X1] CPU=Intel i5 2520M, Memory=8GB
{% endhighlight %} 
