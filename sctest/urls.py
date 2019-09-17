from django.urls import path, re_path
from django.conf.urls import url
from .views import AllSchoolView, StudentList, StudentDetail, AccountDetail

urlpatterns = (
    path("all", AllSchoolView.as_view()),
    url(r'students/$', StudentList.as_view()),
    url(r'students/(?P<name>.+)/$', StudentDetail.as_view()),
    url(r'register/$', AccountDetail.as_view()),
)
