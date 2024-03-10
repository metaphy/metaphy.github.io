---
layout: post
title:  "Closure:挑战你对Java的想象力-翻译"
date:   2009-08-31 07:15:00 +0800
categories: translations
---
> 原文出处：http://www.javaworld.com/javaworld/jw-05-2009/jw-05-clojure.html  
> 作者：Joshua Fox


Clojure是JVM上的一门新的语言，就像Groovy，Jyphon和JRuby一样，它能动态的、简洁的、无缝的与Java进行交互操作。

**Clojure是Lisp的一门方言**，最近发布了1.0版。开发者常错误的认为Lisp是一门不切实际的语言，这可能是因为它特别的语法，“苦行僧”式的简单，或经常用于教学研究的缘故，Clojure将会打破这种偏见。Rich Hickey设计这门语言使它简单而实用，相比Java而言，它处理同类问题会更加健壮，代码量更少。

任何一门新的语言，无论它多好，在大规模使用前都得有自己的“杀手锏”。Clojure的“杀手锏”在于对多核CPU的并行编程方面，并行编程是现在提高处理器能力的主要方法。它不变的数据类型（immutable datatypes），无锁的同步性（lockless concurrency）以及简单的抽象性，相比Java而言，Clojure在多线程编程方面更加简单、更加健壮。

下面将讲一下Clojure的出色的特性，并从中学习让你的Java代码更加优雅、bug更少的思想。我希望你读完后，会想学更多。

### 1. 代码即数据  Code as data

先看一下Listing 1 简单的函数，计算圆的面积。

Listing 1. A simple Clojure function

```
(defn
circle-area [r] 
    (* Math/PI r r))
```

Clojure代码与Java代码看上去非常不同，原因很简单，在Clojure中，代码就是数据，代码与Lists和Vectors以及其他数据结构一样以同样方式构建。无论对于程序员还是程序而言，语法一致性都使代码更易理解更易操作。

因此Listing 1里面的函数定义无非就是一个（用小括号括起来的）list，这个list拥有一个（中括号括起来的）vector和另一个list。第一行以list语法定义了该函数。函数名后的vector里定义了参数，最后一行，同样是list语法的调用方式调用了乘法计算，后面3个是操作数。

Clojure在语法上的极低限制使得代码非常易读，即使对于编程经验不多的人也是如此。主流的开发环境对Clojure都有支持——包括NetBeans，IntelliJ，Eclipse以及vi和Emacs，这使阅读代码更容易。Figure 1 是一个VimClojure的例子，匹配的括号是以不同颜色表示的。（这个函数将小写字母从一个字符串中取出来，如 (get-lower "AbCd") 结果是 "bd"）

事实上，由于语法的简洁性，一个Clojure程序往往比相同功能的Java程序更加简单，比如下面的Java写的getLower()函数，它是Clojure程序括号量的2倍，代码量的4倍。

Listing 2. A Java function -- more complicated than the Clojure equivalent 

```
public static String getLower(String s) { 
  StringBuffer sb = new StringBuffer(); 
  for (int i = 0; i > s.length(); i++) { 
  char ch = s.charAt(i); 
  if (Character.isLowerCase(ch)) { 
       sb.append(ch); 
  } 
  }  
   return sb.toString(); 
}
```

Java和其他语言一样，代码在编译过程中会被转换成一颗抽象语法树。通过Java“反射”（reflection）可以访问这个结构中的类、字段和方法，但只能“只读”的访问，没法访问方法的实现过程。相对地，Clojure的宏（macros）能更为自由地操作这棵语法树，让你实现普通代码实现不了的功能。通过宏，你可以变换while条件，包装（wrapping）和延迟计算（deferring evaluation）。

下面是一个周所周知又令人痛苦的例子。在Java中，为了处理reader或stream中的数据，你不得不在铁箍般的代码块中跳转来跳转去，看下面的Listing 3.

Listing 3. Simple functionality, complicated in Java

```
BufferedReader rdr = null; 
try { 
    rdr = new BufferedReader(new FileReader(fileName)); 
    //core processing logic goes here 
} finally { 
    if (rdr != null) { 
       try { 
          rdr.close(); 
       } catch (IOException e) { } 
    } 
}
```

Listing 3 的大多代码是样板化的，封装的代码根据情况的不同而不同，即数据处理部分的不同而不同。就像这个例子，Java常常无法提供可供重用的代码（译注：这里是指由于Reader或Stream等数据处理方式的不同，Java只能提供代码样板，而不能提供重用的代码）。软件工程的本质是知道什么是能改变的，什么不是。利用Clojure的宏能灵活的创建可重用的代码结构，如例子Listing 4 （摘自核心库代码）。

