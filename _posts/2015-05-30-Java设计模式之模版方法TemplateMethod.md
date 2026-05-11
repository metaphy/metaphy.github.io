---
layout: post
title:  "Java设计模式之模版方法Template Method"
date:   2015-05-30 21:10:00 +0800
categories: java
--- 

模版方法是除了“解释器模式”之外的另外一个“类级别行为模式”，其他的都是“对象级行为模式”。模版方法是对“算法”的抽象。简单的说，模版中有负责定义“算法框架”的部分，有负责实现具体算法步骤的部分。 

下面以电商的订单处理流程来演示。我们把整个流程分为4步：

1. 校验订单信息并扣减库存（通用逻辑，使用具体方法实现）
2. 计算折扣/支付金额（不同订单类型计算逻辑不同，由子类实现）
3. 支付扣款（支付方式不同，如微信、支付宝、银行卡等，由子类实现）
4. 发送通知（通用逻辑，使用具体方法实现）

其中，第1和4步是通用步骤，第2和3步需根据不同场景进行定制。

{% highlight java %}
/**
 * 1. 抽象类：定义订单处理的骨架和模板方法
 */
public abstract class AbstractOrderProcessor { 
    /**
     * 模板方法：定义了处理订单的算法骨架。
     * 通常设置为 final，防止子类重写修改整个流程顺序。
     */
    public final void processOrder(String orderId) {
        // 步骤1：校验订单信息并扣减库存（公共逻辑）
        validateAndDeductStock(orderId); 
        
        // 步骤2：计算折扣金额（定制逻辑，由子类实现）
        double finalPrice = calculateDiscount(orderId);
        
        // 步骤3：支付扣款（定制逻辑，由子类实现）
        pay(orderId, finalPrice);
        
        // 步骤4：发送通知（带钩子的逻辑）
        if (needNotification()) {   // 钩子方法控制是否发送
            sendNotification(orderId);
        }
    }

    // ---------- 具体方法（公共逻辑） ----------
    private void validateAndDeductStock(String orderId) {
        System.out.println("[公共逻辑] 1.订单检查完成，库存已扣减。订单号：" + orderId );
    }
 
    private void sendNotification(String orderId) {
        System.out.println("[公共逻辑] 4.发送通知：订单 " + orderId + " 处理完成，已发送通知。");
    }

    // ---------- 抽象方法（定制逻辑，必须由子类实现） ----------
    protected abstract double calculateDiscount(String orderId);
    
    protected abstract void pay(String orderId, double finalPrice);

    // ---------- 钩子方法（提供默认实现，子类可选择重写来控制流程） ----------
    protected boolean needNotification() {
        return true; 
    }
}

/**
 * 2. 具体子类：普通商品订单（支付宝支付，无折扣）
 */
public class NormalOrderProcessor extends AbstractOrderProcessor { 
    @Override
    protected double calculateDiscount(String orderId) {
        System.out.println("[定制逻辑] 2.普通订单无折扣，按原价计算。");
        return 100.0; // 假设原价100
    }

    @Override
    protected void pay(String orderId, double finalPrice) {
        System.out.println("[定制逻辑] 使用支付宝支付，订单：" + orderId + "，金额：" + finalPrice);
    }
}

/**
 * 3. 具体子类：促销秒杀订单（银行卡支付，打折，且不需要发送通知）
 */
public class SeckillOrderProcessor extends AbstractOrderProcessor { 
    @Override
    protected double calculateDiscount(String orderId) {
        System.out.println("[定制逻辑] 2.秒杀订单打6折！");
        return 100 * 0.6; 
    }

    @Override
    protected void pay(String orderId, double finalPrice) {
        System.out.println("[定制逻辑] 3.使用银行卡支付，订单：" + orderId + "，金额：" + finalPrice);
    }

    // 重写钩子方法，控制算法流程
    @Override
    protected boolean needNotification() {
        return false; // 秒杀订单不发送通知
    }
}

/**
 * 4. 客户端测试代码
 */
public class TemplateMethodDemo {
    public static void main(String[] args) {
        System.out.println("========== 处理普通订单 ==========");
        AbstractOrderProcessor normalProcessor = new NormalOrderProcessor();
        normalProcessor.processOrder("ORD-1001");
        System.out.println("订单已完成！");

        System.out.println("\n========== 处理秒杀订单 ==========");
        AbstractOrderProcessor seckillProcessor = new SeckillOrderProcessor();
        seckillProcessor.processOrder("SK-223001");
        System.out.println("订单已完成！");
    }
} 
{% endhighlight %}


``` 
========== 处理普通订单 ==========
[公共逻辑] 1.订单检查完成，库存已扣减。订单号：ORD-1001
[定制逻辑] 2.普通订单无折扣，按原价计算。
[定制逻辑] 3.使用支付宝支付，订单：ORD-1001，金额：100.0
[公共逻辑] 4.发送通知：订单 ORD-1001 处理完成，已发送通知。
订单已完成！

========== 处理秒杀订单 ==========
[公共逻辑] 1.订单检查完成，库存已扣减。订单号：SK-223001
[定制逻辑] 2.秒杀订单打6折！
[定制逻辑] 3.使用银行卡支付，订单：SK-223001，金额：60.0
订单已完成！
```



{% include design-pattern-contents.html %}