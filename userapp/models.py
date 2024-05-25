from django.db import models

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True)
    location = models.CharField(max_length=100,null=True)
    nationality = models.CharField(max_length=50,null=True)
    education = models.TextField(blank=True, null=True)
    languages = models.CharField(max_length=200, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    social_media_links = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    type = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.username}"

class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    project_picture = models.ImageField(upload_to='project_picture/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class WorkExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='work_experiences')
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.position} at {self.company}"

class Certification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date_issued = models.DateField()
    description = models.TextField(blank=True, null=True)
    certificate_picture = models.ImageField(upload_to='certificate/')

    def __str__(self):
        return self.name

