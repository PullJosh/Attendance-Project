from django.contrib import admin

from .models import Person, Photo

# The models listed here will appear in the admin panel
# (If we don't list them, they will exist in the database
# but be invisible from the Admin side.)
admin.site.register(Person)
admin.site.register(Photo)