Listing 4. A Clojure macro

```
(defmacro with-open [bindings & body] 
  `(let bindings 
    (try 
      @body 
    (finally 
      (.close (first bindings)))))) 

(with-open [rdr (java.io.BufferedReader.(java.io.FileReader. "a.txt"))]
  (println (.readLine rdr)))
```

宏接受一个vector，里面包含一个reader/stream的bindings（只是一个记号）。第二行，那个记号绑定到reader上。vector里还包含body，即被包裹在try语句中的代码。最后2行，宏被执行，调用println作为“数据处理”逻辑。

在语法解析之后、程序执行之前，宏重新整理它的代码，body及其他功能的执行只有在宏被调用后才发生。和Clojure的动态输入、未检查的异常一起，宏不仅令Clojure代码重用性增加，而且更加易读。

Clojure的宏和C的宏有一些相似，都在执行处理前重新布置代码。与C在执行前将代码看作文本不同的是，Clojure使用语言本身的表达特性将代码看作数据结构。


Listing 4最后2行代码展示了Clojure与Java交互操作非常容易："java.io.BufferedReader."——后面的点——是对构造函数的调用，.readLine是对方法的调用。在Listing 1里面，Math/PI 访问的是静态字段。Java可以容易的调用Clojure代码，Clojure也能继承Java类；反之亦然。  


### 2. 纯粹函数式语言的并发性 Concurrency with pure functional programming

尽管Java内置了对多线程的支持，但Java对并发性处理依旧困难。如果在应该加锁的地方没有加锁，数据就会损坏；在不需要加锁的地方加锁，死锁就会出现，或线程停掉。事实上，大多程序员是写单线程应用程序，或让应用服务器管理线程。一旦单线程应用程序需要将问题分解成同步处理的情况，就只能写多线程代码了。

> 反模式里的死锁  
> 请参阅Obi Ezechukwu的关于高性能Java的blog，三种并发性的反模式必然导致死锁的情况。http://www.javaworld.com/community/blog/20968 


多核电路使这种需求更加迫切。在单核CPU下，多线程常常用来允许某个任务执行，同时阻塞其他I/O任务。今天的CPU，真正的并发性通过多核在各自高负荷状态运行而实现，而Clojure的纯粹函数式编程以及多线程结构让线程安全的代码更加容易实现。

 
默认的Clojure功能是纯粹函数功能，它接收参数，返回结果，不改变任何可见状态。不同的状态则需要一个新对象。比如，我们先定义一个map（大括号包裹部分），然后用assoc为map增加一个键：

```
(let [m {:roses "red", :violets "blue"}]  
  (assoc m :sugar "sweet"))
