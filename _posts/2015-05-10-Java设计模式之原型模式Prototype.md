---
layout: post
title:  "Java设计模式之原型模式Prototype"
date:   2015-05-10 17:00:00 +0800
categories: java
--- 

创建型模式的最后一种，原型模式，跟之前几种最大的不一样的地方是，它不通过new来创建实例，而是**通过克隆已有实例来创建**。原型(prototype)在Javascript中也是随处可见，Javascript每个对象都有原型，你可以顺着找，找一条“原型链”。

为什么要用原型方式创建对象？

当使用new()创建对象，需要基于复杂计算或数据库查询等耗时操作时，就用原型来替代。原型的clone()直接在内存中创建对象出来。比如，从现有羊克隆一只羊，远远比从头创建一只羊简单。

{% highlight java %}
// 羊类可以被Clone，需要实现 Cloneable 接口
class Sheep implements Cloneable {
    private String name;

    public Sheep(String name) {
        this.name = name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    @Override
    public Object clone() {
        Object sheep = null;
        try {
            // 调用父类的 clone (浅拷贝)
            sheep = super.clone();
        } catch (CloneNotSupportedException e) {
            e.printStackTrace();
        }
        return sheep;
    }

    @Override
    public String toString() {
        return "Sheep[name='" + name + "', hashCode=" + this.hashCode() + "]";
    }
} 

public class PrototypeDemo {
    public static void main(String[] args) {
        // 1. 创建原型对象：多莉
        Sheep dolly = new Sheep("多莉");
        System.out.println("原始羊: " + dolly);

        // 2. 通过克隆创建新对象
        Sheep dollyClone = (Sheep) dolly.clone();
        
        // 验证结果
        System.out.println("克隆羊: " + dollyClone);
        
        // 验证是否为独立对象
        System.out.println("是否为同一个实例? " + (dolly == dollyClone));
        System.out.println("名字是否相同? " + dolly.getName().equals(dollyClone.getName()));
    }
}
{% endhighlight %}

程序执行后输出：
```
原始羊: Sheep[name='多莉', hashCode=769287236]
克隆羊: Sheep[name='多莉', hashCode=935044096]
是否为同一个实例? false
名字是否相同? true
```

{% include design-pattern-contents.html %}