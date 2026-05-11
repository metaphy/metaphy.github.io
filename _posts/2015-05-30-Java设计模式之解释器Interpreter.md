---
layout: post
title:  "Java设计模式之解释器Interpreter"
date:   2015-05-30 15:55:00 +0800
categories: java
--- 

呃......这是使用面向对象概念与方式，来实现一个简单语言的解释，就是一个计算机领域字面意义上的“解释器”。与使用C直接进行词法分析、语法分析不同，解释器模式会把“语法规则”转为“类层次结构”。优点是方便进行规则添加。

```
如果一种特定类型的问题出现的频率非常高，
那就值得把该问题的各个实例表达为一种简单语言定义的句子。
...
解释器模式描述了如何为简单语言定义一个文法，
如何在该语言中表示一个句子，
以及如何解释这些句子。
                        ——引自GoF的《设计模式》
```

比如，现在构造一种只有2个布尔运算符(and/or)的语言，及其解释器。其中，变量、And表达式、Or表达式均是单独的类表示，Context存放变量的初始值。
![pic](/images/2015-05-30-interpreter.png)

 

{% highlight java %}
import java.util.HashMap;
import java.util.Map;

// 上下文：存储变量的值
public class Context {
    private Map<String, Boolean> variables = new HashMap<>();

    public void assign(String name, boolean value) {
        variables.put(name, value);
    }

    public boolean getValue(String name) {
        return variables.getOrDefault(name, false);
    }
}

public interface Expression {
    boolean interpret(Context context);
}

public class Variable implements Expression {
    private String name;

    public Variable(String name) {
        this.name = name;
    }

    @Override
    public boolean interpret(Context context) {
        return context.getValue(name);
    }
}

public class AndExpression implements Expression {
    private Expression left;
    private Expression right;

    public AndExpression(Expression left, Expression right) {
        this.left = left;
        this.right = right;
    }

    @Override
    public boolean interpret(Context context) {
        return left.interpret(context) && right.interpret(context);
    }
}

public class OrExpression implements Expression {
    private Expression left;
    private Expression right;

    public OrExpression(Expression left, Expression right) {
        this.left = left;
        this.right = right;
    }

    @Override
    public boolean interpret(Context context) {
        return left.interpret(context) || right.interpret(context);
    }
}
{% endhighlight %}

下面啊构造一个表达式，并解释它的值： a AND b OR c 
{% highlight java %}
public class InterpreterDemo {
    public static void main(String[] args) {
        // 1. 定义上下文并赋值
        Context context = new Context();
        context.assign("a", true);
        context.assign("b", false);
        context.assign("c", true);

        // 2. 构建语法树： (a AND b) OR c
        Expression a = new Variable("a");
        Expression b = new Variable("b");
        Expression c = new Variable("c");

        Expression andExp = new AndExpression(a, b);
        Expression finalExp = new OrExpression(andExp, c);

        // 3. 解释执行
        boolean result = finalExp.interpret(context);
        System.out.println("变量状态：a=true, b=false, c=true");
        System.out.println("表达式 (a AND b) OR c 的计算结果: " + result);

        // 修改上下文再次测试
        context.assign("c", false);
        result = finalExp.interpret(context);
        System.out.println("修改 c=false 后，结果为: " + result);
    }
}
{% endhighlight %} 

输出结果为：
```
变量状态：a=true, b=false, c=true
表达式 (a AND b) OR c 的计算结果: true
修改 c=false 后，结果为: false
```

现在扩展一下，加上not运算。
{% highlight java %}
public class NotExpression implements Expression {
    private Expression right;

    public NotExpression(Expression right) {
        this.right = right;
    }

    @Override
    public boolean interpret(Context context) {
        return !right.interpret(context);
    }
}
{% endhighlight %} 

我们测试一下运行结果： 

{% highlight java %}
    Expression notExp = new NotExpression(b);
    Expression andExp = new AndExpression(a, notExp);
    boolean result = andExp.interpret(context);

    System.out.println("变量状态：a=true, b=false");
    System.out.println("a AND (NOT b) = " + result);
{% endhighlight %}

输出结果为：
```
变量状态：a=true, b=false
a AND (NOT b) 的计算结果: true
```

{% include design-pattern-contents.html %}