from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'chat/room.html')


#---------------------------Admin and Admins Page Functions ------------------------------
@login_required(login_url="login")
# @allowed_users(allowed_roles=['super_admin'])
def adminsPage(request):
    group = Group.objects.get(name='super_admin')
    group_users = group.user_set.all()

    admin_group = Group.objects.get(name='Admins')
    admin_group_users = admin_group.user_set.all()

    sports_admins = Group.objects.get(name='sports_admins')
    sports_admins_users = sports_admins.user_set.all()

    context = {'group_users':group_users, 'sports_admins_users':sports_admins_users, 'admin_group_users':admin_group_users}
    return render(request , 'base/admins_page.html' , context)

@login_required(login_url="login")
# @allowed_users(allowed_roles=['super_admin'])
def changeRole(request):
   #  message = None
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            HttpResponse("User with the provided email doesnt exist")
            # message = "User with the provided email doesnt exist"
            # return redirect('change_role')
    
        users_group = Group.objects.get(name='Students')
        if users_group not in user.groups.all():
            return HttpResponse("The user isnt registered in the website")
            
        user.groups.remove(users_group)

        admin_group = Group.objects.get(name='Admins')
        user.groups.add(admin_group)

        return redirect('admins_page')

    context = {}
    return render(request , 'base/change_role.html' , context)

@login_required(login_url="login")
# @allowed_users(allowed_roles=['super_admin'])
def addSportsAdmin(request):
   # message = None
   if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            
            return HttpResponse("The user isnt registered in the website")
            message = "The user with the registered email doesnt exist"
            return redirect('add_sports_admin')
    
        users_group = Group.objects.get(name='Students')
        if users_group not in user.groups.all():
            return HttpResponse("The user isnt registered in the website")
            
        user.groups.remove(users_group)

        sports_admin_group = Group.objects.get(name='sports_admins')
        user.groups.add(sports_admin_group)

        return redirect('admins_page')

   context = {}
   return render(request , 'base/change_role.html' , context)


#---------------------------Basic Website Functions ------------------------------

def home(request):
   events = Event.objects.all()
   second_events = Event.objects.all()[0:8]
   topics = Topic.objects.all()[0:4]

   sports_events = Sport_Event.objects.all()[0:4]

   group = Group.objects.get(name='super_admin')
   admin_group = Group.objects.get(name='Admins')
   sports_admins = Group.objects.get(name='sports_admins')
   
   sports_admins_users = sports_admins.user_set.all()
   admin_group_users = admin_group.user_set.all()
   group_super_admin = group.user_set.all()


   context = {'events':events, 'group_super_admin':group_super_admin, 'admin_group_users':admin_group_users, 'sports_admins_users':sports_admins_users, 'sports_events':sports_events, 'topics':topics}
   return render(request , 'base/home.html', context)

def signup(request):
    page = 'signup'

    if request.user.is_authenticated:
      return redirect('home')

    form = MyUserCreationForm()
    
    if request.method == 'POST':
      form = MyUserCreationForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.username = user.username.lower()
         user.save()

         group = Group.objects.get(name='Students')
         user.groups.add(group)
         username = form.cleaned_data.get('username')
         messages.success(request, f'Account successfully created for {username}')

         login(request, user)
         return redirect('home')
      # else:
      #    messages.error(request , 'An error has occured during registration')


    context = {'page':page, 'form':form}
    return render(request , 'base/login_register.html', context)

@unauthenticated_user
def loginPage(request):
   page = 'login'

   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')

      try:
         user = User.objects.get(username=username)
         
      except:
         messages.error(request, 'User does not exist')
      
      user = authenticate(request, username=username , password=password)
      if user is not None:
         login(request, user)
         return redirect('home')
      else:
         messages.error(request, 'Username or Password doesnt exist')


   context = {'page':page}
   return render(request, 'base/login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')

def sportsEvent(request):
   sports_events = Sport_Event.objects.all()
   context = {'sports_events':sports_events}
   return render(request, 'base/events_component.html', context)



#---------------------------User Profile functions ------------------------------
def userProfile(request, pk):
   user = User.objects.get(id=pk)
   events = user.event_set.all()


   context = {'user':user, 'events':events}
   return render(request, 'base/profile.html', context)

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