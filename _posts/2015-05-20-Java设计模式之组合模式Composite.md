---
layout: post
title:  "Java设计模式之组合模式Composite"
date:   2015-05-20 14:00:00 +0800
categories: Java
--- 

谈到树形层次结构，可能首先想到的就是文件系统，或者一个公司的员工组织结构(普通职员，一线经理，二线经理等等)，组合模式非常适合处理这种树形结构的数据。

组合模式(Composite)就是**将对象组织成树形结构以表示“整体-部分”的层次结构的一个模式**，它可以将“单个对象”和“组合对象”以一种一致方式去看待。 组合模式的核心是一个既可以充当叶子节点又可以充当树杈节点的抽象接口。

我们以一个简单的例子来具体说明，比如有这样一种包裹，它既可以包含具体的商品，也可以包含更小的包裹，更小的包裹也可以继续包含商品和再小的包裹。我们要对这样的包裹进行处理，比如计算里面所有商品的价格，那么使用组合模式如下：

* IPackage: 商品和包裹的接口，既可以充当商品，也可以充当包裹
* Package: 包裹，实现IPackage, 里面包含IPackage类型的List
* Product: 具体的某种商品或产品，实现IPackage
* CompositeDemo: 测试类


{% highlight java %}
public interface IPackage {
    boolean isPackage();
    void add(IPackage... pack);
    List<IPackage> getProducts();
    double price();
}
{% endhighlight %}

{% highlight java %}
public class Package implements IPackage{
    private final List<IPackage> products = new ArrayList<>();

    @Override
    public List<IPackage> getProducts() {
        return products;
    }

    @Override
    public boolean isPackage() {
        return true;
    }

    @Override
    public void add(IPackage... packs) {
        Collections.addAll(products, packs);
    }

    @Override
    public double price() {
        return price(this.products);
    }

    private double price(List<IPackage> products) {
        double sum = 0.0;
        for (IPackage pack: products) {
            if (pack.isPackage()) {
                sum += price(pack.getProducts());
            }
            else {
                sum += pack.price();
            }
        }
        return sum;
    }
}
{% endhighlight %}

{% highlight java %}
public class Product implements IPackage{
    private String name;
    private double price;

    public Product(String name, double price){
        this.name = name;
        this.price = price;
    }

    @Override
    public boolean isPackage(){
        return false;
    }

    @Override
    public void add(IPackage... pack) {

    }

    @Override
    public List<IPackage> getProducts() {
        return null;
    }

    @Override
    public double price() {
        return price;
    }
}
{% endhighlight %}

{% highlight java %}
public class CompositeDemo {
    public static void main(String[] args) {
        IPackage p1a = new Product("p1a", 1.0);
        IPackage p1b = new Product("p1b", 2.0);

        IPackage box1 = new Package();
        box1.add(p1a, p1b);

        System.out.println("Box 1 price: " + box1.price());   // 3.0

        IPackage p2a = new Product("p2a", 5.0);
        IPackage p2b = new Product("p2b", 7.0);

        IPackage box2 = new Package();
        box2.add(box1, p2a, p2b);

        System.out.println("Box 2 price: " + box2.price());   //15.0
    }
}
{% endhighlight %}
测试结果:
```
Box 1 price: 3.0
Box 2 price: 15.0
```