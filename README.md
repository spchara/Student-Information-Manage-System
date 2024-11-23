## 一、项目概述

### **项目名称**

Student Infomation Manage System

github仓库：[Student Infomation Manage System]()

### **项目目标**

 实现一个管理信息系统，完成教务系统数据库中数据表的设计，使用MySQL实现所设计的数据库，实现数据存储、查询、更新、删除等，并基于所设计的数据库实现一个“学生教务管理系统”

### 技术栈

+ 编程语言：python3.10
+ web框架：django4.2.7
+ 数据库：mysql8.3.5

### 项目结构

```
├─.idea
├─manageSystem
│  ├─migrations
│  │  └─__pycache__
│  └─__pycache__
├─SIMS
│  └─__pycache__
├─static
│  ├─assets
│  │  ├─demo
│  │  └─img
│  ├─css
│  └─js
│  
├─templates
├─README.md
├─manage.py
├─requirements.txt
└─__pycache__

```

## 二、项目需求

### 功能需求

+ 学生、课程、成绩三张表的显示
+ 学生、课程、成绩三张表的查询
+ 学生、课程、成绩三张表的修改
+ 学生、课程、成绩三张表的删除
+ 维持删改过程中的完整性约束

### 非功能需求

+ 高级查询（复合查询、模糊搜索等）
+ 切换删除的模式（restrict / cascade）
+ 服务器部署，可供公网访问

## 三、项目特色

+ 界面美观、用户友好

+ 查询结果分页显示，反馈迅速

    ![image-20241123230918567](README.assets/image-20241123230918567.png)

+ 前端会对填入的字段是否合法进行检测

    ![image-20241123231013434](README.assets/image-20241123231013434.png)

+ 后端对完整性约束进行进一步校验

+ 支持前端静态的模糊搜索

    ![image-20241123231059361](README.assets/image-20241123231059361.png)

+ 部署在服务器上，可以从公网用ip+端口访问

    ![image-20241123231509145](README.assets/image-20241123231509145.png)

    ![image-20241123231918074](README.assets/image-20241123231918074.png)

+ 提供违反完整性约束的报错提示

    ![image-20241123231706160](README.assets/image-20241123231706160.png)

+ 删除模式可以在restrict和cascade中任意切换

    ![image-20241123232101533](README.assets/image-20241123232101533.png)

+ 手机端屏幕适配

    <img src="README.assets/image-20241123232142852.png" alt="image-20241123232142852" style="zoom:67%;" />

## 四、项目演示

1. 项目首页——学生表

![image-20241123233216626](README.assets/image-20241123233216626.png)

表可在底部翻页

2. 学生表高级查询

    ![image-20241123233247901](README.assets/image-20241123233247901.png)

    格式检验

    ![image-20241123233639098](README.assets/image-20241123233639098.png)

    

    复合查询

    ![image-20241123233339636](README.assets/image-20241123233339636.png)

    ![image-20241123233350051](README.assets/image-20241123233350051.png)

    模糊搜索

    ![image-20241123233409975](README.assets/image-20241123233409975.png)

    搜索学号`56`，姓名含`王`

    ![image-20241123233431780](README.assets/image-20241123233431780.png)

3. 课程表记录、高级搜索

    ![image-20241123233612852](README.assets/image-20241123233612852.png)

    先修筛选

    ![image-20241123233721995](README.assets/image-20241123233721995.png)

    ![image-20241123233727601](README.assets/image-20241123233727601.png)

    名字模糊搜索

    ![image-20241123233817150](README.assets/image-20241123233817150.png)

    复合搜索

    ![image-20241123233837673](README.assets/image-20241123233837673.png)

    ![image-20241123233847495](README.assets/image-20241123233847495.png)

4. sc表以及高级搜索

    ![image-20241123233923398](README.assets/image-20241123233923398.png)

    复合搜索

    ![image-20241123234012873](README.assets/image-20241123234012873.png)

    ![image-20241123234024229](README.assets/image-20241123234024229.png)

    ![image-20241123234029133](README.assets/image-20241123234029133.png)

    按成绩排行

    ![image-20241123234053386](README.assets/image-20241123234053386.png)

