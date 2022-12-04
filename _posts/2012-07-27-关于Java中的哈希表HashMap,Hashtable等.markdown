---
layout: post
title:  "关于Java中的哈希表HashMap,Hashtable等"
date:   2012-07-27 10:10:00 +0800
categories: Java
---
**首先来了解一下基本概念**

所谓哈希表(Hash Table，又叫散列表)，是存储键值对(Key-value)的表，它有下面的特性：它能把关键码(key)映射到表中的一个位置来直接访问，这样访问速度就非常快。其中的映射函数称为散列函数(Hash function)。

1. 对于关键字key, f(key)是其存储位置，f则是散列函数

2. 如果key1 != key2 但是 f(key1) == f(key2),这种现象称为冲突(collison)。冲突不可避免，这是因为key值无限而表容量总是有限(*见篇末思考题*)。我们追求的是对任意关键字，散列到表中的地址概率是相等的，这样的散列函数为均匀散列函数。

**散列函数有多种**

1. 直接定址法：取关键字或关键字的某个线性函数值为散列地址。即H(key)=key或H(key) = a·key + b，其中a和b为常数（这种散列函数叫做自身函数）

2. 数字分析法

3. 平方取中法

4. 折叠法

5. 随机数法

6. 除留余数法：取关键字被某个不大于散列表表长m的数p除后所得的余数为散列地址。即 H(key) = key MOD p, p<=m。不仅可以对关键字直接取模，也可在折叠、平方取中等运算之后取模。对p的选择很重要，一般取素数或m，若p选的不好，容易产生同义词。

可以想像，当表中的数据个数接近表的容量大小时，发生冲突的概率会明显增大，因此，在“数据个数/表容量”到达某个比例的时侯，需要扩大表的容量，这个比例称为“装填因子”(load factor).

**解决冲突主要有下面两类方法**

1. 分离链接法，就是对hash到同一地址的不同元素，用链表连起来，也叫拉链法

2. 开放定址法，如果地址有冲突，就在此地址附近找。包括线性探测法，平方探测法，双散列等


**然后来看一下Java的Hashtable实现**

java.util.Hashtable的本质是个数组，数组的元素是linked的键值对（单向链表）。

{% highlight java %}
private transient Entry[] table; // Entry数组  
{% endhighlight %}

{% highlight java %}
private static class Entry<K,V> implements Map.Entry<K,V> {  
    int hash;  
    K key;  
    V value;  
    Entry<K,V> next; // Entry此处表明是个单链表  
    ...  
}  
{% endhighlight %}

我们可以使用指定数组大小、装填因子的构造函数，也可以使用默认构造函数，默认数组的大小是11，装填因子是0.75.
{% highlight java %}
public Hashtable(int initialCapacity, float loadFactor) {  
...  
}  
public Hashtable() {  
    this(11, 0.75f);  
}  
{% endhighlight %}

当要扩大数组时，大小变为oldCapacity * 2 + 1，当然这无法保证数组的大小总是素数。
来看下其中的元素插入的方法，put方法：
{% highlight java %}
public synchronized V put(K key, V value) {  
    // Make sure the value is not null  
    if (value == null) {  
        throw new NullPointerException();  
    }  
      
    // Makes sure the key is not already in the hashtable.  
    Entry tab[] = table;  
    int hash = key.hashCode();  
    int index = (hash & 0x7FFFFFFF) % tab.length;  
    for (Entry<K, V> e = tab[index]; e != null; e = e.next) {  
        if ((e.hash == hash) && e.key.equals(key)) {  
            V old = e.value;  
            e.value = value;  
            return old;  
        }  
    }  
}  
{% endhighlight %}

Java中Object类有几个方法，其中一个是hashCode(), 这说明Java中所有对象都具有这一方法，调用可以得到对象自身的hash码。对表的长度取余得址，并在冲突位置使用链表。

HashMap与Hashtable的功能几乎一样。但HashMap的的初始数组大小是16而不是11，当要扩大数组时，大小变为原来的2倍，默认的装填因子也是0.75. 其put方法如下，对hash值和index都有更改：
{% highlight java %}
public V put(K key, V value) {  
    if (key == null)  
        return putForNullKey(value);  
    int hash = hash(key.hashCode());  
    int i = indexFor(hash, table.length);  
    for (Entry<K, V> e = table[i]; e != null; e = e.next) {  
        Object k;  
        if (e.hash == hash && ((k = e.key) == key || key.equals(k))) {  
            V oldValue = e.value;  
            e.value = value;  
            e.recordAccess(this);  
            return oldValue;  
        }  
    }  
  
    modCount++;  
    addEntry(hash, key, value, i);  
    return null;  
}  

  
/** 
 * Applies a supplemental hash function to a given hashCode, which 
 * defends against poor quality hash functions.  This is critical 
 * because HashMap uses power-of-two length hash tables, that 
 * otherwise encounter collisions for hashCodes that do not differ 
 * in lower bits. Note: Null keys always map to hash 0, thus index 0. 
 */  
