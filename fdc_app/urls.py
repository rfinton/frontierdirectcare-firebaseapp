from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('refer/', views.refer, name='refer'),
	path('giveaway/', views.giveaway, name='giveaway'),
	path('book/<int:book_id>', views.book_by_id, name='book_by_id'),
]