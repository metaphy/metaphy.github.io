---
layout: post
title:  "Java设计模式之迭代器Iterator"
date:   2015-05-30 16:40:00 +0800
categories: java
--- 

迭代器(Iterator)主要解决如何在不提供数据内部构造的情况下遍历数据。JDBC的ResultSet 就是一个迭代器，典型的方法就是：hasNext() 和 next(). 


![pic](/images/2015-05-30-iterator.png) 


{% highlight java %} 
// 迭代器接口（也可以直接使用 java.util.Iterator，这里为了模式清晰单独定义）
interface MyIterator<T> {
    boolean hasNext();
    T next();
}

// 聚合接口（提供创建迭代器的方法）
interface Aggregate<T> {
    MyIterator<T> createIterator();
}

// 具体的书籍类
class Book {
    private String name;

    public Book(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}

class BookShelf implements Aggregate<Book> {
    private Book[] books;
    private int index = 0;

    public BookShelf(int maxSize) {
        books = new Book[maxSize];
    }

    public void addBook(Book book) {
        if (index < books.length) {
            books[index++] = book;
        } else {
            System.out.println("书架已满，无法添加新书");
        }
    }

    public int getLength() {
        return index;
    }

    @Override
    public MyIterator<Book> createIterator() {
        return new BookShelfIterator();
    }

    private class BookShelfIterator implements MyIterator<Book> {
        private int cursor = 0;

        @Override
        public boolean hasNext() {
            return cursor < index;
        }

        @Override
        public Book next() {
            if (hasNext()) {
                return books[cursor++];
            }
            return null;
        }
    }
}

// 测试代码
public class IteratorPatternDemo {
    public static void main(String[] args) {
        BookShelf bookShelf = new BookShelf(4);
        bookShelf.addBook(new Book("Java编程思想"));
        bookShelf.addBook(new Book("设计模式"));
        bookShelf.addBook(new Book("算法导论"));
        bookShelf.addBook(new Book("Effective Java"));

        MyIterator<Book> iterator = bookShelf.createIterator();
        while (iterator.hasNext()) {
            Book book = iterator.next();
            System.out.println("书籍: " + book.getName());
        }
    }
}

{% endhighlight %} 

输出结果为：
```
书籍: Java编程思想
书籍: 设计模式
书籍: 算法导论
书籍: Effective Java
```
 

{% include design-pattern-contents.html %}