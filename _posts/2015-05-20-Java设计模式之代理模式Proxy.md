---
layout: post
title:  "Java设计模式之代理模式Proxy"
date:   2015-05-20 11:00:00 +0800
categories: Java
--- 

代理模式（Proxy）是一种非常常见的设计模式，它属于结构型模式，本身也非常好理解。义如其名，就是生活中的代理，譬如火车票代售点、房屋中介，或者下图中强健体育公司的联系方式。

![pic](/images/2015-05-06.png)

强健公司的体育器械上并没有直接印他们公司的联系电话，而是印的“114转强健体育”，114电话台充当了代理，完美解耦器械和公司电话号码的强绑定。请考虑这样一个现实的场景，如果哪天强健体育公司的联系电话要变更，印在体育器械上固定号码的方式与使用114代理的方式，哪种更容易呢？

所以，代理模式非常容易理解，就是**为其他对象提供一种代理以控制对这个对象的访问**。下面用Java实现强健公司联系电话的这个功能，各个类的解释如下：

* IContact: 对代理类和实体类行为的抽象，此例中是指提供电话号码
* StrengthSports: 强健体育公司，会提供公司实际的联系电话
* Proxy114: 114查号台，把强健体育提供给它的电话号码提供给大家
* ProxyDemo: 测试用

![pic](/images/2015-05-20-proxy.png)

{% highlight java %}
public interface IContact {
    String contactNumber();
}
{% endhighlight %}

{% highlight java %}
public class StrengthSports implements IContact {
    private String contact = "0411-88afcv01";   //original contact #

    public void setContact(String contact) {
        this.contact = contact;
    }

    @Override
    public String contactNumber() {
        return contact;
    }
}
{% endhighlight %}

{% highlight java %}
public class Proxy114 implements IContact {
    private StrengthSports strengthSports;

    public void setStrengthSportsCorp(StrengthSports strengthSports){
        this.strengthSports = strengthSports;
    }

    @Override
    public String contactNumber() {
        if(strengthSports == null) {
            strengthSports = new StrengthSports();
        }
        return strengthSports.contactNumber();
    }
}
{% endhighlight %}

{% highlight java %}
public class ProxyDemo {
    public static void main(String[] args) {
        StrengthSports strengthSports = new StrengthSports();
        Proxy114 p114 = new Proxy114();
        p114.setStrengthSportsCorp(strengthSports);
        System.out.println("Strength Sports Corp. Contact number: " + p114.contactNumber());

        // Strength Sports Corp changes their contact number
        strengthSports.setContact("131-a0kb-ad05");

        System.out.println("Strength Sports Corp. New Contact number: " + p114.contactNumber());
    }
}

{% endhighlight %}

程序运行结果如下：
{% highlight java %}
Strength Sports Corp. Contact number: 0411-88afcv01
Strength Sports Corp. New Contact number: 131-a0kb-ad05
{% endhighlight %} 