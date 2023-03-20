---
layout: post
title:  "Java设计模式之策略模式Strategy"
date:   2015-05-30 17:10:00 +0800
categories: Java
--- 

策略模式Strategy**定义一系列算法，把它们封装起来，并且使它们可以相互替换**。策略模式应用比较广泛，比如Java AWT的Layout manager，或者Gateway程序中的负载均衡策略等。总之，如果我们需要提供多种策略去实现某一种行为，可以使用策略模式。

还是以负载均衡策略为例做一个分析：
 
* IRule接口，里面只有一个方法，即选取下一个可用的item getNext(current)
* RandomRule，随机策略，从可选item中随机选取一个
* RoundRobinRule，轮询策略，顺序选取item中的下一个
* StrategyDemo，测试类
 
{% highlight java %}
public interface IRule<T> {
    T getNext(T currentItem);
}
{% endhighlight %}

{% highlight java %}
public class RandomRule<T> implements IRule<T>{
    private final List<T> items;
    private final Random rand = new Random();

    public RandomRule(List<T> rules){
        this.items = rules;
    }

    @Override
    public T getNext(T currentRule) {
        int i = rand.nextInt(items.size());
        return items.get(i);
    }
}
{% endhighlight %}


{% highlight java %}
public class RoundRobinRule<T> implements IRule<T>{
    private final List<T> items;

    public RoundRobinRule(List<T> rules){
        this.items = rules;
    }

    @Override
    public T getNext(T currentRule) {
        int currentIndex = 0;
        for (int i = 0; i < items.size(); i++) {
            if (items.get(i).equals(currentRule)) {
                currentIndex = i;
                break;
            }
        }
        int nextIndex = currentIndex == items.size() - 1 ? 0 : currentIndex + 1;
        return items.get(nextIndex);
    }
}
{% endhighlight %}

{% highlight java %}
public class StrategyDemo {
    public static void main(String[] args) {
        List<String> items = new ArrayList<>();
        for (int i = 0; i < 4; i++) {
            items.add("Item " + i);
        }
        IRule<String> roundRobinRule = new RoundRobinRule<>(items);
        test(roundRobinRule, items);

        IRule<String> randomRule = new RandomRule<>(items);
        test(randomRule, items);
    }

    private static void test(IRule<String> rule, List<String> items) {
        System.out.println("Rule: " + rule.getClass().toString());
        String current = items.get(0);

        for (int i = 0; i < 10; i++) {
            String item = rule.getNext(current);
            System.out.println("Pick the item: " + item);
            current = item;
        }
    }
}

{% endhighlight %}
 
程序最终输出如下，我们可以看到，对于轮询方式，item按1，2，3，0的顺序轮替出现，对于随机方式，item以一种随机方式出现。
{% highlight java %}
Rule: class com.test.designpattern.strategy.RoundRobinRule
Pick the item: Item 1
Pick the item: Item 2
Pick the item: Item 3
Pick the item: Item 0
Pick the item: Item 1
Pick the item: Item 2
Pick the item: Item 3
Pick the item: Item 0
Pick the item: Item 1
Pick the item: Item 2
Rule: class com.test.designpattern.strategy.RandomRule
Pick the item: Item 2
Pick the item: Item 1
Pick the item: Item 2
Pick the item: Item 0
Pick the item: Item 0
Pick the item: Item 3
Pick the item: Item 1
Pick the item: Item 1
Pick the item: Item 0
Pick the item: Item 3
{% endhighlight %} 