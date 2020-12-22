"""accounts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include


urlpatterns = [
    path('', include('dialogs.urls')),
    path('', include('mscore.urls', namespace='mscore')),
    # path('relations/', include('relations.urls', namespace='relations'))
    # path('', include('core.urls', namespace='core')),
    # path('', include('mail.urls', namespace='mail')),
    # path('', include('relation.urls', namespace='relations')),
    # path('statistics/', include('instance_statistics.urls', namespace='statistics')),
]
