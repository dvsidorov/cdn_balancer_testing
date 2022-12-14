
create table if not exists cdn_settings (
    id int auto_increment primary key,
    location varchar(255) not null,
    settings json not null,
    unique key (location)
) engine=INNODB;

insert ignore into cdn_settings (location, settings)
values ('default', '{"CDN_HOST": "cdn.example.ru", "CDN_ORIGINS_RATIO": 20}');
