---
layout: post
title:  "Java设计模式之抽象工厂模式AbstractFactory"
date:   2015-05-10 01:00:00 +0800
categories: Java
--- 

一般来说，抽象工厂模式(Abstract Factory)是我们学习设计模式所要接触的第一个模式。抽象工厂所要解决的问题也比较典型，比如你有多套产品线，每套产品线都有自己的风格，并且都可以生产多个具体产品。举个例子，比如你是一名装修设计师，对于一间房子的装修，有多种风格，古典中式风格、西式风格或现代风格，而每种风格下，都有自己的壁纸样式、灯具样式以及沙发样式等等，这种情况就可以使用抽象工厂。类似的例子还有，你设计不同观感(look-and-feel)的用户界面，有windows风格，有金属风格，每种风格下都有自己的标题栏、菜单、按钮等等，对于这些具体项目的创建，使用抽象工厂就很方便。

所以，抽象工厂意图**提供一个创建一系列相关或相互依赖对象的接口，而无需指定它们具体的类**。我们以不同观感的用户界面的设计为例，具体解释一下如何实现。我们有两种风格，分别叫Motif和Windows，每种风格下需要创建它们的菜单栏和按钮：

|        | Motif   | Windows |
| ----   | ----    | ----    |
| Menu    | Motif Menu  | Windows Menu  |
| Button  | Motif Button| Windows Button|


这个Demo涉及的类文件比较多，多达10个。首先是Menu和Button的接口，以及它们分别对应的实体类：
 
* IMenu, Menu接口, 这是对具有不同风格的同一个Item的抽象
* IButton, Button接口
* MotifMenu, Motif 风格下的Menu
* MotifButton, Motif 风格下的Button
* WindowsMenu, Windows 风格下的Menu
* WindowsButton, Windows 风格下的Button

其次是两个不同风格的Factory以及Factory的抽象：

* AbstractUIFactory
* MotifUIFactory
* WindowsUIFactory

最后是Demo代码：
* AbstractFactoryDemo

![pic](/images/2015-05-10-abstractfactory.png)

{% highlight java %}
public class AbstractFactoryDemo {
    public static void main(String[] args) {
        AbstractUIFactory motifFactory = new MotifUIFactory();
        IMenu motifMenu = motifFactory.createMenu();
        IButton motifButton = motifFactory.createButton();

        System.out.println("Below are Motif look-and-feel: ");
        System.out.printf("> %s, %s\n", motifMenu.menuName(), motifButton.buttonName());

        AbstractUIFactory windowsFactory = new WindowsUIFactory();
        IMenu windowsMenu = windowsFactory.createMenu();
        IButton windowsButton = windowsFactory.createButton();

        System.out.println("Below are Windows look-and-feel: ");
        System.out.printf("> %s, %s\n", windowsMenu.menuName(), windowsButton.buttonName());
    }
}
{% endhighlight %}
{% highlight java %}
public interface AbstractUIFactory {
    IMenu createMenu();

    IButton createButton();
}
{% endhighlight %}

{% highlight java %}
public interface IButton {
    String buttonName();
}

{% endhighlight %}
{% highlight java %}
public interface IMenu {
    String menuName();
}
{% endhighlight %}
{% highlight java %}
public class MotifButton implements IButton{
    @Override
    public String buttonName() {
        return "Motif button";
    }
}
{% endhighlight %}


{% highlight java %}
public class MotifMenu implements IMenu{
    @Override
    public String menuName() {
        return "Motif menu";
    }
}
{% endhighlight %}

{% highlight java %}
public class MotifUIFactory implements AbstractUIFactory{
    @Override
    public IMenu createMenu() {
        return new MotifMenu();
    }

    @Override
    public IButton createButton() {
        return new MotifButton();
    }
}
{% endhighlight %}
{% highlight java %}
public class WindowsButton implements IButton{
    @Override
    public String buttonName() {
        return "Windows button";
    }
}
{% endhighlight %}
{% highlight java %}
public class WindowsMenu implements IMenu{
    @Override
    public String menuName() {
        return "Windows menu";
    }
}

{% endhighlight %}
{% highlight java %}
public class WindowsUIFactory implements AbstractUIFactory{
    @Override
    public IMenu createMenu() {
        return new WindowsMenu();
    }

    @Override
    public IButton createButton() {
        return new WindowsButton();
    }
}
{% endhighlight %}

最终输出结果：
```
Below are Motif look-and-feel: 
> Motif menu, Motif button
Below are Windows look-and-feel: 
> Windows menu, Windows button
```

多说一句，司马迁写历史用了一种十分机智的方式，就是写人、写故事，这样历史就活了起来，生动了许多。设计模式应该也是这样。我们应该去记一个个典型的例子，通过例子去理解它背后的那套抽象的机制，而不是直接就是类图或者说解决意图，这些是很重要，但也很难理解，特别容易打击人的学习积极性。

