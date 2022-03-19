from django.contrib import admin

from .models import Category, Brand, Tags, Ingredient, Noodle, SpicyLevel, NoodleImage


class NoodleImageInline(admin.TabularInline):
    model = NoodleImage
    row_filters = ['name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    prepopulated_fields = {'slug': ('name', )}


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    prepopulated_fields = {'slug': ('name', )}


class TagsAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


class NoodleAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    inlines = [NoodleImageInline]
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Noodle, NoodleAdmin)
admin.site.register(SpicyLevel)
