from Trombinoscoop.forms import LoginForm # importation de la class "loginForm" du module forms.py 
from Trombinoscoop.forms import StudentProfileForm
from Trombinoscoop.forms import EmployeeProfileForm , StudentProfileForm
from Trombinoscoop.forms import AddFriendForm
from Trombinoscoop.models import Person , Student, Employee, Message
from datetime import date 
from django.shortcuts import render , redirect, get_object_or_404
from datetime import datetime
from django import forms
from django.http import HttpResponse
from django.contrib.auth.models import User




# def welcome(request):
#     if 'logged_user_id' in request.session:
#         logged_user_id = request.session['logged_user_id']
#         logged_user = Person.objects.get(id=logged_user_id)
 #       return render(request, 'welcom.html')
#     else:
#         return redirect('/login')


# def login(resquest):
#     return render(resquest, 'login.html')

# login n° 1
# def login(request):
#     # Teste si formulaire a été envoyé
#     if len(request.POST) > 0:
#         #Test si les parametres attendus ont été transmis
#         if 'email' not in request.POST or 'password' not in request.POST:
#             error= "Veuillez entre une adresse de courriel et un mot de passe."
#             return render(request, 'login.html', {'error': error})
#         else:
#             email = request.POST['email']
#             password = request.POST['password']

#             # Teste si le mot de passe est le bon
#             if password != 'sesame' or email != 'tayoro':
#                 error = "Adresse de courriel ou mot de passe erroné."
#                 return rendre(request, 'login.html', {'error':error})
#             # Tout es bon, on va a la page d'accueil
#             else:
#                 return redirect('/welcome')
#     else:
#         return render(request, 'login.html')


# ****vrai
def welcome(request):
    # appel de fonction protctetion des page privée "get_logged_user_from_request(request)"
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        # on verifi si un message est passé en paramettre si tel est la cas :
        if 'newMessage' in request.GET and request.GET['newMessage'] != '':
            newMessage = Message(author=logged_user, content=request.GET['newMessage'], publication_date = date.today())
            newMessage.save()

        friendMessages = Message.objects.filter(author=logged_user).order_by('-publication_date')
        return render(request, 'welcome.html', {'logged_user': logged_user, 'friendMessages':friendMessages})
    else:
        return redirect('/login')

def login(request):
    # Teste si formulaire a été envoyé
    if len(request.POST) > 0:
        form = LoginForm(request.POST)
        if form.is_valid():

            ###sesion
            # On initialise notre mail au mail saisir dans le champ mail
            user_email = form.cleaned_data['email']
            # on recherche dans la base de donnée tous la mail correspondant a notre mail saisir dans notre champ login
            logged_user = Person.objects.get(email=user_email)
            # nous comparrons notre mot de pass a notre mot de pass saisir 
            request.session['logged_user_id'] = logged_user.id
            # fin de session
            return redirect('/welcome')
        else:
            return render(request, 'login.html', {'form':form})
    else:
        form = LoginForm() # appel de la class LoginForm()
        return render(request, 'login.html', {'form': form})


#*****vrai
def register(request):
    # si la requette est envoyé et qu'il existe un profil type dans la requette alors 
    if len(request.GET) > 0 and 'profileType' in request.GET:
        studentForm = StudentProfileForm(prefix="st")
        employeeForm = EmployeeProfileForm(prefix="em")
        # si le profileType est un etudiant 
        if request.GET['profileType'] == 'student':
            studentForm = StudentProfileForm(request.GET, prefix='st')
            # la formulaire etudiant est valid
            if studentForm.is_valid():
                # alors enregistrer 
                studentForm.save()
                # et redirige a la page login
                return redirect('/login')
        # sinon si le profiletype est employé 
        elif request.GET['profileType'] == 'employee':
            employeeForm = EmployeeProfileForm(request.GET, prefix='em')
            # et si la formulaire Employer est valide alors 
            if employeeForm.is_valid():
                #alors enregistrer
                employeeForm.save()
                return redirect('/login')
        # Le formulaire n'est pas valide
        return render(request, 'user_profile.html', {'studentForm':studentForm, 'employeeForm': employeeForm})
    else:
        # si la requette n'a pas pu etre envoyé 
        studentForm = StudentProfileForm(prefix='st')
        employeeForm = EmployeeProfileForm(prefix='em')
        return render(request, 'user_profile.html', {'studentForm':studentForm, 'employeeForm': employeeForm})


