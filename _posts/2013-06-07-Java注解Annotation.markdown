---
layout: post
title: "Java注解Annotation"
date:  2013-06-07 12:55:00 +0800
categories: Java
---

Java注解是Java 5的一个重要的新特性，它是一种元数据形式，可以为程序添加语义化信息(比如Spring @Component用来标记一个需要注册到容器的类)；这些信息可以被编译器、解析器或框架等通过反射方式来解析和使用。 

Java内置3种标准注解:
- @Override
- @Deprecated
- @SuppressWarnings

以及4种元注解(就是加在注解上的注解):
- @Target
- @Retention
- @Documented
- @Inherited 

下面举个简单例子解释一下注解的编写以及解析用法，主要有3个类，其中我们先编写UseCase类，这个是一个注解

{% highlight java %}@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface UseCase {
    int id();
    String description() default "";
}
{% endhighlight %}

其次是一个具体类，是一个输入检查工具，InputUtil，除了它自身的方法外，我们给方法上加上之前定义的注解，这样我们可以在之后对方法做进一步解析或处理
{% highlight java %}
public class InputUtil {
    @UseCase(id = 1, description = "Check the user's input")
    public boolean isValidInput(String input) {
        return input == null || input.trim().length() > 0;
    }

    @UseCase(id = 2, description = "Encrypt the password with Base64")
    public String encryptPasswd(String passwd) {
        return Base64.getEncoder().encodeToString(passwd.getBytes());
    }

    public String reverseString(String str) {
        return new StringBuilder(str).reverse().toString();
    }
}
{% endhighlight %}

最后是一个UseCaseTracker，就是用这个类，我们解析InputUtil类上的UseCase 注解：
{% highlight java %}
public class UseCaseTracker {
    public static void trackUseCase(Class<?> clazz) {
        for (Method method: clazz.getDeclaredMethods()){
            UseCase uc = method.getAnnotation(UseCase.class);
            if (uc != null) {
                System.out.println("Found UseCase id: " + uc.id() 
                    + " and description: " +uc.description());
            }
        }
    }


    public static void main(String[] args) {
        trackUseCase(InputUtil.class);
    }
}
{% endhighlight %}

程序输出如下：
```
Found UseCase id: 2 and description: Encrypt the password with Base64
Found UseCase id: 1 and description: Check the user's input
```

