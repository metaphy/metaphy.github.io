---
layout: post
title:  "Java设计模式之桥接模式Bridge"
date:   2015-05-07 12:33:20 +0800
categories: Java
--- 

桥接模式（Bridge）是一种结构型模式，它的定义很简单，即**将抽象部分与它的实现部分分离，使它们都可以独立的变化**。虽然定义简单，但是理解起来却不简单。

我直接用GoF著作中的例子来解释，这是有关图形用户界面开发的例子。Window是抽象父类，其下有XWindow 和PMWindow子类分别对应不同操作系统平台，假设此时，我们需要有一种带图标的Window, 即IconWindow也继承Window，那么为了适应两个不同平台，不得不产生XIconWindow和 PMIconWindow两个子类。

其中的核心问题在于，不同的操作平台(X Window 和PM Window)以及不同样子的Window(IconWindow)并不在一个**抽象维度**，我们把两个不同维度的类型掺杂到一起，必然会导致代码臃肿难看，因为最终不得不做出m * n种组合方案。为了解决相关问题，使用Bridge模式，如下图。

![pic](/images/2015-05-07.png)

再举一个具体的例子，比如我们需要Phone这个类型，其中的两个维度分别是手机品牌(比如我们有Nokia和小米手机）以及手机类型（智能机和传统的按键手机），以及每种手机都有的功能call(); 我们在此对手机类型做单独处理，使Phone这个类包含TypedPhone，这就是Bridge模式。

* ITypePhone: 手机类型的抽象，不管什么类型的手机都有call的功能
* FeaturePhone/SmartPhone: 传统按键手机和智能机，均实现ITypePhone
* Phone: 手机的抽象类，此类使用ITypedPhone的对象作为构造函数的参数，提供的call()方法是ITypePhone的call方法，它是沟通手机品牌和手机类型的桥
* XiaoMiPhone/NokiaPhone: 继承Phone
* BridgeDemo: 测试用

{% highlight java %}
public interface ITypePhone {
    void call();
}
{% endhighlight %}

{% highlight java %}
public class FeaturePhone implements ITypePhone {
    @Override
    public void call() {
        System.out.println("Feature Phone calling");
    }
}
{% endhighlight %}

{% highlight java %}
public class SmartPhone implements ITypePhone {
    @Override
    public void call() {
        System.out.println("Smart Phone calling");
    }
}
{% endhighlight %}

{% highlight java %}
public abstract class Phone {
    private ITypePhone typedPhone;

    public Phone(ITypePhone typedPhone) {
        this.typedPhone = typedPhone;
    }

    protected void call() {
        this.typedPhone.call();
    }
}
{% endhighlight %}

{% highlight java %}
public class NokiaPhone extends Phone{
    public NokiaPhone(ITypePhone typedPhone) {
        super(typedPhone);
    }

    public void call(){
        super.call();
        System.out.println(" --calling from Nokia!");
    }
}
{% endhighlight %}

{% highlight java %}
public class XiaoMiPhone extends Phone{
    public XiaoMiPhone(ITypePhone typedPhone) {
        super(typedPhone);
    }

    public void call(){
        super.call();
        System.out.println(" --calling from XiaoMi!");
    }
}
{% endhighlight %}

{% highlight java %}
public class BridgeDemo {
    public static void main(String[] args) {
        // e.g. we call with Nokia feature phone
        ITypePhone featurePhone = new FeaturePhone();
        Phone nokia = new NokiaPhone(featurePhone);
        nokia.call();

        // we call with Nokia smart phone
        ITypePhone smartPhone = new SmartPhone();
        Phone smartNokia = new NokiaPhone(smartPhone);
        smartNokia.call();

        // then we call with Xiao Mi smart phone
        Phone xiaomi = new XiaoMiPhone(smartPhone);
        xiaomi.call();
    }
}
{% endhighlight %}
测试结果：
{% highlight java %}
Feature Phone calling
 --calling from Nokia!
Smart Phone calling
 --calling from Nokia!
Smart Phone calling
 --calling from XiaoMi!
 {% endhighlight %}
 