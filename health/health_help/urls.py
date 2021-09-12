from django.urls import path 
from . import views

urlpatterns = [
    path('' , views.index , name="index"),
    path('about' , views.about , name="about"),
    path('tablets' , views.tablets , name="tablets"),
    path('excercise' , views.excercise , name="excercise"),
    path('doctor' , views.doctor , name="doctor"),
    path('doctor/<str:join_code>' , views.view_doc , name="view_doc"),
    path('embed_map' , views.embed_map , name="embed_map"),
    path('blog' , views.blog , name="blog"),
    path('add_blog' , views.add_blog , name="add_post"),
    path('view_blog/<str:unique_id>' , views.view_blog , name="view_blog"),
    path('facts' , views.facts , name="facts"),
    path('tablets/<str:tablet>' , views.view_tab, name="view_tab"),
    path('tablets/<str:tablet>/delete' , views.delete_tablet , name="delete_tab" ),
    path('login' , views.login_view , name="login"),
    path('register' , views.register , name="register"),
    path('logout' , views.logout_view , name="logout") ,


]