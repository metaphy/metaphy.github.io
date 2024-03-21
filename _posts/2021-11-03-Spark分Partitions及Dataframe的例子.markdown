---
layout: post
title: "Spark分Partitions及Dataframe的例子"
date: 2021-11-03 21:59:00 +0800
categories: spark
--- 

这个例子很简单，但我也想了半天。有如下的RDD，每行表示某个ID的进账（Inc='I')或出账（Inc='E')金额，统计各个ID的合计金额分别是多少。

{% highlight javascript %}
  [
    {"ID": 1, "Inc": "I", "Amount":102.0},
    {"ID": 2, "Inc": "I", "Amount":300.0},
    {"ID": 3, "Inc": "I", "Amount":220.02},
    {"ID": 1, "Inc": "E", "Amount":2.00},
    {"ID": 2, "Inc": "E", "Amount":100.0},
    {"ID": 3, "Inc": "I", "Amount":79.98}
  ]
{% endhighlight%}

下面是程序，需要注意的是，按ID repartition($"ID") 后，Dataframe.rdd.partitions.size固定是200，因为distinct ID不足200个，所有有大量空的partitions.

{% highlight scala %}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.{DataFrame, SparkSession}

object MyDataMigration {
  val spark = SparkSession.builder().master("local[*]").appName("MyDataMigration").getOrCreate()
  val JSON_FOLDER = "src/main/resources/"

  def main(args: Array[String]): Unit = {
    import spark.implicits._

    val df = getDataFrameFromJSON("MyDataMigration.json")
    
    try {
      val result = df
        .withColumn("RealAmount", expr("case when Inc = 'I' then Amount else 0 - Amount end"))
        .drop("Amount")
        .drop("Inc")
        .repartition($"ID") 
        .groupBy($"ID")
        .agg(sum("RealAmount").as("Total"))
        .sort($"ID")

      result.show
    }
    finally {
      spark.stop
    }
  }

  def getDataFrameFromJSON(file: String): DataFrame = {
    spark.read.option("multiline", "true").json(JSON_FOLDER + file)
  }
}

{% endhighlight %}
