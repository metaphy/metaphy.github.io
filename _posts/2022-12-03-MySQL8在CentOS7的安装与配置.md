---
layout: post
title: "MySQL8在CentOS7的安装与配置."
date: 2022-12-03 21:11:00 +0800
categories: Java-spring
--- 
MySQL在CentOS 7上的安装请参考：https://zhuanlan.zhihu.com/p/623778183
本人安装的是 Server version: 8.0.33 MySQL Community Server - GPL

1. 启动后，查看临时密码
```grep 'temporary password' /var/log/mysqld.log```

2. 登录后，更改临时密码
```mysql -u root -p```
```> ALTER USER 'root'@'localhost' IDENTIFIED BY 'xxxxxxxx';```

3. 我们最好不要直接使用root用户，所以需要创建一个其他用户

```> use mysql```
```> select user, host from user;```
```> CREATE USER 'peter'@'localhost' IDENTIFIED BY 'xxxxxxx';```
```> GRANT ALL PRIVILEGES ON *.* TO 'peter'@'localhost' WITH GRANT OPTION;```
```> FLUSH PRIVILEGES;```
```> UPDATE user SET host = '%' where user = 'peter';```

4. CentOS上查看防火墙状态, 开放端口以及增加端口等等操作
```systemctl status firewalld```
```firewall-cmd --list-ports```
```firewall-cmd --zone=public --add-port=3306/tcp --permanent```
```firewall-cmd --reload```

5. 这样我们就可以使用peter用户进行远程连接了。另外，mysql的配置文件通常是/etc/my.cnf,有些版本可能需要手工配置才允许远程访问
```cat /etc/my.cnf```
比如增加下面这行，或者删除skip-network这行等等
```bind-address=0.0.0.0``` 


 