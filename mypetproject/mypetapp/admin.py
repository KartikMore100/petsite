from django.contrib import admin
from .models import Pet
# Register your models here.
class petadmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name','species','breeds')}
admin.site.register(Pet,petadmin )