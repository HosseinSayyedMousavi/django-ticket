from django.contrib import admin
from .models import Ticket, TicketMessage
# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib import messages
from datetime import datetime
from django import forms
User = get_user_model()

class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["soft_delete"].disabled = False
            self.fields["message"].disabled = True
        else : self.fields["soft_delete"].disabled = True

class UnitInline(admin.TabularInline):
    model = TicketMessage
    form = TicketMessageForm
    extra = 1
    can_delete = False
    readonly_fields =  ("user","get_is_admin","created","viewer","viewed")

    def has_add_permission(self, request, obj=None): return True

    def get_is_admin(self,obj):
        if obj.user.is_superuser or obj.user.is_staff : return True
        return False
    get_is_admin.boolean = True
    get_is_admin.short_description = "is admin"


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'status', 'priority', 'section','created','seen_by_admin','seen_by_user')
    list_display_links = list_display
    inlines = [UnitInline]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Only apply readonly for existing objects (change view)
            return ["user","title","section","priority","seen_by_user","seen_by_admin","created","updated","service","service_type"]
        return []
    
    def get_exclude(self, request, obj):
        if not obj: return ["seen_by_user","seen_by_admin","deleted_at"]
        return []
    add_fieldsets = (
        (None, {
            'fields': ('user', 'status',"title","section","priority"),
        }),
    )





    def render_change_form(self, request, context, *args, **kwargs):
        
        context.update({'save_text': True})
        return super().render_change_form(request, context, *args, **kwargs)
    

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            if instance.pk: 
                original_instance = instance.__class__.objects.get(pk=instance.pk) 
                if instance.soft_delete != original_instance.soft_delete:
                    original_instance.soft_delete = instance.soft_delete
                    original_instance.save()
            else:
                instance.user = request.user
                instance.save()
        formset.save_m2m()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.seen_by_admin:
            obj.seen_by_admin = True
            obj.save()
            messages.add_message(request, messages.INFO, 'Field seen_by_admin has been updated to True.')
        obj.ticketmessage_set.filter(viewed__isnull=True , user=obj.user).update(viewed=datetime.now(),viewer=request.user)
        
        return super().change_view(request, object_id, form_url, extra_context)