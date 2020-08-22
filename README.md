# 在线词典项目实现

### 1. 界面分为一级界面和二级界面(注册和登录)
        功能:  1. 注册 (一级界面，注册成功后为二级界面即为登录界面)
               2. 登录 (需要用户名和密码)
               3. 查单词 (用SQL语句对单词表进行查询)
               4. 查看历史记录 (创建记录表为10条记录再多就删第十一条)
               5. 注销 (返回到一级界面)
### 2. 技术分析
       并发模型：多线程并发模型
       界面跳转：分为两个函数符合条件时调用不同的函数
       存储：数据库 dict库  user表  历史记录表
        user表
              id:primary key auto_increment
              name:varchar(30)  unique(唯一索引)
              password:varchar(30) not null
              register time ：？？？
        历史记录表
              id：primary key auto_increment
              name:varchar(30) not null
              word:varchar(50) not null
              find time:(默认为当前时间)
               