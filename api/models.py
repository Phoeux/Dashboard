from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Task(models.Model):
    class Stage(models.TextChoices):
        TO_DO = 'TD', ('To Do')
        IN_DEVELOPMENT = 'InD', ('In development')
        CODE_REVIEW = 'CR', ('Code review')
        READY_FOR_QA = 'RDFQA', ('Ready for QA')
        IN_QA = 'InQA', ('In QA')
        BLOCKED = 'BLCK', ('Blocked')
        READY_FOR_STAKEHOLDER = 'RFS', ('Ready for stakeholder')
        IN_QA_STAKEHOLDER = 'InQAS', ('In QA stakeholder')
        APPROVED = 'APPR', ('Approved')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    end_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=1), blank=True)
    stage = models.CharField(max_length=50, choices=Stage.choices, default=Stage.TO_DO)

    def __str__(self):
        return self.title
