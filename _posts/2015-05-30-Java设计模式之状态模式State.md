---
layout: post
title:  "Java设计模式之状态模式State"
date:   2015-05-30 17:00:00 +0800
categories: java
--- 

状态模式(State)是一种行为设计模式，让你能**在一个对象的内部状态变化时改变其行为，使其看上去就像改变了自身所属的类一样**。状态模式和有限状态机的概念紧密相关，当我们可以使用状态机来描述一个事情的时候，通常可以采用状态模式。 

同命令模式相比较，一般而言命令模式接口只有一个方法，而状态模式接口有多个方法，并且大多有返回值。

比如我们以自动售货机来举例，我们先画它的状态图：

![pic](/images/2015-05-30-state1.png)

我们可以依据上面的状态机，来抽象出一个State接口，该接口有3个具体的实现类，这些实现类均引用售货机VendingMachine对象，可以方便了解状态转换时的上下文信息。同时，在VendingMachine类还引用各个状态类，这样在VendingMachine对外暴露方法时，其实用的是State具体类的方法。 

* State接口，有各个状态可能用到的方法
* ReadyState / PendingPaymentState / DeliverProductState，各个State的具体实现
* VendingMachine，自动售货机，对外暴露操作售货机的操作方法，其实方法都是需要调用State的方法。售货机还保有一个currentState对象，在调用个State对象的方法时，需要及时转换当前状态
* StateDemo，测试类

![pic](/images/2015-05-30-state2.png)



{% highlight java %}
public interface State {
    String selectItem();
    boolean pay(double amount);
    void dispense(String item);
}
{% endhighlight %}

{% highlight java %}
public class ReadyState implements State{
    private static final String[] products = {"Coke", "Water", "Coffee", "GreenTea", "Juice"};
    private Random rand = new Random();
    private VendingMachine vendingMachine;

    public ReadyState(VendingMachine vendingMachine) {
        this.vendingMachine = vendingMachine;
    }

    @Override
    public String selectItem() {
        return products[rand.nextInt(5)];
    }

    @Override
    public boolean pay(double amount) {
        System.out.println("Invalid operation");
        return false;
    }

    @Override
    public void dispense(String item) {
        System.err.println("Invalid operation: dispense");
    }
}
{% endhighlight %}


{% highlight java %}
public class PendingPaymentState implements State{
    private VendingMachine vendingMachine;

    public PendingPaymentState(VendingMachine vendingMachine) {
        this.vendingMachine = vendingMachine;
    }

    @Override
    public String selectItem() {
        System.err.println("Invalid operation: selectItem");
        return null;
    }

    @Override
    public boolean pay(double amount) {
        // each item price is $3.00
        return Math.abs((amount - 3.00)) < 0.00000001;
    }

    @Override
    public void dispense(String item) {
        System.err.println("Invalid operation: dispense");
    }
}
{% endhighlight %}

{% highlight java %}
public class DeliverProductState implements State{
    private VendingMachine vendingMachine;

    public DeliverProductState(VendingMachine vendingMachine) {
        this.vendingMachine = vendingMachine;
    }

    @Override
    public String selectItem() {
        System.err.println("Invalid operation: selectItem");
        return null;
    }

    @Override
    public boolean pay(double amount) {
        return false;
    }

    @Override
    public void dispense(String item) {
        System.out.println("  --" + item + " has been delivered!");
    }
}
{% endhighlight %}

{% highlight java %}
public class VendingMachine {
    private final State readyState;
    private final State pendingPaymentState;
    private final State deliverProductState;
    private State currentState;
    private String currentItem;

    public VendingMachine() {
        readyState = new ReadyState(this);
        this.currentState = readyState;
        this.pendingPaymentState = new PendingPaymentState(this);
        this.deliverProductState = new DeliverProductState(this);
    }

    public String selectItem() {
        if (currentState == readyState) {
            currentItem = currentState.selectItem();
            System.out.println(currentItem + " is selected!");

            currentState = pendingPaymentState;
            return currentItem;
        } else {
            System.err.println("  --Current item is: " + currentItem + "; you are not in ReadState so you cannot select another one!");
            return null;
        }
    }

    public boolean pay(double amount) {
        if (currentState == pendingPaymentState && currentState.pay(amount)) {
            currentState = deliverProductState;
            System.out.println("  --Payment is done.");
            return true;
        } else {
            System.out.println("  --Payment Failed!");
            return false;
        }
    }

    public void dispenseItem() {
        if (currentState == deliverProductState) {
            currentState.dispense(currentItem);
            currentState = readyState;
        }
    }
}

{% endhighlight %}

{% highlight java %}
public class StateDemo {
    public static void main(String[] args) {
        VendingMachine vendingMachine = new VendingMachine();

        String item = vendingMachine.selectItem();    // somebody select one item and state transmit to Pending payment
        if (item != null) {
            if(vendingMachine.pay(3.00)) {
                vendingMachine.dispenseItem();
            }
        }

        item = vendingMachine.selectItem();
        if (item != null) {
            if (vendingMachine.pay(0.00)) {
                vendingMachine.dispenseItem();
            }
        }

        item = vendingMachine.selectItem();
        if (item != null) {
            if (vendingMachine.pay(3.00)) {
                vendingMachine.dispenseItem();
            }
        }
    }
}
{% endhighlight %}

Fianally the output is
{% highlight java %}
Coke is selected!
  --Payment is done.
  --Coke has been delivered!
Coffee is selected!
  --Payment Failed!
  --Current item is: Coffee; you are not in ReadState so you cannot select another one!
{% endhighlight %} 