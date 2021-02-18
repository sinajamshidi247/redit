from django.urls import path ,include
from . import views

app_name = 'posts'

urlpatterns = [
    path('api/posts/',views.PostList.as_view()),
    path('api/posts/<int:pk>/vote',views.VoteCreate.as_view()),
    path('api/posts/<int:pk>/',views.PostDelete.as_view()),

]

