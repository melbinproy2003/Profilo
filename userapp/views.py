from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Project, WorkExperience, Certification
from .forms import ProfileForm, ProjectForm, WorkExperienceForm, CertificationForm
from .utils import identify_social_media_platform

# Create your views here.

def indexpage(request):
    return render(request, 'user/index.html')

def userregistration(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']

        if password == confirm_password:
            if Profile.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
                return redirect('signup')
            else:
                usertable = Profile(username=username, email=email, password=password, type='user')
                usertable.save()
                messages.success(request, 'Registration successful')
                return redirect('signin')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
    return render(request, 'user/registration.html')

def userlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = Profile.objects.get(email=email, password=password)
            request.session['username'] = user.username
            request.session['id'] = user.id
            request.session['type'] = user.type
            if user.type == 'admin':
                return redirect('webadmin')
            else:
                return redirect('userhome')
        except Profile.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')
    return render(request, 'user/login.html')
    
def userhome(request):
    if 'id' in request.session and request.session['type'] == 'user':
        name = request.session['username']
        id = request.session['id']
        try:
            profile = Profile.objects.get(id=id)
            social_media_links = profile.social_media_links.split(",") if profile.social_media_links else []
            social_media_platforms = [(link.strip(), identify_social_media_platform(link.strip())) for link in social_media_links]
            return render(request, 'user/userhome.html', {'profile': profile, 'name': name, 'social_media_platforms': social_media_platforms})
        except Profile.DoesNotExist:
            return redirect('signin')
    else:
        return redirect('signin')
    
def webadmin(request):
    if 'username' in request.session and request.session['type'] == 'admin':
        name = request.session['username']
        return render(request, 'admin/home.html', {'name': name})
    else:
        return redirect('signin')

def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    if 'id' in request.session:
        del request.session['id']
    if 'type' in request.session:
        del request.session['type']
    return redirect('index')

def update_profile(request):
    profile_id = request.session.get('id')
    if not profile_id:
        messages.error(request, 'User not found in session')
        return redirect('signin')

    profile = get_object_or_404(Profile, id=profile_id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_detail', profile_id=profile_id)
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'user/update_profile.html', {'form': form, 'profile': profile})

def profile_detail(request, profile_id):
    try:
        name = request.session['username']
        profile = Profile.objects.get(id=profile_id)
        social_media_links = profile.social_media_links.split(",") if profile.social_media_links else []
        social_media_platforms = [(link.strip(), identify_social_media_platform(link.strip())) for link in social_media_links]
        return render(request, 'user/profile_detail.html', {'profile': profile, 'social_media_platforms': social_media_platforms,'name':name})
    except Profile.DoesNotExist:
        messages.error(request, 'Profile not found')
        return redirect('create_profile')

# Insert project
def projects(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            try:
                profile_id = request.session.get('id')
                if not profile_id:
                    return redirect('login')

                profile = Profile.objects.get(id=profile_id)
                project.profile = profile
                project.save()
                return redirect('projects')
            except Profile.DoesNotExist:
                form.add_error(None, "Profile not found")
    else:
        form = ProjectForm()
    
    return render(request, 'user/addproject.html', {'form': form})

def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'user/addproject.html', {'form': form, 'project': project})

# List projects
def listprojects(request):
    name = request.session['username']
    profile_id = request.session.get('id')
    if not profile_id:
        messages.error(request, 'User not found in session')
        return redirect('signin')
    
    try:
        profile = Profile.objects.get(id=profile_id)
        projects = profile.projects.all()
        return render(request, 'user/projects.html', {'projects': projects,'profile':profile, 'name':name})
    except Profile.DoesNotExist:
        messages.error(request, 'Profile not found')
        return redirect('signin')

def remove_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('projects')

def work_experience_list(request):
    name = request.session['username']
    profile_id = request.session.get('id')
    if not profile_id:
        messages.error(request, 'User not found in session')
        return redirect('signin')

    profile = get_object_or_404(Profile, id=profile_id)
    work_experiences = profile.work_experiences.all()
    return render(request, 'user/work_experience_list.html', {'work_experiences': work_experiences, 'profile': profile, 'name':name})

def add_work_experience(request):
    profile_id = request.session.get('id')
    if not profile_id:
        messages.error(request, 'User not found in session')
        return redirect('signin')

    profile = get_object_or_404(Profile, id=profile_id)

    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            work_experience = form.save(commit=False)
            work_experience.profile = profile
            work_experience.save()
            messages.success(request, 'Work experience added successfully!')
            return redirect('work_experience_list')
    else:
        form = WorkExperienceForm()
    return render(request, 'user/add_work_experience.html', {'form': form})

def remove_work_experience(request, pk):
    profile_id = request.session.get('id')
    if not profile_id:
        messages.error(request, 'User not found in session')
        return redirect('signin')

    work_experience = get_object_or_404(WorkExperience, pk=pk, profile__id=profile_id)
    work_experience.delete()
    messages.success(request, 'Work experience removed successfully!')
    return redirect('work_experience_list')

def add_certification(request):
    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            certification = form.save(commit=False)
            profile_id = request.session.get('id')
            if profile_id:
                profile = get_object_or_404(Profile, id=profile_id)
                certification.profile = profile
                certification.save()
                return redirect('certification_list')
            else:
                form.add_error(None, "Profile ID not found in session.")
    else:
        form = CertificationForm()

    return render(request, 'user/add_certification.html', {'form': form})

def certification_list(request):
    name = request.session['username']
    profile_id = request.session['id']
    profile = get_object_or_404(Profile, id=profile_id)
    certifications = Certification.objects.filter(profile=request.session['id'])
    return render(request, 'user/certification_list.html', {'certifications': certifications,'profile':profile, 'name':name})

def remove_certification(request, certification_id):
    certification = get_object_or_404(Certification, id=certification_id)
    certification.delete()
    return redirect('certification_list')

def website(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    projects = Project.objects.filter(profile=profile)
    certifications = Certification.objects.filter(profile=profile)
    work_experiences = WorkExperience.objects.filter(profile=profile)

    social_media_links = profile.social_media_links.split(",") if profile.social_media_links else []
    social_media_platforms = [(link.strip(), identify_social_media_platform(link.strip())) for link in social_media_links]
    
    context = {
        'social_media_platforms': social_media_platforms,
        'profile': profile,
        'projects': projects,
        'certifications': certifications,
        'workexperiences': work_experiences
    }
    return render(request, 'user/website.html', context)

def allprofiles(request):
    profiles = Profile.objects.all()
    return render(request, 'user/profileview.html',{'profiles':profiles})

def search(request):
    query = None
    profile = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        profile = Profile.objects.filter(Q(first_name=query) | Q(username=query))
    else:
        profile = []

    context = {'profile': profile, 'query': query}
    return render(request, 'user/profileview.html', context)