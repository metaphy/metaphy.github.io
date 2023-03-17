---
layout: post
title:  "Java设计模式之命令模式Command"
date:   2015-05-30 12:30:00 +0800
categories: Java
--- 

命令模式(Command Pattern)是一种行为设计模式，**它可将请求转换为一个包含与请求相关的所有信息的独立对象。该转换让你能根据不同的请求将方法参数化、 延迟请求执行或将其放入队列中， 且能实现可撤销操作**。

命令模式非常好理解，下面我们以台灯和台灯遥控器为例子，看看如何实现。

* Command 接口，只有execute()一个方法
* Light, 台灯，有开/关/改变颜色等方法，这是命令最终的执行者
* LightOnOffCommand, 开关灯的命令，实现Command execute()方法，这个类需要包含Light对象，所以其实execute()时候是调用Light的turnOn和turnOff
* LightColorCommand, 改变灯光颜色的命令，同样包含Light对象，并最终调用Light的changeColor()方法
* RemoteController, 遥控器，包含LightOnOffCommand和LightColorCommand等命令，遥控器的所有命令都对Command object下达
* CommandDemo, 测试类

![pic](/images/2015-05-30-command.png)

{% highlight java %} 
public interface Command {
    void execute();
}
{% endhighlight %}
{% highlight java %} 
public class Light {
    private boolean isOn = false;
    private static final String[] colors = {"Red", "Blue", "Green", "Yellow"};

    public boolean isLightOn() {
        return isOn;
    }

    public void turnOn(){
        isOn = true;
        System.out.println("Light is On...");
    }
    public void turnOff(){
        isOn = false;
        System.out.println("Light is Off!");
    }

    public void changeColor(){
        if (isOn) {
            int colorIndex = new java.util.Random().nextInt(4);
            System.out.println("-- Change the color to " + colors[colorIndex]);
        }
    }
}
{% endhighlight %}
{% highlight java %} 
public class LightOnOffCommand implements Command {
    private Light light;

    public LightOnOffCommand(Light light){
        this.light = light;
    }

    @Override
    public void execute() {
        if(light.isLightOn()){
            light.turnOff();
        } else {
            light.turnOn();
        }
    }
}
{% endhighlight %}
{% highlight java %} 
public class LightColorCommand implements Command {
    private Light light;

    public LightColorCommand(Light light){
        this.light = light;
    }

    @Override
    public void execute() {
        light.changeColor();
    }
}
{% endhighlight %}
{% highlight java %} 
public class RemoteController {
    private Command onOffCommand;
    private Command colorCommand;

    public void setOnOffCommand(Command onOffCommand) {
        this.onOffCommand = onOffCommand;
    }

    public void setColorCommand(Command colorCommand) {
        this.colorCommand = colorCommand;
    }

    public void pressOnOffButton(){
        onOffCommand.execute();
    }

    public void changeColor(){
        colorCommand.execute();
    }
}
{% endhighlight %}
{% highlight java %} 
public class CommandDemo {
    public static void main(String[] args) {
        Light tableLamp = new Light();
        Command onOffCommand = new LightOnOffCommand(tableLamp);
        Command colorCommand = new LightColorCommand(tableLamp);

        RemoteController remoteController = new RemoteController();
        remoteController.setOnOffCommand(onOffCommand);
        remoteController.setColorCommand(colorCommand);

        remoteController.pressOnOffButton();
        remoteController.changeColor();
        remoteController.pressOnOffButton();
        remoteController.changeColor();
        remoteController.pressOnOffButton();
        remoteController.changeColor();
    }
}
{% endhighlight %}

程序执行结果：
```
Light is On...
-- Change the color to Red
Light is Off!
Light is On...
-- Change the color to Yellow
```
