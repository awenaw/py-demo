
server.py 的行为很古怪，ipv6访问，页面一直转圈，新开一个v4的页面访问，v6突然就不转圈了，很古怪；
ipv6server.py是监听了8000端口；
dual_port_server.py是监听了80和8000端口。

2025 年 9 月 24 日
经过多次验证， ipv6server.py是表现良好的，ipv6允许，全球可达的访问。
运行：python3 ipv6server.py
端口：900