static int hash(int h) {  
    // This function ensures that hashCodes that differ only by  
    // constant multiples at each bit position have a bounded  
    // number of collisions (approximately 8 at default load factor).  
    h ^= (h >>> 20) ^ (h >>> 12);  
    return h ^ (h >>> 7) ^ (h >>> 4);  
}  
  
/** 
 * Returns index for hash code h. 
 */  
static int indexFor(int h, int length) {  
    return h & (length-1);  
}  
{% endhighlight %}


**再看看其它开源的Java库中的Hashtable**

目前存在多个开源的Java Collection实现，各个目的不同，侧重点也不同。以下对开源框架中哈希表的分析主要从几个方面入手：默认装填因子和capacity扩展方式，散列函数以及解决冲突的方法。

1. Trove - Trove库提供一套高效的基础集合类。

gnu.trove.set.hash.THashMap的继承关系：THashMap -> TObjectHash -> THash，其内部的键和值使分别用2个数组表示。其解决冲突的方式采用开放寻址法，开放寻址法对空间要求较高，因此其默认装填因子load factor是0.5，而不是0.75. 下面看代码一步步解释：

默认初始化，装填因子0.5，数组大小始从素数中取，也就是始终是素数。
{% highlight java %}
/** the load above which rehashing occurs. */  
public static final float DEFAULT_LOAD_FACTOR = 0.5f;  
  
protected int setUp( int initialCapacity ) {  
    int capacity;  
    capacity = PrimeFinder.nextPrime( initialCapacity );  
    computeMaxSize( capacity );  
    computeNextAutoCompactionAmount( initialCapacity );  
    return capacity;  
}  

{% endhighlight %}

然后看其put方法，insertKey(T key)是其散列算法，hash码对数组长度取余后，得到index，首先检查该位置是否被占用，如果被占用，使用双散列算法解决冲突，也就是代码中的insertKeyRehash()方法。
{% highlight java %}
public V put(K key, V value) {  
    // insertKey() inserts the key if a slot if found and returns the index  
    int index = insertKey(key);  
    return doPut(value, index);  
}  
  
  
protected int insertKey(T key) {  
    consumeFreeSlot = false;  
  
    if (key == null)  
        return insertKeyForNull();  
  
    final int hash = hash(key) & 0x7fffffff;  
    int index = hash % _set.length;  
    Object cur = _set[index];  
  
    if (cur == FREE) {  
        consumeFreeSlot = true;  
        _set[index] = key;  // insert value  
        return index;       // empty, all done  
    }  
  
    if (cur == key || equals(key, cur)) {  
        return -index - 1;   // already stored  
    }  
  
    return insertKeyRehash(key, index, hash, cur);  
}  

{% endhighlight %}



2. Javolution - 对实时、内置、高性能系统提供Java解决方案

Javolution中的哈希表是jvolution.util.FastMap, 其内部是双向链表，默认初始大小是16，扩展时变为2倍。并没有显式定义load factor, 从下面语句可以知道，其值为0.5
{% highlight java %}
if (map._entryCount + map._nullCount > (entries.length >> 1)) { // Table more than half empty.  
    map.resizeTable(_isShared);  
}  
{% endhighlight %}

再看下put函数，比较惊人的是其index和slot的取得，完全是用hashkey移位的方式取得的，这样同时计算了index和避免了碰撞。
{% highlight java %}
private final Object put(Object key, Object value, int keyHash,  
        boolean concurrent, boolean noReplace, boolean returnEntry) {  
    final FastMap map = getSubMap(keyHash);  
    final Entry[] entries = map._entries; // Atomic.  
    final int mask = entries.length - 1;  
    int slot = -1;  
    for (int i = keyHash >> map._keyShift;; i++) {  
        Entry entry = entries[i & mask];  
        if (entry == null) {  
            slot = slot < 0 ? i & mask : slot;  
            break;  
        } else if (entry == Entry.NULL) {  
            slot = slot < 0 ? i & mask : slot;  
        } else if ((key == entry._key) || ((keyHash == entry._keyHash) && (_isDirectKeyComparator ? key.equals(entry._key)  
                : _keyComparator.areEqual(key, entry._key)))) {  
            if (noReplace) {  
                return returnEntry ? entry : entry._value;  
            }  
            Object prevValue = entry._value;  
            entry._value = value;  
            return returnEntry ? entry : prevValue;  
        }  
    }  
    ...  
}      

{% endhighlight %}


*思考题*


如果表容量无限，元素个数也无限，表是否必然能一一对应地包含所有元素？