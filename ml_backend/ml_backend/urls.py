from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),

    # Test homepage
    path('', lambda request: HttpResponse("""
        <html>
        <head>
        <title>ML AI Backend</title>
        <link rel="icon" href="data:,">
        </head>
        <body>
        <h1>ML AI Backend Running Successfully</h1>
        </body>
        </html>
                                         """)),

    # App URLs
    path('api/', include('ai_ml_assistant.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)