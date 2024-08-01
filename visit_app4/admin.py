from django.contrib import admin
from .models import Dairy, Taluk, Village, Employee, VisitType, Photo, Visit
from .forms import VisitForm

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1

@admin.register(Dairy)
class DairyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','village', 'created_at', 'created_by', 'modified_at', 'modified_by')
    search_fields = ('name',)

@admin.register(Taluk)
class TalukAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'created_by', 'modified_at', 'modified_by')
    search_fields = ('name',)

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'taluk', 'created_at', 'created_by', 'modified_at', 'modified_by')
    search_fields = ('name', 'taluk__name')
    list_filter = ('taluk',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role','get_taluks', 'created_at', 'created_by', 'modified_at', 'modified_by')
    search_fields = ('name', 'role')
    filter = ('taluks',)

    def get_taluks(self, obj):
        return ", ".join([f"{i + 1}. {vt.name}" for i, vt in enumerate(obj.taluks.all())])

@admin.register(VisitType)
class VisitTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'created_by', 'modified_at', 'modified_by')
    search_fields = ('name',)

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    form = VisitForm
    list_display = ('id', 'employee', 'get_visit_types', 'taluk', 'village', 'dairy', 'summary', 'date_created', 'gps', 'created_at', 'created_by', 'modified_at', 'modified_by')
    search_fields = ('employee__name', 'taluk__name', 'village__name', 'dairy__name', 'summary')
    list_filter = ('employee', 'taluk', 'village', 'dairy', 'date_created')
    ordering = ['date_created', '-employee']
    filter = ('visit_types',)
    inlines = [PhotoInline]

    class Media:
        js = ('js/filter.js',)

    def get_visit_types(self, obj):
        return ", ".join([f"{i + 1}. {vt.name}" for i, vt in enumerate(obj.visit_types.all())])

    get_visit_types.short_description = 'Visit Types'
