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
    url(r'^user/profile', views.profile, name='profile'),
    url(r'^project/(?P<id>\d+)$', views.project, name='project'),
    url(r'^user/<int:user_id>', views.posted_by, name='posted_by'),
    url(r'^update/user/',views.update_profile, name='update_profile'),
    url(r'^project/(?P<id>\d+)/vote/$',views.vote, name='vote'),
    url(r'^api/', views.api, name='api'),
    url(r'^api/project/', views.ProjectList.as_view()),
    url(r'^api/users/', views.UserList.as_view()),
    url(r'^api/project/<int:pk>/',views.ProjectDescription.as_view()),
    url(r'^api/user/<int:pk>/',views.UserDescription.as_view()),
    url(r'^search/', views.search_project, name='search'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)