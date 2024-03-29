from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Ticket, TicketMessage

User = get_user_model()


class UnitInline(admin.TabularInline):
    model = TicketMessage
    extra = 0
    readonly_fields = ("user",)

    def has_add_permission(self, request, obj=None): return True

    def has_change_permission(self, request, obj=None): return False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "status", "priority", "section", "created")
    list_display_links = list_display

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Only apply readonly for existing objects (change view)
            return ["user", "title", "section", "priority", "seen_by_user", "seen_by_admin", "created", "updated"]
        return []

    add_fieldsets = (
        (None, {
            "fields": ("user", "status", "title", "section", "priority"),
        }),
    )

    def get_inlines(self, request, obj):
        inlines = []
        if obj:
            inlines = [
                UnitInline
            ]
        return inlines

    def save_model(self, request, obj, *args, **kwargs):
        if obj.pk:
            for o in obj.ticketmessage_set.all():
                if o.user is None:
                    o.user = request.user
                    o.save()
        obj.save()
        super().save_model(request, obj, *args, **kwargs)

    def render_change_form(self, request, context, *args, **kwargs):

        context.update({"save_text": True})
        return super().render_change_form(request, context, *args, **kwargs)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            # Do something with instance
            if not instance.pk:
                instance.user = request.user
                instance.save()
        formset.save_m2m()
