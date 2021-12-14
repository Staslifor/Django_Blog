from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', AnotherLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', UpdateProfile.as_view(), name='profile'),
    path('create/', create_to_blog, name='create'),
    path('detail/<int:pk>', BlogDetail.as_view(), name='detail'),
    path('load/', load_blog, name='load_csv')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
