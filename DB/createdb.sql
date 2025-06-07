create table file_tag
(
    tag_id  int auto_increment
        primary key,
    user_id int         not null,
    tag     varchar(50) not null,
    constraint uk_user_tag
        unique (user_id, tag)
);


create table files
(
    file_id     int auto_increment
        primary key,
    user_id     int                                not null,
    filename    varchar(255)                       not null,
    file_path   varchar(255)                       not null,
    file_type   varchar(50)                        not null,
    upload_time datetime default CURRENT_TIMESTAMP null,
    size        bigint                             not null,
    tag         varchar(40)                        null,
    description varchar(200)                       null
);

create table photo_tag
(
    tag_id  int auto_increment
        primary key,
    user_id int         not null,
    name    varchar(10) not null,
    tag     varchar(10) null,
    constraint uk_user_tag
        unique (user_id, tag)
);

create table share_links
(
    link_id    int auto_increment
        primary key,
    user_id    int                                null,
    created_at datetime default CURRENT_TIMESTAMP null,
    share_path varchar(255)                       null comment '分享文件物理路径',
    file_name  varchar(255)                       null comment '原始文件名',
    url        varchar(255)                       null,
    qrcodePath varchar(255)                       null
);

create table users
(
    user_id       int auto_increment
        primary key,
    telephone     varchar(20)                        not null,
    username      varchar(50)                        not null,
    email         varchar(100)                       not null,
    password_hash varchar(255)                       not null,
    storage_quota bigint   default 10737418240       null,
    used_storage  bigint   default 0                 null,
    created_at    datetime default CURRENT_TIMESTAMP null,
    constraint email
        unique (email),
    constraint telephone
        unique (telephone)
);