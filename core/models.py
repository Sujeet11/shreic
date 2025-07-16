from django.db import models
from django.contrib.auth.models import AbstractUser

# 🌍 Location Models
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# 🎓 College & Gender
class College(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Gender(models.Model):
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.gender

# 👤 Custom User
class MyUser(AbstractUser):
    full_name = models.CharField(max_length=200)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubCategory1(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SubCategory2(models.Model):
    name = models.CharField(max_length=100)
    subcategory1 = models.ForeignKey(SubCategory1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class BookDet(models.Model):
    seller = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication = models.CharField(max_length=100)
    year = models.IntegerField()
    mrp = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='book_covers/')
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory1 = models.ForeignKey(SubCategory1, on_delete=models.SET_NULL, null=True)
    subcategory2 = models.ForeignKey(SubCategory2, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class NotesDet(models.Model):
    uploader = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='notes_files/')

    publication = models.CharField(max_length=100)
    year = models.IntegerField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory1 = models.ForeignKey(SubCategory1, on_delete=models.SET_NULL, null=True)
    subcategory2 = models.ForeignKey(SubCategory2, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class ChatRoom(models.Model):
    user1 = models.ForeignKey(MyUser, related_name='chat_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(MyUser, related_name='chat_user2', on_delete=models.CASCADE)

    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}"

class ChatW(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # 👈 NEW LINE

    def __str__(self):
        return f"From {self.sender.username}: {self.message[:30]}"

class Notification(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

class ShoppingCart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    book = models.ForeignKey(BookDet, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} in {self.user.username}'s cart"

class Order(models.Model):
    buyer = models.ForeignKey(MyUser, related_name='orders_placed', on_delete=models.CASCADE)
    seller = models.ForeignKey(MyUser, related_name='orders_received', on_delete=models.CASCADE)
    book = models.ForeignKey(BookDet, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"Order: {self.book.title} from {self.seller} to {self.buyer}"

class BookReq(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    requested_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} requested {self.title}"
