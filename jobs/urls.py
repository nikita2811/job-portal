from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobsViewSet,JobListView

router = DefaultRouter()
router.register('jobs', JobsViewSet, basename='job')   # ✅ auto generates all URLs

urlpatterns = [
    path('', include(router.urls)),
     path('matched/', JobListView.as_view(), name='matched-jobs'),
]