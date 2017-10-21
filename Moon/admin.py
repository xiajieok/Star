from django.contrib import admin

# Register your models here.
from Moon.models import Host
class HostAdmin(admin.ModelAdmin):
    list_display = [
                'hostname',
                'ip',
                'os',
                'memory',
                'disk',
                'vendor_id',
                # 'model_name',
                'cpu',
                'product',
                'Manufacturer',
                'sn']

admin.site.register(Host,HostAdmin)
