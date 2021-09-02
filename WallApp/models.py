from django.db import models
import re
import bcrypt

class UserManager(models.Manager):

    def reg_validation(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        errors = {}
        if len(postData['fname']) <= 0:
            errors["fname"] = "Must enter a first name!"
        elif len(postData['fname']) < 2:
            errors["fname"] = "First name should be at least 2 characters!"
        if len(postData['lname']) <= 0:
            errors["lname"] = "Must enter a last name!"
        elif len(postData['lname']) < 2:
            errors["lname"] = "Last name should be at least 2 characters!"
        if len(postData['pwd']) <= 0:
            errors["pwd"] = "Password is required!"
        if len(postData['pwd']) < 8:
            errors['pwd'] = "Password must be at least 8 characters!"
        if len(postData['email']) <= 0:
            errors["email"] = "Email is required!"
        if (not EMAIL_REGEX.match(postData["email"])):
            errors['email'] = "Invalid email format."    
        if User.objects.filter(email = postData['email'].lower()).exists():
            errors['email'] = "Email already exists."
        # if User.objects.filter(password = postData['pword']).exists():
        #     errors['pword'] = "Password already in use"
        if postData['confirm_pwd'] != postData['pwd']:
            errors['pwd3'] = "Confirmation password does not match password!"
        return errors
        
    def log_validation(self, postData):
        errors = {}
        try:
            user = User.objects.get(email = postData['email'])
        except:
            errors['email'] = f"Email address {postData['email']} is not registered in our database!"
            return errors
        if not bcrypt.checkpw(postData['pwd'].encode(), user.password.encode()):
            errors['pwd'] = "Password does not match our database!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def __repr__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Message(models.Model):
    message_text = models.TextField()
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment_text = models.TextField()
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        