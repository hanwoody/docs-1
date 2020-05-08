# 在centos上部署rtframe及相关组件，需要注意几个问题


* docker run -w映射目录容器内的程序对映射的目录没有写权限，这个和selinux鉴权有关，最直接的方式就是关闭它
修改/etc/selinux/config,将SELINUX=enforcing 修改为 SELINUX=disabled，重启生效

* nsqadmin的管理功能使用不正常，不能正确解析生成的节点域名，这个和firewalld.service有关，最直接的方式就是关闭

systemctl disable firewalld.service

