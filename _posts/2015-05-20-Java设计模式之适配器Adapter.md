---
layout: post
title: "Java设计模式之适配器Adapter"
date: 2015-05-20 08:00:01 +0800
categories: java
--- 

适配器(Adapter)，顾名思义，就是把不同的接口或类“适配”到一起，让原本因接口不匹配而无法协同工作的组件能够顺畅地协作。比如家庭用电和家用电器电压不匹配时，变压器干的事情那样。

常见的，给手机充电。需要把普通电压220V转为手机适用的5V电压。

{% highlight java %}
// 1. Target (目标接口)：手机期待的 5V 电压
interface MobileVoltage {
    int output5V();
}

// 2. Adaptee (被适配者)：普通的 220V 电压
class FamilyVoltage {
    public int output220V() {
        return 220;
    }
}

// 3. Adapter (适配器)：将 220V 转换为 5V
class PowerAdapter implements MobileVoltage {
    private FamilyVoltage familyVoltage;

    public PowerAdapter(FamilyVoltage familyVoltage) {
        this.familyVoltage = familyVoltage;
    }

    @Override
    public int output5V() {
        int src = familyVoltage.output220V();
        System.out.println("适配器：检测到输入电压 " + src + "V");
        int dst = src / 44;
        System.out.println("适配器：转换完成，输出电压 " + dst + "V");
        return dst;
    }
}

// 4. Client (客户端)：手机
public class AdapterDemo {
    public static void main(String[] args) {
        System.out.println("--- 开始充电 ---");

        FamilyVoltage v220 = new FamilyVoltage();

        MobileVoltage adapter = new PowerAdapter(v220);

        int finalVoltage = adapter.output5V();

        System.out.println("手机状态：已接收 " + finalVoltage + "V，充电中...");
    }
}
{% endhighlight %}

输出结果:
```
--- 开始充电 ---
适配器：检测到输入电压 220V
适配器：转换完成，输出电压 5V
手机状态：已接收 5V，充电中...
```

{% include design-pattern-contents.html %}