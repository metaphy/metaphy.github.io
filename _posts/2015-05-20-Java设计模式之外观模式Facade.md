---
layout: post
title:  "Java设计模式之外观模式Facade"
date:   2015-05-20 14:00:01 +0800
categories: Java
--- 

外观模式（Facade Pattern）**隐藏系统的复杂性，并向客户端提供了一个通用的访问接口**。 这种类型的设计模式属于结构型模式，它向现有的系统添加一个接口，来隐藏系统的复杂性，如下图。

![pic](/images/2015-05-20-facade.png)

外观模式优点也很明显，它使得Client和系统之间的耦合松散，为Client屏蔽了系统的各个子组件，减少了Client访问系统的复杂性。

外观模式和代理模式有一定相似性，都是对外隐藏内部的细节，不同之处在于代理和它代理的对象使用统一接口，而外观模式因为隐藏的是多个子系统多个不同的功能，所以其并不使用统一接口。

举个例子。假设用户进行电视购物，完整购物流程包含查询库存，进行支付，送货等等，如果购物时分别与这些子系统打交道，那么整个系统的复杂性必然会上升，我们使用Facade模式来简化这个处理过程。

* Inventory/Payment/Shipment: 分别代表各个子系统，提供查询库存，进行支付，送货等等服务
* TVShopping: Facade类，包含上面说的各个子系统的对象，对外提供统一方法
* FacadeDemo: 测试类

{% highlight java %} 
public class Inventory {
    public boolean isStockEnough(int buyCount) {
        boolean hasStock = buyCount < 1000;

        if(hasStock)  System.out.println("Inventory checked!");
        else System.out.println("No enough inventory!");

        return hasStock;
    }
}
{% endhighlight %}

{% highlight java %} 
public class Payment {
    public void pay() {
        System.out.println("Payment is done!");
    }
}
{% endhighlight %}

{% highlight java %} 
public class Shipment {
    public void startShipment(){
        System.out.println("Start shipping ...");
    }

    public void endShipment(){
        System.out.println("End shipment!");
    }
}
{% endhighlight %}

{% highlight java %} 
public class TVShopping {
    private final Inventory inventory = new Inventory();
    private final Payment payment = new Payment();
    private final Shipment shipment = new Shipment();

    public boolean hasStock(int buyCount){
        return inventory.isStockEnough(buyCount);
    }

    public void userPay(){
        payment.pay();
    }

    public void shipmentProcess(){
        shipment.startShipment();
        shipment.endShipment();
    }
}
{% endhighlight %}

{% highlight java %} 
public class FacadeDemo {
    public static void main(String[] args) {
        // So, the client just use the TVShopping as Facade
        // and don't need to touch the sub-systems
        TVShopping tvShopping = new TVShopping();

        if (tvShopping.hasStock(15)) {
            tvShopping.userPay();
            tvShopping.shipmentProcess();
        }
    }
}
{% endhighlight %}


测试后输出：

{% highlight java %} 
Inventory checked!
Payment is done!
Start shipping ...
End shipment!
{% endhighlight %}