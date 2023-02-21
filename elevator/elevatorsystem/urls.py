from django.urls import path
from .views import ElevatorViewSet

urlpatterns = [
    path('initialize',
         ElevatorViewSet.as_view({'post': 'initialize_elevators'})),
    path('<int:pk>/requests',
         ElevatorViewSet.as_view({'get': 'requests'})),
    path('<int:pk>/next_destination',
         ElevatorViewSet.as_view({'get': 'next_destination'})),
    path('<int:pk>/is_moving/',
         ElevatorViewSet.as_view({'get': 'is_moving'})),
    path('<int:pk>/add_request/',
         ElevatorViewSet.as_view({'put': 'add_request'})),
    path('<int:pk>/mark_maintenance/',
         ElevatorViewSet.as_view({'post': 'mark_maintenance'})),
    path('<int:pk>/mark_operational/',
         ElevatorViewSet.as_view({'post': 'mark_operational'})),
    path('<int:pk>/open_door/',
         ElevatorViewSet.as_view({'post': 'open_door'})),
    path('<int:pk>/close_door/',
         ElevatorViewSet.as_view({'post': 'close_door'})),

]
