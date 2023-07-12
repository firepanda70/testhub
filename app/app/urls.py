from django.contrib import admin
from django.urls import include, path

handler404 = 'polls.views.page_not_found'
handler500 = 'polls.views.server_error'

urlpatterns = [
    path('', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls'))
]