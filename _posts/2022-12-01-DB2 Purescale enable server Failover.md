---
layout: post
title: "DB2 Purescale enable server Failover"
date: 2022-12-01 19:35:00 +0800
categories: database
--- 

我们的DB2 PS在云上本身就是cluster 部署，有2个members，故且叫做test1.ab.member 和 test2.ab.member, 两者的端口分别是50000和60000，数据库名都是SAMPLEDB。DB2 PS 本身是支持一个叫做ACR（Automatic Client Reroute）的特性的，即在一个member出现故障时候，Client自动连到另一个member上。下面介绍的是JDBC的连接方式。

在经过多次试验之后，发现下面模式是最快Fail over的，我本地的测试是在test1 故障之后，Springboot Hikaripool只用了4 sec 就切换到test2 member上 
{% highlight java %}  
jdbc:db2://test1.ab.member:50000/SAMPLEDB:currentSchema=SCHE1;sslConnection=true;sslTrustStoreLocation=1.jks;enableSeamlessFailover=true;enableClientAffinitiesList=1;clientRerouteAlternateServerName=test2.ab.member;clientRerouteAlternatePortNumber=60000;
{% endhighlight %}


而不加这一句enableClientAffinitiesList=1，最终也可以fail over 到test2 member成功，但是花了46 sec，比上面的配置花费时间远远要多：
{% highlight java %}  
jdbc:db2://test1.ab.member:50000/SAMPLEDB:currentSchema=SCHE1;sslConnection=true;sslTrustStoreLocation=1.jks;enableSeamlessFailover=true;clientRerouteAlternateServerName=test2.ab.member;clientRerouteAlternatePortNumber=60000;
{% endhighlight %}

另外，如果不使用enableSeamlessFailover=true，而是使用enableSysplexWLB=true的话，这种Failover 就会失败，报DB Connection连不上的错误；这个地方花了好长时间试验。
{% highlight java %}  
jdbc:db2://test1.ab.member:50000/SAMPLEDB:currentSchema=SCHE1;sslConnection=true;sslTrustStoreLocation=1.jks;enableSysplexWLB=true;clientRerouteAlternateServerName=test2.ab.member;clientRerouteAlternatePortNumber=60000;
{% endhighlight %}

所以，遇到问题一定要从根本的官方文档上去查，而不能似是而非地躲过去。另外不得不吐槽一句，IBM的文档水平跟MS的文档简直天上地下的区别，微软的文档写的非常贴心。



参考： https://www.ibm.com/support/pages/faq-how-configure-jdbc-driver-automatic-client-re-route