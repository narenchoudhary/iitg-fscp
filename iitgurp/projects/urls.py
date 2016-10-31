from __future__ import unicode_literals

from django.conf.urls import url

from . import views_faculty, views_student

urlpatterns = [
    url(r'^projects/faculty/create/$', views_faculty.ProjectCreate.as_view(),
        name='fac-project-create',),
    url(r'^projects/faculty/list/$', views_faculty.ProjectList.as_view(),
        name='fac-project-list'),
    url(r'^projects/faculty/detail/(?P<pk>\d+)/$',
        views_faculty.ProjectDetail.as_view(), name='fac-project-detail'),
    url(r'^projects/faculty/update/(?P<pk>\d+)/$',
        views_faculty.ProjectUpdate.as_view(), name='fac-project-update'),

    url(r'^projects/student/list/$',
        views_student.ProjectList.as_view(), name='stud-project-list'),
    url(r'^projects/student/detail/(?P<pk>\d+)/$',
        views_student.ProjectDetail.as_view(), name='stud-project-detail'),
    url(r'^projects/student/apply/(?P<pk>\d+)/$',
        views_student.ProjectStudRelCreate.as_view(),
        name='stud-project_stud_rel-create'),
]