#******vrai
# protctetion des page privée P246

def get_logged_user_from_request(request):
    # on regarde s'il existe un id utilisateur 
    if 'logged_user_id' in request.session:  
        logged_user_id = request.session['logged_user_id']
        # si utilisateur est authentifier 
        # on cherhce un etudiant 
        if len(Student.objects.filter(id=logged_user_id)) == 1:
            return Student.objects.get(id=logged_user_id)
        # on cherche un employe
        elif len(Employee.objects.filter(id=logged_user_id)) == 1:
            return Employee.objects.get(id=logged_user_id)
        # si on a rien trouvé
        else:
            return None
    else:
        return None


#**************************************essais************************
# def register(request):
#     if len(request.GET) > 0:       
#         form = StudentProfileForm(request.GET)
#         if form.is_valid():
#             form.save()
#             return redirect('/login')
#         else:
#             return render(request,'user_profile.html', {'form': form})
#     else:
#         form = StudentProfileForm()
#         return render(request, 'user_profile.html', {'form': form})

# def welcome(request):
#     homme = 'roma'
#     return render(register, 'welcome.html')


#************************************nvtes
# def register(request):
#     if len(request.GET) > 0 and 'profileType' in request.GET:
#         studentFrom = StudentProfileForm(prefix="st")
#         employeeForm = EmployeeProfileForm(prefix="em") 
#         if request.GET['profileType'] == 'student' :
#             studentFrom =  StudentProfileForm(request.GET, prefix="st")
#             if studentFrom.is_valid():
#                 studentFrom.save()
#                 return redirect('/login')
#         elif request.GET['profileType'] == 'employee':
#             employeeForm = EmployeeProfileForm(request.GET, prefix="em")
#             if employeeForm.is_valid():
#                 Employee.save()
#                 return redirect('/login')
#         return render(request, 'user_profile.html', {'studentFrom': studentFrom, 'employeeForm': employeeForm})
#     else:
#         studentFrom = StudentProfileForm(prefix="st")  
#         employeeForm = EmployeeProfileForm(prefix="em")
#         return render(request, 'user_profile.html', {'studentForm': studentFrom, 'employeeForm': employeeForm})    
        

def add_friend(request):
    logged_user = get_logged_user_from_request(request)
    # si authentifier 
    if logged_user:
        # Test si le formulaire a été envoyé
        # s'il ya une requette 
        if len(request.GET) > 0:
            form = AddFriendForm(request.GET)
            # et que le formulaire est valide 
            if form.is_valid():
                # on prend le mail saisir dans le champ
                new_friend_email = form.cleaned_data['email']
                # et on le recherche dans la base de données
                newFriend = Person.objects.get(email=new_friend_email)
                # on ajout aux amis
                logged_user.friends.add(newFriend)
                # et on sauvegarde la requette
                logged_user.save()
                return redirect('/welcome')
            # si le formaulaire n'est pas valide alors 
            else:
                return render(request, 'add_friend.html', {'form': form})
        # si le formulaire n'a pas été envoyé 
        else:
            form = AddFriendForm()
            # renvoyer le formulaire AddFriendForm a 'add_friend.html'
            return render(request, 'add_friend.html', {'form': form})
    # sinon authentifie toi 
    else:
        return redirect('/login')
    
    
