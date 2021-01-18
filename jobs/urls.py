from django.urls import path

from . import views

urlpatterns = [
    path('new', views.new, name='new_job'),
    path('new/emap2sec', views.newEmap2Sec, name='new_emap2sec'),
    path('new/emap2secplus', views.newEmap2SecPlus, name='new_emap2sec+'),
    path('new/mainmast', views.newMainmast, name='new_mainmast'),
    path('new/mainmastseg', views.newMainmastSeg, name='new_mainmastseg'),
    path('confirm/emap2sec/<uuid:id>',
         views.confirmEmap2Sec, name='confirm_emap2sec'),
    path('view/emap2sec/<uuid:id>', views.viewEmap2Sec, name='view_emap2sec'),
]
