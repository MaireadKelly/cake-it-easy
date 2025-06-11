# inspect_categories.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cake_it_easy.settings")
django.setup()

from products.models import Category

print("\n📦 Categories in your database:")
for cat in Category.objects.all():
    print(f"- ID: {cat.id} | Name: {cat.name}")
