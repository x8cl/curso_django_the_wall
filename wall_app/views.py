from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

def home(request):
    return (render(request, 'wall_app/login.html'))

def register(request):
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        errors = User.objects.validador_campos(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            #Si se produce un error pero no queremos perder los datos....
            request.session['level_mensaje'] = 'alert-danger'
            return redirect('/') 
        else:
            request.session['registro_nombre'] = ""
            request.session['registro_apellido'] = ""
            request.session['registro_email'] = ""

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

            obj = User.objects.create(first_name=first_name, last_name=last_name,email=email,password=password_hash)
            messages.success(request, "Usuario registrado con éxito!!!!")
            request.session['level_mensaje'] = 'alert-success'
            
        return redirect('/')

    return render(request, 'wall_app/login.html')


def login(request):
    if request.method == 'GET':
        return redirect("/")
    else:
        if request.method == 'POST':
            user = User.objects.filter(email=request.POST['email_login'])
            #Buscamos el correo ingresado en la BD             
            if user : #Si el usuario existe
                usuario_registrado = user[0]
                if bcrypt.checkpw(request.POST['password_login'].encode(), usuario_registrado.password.encode()):
                    usuario = { # session
                        'id':usuario_registrado.id,
                        'first_name':usuario_registrado.first_name,
                        'last_name':usuario_registrado.last_name,
                        'email':usuario_registrado.email,
                        # 'rol':usuario_registrado.rol,
                    }

                    request.session['usuario'] = usuario
                    messages.success(request,"Ingreso correcto!!!!")
                    return redirect('/wall')
                else:
                    messages.error(request,"Datos mal ingresados o el usuario no existe!!!")
                    return redirect('/')
            else:
                messages.error(request,"Datos mal ingresados o el usuario no existe!!!")
                return redirect('/')

def wall(request):
    context={
        'messages': Message.objects.all().order_by('-created_at'),
        'comments': Comment.objects.all().order_by('-created_at'),
    }
    return render(request, 'wall_app/wall.html', context)

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    return redirect('/')

def new_message(request):
    if request.method == 'GET':
        return redirect('/') 
    
    else:
        if request.method == 'POST':
            errors = Message.objects.validador_campos(request.POST)

            if len(errors) > 0:
                for key,value in errors.items():
                    messages.error(request,value)
                return redirect('/wall')
            else:
                id_user = request.session['usuario']['id']
                user_id = User.objects.get(id=id_user)
                message = request.POST['message']
                obj = Message.objects.create(user_id = user_id, message = message)
                obj.save()
                return redirect('/wall')


def new_comment(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        if request.method == 'POST':
            errors = Comment.objects.validador_campos(request.POST)

            if len(errors) > 0:
                for key,value in errors.items():
                    messages.error(request,value)
                return redirect('/wall')
            else:
                id_user = request.session['usuario']['id']
                user_id = User.objects.get(id=id_user)
                id_message = request.POST['message_id']
                message_id = Message.objects.get(id=id_message)
                comment = request.POST['comment']
                obj = Comment.objects.create(user_id = user_id, message_id = message_id, comment = comment)
                obj.save()
                return redirect('/wall')

                

