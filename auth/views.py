from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from videoapp.views import upload_video

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Set authenticated message
            error_message = "Authenticated!"
            return redirect('upload_video')
        else:
            # Authentication failed, set error message
            error_message = "Invalid username or password."
    return render(request, 'login.html', {'error_message': error_message})
