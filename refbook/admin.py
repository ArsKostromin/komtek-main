from django.contrib import admin
from .models import ReferenceBook, ReferenceBookVersion, ReferenceBookElement

class ReferenceBookVersionInline(admin.TabularInline):
    model = ReferenceBookVersion
    extra = 1
    fields = ('version', 'start_date')
    ordering = ('start_date',)
    show_change_link = True
    
class ReferenceBookElementInline(admin.TabularInline):
    model = ReferenceBookElement
    extra = 1
    fields = ("code", "value")
    ordering = ("code",)

@admin.register(ReferenceBook)
class ReferenceBookAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", 'current_version', 'current_version_start_date')
    search_fields = ("code", "name")
    ordering = ("id",)
    inlines = [ReferenceBookVersionInline]
    
    fieldsets = (
        ("Основная информация", {
            "fields": ("code", "name", "description"),
        }),
    )
    
    def current_version(self, obj):
        """ Получаем последнюю (текущую) версию справочника """
        latest_version = obj.versions.order_by('-start_date').first()
        return latest_version.version if latest_version else "—"

    def current_version_start_date(self, obj):
        """ Получаем дату начала действия последней версии """
        latest_version = obj.versions.order_by('-start_date').first()
        return latest_version.start_date if latest_version else "—"
    
    current_version.short_description = "Текущая версия"
    current_version_start_date.short_description = "Дата начала версии"

@admin.register(ReferenceBookVersion)
class ReferenceBookVersionAdmin(admin.ModelAdmin):
    list_display = ("id", "reference_book_code", "reference_book_name", "version", "start_date")
    search_fields = ("version",)
    list_filter = ("start_date",)
    ordering = ("reference_book", "start_date")
    inlines = [ReferenceBookElementInline]  # Вложенные элементы
    
    def reference_book_code(self, obj):
        return obj.reference_book.code
    
    def reference_book_name(self, obj):
        return obj.reference_book.name

    reference_book_code.short_description = "Код справочника"
    reference_book_name.short_description = "Наименование справочника"

@admin.register(ReferenceBookElement)
class ReferenceBookElementAdmin(admin.ModelAdmin):
    list_display = ("id", "version", "code", "value")
    search_fields = ("code", "value")
    ordering = ("version", "code")