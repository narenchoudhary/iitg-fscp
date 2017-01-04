from django.conf.urls import url

from . import views, views_faculty, views_student

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^help/$', views.HelpPageView.as_view(), name='help'),

    url(r'^student/home/$', views_student.Home.as_view(), name='stud-home'),
    url(r'^student/detail/$', views_student.StudentDetail.as_view(),
        name='stud-detail'),
    url(r'^student/update/$', views_student.StudentUpdate.as_view(),
        name='stud-update'),
    url(r'^student/faculty/search', views_student.FacultySearch.as_view(),
        name='stud-fac-search'),
    url(r'^student/faculty/(?P<pk>\d+)/detail/$',
        views_student.FacultyDetail.as_view(), name='stud-fac-detail'),

    url(r'^faculty/home/$', views_faculty.Home.as_view(), name='fac-home'),
    url(r'^faculty/detail/$', views_faculty.FacultyDetail.as_view(),
        name='fac-detail'),
    url(r'^faculty/update/$', views_faculty.FacultyUpdate.as_view(),
        name='fac-update'),
    url(r'^faculty/student/(?P<pk>\d+)/detail/$',
        views_faculty.StudentDetail.as_view(), name='fac-student-detail'),
    url(r'^faculty/search/faulty/$', views_faculty.FacultySearch.as_view(),
        name='fac-faculty-search'),
    url(r'^faculty/search/faulty/detail/(?P<pk>\d+)/$',
        views_faculty.FacultySearchDetail.as_view(),
        name='fac-search-faculty-detail'),
    url(r'^faculty/search/student/$', views_faculty.SearchStudent.as_view(),
        name='fac-student-search'),
    url(r'^faculty/search/student/detail/(?P<pk>\d+)/$',
        views_faculty.StudentSearchDetail.as_view(),
        name='fac-search-student-detail')
]
