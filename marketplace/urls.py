from django.urls import path
from marketplace import views

app_name = 'marketplace'

urlpatterns = [
    path('add/energy-type' , views.EnergyType_ViewSet.as_view({'post' : 'add_energy_type'}) , name='add') ,
    path('get/energy-type' , views.EnergyType_ViewSet.as_view({'post' : 'get_energy_type'}) , name='get') ,
    path('list/energy-type' , views.EnergyType_ViewSet.as_view({'post' : 'list_energy_type'}) , name='list') ,
    path('update/energy-type' , views.EnergyType_ViewSet.as_view({'post' : 'update_energy_type'}) , name='update') ,
    path('delete/energy-type' , views.EnergyType_ViewSet.as_view({'post' : 'delete_energy_type'}) , name='delete') ,

    path('add/energy' , views.Energy_ViewSet.as_view({'post' : 'add_energy'}) , name='add') ,
    path('get/energy' , views.Energy_ViewSet.as_view({'post' : 'get_energy'}) , name='get') ,
    path('list/energy' , views.Energy_ViewSet.as_view({'post' : 'list_energy'}) , name='list') ,
    path('update/energy' , views.Energy_ViewSet.as_view({'post' : 'update_energy'}) , name='update') ,
    path('delete/energy' , views.Energy_ViewSet.as_view({'post' : 'delete_energy'}) , name='delete') ,


    path('offer/energy/price' , views.Offer_Energy_ViewSet.as_view({'post' : 'offer_energy_price'}) , name='update') ,
    path('offer/energy/accept/reject' , views.Offer_Energy_ViewSet.as_view({'post' : 'offer_accept_reject'}) , name='update') ,
    path('view/energy/offers' , views.Offer_Energy_ViewSet.as_view({'post' : 'view_offer_energy_price'}) , name='update') ,
]