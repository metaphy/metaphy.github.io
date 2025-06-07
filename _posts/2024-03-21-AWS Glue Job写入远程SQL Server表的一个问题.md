---
layout: post
title:  "AWS Glue Job写入远程SQL Server表的一个问题"
date:   2024-03-21 12:00:00 +0800
categories: spark
--- 

我一直在想，程序员的价值是什么？或者问题再小点，程序员的时间花在哪？程序员累，累在什么地方？ 

前段时间，我需要在AWS的Glue上写一个pyspark的Job，程序非常简单，把一个表的数据从一个数据库全量更新到另外一个数据库。我这边作为源数据，数据库一直都是AWS上的redshift，虽然对redshift，mysql都做过，但当听说对方是SQL Server后，凭着职业直觉，心中还是隐隐有点担忧。 

程序确实非常简单，100行左右的代码，很多还是可以复用的之前Job的code，写完后测试，在我测试环境中完全没有问题，于是开心的等待对方数据库ready。

对方数据库和表建好之后，拿到credentials，就把数据推送过去了，发现数据有点小问题，就又推送了一遍，告诉对方推送过去的数据量，让他们检查一下。 

不出意外的，意外发生了，对方告诉我收到了2n条数据，多了一份。于是，我们开头所说的时间花费，开始花了。

1. 我先仔细检查了代码，并未有什么问题，又在我测试数据库测试了一遍，也没有问题，每次刷新数据前都能清空之前数据，并不会让数据成倍增加

2. 又做了些工作，检查对方数据库中表的数据量，作为我这边的验证手段

3. 再次检查代码，在数据sink前有一个preactions的参数，用来清空target表，看来是这个地方出问题了 
	```
	  glueContext.write_dynamic_frame.from_jdbc_conf( \
			frame = df_1, catalog_connection = db_link_1, \
			connection_options = {"preactions":"truncate table table_1", \
			"dbtable": "table_1", "database": "db_1"}, \
			redshift_tmp_dir = some_tmp_dir)
	``` 

4. 因为程序并没有报错，所以只能模糊描述问题，在网上搜索答案。首先找到了stackoverflow上有人遇到个一模一样的问题，他的目标数据库是MySQL，只是光有问题没有答案。还有其他人有类似问题，但都没提供解决方案。  
    `https://stackoverflow.com/questions/61611845/preactionstruncate-table-is-not-working-in-gluecontext-write-dynamic-frame-fr`

    `https://repost.aws/questions/QUR4mvZ1NUQvKof115XSOxPg/aws-glue-s3-to-redshift-etl-job-ignored-preactions-and-postactions`

5. 查官方文档, 尝试把上面的from_jdbc_conf 改成 from_catalog，没有用，至此决定使用其他方案

6. 尝试加载SQL server驱动，使用SQL去执行，失败

7. 突然灵机一动，为什么不用DataFrame 去写？知道AWS Glue 有多坑了吗，它整了个自己的dynamic frame，简写也是df

8. 于是把df_1 转成 dataframe_df_1, 直接写：
	```
	dataframe_df_1.write.format("jdbc") \
		.option("url", JDBC_URL) \
		.option("dbtable", table_1) \
		.option("user", user_1) \
		.option("password", pwd_1) \
		.option("driver", SQL_SERVER_DRIVER) \
		.mode("overwrite") \
		.save()
	```
9. 因为SQL Server的JDBC URL 跟其他的还不一样，所以这个地方也卡了一下，到最终问题解决，已经过去4个多小时。所以时间都花在了哪？就是花在这里。

10. 总结：这里首先要吐槽一下AWS Glue的代码，烂的莫名其妙，就看上面的函数方法，write_dynamic_frame.from_jdbc_conf，write不是对应的to吗？write...from是几个意思？到底是读是写？说实话，当初看到这个方法的时候差点被气笑了。从这个事情中，最终得到的教训就是一定要做数据验证，验证数据数量，验证每个字段的值等等；还有就是一定要远离这种垃圾的库，这种不成熟的东西包含特别多的坑。

11. 2024-12-14更新。最近发现这个很可能是id权限不够的问题。id的delete权限和truncate权限一般不是一个，比如redshift上delete是单独权限，而truncate权限等同于表owner权限。查了一下，SQL Server上对表delete和truncate操作也是分开的授权。如果真是这个问题，那么dynamic_frame在写数据的时候遇到没有权限的问题不报错而继续执行，也是非常奇葩了。

	```
	--SQL Server delete: 
	GRANT DELETE ON qa.test1 TO user1;

	-- truncate authorization	
	GRANT ALTER ON qa.test1 TO user1;
	```
