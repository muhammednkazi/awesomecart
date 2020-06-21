from django.contrib import admin

# Register your models here.
from .models import product,contactus_table,Order,OrderUpdate
# registering product table in database
admin.site.register(product)
admin.site.register(contactus_table)
admin.site.register(Order)
admin.site.register(OrderUpdate)