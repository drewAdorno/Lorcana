from django.urls import path
from . import views

urlpatterns = [
    path('', views.card_list, name='card_list'),  # For viewing all cards
    path('create-deck/', views.create_deck, name='create_deck'),
    path('deck/<int:deck_id>/add/', views.add_to_deck, name='add_to_deck'),
    path('deck/<int:deck_id>/', views.view_deck, name='view_deck'),
    path('deck/<int:deck_id>/remove/<int:card_id>/', views.remove_from_deck, name='remove_from_deck'),
]
