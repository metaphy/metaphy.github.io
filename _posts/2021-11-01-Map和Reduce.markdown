---
layout: post
title: "Map和Reduce"
date: 2021-11-01 22:33:00 +0800
categories: scala
--- 

这半年多来，对Scala/Spark接触很多，而越学习，越感到之前的无知，所谓“学然后知不足”。函数式编程的思维方式和之前Java的或者说面向对象的思维方式有很大不同，而思维惯性又难克服，必须有意识地使用这样风格去思考。

举个简单的例子： 查找某个文件夹下所有文件内容，将所有"db.xxx"的内容中的xxx找出来。

我熟悉Java，之前使用Java实现过，不外是递归遍历根文件夹，对找到的文件逐行扫描，碰到就找出来。用Scala实现的时候遇到一些困难，主要是思考方式的挑战。最终解决的时候，算是彻底明白了Map和Reduce，并震惊于这种解决方式的简练和优雅！

{% highlight scala %}
object Sample extends App{
  val dir = new File("src/main/")

  println (s"Find all matches from the src folder: ${dir.getAbsolutePath}")

  getFiles(dir)             //fild all files of this folder
  .flatMap(findTableNames)  //onefile -> List  so we need to use flatMap instead of map
  .distinct
  .sorted
  .foreach(println)

  /**
   * get all files
   */
  def getFiles(file: File): Array[File] = {
    val files = file.listFiles()
      .filter(! _.isDirectory)
      .filter(_.getName.endsWith(".scala"))

    files ++ file.listFiles().filter(_.isDirectory).flatMap(getFiles)
  }

  /**
   * get the matches from one file
   */
  def findTableNames(file: File): List[String] = {
    val source = Source.fromFile(file, "UTF-8")
    val lines = source.mkString
    source.close

    //match "db.xxx" until a space or , or newline 
    val pattern = new Regex("(?<=db\\.)[a-zA-Z0-9_]+(?=[,\\s\\n])")    
    pattern.findAllIn(lines).toList.distinct
  }
}

{% endhighlight %}
