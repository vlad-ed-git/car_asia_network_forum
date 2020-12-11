from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, LoginForm, AccountUpdateForm
from rest_framework.authtoken.models import Token
from .models import Account
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from achievements.views import get_new_user_achievements_count, get_new_user_achievements, get_all_user_achievements, mark_new_user_achievements_as_viewed

def must_authenticate_view(request):
    if request.user.is_authenticated:
    	logout(request)
    return render(request, 'account/must_authenticate.html', {})

def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)


def logout_view(request):
	logout(request)
	return redirect('home')


def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect("home")

	if request.POST:
		form = LoginForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")

	else:
		form = LoginForm()

	context['login_form'] = form

	return render(request, "account/login.html", context)

@csrf_exempt
def logout_from_main_site_view(request):
    try:
      if request.POST:
        email = request.POST['email']
        token = request.POST['token']
        account = Account.objects.get(email=email)
        true_token = Token.objects.get(user=account)
        if true_token.key == token:
            logout(request)
            return redirect('https://asiacarnetwork.com') #JsonResponse({'success':'User has been logged out!' }) #
        else:
            return JsonResponse({'error':'Wrong token or email' })
      else:
          return JsonResponse({'error':'Suspiscious attempt!' })
    except Exception as err:
      msg = str(err)
      return JsonResponse({'exception raised': msg })
        
@csrf_exempt
def login_from_main_site_view(request):
    
    if request.POST:
        email = request.POST['email']
        token = request.POST['token']
        account = Account.objects.get(email=email)
        true_token = Token.objects.get(user=account)
        if true_token.key == token:
            login(request, account, backend='django.contrib.auth.backends.AllowAllUsersModelBackend')
            return redirect("home") #logged in
        else:
            return redirect("home") # logged out
    
    else:
        return JsonResponse({'error':'Suspiscious attempt!' })
    
def profile_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES or None, instance=request.user)
		if form.is_valid():
			form.save()
			form.initial = {
				"email": request.user.email, 
				"username": request.user.username,
				"display_name": request.user.display_name,
				"profile_picture": request.user.profile_picture,
			}
			context['success_message'] = "Updated"
		else:
    		#preserve initial data
			form.initial = {
				"email": request.POST['email'],
				"username": request.POST['username'],
				"display_name": request.POST['display_name'],
				"profile_picture": request.user.profile_picture,
			}
	else:
		form = AccountUpdateForm(

			initial={
					"email": request.user.email, 
					"username": request.user.username,
					"display_name": request.user.display_name,
					"profile_picture": request.user.profile_picture,
				}
			)

	context['profile_form'] = form
	new_achievements_count = get_new_user_achievements_count(request)
	if new_achievements_count:
		context['new_achievements_count'] = new_achievements_count
		context['new_achievements'] = get_new_user_achievements(request)
		mark_new_user_achievements_as_viewed(request)
	achievements_counts_list = get_all_user_achievements(request)
	if achievements_counts_list:
		context['discussion_starter'] = achievements_counts_list['discussion_starter']
		context['got_likes'] = achievements_counts_list['got_likes']
		context['celebrity'] = achievements_counts_list['celebrity']
		context['avid_reader'] = achievements_counts_list['avid_reader']
	return render(request, "account/profile.html", context)

def get_total_users(request, exclude_staff=False):
    if exclude_staff:
        return Account.objects.filter(is_super_editor=False, is_editor=False, is_admin=False).count()
    else:
        return Account.objects.filter().count() 