--创建user表
create table user(
id int primary key auto_increment,
name varchar(30) not null,
password char(20) not null
);

--创建history表
create table history (
id int primary key auto_increment,
word varchar(30),
time datetime default now(),
user_id int,
foreign key (user_id) references user(id)
);

