from django.contrib import admin
from Earth import models

admin.site.register(models.Article)
admin.site.register(models.UserProfile)
admin.site.register(models.Tag)
admin.site.register(models.Category)