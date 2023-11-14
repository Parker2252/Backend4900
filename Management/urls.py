"""
URL configuration for investments project - portfolio app.
"""
from django.urls import path
from Management import views

urlpatterns = [
    path('', views.guest_list),
    path('food', views.food_list),
    path('food/<int:id>/', views.food_list),
    path('catering', views.catering_list),
    path('catering/<int:id>/', views.catering_detail),
    path('event', views.event_list),
    path('event/<int:id>/', views.event_list),
    path('upload/<int:id>/', views.add_image),
    path('invitations/user/', views.get_invitations_by_user, name='get_invitations_by_user'),
    path('invitations/event/<int:event_id>/', views.get_invitations_by_event, name='get_invitations_by_event'),
    path('update-status/<int:invitation_id>/', views.update_invitation_status, name='update-invitation-status'),
    # path('api/customers/', views.customer_list),
    # path('api/mycustomers/', views.my_customer_list),
    # path('api/customers/<int:pk>', views.getCustomer),
    # path('api/investments/', views.investment_list),
    # path('api/investments/<int:pk>', views.getInvestment),
    # path('api/stocks/', views.stock_list),
    # path('api/stocks/<int:pk>', views.getStock),
]
