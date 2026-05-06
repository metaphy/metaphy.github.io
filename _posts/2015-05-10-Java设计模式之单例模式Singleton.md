---
layout: post
title:  "Java设计模式之单例模式Singleton"
date:   2015-05-10 14:00:00 +0800
categories: java
--- 

这应该是最简单的一个模式了，不用特意的学习，写的多了，自然就会用到。简而言之，单例(Singleton)就是一个在面向对象编程范式下的**全局变量**，它在程序的整个生命周期中只存在一份，并能够在不同模块、类或函数中被随时访问。因此，它要求：

1. 构造函数私有化，确保只有一个对象实例可以被创建

2. 提供全局访问点（如下的静态方法）

{% highlight java %}
public class DatabaseConnection {
    // 使用 volatile 关键字防止指令重排
    private static volatile DatabaseConnection instance;

    private DatabaseConnection() {
        // ...
    }

    public static DatabaseConnection getInstance() {
        // 第一层检查：如果实例已经存在，直接返回，不进入同步块
        if (instance == null) {
            synchronized (DatabaseConnection.class) {
                // 第二层检查：进入同步块后，再次确认是否被其他线程创建
                if (instance == null) {
                    instance = new DatabaseConnection();
                }
            }
        }
        return instance;
    }
}
{% endhighlight %}

{% include design-pattern-contents.html %}