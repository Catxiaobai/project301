from django.db import models

# Create your models here.


# 人员
class Personnel(models.Model):
    person_name = models.TextField(default='', unique=True)
    person_age = models.IntegerField(default='')
    person_gender = models.TextField(default='')
    person_account = models.TextField(default='')
    person_password = models.TextField(default='')
    person_authority = models.IntegerField(default='')

    def to_dict(self):
        return {
            'person_id': self.id,
            'person_name': self.person_name,
            'person_age': self.person_age,
            'person_gender': self.person_gender,
            'person_account': self.person_account,
            'person_password': self.person_password,
            'person_authority': self.person_authority,
        }


# 项目
class Item(models.Model):
    item_name = models.TextField(default='', unique=True)
    item_content = models.TextField(default='')
    item_introduction = models.TextField(default='')
    item_date = models.DateTimeField(default='')
    item_leader = models.ForeignKey(Personnel, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            'item_id': self.id,
            'item_name': self.item_name,
            'item_content': self.item_content,
            'item_introduction': self.item_introduction,
            'item_date': self.item_date,
            # 'item_leader': self.item_leader,
        }


# 设计准则
class DesignCriteria(models.Model):
    name = models.TextField(default='', unique=True)
    content = models.TextField(default='')
    group = models.TextField(default='')
    type = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'group': self.group,
            'type': self.type,
        }


# 分析规则
class AnalysisRules(models.Model):
    group = models.TextField(default='')
    type = models.TextField(default='')
    name = models.TextField(default='', unique=True)
    content = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'group': self.group,
            'type': self.type,
        }