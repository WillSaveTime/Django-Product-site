from django.contrib import admin

from core.admin import BaseModelAdmin, AUDIT_FIELDS
from .models import Pyme, PymeUser


class PymeUserStackedInline(admin.StackedInline):
    model = PymeUser
    exclude = AUDIT_FIELDS

@admin.register(Pyme)
class PymeAdmin(BaseModelAdmin):
    inlines = (PymeUserStackedInline,)
    exclude = ('code',) + AUDIT_FIELDS
    list_display = ('name', 'code') + AUDIT_FIELDS
