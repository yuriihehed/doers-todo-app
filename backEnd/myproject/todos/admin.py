from django.contrib import admin
from .models import Team, TeamMember, Category, ToDo

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'get_members')  # Display members in admin
    search_fields = ('name', 'created_by__username')
    list_filter = ('created_at',)
    filter_horizontal = ('members',)  # Allows selecting multiple users easily

    def get_members(self, obj):
        return ", ".join([user.username for user in obj.members.all()])

    get_members.short_description = "Team Members"  # Column name in admin

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'user', 'joined_at')
    search_fields = ('name', 'team__name', 'user__username')
    list_filter = ('team', 'joined_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'team', 'state', 'created_at', 'deadline')
    search_fields = ('title', 'user__username', 'team__name')
    list_filter = ('state', 'created_at', 'deadline')
    ordering = ('-created_at',)
