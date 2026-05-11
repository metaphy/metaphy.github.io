---
layout: post
title:  "Java设计模式之备忘录模式Memento"
date:   2015-05-30 16:10:00 +0800
categories: java
--- 

备忘录模式(Memento)，用于暂存一个对象的状态，以及可以恢复对象状态。比如，编辑器中的Undo，或游戏中的存档。

下面例子，使用游戏存档，演示如何应用这个模式。 

最先考虑的，肯定是存档信息本身，我们称呼它为一个“GameSave”. 例子中，我们只保存一个游戏属性，即玩家的生命值。

{% highlight java %}
public class GameSave {
    private final int playerLives;

    public GameSave(int playerLives) {
        this.playerLives = playerLives;
    }

    public int getPlayerLives() { return playerLives; }
}
{% endhighlight %}

其次，是当前游戏，即我们要暂存东西的“原本”，它知道自己当前状态，并可以暂存/恢复这一状态。

{% highlight java %}
public class GameCharacter {
    private int playerLives;

    public GameCharacter(int playerLives){
        this.playerLives = playerLives;
    }

    public GameSave save() {
        System.out.println("进度保存中... 当前生命: " + playerLives);
        return new GameSave(playerLives);
    }

    public void restore(GameSave memento) {
        this.playerLives = memento.getPlayerLives();
        System.out.println("存档回滚成功！当前生命: " + playerLives);
    }

    // 模拟游戏进行
    public void fight() {
        if (this.playerLives - 10 > 0) {
            this.playerLives -= 10;
        } else {
            this.playerLives = 0;
        }

        System.out.println("经历了一场恶战，生命剩余: " + playerLives);
    }
}
{% endhighlight %}

最后，对游戏存档的管理：
{% highlight java %}
import java.util.Stack;

public class SaveManager {
    private final Stack<GameSave> saveHistory = new Stack<>();

    public void addSave(GameSave save) {
        saveHistory.push(save);
    }

    public GameSave getLatestSave() {
        return saveHistory.pop();
    }

    public static void main(String[] args) {
        GameCharacter hero = new GameCharacter(12);
        SaveManager manager = new SaveManager();

        // 存档
        manager.addSave(hero.save());

        // 激战
        hero.fight();
        System.out.println("糟糕，快挂了！");

        // 从存档恢复
        hero.restore(manager.getLatestSave());
    }
}
{% endhighlight %}

可以看到，上面例子中，有3个核心角色：

1. 备忘录Memento (即游戏存档)

2. 发起者Originator (游戏的角色)

3. 调用者Caretaker (玩家，对存档进行管理)
 
备忘录模式的潜在问题是，如果需要备忘的对象状态非常复杂，则状态保存需要占用过多资源。此时需要考虑把状态文件化保存。

![pic](/images/2015-05-30-memento.png)


游戏输出：
```
进度保存中... 当前生命: 12
经历了一场恶战，生命剩余: 2
糟糕，快挂了！
进度回滚成功！当前生命: 12
```
{% include design-pattern-contents.html %}