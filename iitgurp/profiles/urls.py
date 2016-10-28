from django.conf.urls import url

from . import views, views_faculty, views_student

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='login'),

    url(r'^student/home/$', views_student.Home.as_view(), name='stud-home'),
    url(r'^student/detail/$', views_student.StudentDetail.as_view(),
        name='stud-detail'),
    url(r'^student/update/$', views_student.StudentUpdate.as_view(),
        name='stud-update'),

    url(r'^faculty/home/$', views_faculty.Home.as_view(), name='fac-home'),
    url(r'^faculty/detail/$', views_faculty.FacultyDetail.as_view(),
        name='fac-detail'),
    url(r'^faculty/update/$', views_faculty.FacultyUpdate.as_view(),
        name='fac-update'),
]
