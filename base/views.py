from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'base/home.html')


@login_required(login_url='login')
def updateProfile(request):
   user = request.user
   update_form = UserProfileForm(instance=user)
   if request.method == 'POST':
      update_form = UserProfileForm(request.POST,request.FILES, instance=user)
      if update_form.is_valid():
         update_form.save()
         return redirect('user_profile' , pk=user.id)
 
   context = {'update_form':update_form}
   return render(request,'base/update_profile.html', context)

@login_required(login_url='login')
def deleteUser(request, pk):
   user = User.objects.get(id=pk)

   if request.method == 'POST':
      user.delete()
      return  redirect('home')

   return render(request, 'base/delete.html' , {'obj' :user})

