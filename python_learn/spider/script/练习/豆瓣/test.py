class Student:  # 定义Student类
    def __init__(self, name):  # 定义构造方法
        self.name = name
        print("姓名为%s的对象被创建！" % self.name)

    def __len__(self):
        return len(self.name)


ha = Student("haha")
print(ha.__len__())
