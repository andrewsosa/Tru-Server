"""Tru URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from snippets import views as snippets_views
from API import views as API_views

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Routers provide an easy way of automatically determining the URL conf.
api_router = routers.DefaultRouter()
api_router.register(r'snippets', snippets_views.SnippetViewSet)
api_router.register(r'users', API_views.UserViewSet, 'User')
api_router.register(r'feed', API_views.FeedViewSet, 'Feed')
api_router.register(r'accounts', API_views.AccountViewSet, 'Account')
#api_router.register(r'create_auth', API_views.create_auth)

"""
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
"""

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #url(r'^api/create_auth/', API_views.create_auth),
    url(r'^api/', include(api_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
