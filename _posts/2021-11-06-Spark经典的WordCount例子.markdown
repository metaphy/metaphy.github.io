---
layout: post
title: "Spark经典的WordCount例子"
date: 2021-11-06 20:00:00 +0800
categories: scala-spark
--- 

这是经典的Spark的WordCount的例子，演示了Spark分布式数据集的诸多方面，以及Map/Reduce的用法。

{% highlight scala %}
import org.apache.spark.sql.{DataFrame, SparkSession}

object WordCount {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().master("local[*]").appName("WordCount").getOrCreate()

    // Below textFile is RDD[String], each line in the txt is a row
    val textFile = spark.sparkContext.textFile("file:///tmp/WordCount.txt")

    val words = textFile
      .flatMap(line => line.split(" "))
      .map((_, 1))    // map(word => (word, 1))  : each word to a (word,1) tuple
      .reduceByKey(_ + _) // reduced by key, the result will be a list of tuple

    words.saveAsTextFile("file:///tmp/saved_word_count")  // RDD will be saved in partitions

    import spark.implicits._
    val df: DataFrame = words.toDF   // with the spark implicits, thd RDD could be easily converted to a DataFrame
    df.show

    spark.stop
  }
}
{% endhighlight %}

打开/tmp/saved_word_count文件夹，里面存了2个partitions的数据。

{% highlight scala %} 
user@/tmp/saved_word_count $ ls
part-00000  part-00001  _SUCCESS

user@/tmp/saved_word_count $ cat part-00000
(Africa,3)
(birds,1)
(means,1)
(surrounding,1)
(is,1)
(have,1)
(region,1)
(one,1)
(jealousy,1)
...
{% endhighlight %}

