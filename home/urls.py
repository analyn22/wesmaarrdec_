from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about_us, name="about"),
    
    path('events/', views.events, name="events"),
    path('event/<str:pk>/', views.event, name="event"),
    path('add-event/', views.add_event, name="add-event"),
    path('edit-event/<str:pk>/', views.edit_event, name="edit-event"),
    path('delete-event/<str:pk>/', views.delete_event, name="delete-event"),

    path('special-orders/', views.special_orders, name="special-orders"),
    path('add-order/', views.add_order, name="add-order"),
    path('edit-order/<str:pk>/', views.edit_order, name="edit-order"),
    path('delete-order/<str:pk>/', views.delete_order, name="delete-order"),

    path('add-event-agency/<str:pk>/', views.add_event_agency, name="add-event-agency"),
    path('edit-event-agency/<str:pk>/', views.edit_event_agency, name="edit-event-agency"),
    path('delete-event-agency/<str:pk>/', views.delete_event_agency, name="delete-event-agency"),

    path('memorandums/', views.memorandums, name="memorandums"),
    path('add-memo/', views.add_memo, name="add-memo"),
    path('edit-memo/<str:pk>/', views.edit_memo, name="edit-memo"),
    path('delete-memo/<str:pk>/', views.delete_memo, name="delete-memo"),

    path('comm-letters/', views.comm_letters, name="comm-letters"),
    path('add-letter/', views.add_letter, name="add-letter"),
    path('edit-letter/<str:pk>/', views.edit_letter, name="edit-letter"),
    path('delete-letter/<str:pk>/', views.delete_letter, name="delete-letter"),

    path('moas/', views.moas, name="moas"),
    path('moa/<str:pk>/', views.moa, name="moa"),
    path('add-moa/', views.add_moa, name="add-moa"),
    path('edit-moa/<str:pk>/', views.edit_moa, name="edit-moa"),
    path('delete-moa/<str:pk>/', views.delete_moa, name="delete-moa"),

    path('add-party/<str:pk>/', views.add_party, name="add-party"),
    path('edit-party/<str:pk>/', views.edit_party, name="edit-party"),
    path('delete-party/<str:pk>/', views.delete_party, name="delete-party"),

    path('add-signatory/<str:pk>/', views.add_signatory, name="add-signatory"),
    path('edit-signatory/<str:pk>/', views.edit_signatory, name="edit-signatory"),
    path('delete-signatory/<str:pk>/', views.delete_signatory, name="delete-signatory"),

    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),

    path('profile/', views.profile, name="profile"),
    path('edit-profile/', views.edit_profile, name="edit-profile"),
    path('edit-info/', views.edit_info, name="edit-info"),
]