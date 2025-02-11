from django.urls import path
from .views import *
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Buchi API",
        default_version='v1',
        description="API documentation for the Buchi app",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)




urlpatterns = [
    path('signup/', SignupView.as_view(),name='signup'),
    path('login/', Login.as_view(),name='login'),
     path('logout/', logoutapi.as_view(),name='logout'),
    path('users/', UserList.as_view(), name='user-list'),
    path('todo/', CreateTodo.as_view(), name='todo'),
    path('list/', ListTodo.as_view(), name='list'),
    path('update/<str:pk>/', UpdateTodo.as_view(), name='update'),
    path('delete/<str:pk>/', Delatetodo.as_view(),name='delete'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    re_path(r'^api/schema(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
 



