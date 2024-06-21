"""
URL configuration for mypetproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mypetapp.views import petview,petdetail
from django.conf import settings
from django.conf.urls.static import static
from mypetapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('petview/', petview.as_view()),
    path('PetBycategory',views.petviewcmfun,name='petbycategory'),
    path('search/',views.search,name='search'),
    path('register/',views.register, name='register'),
    path('login/',views.login,name='login'),
    path('detail/<int:pk>/',petdetail.as_view(), name='detail'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('viewcart/',views.viewcart,name='viewcart'),
    path('changequantity/', views.cq, name="changequantity"),
    path('summarpage/', views.summary, name='summary'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('logout/', views.logout, name='logout'),
    path('success',views.success,name='success'),
    path('PetDetail/<slug:slug>',petdetail.as_view(),name='PetDetail'),
    path('PetBycategory/<str:data>',views.petviewcmfun,name='petbycategory')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
