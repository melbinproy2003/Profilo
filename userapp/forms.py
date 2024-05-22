from django import forms
from .models import Profile, Project, WorkExperience, Certification

class ProfileForm(forms.ModelForm):
    social_media_links = forms.CharField(
        label='Social Media Links',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter social media links separated by commas'})
    )

    class Meta:
        model = Profile
        fields = [
            'username','first_name', 'last_name', 'date_of_birth', 'gender', 'location',
            'nationality', 'education', 'languages', 'interests', 'bio',
            'profile_picture', 'social_media_links',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.RadioSelect,
            'education': forms.Textarea(attrs={'rows': 3}),
            'languages': forms.Textarea(attrs={'rows': 3}),
            'interests': forms.Textarea(attrs={'rows': 3}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
    
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description','project_picture', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter project title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter project description', 'class': 'form-control'}),
            'link': forms.URLInput(attrs={'placeholder': 'Enter project link', 'class': 'form-control'}),
        }

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company', 'position', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
        }

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuer', 'date_issued', 'description', 'certificate_picture']