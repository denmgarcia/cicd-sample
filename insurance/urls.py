from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import InsuranceDetail, InsuranceList, InsuranceCreateFakeData

urlpatterns = [
    path("", InsuranceList.as_view()),
    path("<int:pk>/", InsuranceDetail.as_view()),
    # Test data
    path("test/", InsuranceCreateFakeData.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
