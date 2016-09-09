from django.db import models


# Create your models here.
class Host(models.Model):
    '''
    主机名、ip、系统版本、内存、硬盘、制造商、cpu、厂商、生产商,SN
    '''
    hostname = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    os = models.CharField(max_length=50)
    memory = models.CharField(max_length=50)
    disk = models.CharField(max_length=50)
    vendor_id = models.CharField(max_length=50)
    # model_name = models.CharField(max_length=50)
    cpu = models.CharField(max_length=50)
    product = models.CharField(max_length=50)
    Manufacturer = models.CharField(max_length=50)
    sn = models.CharField(max_length=50)
