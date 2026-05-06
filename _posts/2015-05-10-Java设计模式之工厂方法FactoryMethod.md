---
layout: post
title:  "Java设计模式之工厂方法Factory Method"
date:   2015-05-10 09:00:00 +0800
categories: java
--- 

这个模式不用学习，代码写多了，自然就会写出来。

大家应该都写过这种代码，使用if-else或switch控制的业务流，这就是一个最简单的工厂（simple-factory）。比如下面代码，对于给定的不同操作“operation”，返回不同的操作结果“operationResult”：

{% highlight java %}
switch(operation) {
    case "SQL_COUNT":
        operationResult = sqlCount(leftText);
        break;
    case "CHANGE_TO_LIST":
        operationResult = changeToList(leftText);
        break;
    case "COMPARE_LISTS":
        operationResult = compareTwoLists(leftText, rightText);
        break; 
}
{% endhighlight %}
 
当上面的分支代码进一步增多，复杂，我们把operation操作抽象成接口。而每个具体的操作步骤，变成了这个接口的实现。

{% highlight java %}
public interface IOperation {
    String execute(String leftText, String rightText);
}

public class SqlCountOperation implements IOperation {
    @Override
    public String execute(String leftText, String rightText) {
        // 原 sqlCount(leftText) 逻辑
        return "SQL Count Result of " + leftText;
    }
}

public class ChangeToListOperation implements IOperation {
    @Override
    public String execute(String leftText, String rightText) {
        // 原 changeToList(leftText) 逻辑
        return "List Result";
    }
}
{% endhighlight %}

现在，我们定义一个生产这种“operation”的工厂，它往外输出的就是上面定义的IOperation。通常定义一个抽象的工厂和多个具体的工厂。

{% highlight java %}
public interface OperationFactory {
    IOperation createOperation();   //这个接口方法没有参数
}

public class SqlCountFactory implements OperationFactory {
    public IOperation createOperation() { return new SqlCountOperation(); }
}

public class ChangeToListFactory implements OperationFactory {
    public IOperation createOperation() { return new ChangeToListOperation(); }
}
{% endhighlight %}

实际工程中，常结合注册机制来消除最后的 switch。

{% highlight java %}
// 1. 建立类型与工厂的映射 (可以放在静态代码块或配置中)
Map<String, OperationFactory> factoryMap = new HashMap<>();
factoryMap.put("SQL_COUNT", new SqlCountFactory());
factoryMap.put("COMPARE_TO_LISTS", new ChangeToListFactory());

// 2. 动态获取并执行
OperationFactory factory = factoryMap.get(operation);
if (factory != null) {
    IOperation op = factory.createOperation();
    operationResult = op.execute(leftText, rightText);
}
{% endhighlight %}

{% include design-pattern-contents.html %}