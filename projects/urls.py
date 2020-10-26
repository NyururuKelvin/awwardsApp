from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns=[
    url('^$',views.index,name = 'home'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^login', LoginView.as_view(), name='login_url'),
    url(r'^logout/', LogoutView.as_view(next_page='login_url'), name='logout_url'),
    url(r'^new/project', views.new_project, name='new_project'),
    url(r'^user/profile/', views.profile, name='profile'),
    url(r'^project/<int:project_id>/', views.project, name='project'),
    url(r'^user/<int:user_id>', views.posted_by, name='posted_by'),
    url(r'^update/user/',views.update_settings, name='update_settings'),


]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)