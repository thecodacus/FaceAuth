
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View

from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from .forms import UserLoginForm, UserRegForm, UserFaceRegForm

from .utils import Base64ToNpImage, TensorflowBridge, Recognizer

from django.http import JsonResponse


import pickle
# Create your views here.
@login_required
def Home(request):
	return render(request,'recognition/home.html',{})

def Login(request):
	return render(request,'recognition/login.html',{})

class Auth(APIView):
	def get(self,request):
		return Response({'message':'use post request to use the auth api'})

	def post(self,request):
		return Response({'message':'use post request to use the auth api'})


class UserLoginView(View):
	form_class=UserLoginForm
	template_name='recognition/login.html'

	def get(self,request):
		form=self.form_class(None)
		return render(request,self.template_name,{'form':form})
	
	def post(self,request):
		form= self.form_class(request.POST)

		if form.is_valid():
			user=form.save(commit=False)
			# clean normalize data
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user.set_password(password)
			user.save()

			#return if credentials are correct

			user=authenticate(username=username,password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					#TODO Redirect to Face Registration pageß
					return redirect('recognition:home')
		print('something is wrong')
		return render(request,self.template_name,{'form':form})

class UserRegistrationView(View):
	form_class=UserRegForm
	template_name='recognition/register.html'

	def get(self,request):
		form=self.form_class(None)
		return render(request,self.template_name,{'form':form})
	
	def post(self,request):
		form= self.form_class(request.POST)

		if form.is_valid():
			user=form.save(commit=False)
			# clean normalize data
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user.set_password(password)
			user.save()

			#return if credentials are correct

			user=authenticate(username=username,password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					#TODO Redirect to Face Registration pageß
					return redirect('recognition:home')
		print('something is wrong')
		return render(request,self.template_name,{'form':form})


@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class UserFaceRegView(View):
	form_class=UserFaceRegForm
	template_name='recognition/reg-face.html'
	base64ToNpImage= Base64ToNpImage()
	tfBridge=TensorflowBridge()
	recogzr=Recognizer()

	def get(self,request):
		form=self.form_class(None)
		return render(request,self.template_name)
	
	def post(self,request):

		data = request.POST.getlist('imgs[]')
		images= self.base64ToNpImage.decodeArray(data)
		faces = self.tfBridge.imagesToFaces(images,(160,160))
		# return err if no face found
		if len(faces)==0:
			return JsonResponse({'status':'failed'}, status=201) 
		else:
			ppFaces=self.tfBridge.preprocessFaces(faces)
			embedded=self.tfBridge.embeddFaces(ppFaces)
			request.user.facesignature.signatures=pickle.dumps(embedded)
			request.user.facesignature.face=data[0]
			request.user.save()
			self.recogzr.train(User.objects.all())
			return JsonResponse({'status':'success'}, status=201) 



# login without password
# user.backend = 'django.contrib.auth.backends.ModelBackend'
# login(request, user)







