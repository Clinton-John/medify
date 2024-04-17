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
