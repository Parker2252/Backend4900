from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):

    USER_TYPES = (
        ('Event Planner', 'Event Planner'),
        ('Guest', 'Guest'),
        # Add more user types as needed
    )

    type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    def __str__(self):
        return str(self.id)


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='events_organizer')
    rsvp = models.ManyToManyField(Users, related_name='events_attending')
    event_date = models.DateTimeField(default=timezone.now)
    number_of_guests = models.PositiveIntegerField()
    catering = models.ForeignKey('Catering', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='images/',null=True)

    def __str__(self):
        return self.name


class GuestRSVP(models.Model):
    rsvp_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    food_choice = models.ForeignKey('FoodItem', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.food_choice)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        unique_together = ('event_id', 'email')


class Catering(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    foodItems = models.ManyToManyField('FoodItem', related_name='caterings')

    def __str__(self):
        return self.name

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()
    

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    invite_status = models.CharField(max_length=255, default='Pending')  # You can adjust this based on your needs

    def __str__(self):
        return f"{self.user.username}"


# class FoodItem(models.Model):
#     catering = models.ForeignKey(Catering, on_delete=models.CASCADE, related_name='food_items', blank=True, null=True)
#     food = models.CharField(max_length=200)
#     dessert = models.CharField(max_length=50)

#     def __str__(self):
#         return self.food


class Testimonials(models.Model):
    names = models.CharField(max_length=50)
    ratings = models.CharField(max_length=50)
    reviews = models.CharField(max_length=50)
    user_id = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, blank=True)
    rsvp_id = models.ForeignKey('GuestRSVP', on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    testimonials_id = models.AutoField(primary_key=True)

    def created(self):
        self.acquired_date = timezone.now()
        self.save()

    def updated(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.pk)


class Admin(models.Model):
    admin_id = models.CharField(max_length=30, primary_key=True)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
    rsvp_id = models.ForeignKey('GuestRSVP', on_delete=models.CASCADE)
    testimonials_id = models.ForeignKey('Testimonials', on_delete=models.CASCADE)

    def __str__(self):
        return self.pk


# class Event(models.Model):
#     event_id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey('Users', on_delete=models.CASCADE, null=True)
#     rsvp_id = models.ForeignKey('GuestRSVP', on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return f'Event ID: {self.event_id}, User ID: {self.user_id_id}'
