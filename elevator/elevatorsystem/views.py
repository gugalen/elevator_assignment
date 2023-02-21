from django.db import models
from django.utils import timezone
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Elevator
from .serializers import ElevatorSerializer
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class ElevatorViewSet(viewsets.ViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    @csrf_exempt
    @action(detail=True, methods=['post'])
    def initialize_elevators(self, request, *args, **kwargs):
        elevators_count = request.data.get('elevators_count')
        if elevators_count is None or not isinstance(elevators_count, int) or elevators_count < 1:
            return Response('Invalid number of elevators.', status=status.HTTP_400_BAD_REQUEST)

        Elevator.objects.all().delete()

        elevators = []
        for i in range(0, elevators_count):
            elevator_obj = Elevator.objects.create()
            elevator_obj.save()
            elevators.append(elevator_obj)

        serializer = ElevatorSerializer(elevators, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def requests(self, request, pk=None, *args, **kwargs):
        elevator = Elevator.objects.get(id=pk)
        if elevator is None:
            return Response("Invalid elevator number.", status=status.HTTP_404_NOT_FOUND)
        return Response(elevator.requests)

    @action(detail=True, methods=['get'])
    def next_destination(self, request, pk=None):
        elevator = Elevator.objects.get(id=pk)
        if elevator is None:
            return Response("Invalid elevator number.", status=status.HTTP_404_NOT_FOUND)

        if len(elevator.requests) == 0:
            res = {
                "destination_floor": None
            }
            return Response(res, status=status.HTTP_200_OK)
        res = {
            "destination_floor": elevator.requests[0]
        }
        return Response(res, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def is_moving(self, request, pk=None):
        elevator = Elevator.objects.get(id=pk)
        if elevator is None:
            return Response("Invalid elevator number.", status=status.HTTP_404_NOT_FOUND)

        elevator_direction = ""
        if elevator.direction == 1:
            elevator_direction = "Moving Up"
        elif elevator.direction == -1:
            elevator_direction = "Moving Down"
        else:
            elevator_direction = "Stationary"

        res = {
            "elevator_direction": elevator_direction
        }
        return Response(res, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def add_request(self, request, pk=None):
        elevator = Elevator.objects.get(id=pk)
        if elevator.status == 'maintenance':
            return Response('Elevator is currently under maintenance.',
                            status=status.HTTP_403_FORBIDDEN)

        floor = request.data.get('floor')
        if not isinstance(floor, int) or floor < 0:
            return Response('Invalid floor number.', status=status.HTTP_400_BAD_REQUEST)

        elevator.requests.append(floor)
        elevator.requests = list(set(elevator.requests))  # Remove duplicates
        elevator.requests.sort()
        elevator.save()

        return Response(f'Request added for elevator {pk}', status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def mark_maintenance(self, request, pk=None):
        elevator = Elevator.objects.get(id=pk)
        elevator.status = 'maintenance'
        elevator.requests = []
        elevator.stop()
        elevator.save()

        return Response('Elevator marked under maintenance.')

    @action(detail=True, methods=['put'])
    def mark_operational(self, request, pk=None):
        elevator = Elevator.objects.get(id=pk)
        elevator.status = 'available'
        elevator.save()

        return Response('Elevator marked operational.')

    @action(detail=True, methods=['put'])
    def open_door(self, request, pk):
        elevator = Elevator.objects.get(id=pk)
        if elevator is None:
            return Response('Elevator not found.',
                            status=status.HTTP_404_NOT_FOUND)

        if elevator.status == 'maintenance':
            return Response('Elevator is currently under maintenance.',
                            status=status.HTTP_403_FORBIDDEN)

        elevator.open_door()
        return Response('Door opened.')

    @action(detail=True, methods=['put'])
    def close_door(self, request, pk):
        elevator = Elevator.objects.get(id=pk)
        if elevator is None:
            return Response('Elevator not found.',
                            status=status.HTTP_404_NOT_FOUND)

        if elevator.status == 'maintenance':
            return Response('Elevator is currently under maintenance.',
                            status=status.HTTP_403_FORBIDDEN)

        elevator.close_door()
        return Response('Door closed.')
