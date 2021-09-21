from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def validador_campos(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        JUST_LETTERS = re.compile(r'^[a-zA-Z.]+$')
        PASSWORD_REGEX = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')

        errors = {}

        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email_exits'] = "Email ya registrado!!!"
        else:
            if len(postData['first_name'].strip()) < 2 or len(postData['first_name'].strip()) > 30:
                errors['first_name_len'] = "Nombre debe tener entre 2 y 30 caracteres"

            if len(postData['last_name'].strip()) < 2 or len(postData['last_name'].strip()) > 30:
                errors['last_name_len'] = "Apellido debe tener entre 2 y 30 caracteres"
            
            if not JUST_LETTERS.match(postData['first_name']) or not JUST_LETTERS.match(postData['last_name']):
                errors['just_letters'] = "Solo se permite el ingreso de letras en el nombre y apellido"
                
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "Formato correo no válido"
            
            if not PASSWORD_REGEX.match(postData['password']):
                errors['password_format'] = "Formato contraseña no válido"

        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Contraseñas no coinciden"

        return errors

class MessageManager(models.Manager):
    def validador_campos(self, postData):
        errors = {}
        if len(postData['message'].strip()) < 1 or len(postData['message'].strip()) > 500:
            errors['message_len'] = "Tu publicación debe tener 500 caracteres máximo"
        return errors

class CommentManager(models.Manager):
    def validador_campos(self, postData):
        errors = {}
        if len(postData['comment'].strip()) < 1 or len(postData['comment'].strip()) > 500:
            errors['comment_len'] = "El comentario debe tener 500 caracteres máximo"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

class Message(models.Model):
    user_id = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()
    
class Comment(models.Model):
    user_id = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    message_id = models.ForeignKey(Message, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()