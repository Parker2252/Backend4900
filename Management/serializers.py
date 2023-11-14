from django.contrib.auth.models import User
from .models import Users, GuestRSVP, Testimonials, Admin, Event, Catering, FoodItem,Invitation
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'username', 'email','type')

    def to_internal_value(self, data):
        if isinstance(data, int):
            return Users.objects.get(id=data)
        return super().to_internal_value(data)


class GuestRSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestRSVP
        fields = '__all__'


class TestimonialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class FoodItemSerializer(serializers.ModelSerializer):
     class Meta:
        model = FoodItem
        fields = '__all__'

class CateringSerializer(serializers.ModelSerializer):
    foodItems = FoodItemSerializer(many=True, read_only=True)

    class Meta:
        model = Catering
        fields = '__all__'

    def to_internal_value(self, data):
        print("hello asghar", type(data))
        if isinstance(data, int):
            return Catering.objects.get(id=data)
        elif isinstance(data, str):
            return Catering.objects.get(id=int(data))
        elif isinstance(data, list):
            return Catering.objects.get(id=data[0])
        return super().to_internal_value(data)



class EventSerializer(serializers.ModelSerializer):
#    rsvp = serializers.StringRelatedField(many=True)
   rsvp = UsersSerializer(many=True)
   catering = CateringSerializer()
   user = UsersSerializer()
   class Meta:
        model = Event
        fields = '__all__'


class CreateEventSerializer(serializers.ModelSerializer):
   rsvp = serializers.PrimaryKeyRelatedField(many=True, queryset=Users.objects.all())
   user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
   catering = serializers.PrimaryKeyRelatedField(queryset=Catering.objects.all())
#    image = serializers.ImageField()
   class Meta:
        model = Event
        fields = '__all__'

class EventImageSerializer(serializers.ModelSerializer):
   image = serializers.ImageField()
   class Meta:
        model = Event
        fields = '__all__'

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'

   


class InvitationWithDetailsSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    event = EventSerializer()

    class Meta:
        model = Invitation
        fields = '__all__'








class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'},
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=True)

    class Meta:
        model = Users
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name','type')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'type': {'required': True},
            'password': {'write_only': True, 'min_length': 6},
            'password2': {'write_only': True, 'min_length': 6}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        users = Users.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            type=validated_data['type'],
        )
        users.set_password(validated_data['password'])
        users.save()

        return users

# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
#         extra_kwargs = {
#             'first_name': {'required': True},
#             'last_name': {'required': True},
#             'password': {'write_only': True, 'min_length': 6},
#             'password2': {'write_only': True, 'min_length': 6}
#         }
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#
#         return attrs
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#
#         return user
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('pk', 'username', 'is_superuser', 'first_name', 'last_name', 'email')
