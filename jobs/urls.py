from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobsViewSet,JobListView
from .consumers import JobConsumer

router = DefaultRouter()
router.register('jobs', JobsViewSet, basename='job')   # ✅ auto generates all URLs

urlpatterns = [
    path('', include(router.urls)),
     path('matched/', JobListView.as_view(), name='matched-jobs'),

]

websocket_urlpatterns = [
    path('ws/jobs/', JobConsumer.as_asgi()),
]
