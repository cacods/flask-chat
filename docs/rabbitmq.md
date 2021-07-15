# Install and setting up RabbitMQ

- Install on Debian based systems:

```bash
$ sudo apt install rabbitmq-server
$ sudo rabbitmqctl add_user admin admin
$ sudo rabbitmqctl set_user_tags admin administrator
$ sudo rabbitmqctl add_vhost local_vhost
$ sudo rabbitmqctl set_permissions -p local_vhost admin ".*" ".*" ".*"
$ sudo rabbitmq-plugins enable rabbitmq_management
```

After last command, RabbitMQ runs a web interface on `127.0.0.1:15672`. The 
credentials to login are Username: admin, Password: admin. 