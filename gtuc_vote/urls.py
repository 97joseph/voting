from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from voting import views

urlpatterns = [
    # User  DAshboard
    path('', views.home, name="home"),
    path('students/', views.StudentList.as_view(), name="student-list"),
    path('students/add/', views.StudentCreate.as_view(), name="student-add"),
    path('position/add/', views.PositionCreate.as_view(), name="position-add"),
    path('positions/', views.position_list, name="position-list"),
    path('candidate/add/', views.CandidateCreate.as_view(), name="candidate-add"),
    path('candidates/', views.candidate_list, name="candidate-list"),

    path('report/', views.report, name="report"),

    # Voting Interface
    path('polls/', views.election_home, name="election_home"),
    path('v/<int:election_id>/', views.voting, name="voting"),
    path('v/<int:election_id>/vote', views.vote, name="vote"),
    path('v/live/', views.results_list, name="live"),


    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('polls/<int:election_id>/results/', views.results, name='results'),
    path('polls/resultsdata/<str:obj>/', views.resultsData, name="resultsdata"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)