import configparser


class ConfigParser(object):
    def __init__(self, conf_path):
        self.fpath = conf_path
        self.cf = configparser.ConfigParser()
        self.cf.read(self.fpath, encoding='UTF-8')

    def write(self):
        filename = open(self.fpath, 'w')
        self.cf.write(filename)
        filename.close()

    # 添加指定的节点
    def add_section(self, section):
         sections = self.cf.sections()
         if section in sections:
             return
         else:
             self.cf.add_section(section)

    # 删除节点
    def remove_section(self, section):
        return self.cf.remove_section(section)

    #返回文件中的所有sections
    def sections(self):
        return self.cf.sections()

    # 获取节点下option对应的value值
    def get(self,section,option):
        return self.cf.get(section,option)

    # 在指定的section下添加option和value值
    def set(self,section,option,value):
        if self.cf.has_section(section):
            self.cf.set(section,option,value)

    #移除指定section点内的option
    def remove_option(self, section,option):
        if self.cf.has_section(section):
            resutl = self.cf.remove_option(section,option)
            return resutl
        return False

    # 返回section内所有的option和value列表
    def items(self, section):
        return self.cf.items(section)

    # 返回section所有的option
    def options(self, section):
        return self.cf.options(section)