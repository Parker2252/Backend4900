from rest_framework import status, generics
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from rest_framework.response import Response
from .models import GuestRSVP, FoodItem, Catering, Users,Invitation
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
# from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
import json


# @csrf_exempt


@api_view(['GET'])
def guest_list(request):
    # Retrieve or update the guest list.
    if request.method == 'GET':
        guest_list = GuestRSVP.objects.all()
        serializer = GuestRSVPSerializer(guest_list, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = GuestRSVPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def guest_detail(request, rsvp_id):
    # Retrieve, update, or delete a guest RSVP instance.
    try:
        guest = GuestRSVP.objects.get(rsvp_id=rsvp_id)
    except GuestRSVP.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GuestRSVPSerializer(guest)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GuestRSVPSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST','DELETE','PUT'])
def food_list(request, id=None):
    if request.method == 'GET':
        if id is not None:
            try:
                food = FoodItem.objects.get(pk=id)
                serializer = FoodItemSerializer(food)
                return Response({'data': serializer.data})
            except FoodItem.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            food_list = FoodItem.objects.all()
            serializer = FoodItemSerializer(food_list, many=True)
            return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = FoodItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = FoodItemSerializer(food,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        food.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'POST'])
def catering_list(request):
    # Retrieve or update the food list.
    if request.method == 'GET':
        catering_list = Catering.objects.all()
        serializer = CateringSerializer(catering_list, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = CateringSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def catering_detail(request, id):
    # Retrieve, update, or delete food instance.
    try:
        Catering_detail = Catering.objects.get(pk=id)
    except Catering.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CateringSerializer(Catering_detail)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CateringSerializer(Catering_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Catering_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def add_image(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EventImageSerializer(event, data={'image': request.data.get('image')}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE','POST'])
# @parser_classes([MultiPartParser, FormParser])
def event_list(request, id=None):
    if request.method == 'POST':
        print(request.data)
        serializer = CreateEventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            create_invitations_for_event(event,instance=event, created=True)
            s = EventSerializer(event)
            return Response(s.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if id is None:
        # Handle the case where id is not provided (e.g., list all events).
        if request.method == 'GET':
            events = Event.objects.filter(user=request.user)
            # events = Event.objects.all()
            serializer = EventSerializer(events, many=True)
            return Response({'data': serializer.data})

    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response({'data': serializer.data})

    elif request.method == 'PUT':
        serializer = CreateEventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@receiver(post_save, sender=Event)
def create_invitations_for_event(sender, instance, created, **kwargs):
    if created:
        rsvp_users = instance.rsvp.all()
        for user in rsvp_users:
            Invitation.objects.create(event=instance, user=user)


@api_view(['GET'])
def get_invitations_by_user(request):
    invitations = Invitation.objects.filter(user=request.user)
    serializer = InvitationWithDetailsSerializer(invitations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_invitations_by_event(request, event_id):
    invitations = Invitation.objects.filter(event=event_id)
    serializer = InvitationWithDetailsSerializer(invitations, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
def update_invitation_status(request, invitation_id):
    try:
        invitation = Invitation.objects.get(pk=invitation_id)
    except Invitation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Assuming you have a field named 'invite_status' in your request data
    serializer = InvitationSerializer(invitation, data={'invite_status': request.data.get('invite_status')}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def users_list(request):
    # Retrieve or update the guest list.
    if request.method == 'GET':
        users_list = Users.objects.all()
        serializer = UsersSerializer(users_list, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, rsvp_id):
    # Retrieve, update, or delete a guest RSVP instance.
    try:
        guest = Users.objects.get(rsvp_id=rsvp_id)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UsersSerializer(guest)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UsersSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterView(generics.CreateAPIView):
    #Register a new user - requester need not be authorized
    queryset = Users.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response(UsersSerializer(request.user).data)
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)







