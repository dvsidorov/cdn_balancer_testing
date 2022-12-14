# О проекте

    CDN BALANCER SERVICE - Тестовое задание “Сервис-балансировщик видео-трафика”
## Старт проекта on localhost
~~~
docker-compose up db-mysql
docker exec -i balancer.db mysql -ubalancer -pbalancer balancer_db < ./database/create_tables.sql
docker-compose down; docker-compose pull; docker-compose up -d;
~~~


## Нагрузочное тестирование (Apache Bench)
~~~
apt-get install apache2-utils
ab -n 100000 -c 100 http://localhost:8000/?video=http://s1.origin-cluster.ru/video/1488/xcg2djHckad.m3u8
~~~ 

### Prerequisites

* docker
* docker-compose >= 3.6
