from __future__ import unicode_literals

from django.conf.urls import url

from . import views_faculty, views_student

urlpatterns = [
    url(r'^faculty/projects/create/$', views_faculty.ProjectCreate.as_view(),
        name='fac-project-create',),
    url(r'^faculty/projects/list/$', views_faculty.ProjectList.as_view(),
        name='fac-project-list'),
    url(r'^faculty/projects/detail/(?P<pk>\d+)/$',
        views_faculty.ProjectDetail.as_view(), name='fac-project-detail'),
    url(r'^faculty/projects/update/(?P<pk>\d+)/$',
        views_faculty.ProjectUpdate.as_view(), name='fac-project-update'),
    url(r'^faculty/projects/search/$',
        views_faculty.SearchProject.as_view(), name='fac-project-search'),

    url(r'^student/projects/list/$',
        views_student.ProjectList.as_view(), name='stud-project-list'),
    url(r'^student/projects/detail/(?P<pk>\d+)/$',
        views_student.ProjectDetail.as_view(), name='stud-project-detail'),
    url(r'^student/projects/apply/(?P<pk>\d+)/$',
        views_student.ProjectStudRelCreate.as_view(),
        name='stud-project_stud_rel-create'),
    url(r'^student/projects/deapply/(?P<pk>\d+)/$',
        views_student.ProjectStudRelDelete.as_view(),
        name='stud-project_stud_rel-delete'),
    url(r'^student/projects/search/',
        views_student.SearchProject.as_view(), name='stud-project-search'),
]