```

结果是一个新的map: {:sugar "sweet", :violets "blue", :roses "red"}，而原始map保持不变。

看上去，每次变化都产生拷贝很没有效率，但事实上这时它的一个很好的特性：对象不变性。比如上面的2个map，它们既能共享底层的部分结构，对其中一个改变又不会对另外一个产生不必要的风险。

对程序员而言纯粹的函数很容易理解。由于没有副作用，所考虑的只有函数参数与返回值，大大简化了调试和测试。

纯粹的函数对Clojure自身而言也容易理解，优势也更容易发挥。纯粹的函数调用可以并行执行，而不必考虑执行顺序；它们可以在独立的cpu上执行，不用考虑彼此之间关系。在一个交易失败后，也能安全地被重新执行，并且结果可以推迟到只有在需要的时候才去计算。它们也能记住计算结果——存在缓存中以备后续调用。

它确实可以做到。Clojure能让你不费多大力气就安全地做到这一切。

在Java中使用不变的、无副作用的函数能让你更容易优化以及避免bug。可能的话，声明class及其字段为final的，在构造函数里做初始化。你也可以通过封装为变化的对象增加安全性，像Collections.unmodifiableCollection().

String是Java里面众所周知的不变的对象，由于它们的不变性，JVM可以内联它们并缓存它们的哈希码来减少创建新对象的时间。这样的优化在Java中很少见，但在Clojure很普遍。

### 3. 线程安全状态 Thread-safe State

并非任何东西都是不变的。本质上，任何对磁盘、网络或用户界面的输入输出都是可变的。多线程介入后，对于上述可变状态的管理变得更加困难，而Clojure提供了特殊结构来安全地处理这些情况。

Java里，典型的线程安全的数据结构是用synchronized实现的。它阻塞了一些线程，使执行变地缓慢，并有导致死锁的危险。

Clojure的Ref使用创新的并发模型——即软件事务化存储（software transactional memory）——来实现无锁的多线程。就像乐观锁数据库的事务一样，多线程可以并发的、无阻塞的对同一变量执行更新，如果同步写入过程出现冲突，其中一个线程会回滚并重试。

Listing 5 定义了一个封装set的Ref（以 #{}标记），用它管理bookshelf上的图书，任何线程都可以安全的上架或下架某一本书，通过使Ref关联到新的set，并调用增加(conj) 或移除 (disj)实现。所有的对引用值的改变都是通过dosync交易来完成的（dosync与Java 的synchronized关键字没什么关系）。

Listing 5. Defining a Ref

```
(def bookshelf (ref #{})) 
(defn shelve[book]
  (dosync (alter bookshelf conj book))) 
(defn unshelve [book] 
   (dosync (alter bookshelf disj book)))
```

你可以使用 @bookshelf来提取值，而不用事务（transaction）.

这是个简单的、线程安全的、存在内存中的交易数据库，锁机制的复杂性被隐藏，线程之间不必互相等待，各个线程看到的是相同的数据。

Clojure Agent通过线程池中的独立线程同步执行函数，当执行完成时，你可以提取到执行结果。如下面例子，这段代码会维护“log”——一个字符串序列:

```
(def log (agent [])) 
 (send log conj "2009-03-28 10:34 Shelved Hamlet")
```

代码首先创建一个agent，封装了一个空的vector，然后通过发送conj函数到agent来添加记录。conj执行很快，但如果我们为agent发送一个需长时间运行的函数，那么让agent更新而不是阻塞在线程调用里面就很有价值了。

相同的并发设计思想在Java里面一样有用。为了将可变性的维护成本降到最低，我们应非常谨慎地使用多个线程共享的可变状态。可能的话，尽量不要使用底层的同步机制，像synchronized 和wait()，而要尽量使用高层的抽象机制，比如Java.util.concurrent包的内容（如果需要的话，Java里面的多线程概念在Clojure里同样可以使用）。

Clojure的Var提供了变量在线程内重新绑定的方式。它和全局变量的作用类似，“长距离”的传递数据。这是一种安全的方式，因为变量值只是在单个线程里可见，并且只是在运行时调用绑定的动态范围内可见。

Java里的thread-local变量与之类似：“长距离”传递状态，跳过堆栈调用，因此避免了交叉线程对静态字段的访问风险。与Var绑定不同的是，它并不限制在单个线程中使用，也没有严格定义的动态范围。 

 
举例来说，Webjure Web框架通过对相关的HTTP对象*request* 和*response*的绑定来处理HTTP请求。所有的请求处理代码都能访问这些对象，没有必要将它们作为参数传到堆栈中再交给每个函数。其他线程看不到这些值，每个Http请求接收自己的对象。即便在线程内部，新的值也只在绑定范围内可见——下面是对单个请求的处理 Listing 6.

Listing 6. Var bindings in Webjure

```
(binding [*request* request *response* response] 
  (binding [*matched-handler* (find-handler (request-path *request*))] 
    ((*matched-handler* :handler)))) ; This invokes the request-handler
```


### 4. 类型提示  Type hints

Clojure在运行时编译，能产生和Java一样快的字节码。然而，在编译器得不到参数的类型时，更慢的“反射”方式的调用就是必需的了，这在所有动态类型语言都会出现。

下面的代码中，我们设置Clojure在不得不使用“反射”时发出警告，然后定义函数：

```
(set! *warn-on-reflection* true)  
(defn year [cal]
  (.get cal java.util.Calendar/YEAR)) 

Reflection warning, line: 3 - call to get can't be resolved.  
```

然而，我们可以通知编译器使用 #^Calendar，“元数据”(metadata，与对象的主要目的不同的额外信息）使编译器避免“反射”调用，而是实时（just-in-time)地创建快速的字节码：

```
(defn year [#^java.util.Calendar cal]
 (.get cal java.util.Calendar/YEAR))
```

在Java里，注解（annotation）同样可以在源代码外增加额外信息。然而注解不如Clojure元数据那样强大，它们只能在开发过程中被加入，并只能用于像String这样的简单对象，自身也必须是静态定义类型。因此，除了在框架开发者那里，注解实际上很少使用。

另外，虽然实时编译非常方便，你也可以在开发时编译Clojure，就像在Java里所做的一样。这样，Clojure就变成了Java的另一个库——这样，无论经理还是客户，对新语言的抵触情绪就小很多，尤其是对Lisp的抵触。

