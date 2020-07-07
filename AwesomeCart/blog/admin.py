from django.contrib import admin

# Register your models here.
from .models import Blogpost
# registering product table in database
admin.site.register(Blogpost)
