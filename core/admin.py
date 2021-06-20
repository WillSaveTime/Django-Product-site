from django.contrib import admin

AUDIT_FIELDS = (
    "created_date",
    "updated_date",
    "deleted_date",
)

class BaseModelAdmin(admin.ModelAdmin):
    exclude = AUDIT_FIELDS