5. 删除以及插入功能的初始界面，需要先点击选择需要操作的表

    ![image-20241123234114611](README.assets/image-20241123234114611.png)

    ![image-20241123234138935](README.assets/image-20241123234138935.png)

    **学生表：**

    ![image-20241123234156939](README.assets/image-20241123234156939.png)

    ​	**学生表的修改**（主键不可修改，因为认为学号不应该有修改的需求，如果一定需要修改，则自行删除记录并重新插入）

    ​	前端的约束：

    ![image-20241123234232594](README.assets/image-20241123234232594.png)

    ![image-20241123234319055](README.assets/image-20241123234319055.png)

    ![image-20241123234326502](README.assets/image-20241123234326502.png)

    ![image-20241123234334083](README.assets/image-20241123234334083.png)

    ​	学生表的删除

    ​	试图删除某学生

    ​	![image-20241124000012271](README.assets/image-20241124000012271.png)

    报错提醒不能删除，因为被其他记录依赖，违反了参照完整性

    ![image-20241124000042511](README.assets/image-20241124000042511.png)

    找到对应的成绩记录

    ![image-20241124000148784](README.assets/image-20241124000148784.png)

    点击按钮将删除模式改为级联删除：

    ![image-20241124000214616](README.assets/image-20241124000214616.png)

    再次尝试删除，成功

    ![image-20241124000234350](README.assets/image-20241124000234350.png)

    查看刚才的成绩记录，可以看到已经被级联删除

    ![image-20241124000251607](README.assets/image-20241124000251607.png)

    

    ​	课程表的修改

    ​	![image-20241123234512280](README.assets/image-20241123234512280.png)		试图将先修课程改为不存在的课程

    ​	![image-20241123235020334](README.assets/image-20241123235020334.png)

    报错

    ![image-20241123235027990](README.assets/image-20241123235027990.png)

    学分不合法

    ![image-20241123235121572](README.assets/image-20241123235121572.png)

    报错

    ![image-20241123235127887](README.assets/image-20241123235127887.png)

    课时不合法

    ![image-20241123235154639](README.assets/image-20241123235154639.png)

    报错

    ![image-20241123235146153](README.assets/image-20241123235146153.png)

    正常修改

    ![image-20241123235210442](README.assets/image-20241123235210442.png)

    成功

    ![image-20241123235218531](README.assets/image-20241123235218531.png)

    

    课程的删除（当前为级联删除，限制删除不再掩饰）

    ![image-20241123235250454](README.assets/image-20241123235250454.png)

    ![image-20241123235255209](README.assets/image-20241123235255209.png)

    无法再查找到，删除成功

    ![image-20241123235319149](README.assets/image-20241123235319149.png)

    **SC的修改**

    ![image-20241123235344035](README.assets/image-20241123235344035.png)

    仅能修改成绩

    ![image-20241123235404951](README.assets/image-20241123235404951.png)

    ![image-20241123235415565](README.assets/image-20241123235415565.png)

    同样具有检测

    正常修改

    ![image-20241123235434145](README.assets/image-20241123235434145.png)

    可以看到分数被成功修改

    ![image-20241123235512659](README.assets/image-20241123235512659.png)

    

    6. 三张表的删除

        每个字段的格式都有提示，并且有前端的合法性检验

        ![image-20241124000359515](README.assets/image-20241124000359515.png)

        例如：

        ![image-20241124000442711](README.assets/image-20241124000442711.png)

        ![image-20241124000505473](README.assets/image-20241124000505473.png)

        ![image-20241124000510031](README.assets/image-20241124000510031.png)

        其中课程记录的主键无法自行填写，会有后端自动分配课程编号

        例如当前课程最大编号为C048

        ![image-20241124000603760](README.assets/image-20241124000603760.png)

        先修课程为不存在的课程

        ![image-20241124000845609](README.assets/image-20241124000845609.png)

        ![image-20241124000849866](README.assets/image-20241124000849866.png)

        ![image-20241124000920139](README.assets/image-20241124000920139.png)

        成功添加之后，可以看到课程号被自定分配为了递增的`C049`

        ![image-20241124000951979](README.assets/image-20241124000951979.png)

        添加一个不存在的学生的成绩

        ![image-20241124001202830](README.assets/image-20241124001202830.png)

        报错

        ![image-20241124001222509](README.assets/image-20241124001222509.png)

        添加一个正常的学生成绩，但没有先修课

        ![image-20241124001751335](README.assets/image-20241124001751335.png)

        报错提示先修课未修

        ![image-20241124001807399](README.assets/image-20241124001807399.png)

        正常添加

        ![image-20241124001928027](README.assets/image-20241124001928027.png)

        可以看到刚才添加的成绩记录

        ![image-20241124001945472](README.assets/image-20241124001945472.png)

        添加学生记录

        ![image-20241124003804666](README.assets/image-20241124003804666.png)

        报错提醒主键冲突，违反了实体完整性约束

        ![image-20241124003818589](README.assets/image-20241124003818589.png)

        ![image-20241124003828276](README.assets/image-20241124003828276.png)

        换一个主键之后成功添加，之后可以在student表里查看到他

        ![image-20241124003857616](README.assets/image-20241124003857616.png)

        

        

    

​		