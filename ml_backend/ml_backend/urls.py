from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),

    # Test homepage
    path('', lambda request: HttpResponse("ML AI Backend Running Successfully")),

    # App URLs
    path('api/', include('ai_ml_assistant.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)