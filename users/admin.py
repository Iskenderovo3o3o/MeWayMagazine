from django.contrib import admin

from users.models import User


class UsersAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "email",
                    "name",
                    "number",
                    "is_staff",
                    "is_superuser",)
    list_display_links = ("id", "email", "name", "number")
    search_fields = ("email", "name", "number")
    list_per_page = 12


admin.site.register(User, UsersAdmin)
