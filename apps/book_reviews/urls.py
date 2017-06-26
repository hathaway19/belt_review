from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^/add_review$', views.add_review_page, name="add_review"), 
	url(r'^/create_review$', views.create_review, name="create_review"),  
	url(r'^(?P<id>[\d]+)$', views.show_book, name="show"),
	url(r'^/show_user/(?P<id>[\d]+)$', views.show_user, name="show_user"),
	url(r'^delete/(?P<id>[\d]+)$', views.delete_review, name="delete"),
]