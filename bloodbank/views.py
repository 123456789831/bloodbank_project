from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import User, BloodRequest

# Home Page
def home(request):
    return render(request, 'bloodbank/home.html')

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'bloodbank/register.html', {'form': form})

# User Login
def user_login(request):
    error = ''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            return redirect('dashboard')
        except User.DoesNotExist:
            error = 'Invalid login credentials'
    return render(request, 'bloodbank/login.html', {'error': error})

# Admin Login
def admin_login(request):
    error = ''
    if request.method == 'POST':
        if request.POST['username'] == 'admin' and request.POST['password'] == 'admin123':
            request.session['admin'] = True
            return redirect('dashboard')
        else:
            error = 'Invalid admin credentials'
    return render(request, 'bloodbank/admin_login.html', {'error': error})

# Dashboard
def dashboard(request):
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    message = ''
    if request.method == 'POST':
        blood_group = request.POST['blood_group']
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        user = User.objects.get(id=user_id)

        # Simulate blood availability (you can replace with real DB logic)
        available_groups = ['A+', 'B+', 'O+']
        is_available = blood_group in available_groups

        BloodRequest.objects.create(user=user, blood_group=blood_group, is_available=is_available)

        if is_available:
            message = f"{blood_group} blood is available. Admin has been notified."
        else:
            message = f"{blood_group} blood is not available at the moment."
    return render(request, 'bloodbank/dashboard.html', {'blood_groups': blood_groups, 'message': message})
