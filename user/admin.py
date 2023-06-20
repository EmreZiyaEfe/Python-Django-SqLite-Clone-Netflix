from django.contrib import admin
from .models import *
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['isim', 'user', 'olusturulma_tarihi']
    list_filter = ['user']
    search_fields = ['isim', 'user__username']
    readonly_fields = ['id', 'olusturulma_tarihi', 'slug']
    slug = models.SlugField(null=True, editable=False)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Hesap)