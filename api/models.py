from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from djangoflutterwave.models import FlwPlanModel


# Create your models here.class Profile(models.Model):

class Profile(models.Model):
    gender_choice = ("Male", "Male"),("Female","Female")
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_pic = models.FileField('Profile Pic', blank=True, null=True, upload_to='profile_images/')
    gender = models.TextField(blank=True, null=True, choices=gender_choice)
    mobile = models.CharField(max_length=18, blank=True, null=True)
    access_plan = models.OneToOneField(FlwPlanModel, on_delete=models.CASCADE, blank=True, null=True, related_name= 'access_status')

    def __str__(self):
            return self.user.username

        
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @classmethod
    def filter_by_accessplan(cls, filter_access_plan):
        try:
            profile= cls.objects.filter(access_plan__flwplanmodel__icontains=filter_access_plan)
            return profile
        except Exception:
            return  "No profile found in your filter access plan"



class Content(models.Model):
    title = models.CharField(max_length=255 )
    description = models.TextField()
    content_file = models.FileField(upload_to='content_files/')
    content_accessplan = models.OneToOneField(FlwPlanModel, on_delete=models.CASCADE,blank=True, null=True,related_name= 'access_plan')
    created_at = models.DateTimeField(auto_created=True)
    updated_on = models.DateTimeField(auto_created=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def save_content(self):
        self.save()

    def delete_content(self):
        self.delete() 

    @classmethod
    def filter_by_accessplan(cls, filter_access_plan):
        try:
            content= cls.objects.filter(content_accessplan__FlwPlanModel__icontains=filter_access_plan)
            return content
        except Exception:
            return  "No content found in your filter access plan"




    





