import uuid
from django.db import models
from django.utils import timezone


# Create your models here.
class Goal(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)

    code = models.CharField(max_length=20)
    summary = models.CharField(max_length=80)
    description = models.CharField(max_length=200, blank=True, null=True)

    deadline = models.DateField(null=True, blank=True, default=timezone.now)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'secretary_goal'

    @property
    def represent(self):
        return f'[{self.code}] {self.summary}'

class ActionItem(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    summary = models.CharField(max_length=80)
    goal = models.ForeignKey(
        Goal,
        models.PROTECT,
        related_name='action_items',
        related_query_name='action_item',
    )

    priority = models.IntegerField(default=0)

    original_estimate = models.DecimalField(default=0.5, max_digits=8, decimal_places=1)
    current_estimate = models.DecimalField(default=0.5, max_digits=8, decimal_places=1)
    elapsed_deep_work = models.PositiveSmallIntegerField(default=0)
    elapsed_pomodoro = models.PositiveSmallIntegerField(default=0)

    deadline = models.DateField(null=True, blank=True, default=timezone.now)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'secretary_action_item'

    @property
    def represent(self):
        brain = '🧠' * self.elapsed_deep_work
        tomato = '🍅' * self.elapsed_pomodoro
        return f'{self.summary} {brain} {tomato}'


class Memory(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    summary = models.CharField(max_length=80)
    description = models.CharField(max_length=1000, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now=True)
    # reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'secretary_memory'


class History(models.Model):
    memory = models.ForeignKey(
        Memory,
        models.PROTECT,
        related_name='histories',
        related_query_name='history',
    )
    reviewed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'secretary_memory_history'
