from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


class RegistrationForm(UserCreationForm):
	class Meta:
		model = Account
		fields = ("email",  'display_name', "password1", "password2")


class LoginForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login credentials")


class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('email',  'display_name', 'profile_picture')

	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use.' % email)

	def clean_display_name(self):
		display_name = self.cleaned_data['display_name']
		nameNoSpaces = display_name.replace(" ", "")
		if (len(nameNoSpaces) > 1 and len(nameNoSpaces) < 120):
			return display_name
		raise forms.ValidationError('Sorry, we failed to validate your name')

	def clean_profile_picture(self):
		return self.cleaned_data['profile_picture']