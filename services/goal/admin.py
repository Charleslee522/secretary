from datetime import timedelta
from django import forms
from django.db import models
from django.db.models import (
    F,
    Q,
)
from django.contrib import admin
from django.utils import timezone
from services.goal.models import (
    ActionItem,
    Goal,
    Memory,
)


class ActionItemInline(admin.TabularInline):
    model = ActionItem
    extra = 0

    fields = [
        'uuid',
        'summary',
        'goal',
        'priority',
        'deadline',
        'original_estimate',
        'end_at',
    ]

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


# Register your models here.
@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):

    list_display = [
        'code',
        'summary',
        'description',
    ]

    inlines = [
        ActionItemInline,
    ]

    ordering = ('code',)


class GoalChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return obj.represent

def goal(obj):
    return obj.goal.represent

def summary(obj):
    return obj.represent

def done(modeladmin, request, queryset):
    queryset.update(end_at=timezone.now())
done.short_description = "Done!"

def done_with_one_pomo(modeladmin, request, queryset):
    queryset.update(
        end_at=timezone.now(),
        elapsed_pomodoro=F('elapsed_pomodoro') + 1,
    )
done_with_one_pomo.short_description = "Done in 1 pomo!"

class StatusFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'end_at'

    def lookups(self, request, model_admin):
        return (
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('done_yesterday', 'Done Yesterday'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'in_progress':
            return queryset.filter(end_at__isnull=True)
        if self.value() == 'done':
            return queryset.filter(end_at__isnull=False)
        if self.value() == 'done_yesterday':
            now = timezone.now()
            hour = timezone.localtime().hour
            yesterday_begin = now - timedelta(hours=hour+24)
            yesterday_end = now - timedelta(hours=hour)

            return queryset.filter(
                end_at__gte=yesterday_begin,
                end_at__lte=yesterday_end,
            )

class CreatedAtFilter(admin.SimpleListFilter):
    title = 'CreatedAt'
    parameter_name = 'created_at'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            now = timezone.now()
            hour = timezone.localtime().hour
            today_begin = now - timedelta(hours=hour)

            return queryset.filter(
                created_at__gte=today_begin,
            )


@admin.register(ActionItem)
class ActionItemAdmin(admin.ModelAdmin):

    list_display = (
        summary,
        goal,
        'priority',
        'deadline',
        'elapsed_deep_work',
        'elapsed_pomodoro',
        'end_at',
    )

    list_editable = (
        'deadline',
        'elapsed_deep_work',
        'elapsed_pomodoro',
        'end_at',
    )

    actions = [
        done,
        done_with_one_pomo,
    ]

    list_filter = (
        StatusFilter,
        CreatedAtFilter,
    )

    ordering = (
        'end_at',
        'priority',
        'deadline',
        'goal',
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == 'goal':
            return GoalChoiceField(queryset=Goal.objects.all().order_by('code'))

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ActionItemAdmin, self).get_form(request, obj, **kwargs)
        return form


class ReviewFilter(admin.SimpleListFilter):
    title = 'Review'
    parameter_name = 'reviewed_at'

    def lookups(self, request, model_admin):
        return (
            ('review', 'Review'),
        )

    def __get_filter(self, queryset, hours):
        now = timezone.now()
        return queryset.filter(
            created_at__lte=now - timedelta(hours=hours),
            reviewed_at__lte=now - timedelta(hours=hours),
        )

    def queryset(self, request, queryset):
        if self.value() == 'review':

            f_never = queryset.filter(reviewed_at__isnull=True)
            f_after_one_day = self.__get_filter(queryset, 24)
            f_after_one_week = self.__get_filter(queryset, 7*24)
            f_after_one_month = self.__get_filter(queryset, 30*24)

            return f_never | f_after_one_day | f_after_one_week | f_after_one_month


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):

    list_display = [
        'short_uuid',
        'summary',
        'description',
        'created_at',
        # 'reviewed_at',
    ]

    list_editable = [
        # 'reviewed_at',
    ]

    list_filter = [
        ReviewFilter,
    ]

    def short_uuid(self, obj):
        return str(obj.uuid)[:4]
    short_uuid.short_description = 'short uuid'
    short_uuid.allow_tags = True

    def admin_get_variants(self, obj):
        return linebreaks(obj.description)
