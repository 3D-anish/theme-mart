from django.shortcuts import render, redirect, get_object_or_404
from accounts.helper_func import get_user_object_from_username_or_email
from django.contrib.auth import get_user_model, authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import RegisterForm, ChangePasswordForm, EditProfileForm, ResetPasswordForm
from .decorators import deny_autheticated_user

# Create your views here.

@deny_autheticated_user
def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f"We have sent a verification link to your email.")
            return redirect("accounts:login")
    else:
        form = RegisterForm()
    
    ctx = {
        "title" : "Register | ThemeMart",
        "form" : form,
    }
    return render(request, "accounts/register.html", ctx)

@deny_autheticated_user
def verify_email(request):
    unverified_user_obj = get_object_or_404(get_user_model(),uuid = request.GET.get('token'),is_verified = False)
    if request.method == 'POST':
        ans = request.POST.get("answer")
        if ans == 'yes':
            unverified_user_obj.activate_account()
            messages.success(request,"Email verified successfully")
            return redirect("accounts:login")
        else:
            messages.warning(request,"Don't be oversmart")
    ctx = {
        "title" : "Verify Email | ThemeMart",
    }
    return render(request, "accounts/verify_email.html", context=ctx)

@deny_autheticated_user
def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get("username_or_email")
        password = request.POST.get("password")
        user_obj = get_user_object_from_username_or_email(username_or_email)
        if user_obj and user_obj.is_verified == True:
            valid_user = authenticate(request,username = user_obj.username, password = password)
            if valid_user:
                login(request,valid_user)
                messages.success(request,"Logged in successfully")
                invalid_redirect_urls = [
                    '/accounts/logout/',
                    '/accounts/register/',
                    '/accounts/login/',
                ]
                if request.GET.get("next") and not request.GET.get("next") in invalid_redirect_urls:
                    return redirect(request.GET.get("next"))
                else:
                    return redirect("main:home")
            else:
                messages.warning(request, "Password is incorrect")
                return redirect("accounts:login")
        elif user_obj and user_obj.is_verified == False:
            user_obj.send_verification_link()
            messages.success(request, 'Account is not verified. We have sent verification link to your mail.')
            return redirect("accounts:login")
        else:
            messages.warning(request, f"No account found with this username/email({username_or_email})")
            return redirect("accounts:login")
            
    ctx = {
        "title": "Login | ThemeMart",
    }
    return render(request, "accounts/login.html", ctx)

@login_required
def logout_view(request):
    request.user.session_set.all().delete()
    # logout(request)
    messages.success(request,"Logged out successfully")
    return redirect("accounts:login")

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():
            current_password = form.cleaned_data.get("current_password")
            valid_user = authenticate(request,username = request.user.username,password =current_password )
            if not valid_user:
                form.add_error("current_password","Current Password is incorrect")
            else:
                form.save(valid_user)
                login(request,valid_user)
                messages.success(request,"Password Changed successfully")
                return redirect("accounts:change_password")
    else:
        form = ChangePasswordForm()
    
    ctx = {
        "title" : "Change Password | ThemeMart",
        "form" : form,
    }
    return render(request, "accounts/change_password.html", context=ctx)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(data=request.POST,files=request.FILES,instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile updated successfully")
            return redirect("accounts:edit_profile")
    else:
        form = EditProfileForm(instance=request.user)
    
    ctx = {
        "title" : "Edit Profile | ThemeMart",
        "form" : form,
    }
    return render(request,"accounts/edit_profile.html",context=ctx)

@deny_autheticated_user
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        user_obj = get_user_model().objects.filter(email = email, is_active = True, is_verified = True).first()
        if user_obj:
            user_obj.send_reset_password_link()
            messages.success(request,f"We have sent a reset password link to this email({email})")
            return redirect("accounts:login")
        else:
            messages.warning(request,f"We Could not found any account with this Email({email})")
            return redirect("accounts:forgot_password")
    
    ctx = {
        "title" : "Forgot Password | ThemeMart",
    }
    return render(request, "accounts/forgot_password.html", context=ctx)

@deny_autheticated_user
def reset_password(request):
    user_obj = get_object_or_404(get_user_model(),uuid = request.GET.get('token'),is_active = True,is_verified = True)
    if request.method == 'POST':
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            form.save(user_obj)
            messages.success(request,"Password changed successfully")
            return redirect("accounts:login")
    else:
        form = ResetPasswordForm()
    
    ctx = {
        "title" : "Reset Password | ThemeMart",
        "form" : form,
    }
    return render(request, "accounts/reset_password.html", context=ctx)
