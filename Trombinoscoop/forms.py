from django import forms # importation de la bibliotech "forms"
from Trombinoscoop.models import Person # import Person depuis la le mondule models
from Trombinoscoop.models import Student # import Student depuis la le mondule models
from Trombinoscoop.models import Employee 

class LoginForm(forms.Form): # creation d'une class qui prend en parametre le formulaire "form"de la bibliotech "forms"
    email = forms.EmailField(label='Couriel')
    password = forms.CharField(label='Mot de passe', widget = forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        # recupere les donnée dans les formulaires email et password .
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        # Verifie que les deux champs sont valides 
        if email and password:
            #cherche toute personne dont le mot de passe et l'adresse e-mail correspondent a ce qui a ete entré dans le formulaire
            result = Person.objects.filter(password=password, email=email)
            if len(result) != 1: # verifie qu'il n'y a qu'un seul resultat. 
                raise forms.ValidationError("Adresse de courriel ou mot de passe erroné(e). ")   
        return cleaned_data


class StudentProfileForm(forms.ModelForm):
    class Meta: # cree et configue notre formulaire , et se base sur le modèle student 
        model = Student
        exclude = ('friends',)
        
        
class EmployeeProfileForm(forms.ModelForm):
    class Meta: # cree et configue notre formulaire , et se base sur le modèle employee 
        model = Employee
        exclude = ('friends',)
    

class AddFriendForm(forms.Form):
    email = forms.EmailField(label='Courriel :')
    def clean(self):
        cleaned_data = super(AddFriendForm, self).clean()
        email = cleaned_data.get("email")

        # Verifie que le champ est valide
        if email:
            # recherche le mail dans la base de donnés
            result = Person.objects.filter(email=email)
            # if le mail n'est pas unique dans la base de données 
            if len(result) !=1:
                raise forms.ValidationError("Adresse de courruel erronée")
        return cleaned_data