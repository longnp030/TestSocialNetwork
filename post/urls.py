from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from .views import *
from tomo import settings

urlpatterns = [
    
] + static('images', document_root=settings.POST_IMAGE_DIR)