from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
]
#     path('products/', include('products.urls')),
#     path('customcakes/', include('customcakes.urls')),
#     path('checkout/', include('checkout.urls')),
#     path('contact/', include('contact.urls')),
#     path('profile/', include('profiles.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)