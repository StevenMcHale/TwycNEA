from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
import uuid

# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    

class Timeslot(models.Model):
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    def __str__(self):
        return str(self.start_time)


class EveningDate(models.Model):
    YEAR_GROUP = (
        ('LVI', 'LVI'),
        ('UVI', 'UVI'),
    )
    date = models.DateField(null=True)
    timeslots = models.ManyToManyField(Timeslot)
    year_group = models.CharField(max_length=200, null=True, choices=YEAR_GROUP)

    def __str__(self):
        return str(self.date)


class Building(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    name = models.CharField(max_length=200, null=True)
    building = models.ForeignKey(Building, null=True, on_delete= models.CASCADE)

    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    building = models.ForeignKey(Building, null=True, on_delete= models.SET_NULL)
    room = models.ForeignKey(Room, null=True, on_delete= models.SET_NULL)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.name

# Signal handler to delete the associated user when a student is deleted
@receiver(post_delete, sender=Teacher)
def delete_user_with_teacher(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()



class Student(models.Model):
    YEAR_GROUP = (
        ('LVI', 'LVI'),
        ('UVI', 'UVI'),
    )

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    year_group = models.CharField(max_length=200, null=True, choices=YEAR_GROUP)
    teachers = models.ManyToManyField(Teacher)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.name
    
# Signal handler to delete the associated user when a student is deleted
@receiver(post_delete, sender=Student)
def delete_user_with_student(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()


class Booking(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
    )

    booking_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    student = models.ForeignKey(Student, null=True, on_delete= models.CASCADE)
    teacher = models.ForeignKey(Teacher, null=True, on_delete= models.CASCADE)
    timeslot = models.ForeignKey(Timeslot, null=True, on_delete= models.CASCADE)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    date = models.ForeignKey(EveningDate, null=True, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


class Parent(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name

# Signal handler to delete the associated user when a student is deleted
@receiver(post_delete, sender=Parent)
def delete_user_with_parent(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
