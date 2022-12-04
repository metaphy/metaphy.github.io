---
layout: post
title:  "对JavaScript中原型的理解"
date:   2007-06-18 18:31:00 +0800
categories: Javascript
---

从纯粹的面向对象思想(Java思想)向Javascript语言面向对象思想的转化，经历沉痛而惨烈。Javascript中对象和类的概念转化悄然不动声色，让人迷糊。有时候，对Java理解得越清楚，对Javascript理解起来就越费劲。尤其对Javascript的原型对象的理解颇费功夫。

按照定义，每个javascript对象都有一个原型对象（简称原型），这个原型是由该对象的构造函数所定义（javascript自动创建的），并且对象继承原型的所有属性和方法（函数），比如 一个String对象 的原型为 String.prototype ，如果我们想要给String类添加方法，可以这样做（比如添加常用的trim()方法）：

{% highlight javascript %}
String.prototype.trim = function (){   
  return this.replace(/(^\s*)|(\s*$)/g, "");   
}  
{% endhighlight %}

这将为所有String对象添加trim()方法！这个特性令人相当惊讶，因为这破坏了封装性，就好像在Java中你可以对String类直接进行修改一样。而且function() 可以当作数据来给左操作数赋值（而不仅仅是当作动作），也跟Java非常地不同。

对于Javascript内部类都可以这么改，对于自定义类当然可以这么改，如：

 
{% highlight javascript %}
 
function Circle(x,y,r){   
  this.x = x;   
  this.y = y;   
  this.r = r;   
  //this.prototype = {constructor : this};     /*这句代码可以看作是隐含存在的，因为javascript 中“类”的定义和函数的定义结构上没有差异，所以可以说，所有函数都隐藏有这样一个属性。*/   
}   
{% endhighlight %}


然后，我们给原型加一个得到面积的方法：

 {% highlight javascript %}
Circle.prototype.area = function(){   
  return this.r * this.r * 3.14159 ;   
}  
{% endhighlight %}

可以这样使用：

{% highlight javascript %}
var circ = new Circle(0,0,2) ;   
alert(circ.area()) ;  
{% endhighlight %}

当然，我们也可以在类中很轻松的定义我们想要实现的方法，如，还是上面那个求圆面积：

{% highlight javascript %}
function Circle(x,y,r){   
  this.x = x;   
  this.y = y;    
  this.r = r ;   
  this.area = function (){   
    return this.r * this.r * 3.14159 ;    
  }   
}   
//调用:
var circ = new Circle(0,0,2) ;   
alert(circ.area()) ;   
{% endhighlight %}

两者的调用代码完全一样，那为什么要使用原型呢？我感觉主要是为了解决对内部类型的继承问题，也就是说当你无法修改String的构造函数而想要让所有String实例都具有某一方法的时候，你可以用这个prototype；或者说，你用这个prototype来模拟实现String类的子类，达到对父类进行扩展的目的。

 

参考：

JavaScript权威指南（第四版）

 