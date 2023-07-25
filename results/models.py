from django.db import models
from django.utils import timezone
from users.models import CustomUser

class Result(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    objFunction = models.CharField(max_length=255)
    operation = models.CharField(max_length=255, default='Maximizar')
    constraints = models.JSONField()
    solution = models.JSONField()
    resultDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str({
            'objFunction': self.objFunction,
            'operation': self.operation, 
            'constraints': self.constraints, 
            'solution': self.solution,
            'resultDate': self.resultDate
        })