from django.db import models
from superadminpoint.models import CustomUser as User


# Create your models here.
class TaskModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assignedto = models.ForeignKey(User, on_delete=models.CASCADE,related_name='assigned_tasks')
    duedate = models.DateField()
    status = models.CharField(max_length=20,default='Pending')
    completionreport = models.TextField(default='No Report', null=True, blank=True)
    workedhours = models.IntegerField(null=True,blank=True)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervisor_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + self.assignedto.username

