from rest_framework.routers import DefaultRouter

from .views import UserFileViewSet

router = DefaultRouter()
router.register(r"", UserFileViewSet, basename="user_files")

urlpatterns = router.urls
