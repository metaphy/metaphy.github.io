---
layout: post
title: "Spring Cron表达式"
date: 2022-11-30 11:20:10 +0800
categories: Java-spring
--- 

Spring的Cron表达式如下：
{% highlight java %} 
@Scheduled(cron = "* * * * * *")
{% endhighlight %}

其中，参数从左到右依次代表Second, Minute, Hour, Day, Month, Weekday. 
![image](/images/2022-11-30_1.png)

各个参数的关系应该是AND的关系。如果进一步考虑的话，因为某天和星期几都是对日期的限制，而有时我们不需要这2个条件**同时**进行限制，或者说这2个条件同时起作用的话会导致我们不想要的结果，所以我们要忽略某个条件，这时需要用"?"；问号表示这个条件被忽略掉。

我们以官方给的最后一个例子说明。
![image](/images/2022-11-30_2.png)

{% highlight java %} 
0 0 0 25 12 ？
{% endhighlight %}
这个表示12月25日0点0分0秒，最后的问号表示不考虑它是星期几这个条件；并且最后的星期几不要用"\*"。