def show_profile(request):
    logged_user = get_logged_user_from_request(request)
    if logged_user: # verification si un utilisateur est authentifié
        #Teste si le parametre attendu est bien passé
        if 'userToShow' in request.GET and request.GET['userToShow'] != '': #on controle que l'id de la personnne dont on veut voir est bien passé en parametre
            user_to_show_id = int(request.GET['userToShow']) # on met l'identifant dans une variable en la convertissant directement en intier
            results = Person.objects.filter(id=user_to_show_id) # on recherche l'enregistrement dans correspondant dans la base donnée 
            if len(results)==1:
                if Student.objects.filter(id=user_to_show_id):
                    user_to_show = Student.objects.get(id=user_to_show_id)
                else:
                    user_to_show = Employee.objects.get(id=user_to_show_id)
                return render(request, 'show_profile.html', {'user_to_show': user_to_show})
            else:
                return render(request, 'show_profile.html', {'user_to_show': logged_user})
        # le parametre n'a pas été trouvé
        else:
            return render(request, 'show_profile.html',{'user_to_show': logged_user})
    else:
        return redirect ('/login')
    
    
def modify_profile(request):
    logged_user = get_logged_user_from_request(request)
    # si authentifier 
    if logged_user:
        # Test si le formulaire a été envoyé
        # s'il ya une requette 
        if len(request.GET) > 0:
            
            #si le type de personne connecté est un etudiant
            if type(logged_user) == Student:
                form = StudentProfileForm(request.GET, instance=logged_user)
            #sinon
            else:
                form = EmployeeProfileForm(request.GET, instance=logged_user)
            if form.is_valid():
                form.save()
                return redirect('/welcome')
            else:
                return render(request, 'modify_profile.html', {'form':form}) # on envoi le formulaire 'form' en question vers la page  'modify_profile.html'
        else:
            if type(logged_user) == Student:
                form = StudentProfileForm(instance=logged_user)
            #sinon
            else:
                form = EmployeeProfileForm(instance=logged_user)
            return render(request, 'modify_profile.html', {'form':form})
    else:
        return redirect('/login')
    
    
def logout(request):
    try:
        del request.session['logged_user_id']
    except:
        return redirect('/login')
    return redirect ('/login')
        
        
#def delete_friend_request(request, id):
        # logged_user = get_logged_user_from_request(request)
        # if logged_user:
            # productobj= get_object_or_404(Person, id=id)
            # person= Person()
            # person.friends.remove(productobj)
            # return render(request, 'welcome.html')

            # person=Person()
            # registrationNumber_person = request.registration_number.person
            # friend_person = get_object_or_404(User, id=id)
            # registrationNumber_person.friends.remove(friends_person) # A removes B
            # friend_person.friends.remove(registration_number) # B removes A
            # return render(request, 'welcome.html')
            
            
            # user_with_no_person= User.objects.filter(email__isnull=True)
            # for u in user_with_no_person:
            #     u.person = Person()
            #     u.save()
            #registrationNumber_person = request.registration_number.person
            #riend_person = get_object_or_404(Person, id=id)
            # friend_person = get_object_or_404(Person.objects.select_related('person'), id=id)
            #registrationNumber_person.friends.remove(friends_person) # A removes B
            #friend_person.friends.remove(registration_number) # B removes A
            #return redirect("/") 
        
            
def delete_friend_request(request, id):
    user_person = request.user.person
    friend_person = get_object_or_404(Person,id=id) # Profile instance has the same id as user
    user_person.friends.remove(friend_personn) # A removes B
    friend_person.friends.remove(user_person) # B removes A
    return HttpResponseRedirect('/')

        
#verification qu'une adresse de couriel passée en parametre est valide
def ajax_check_email_field(request):
    html_to_return = ''
    if 'value' in request.GET:
        field = forms.EmailField()
        try:
            field.clean(request.GET['value'])
        except forms.ValidationError as ve:
            html_to_return = '<ul class="errorlist">'
            for message in ve.messages:
                html_to_return += '<li>' + message + '</li>'
            html_to_return += '</ul>'
            
        if len(html_to_return) == 0:
            if len(Person.objects.filter(email=request.GET['value'])) >=1:
                html_to_return ='<ul class="errorlist">'
                html_to_return ='<li>Cette adresse est deja utilisée!</li>'
                html_to_return = '<ul>'
    return HttpResponse(html_to_return)


        
            
