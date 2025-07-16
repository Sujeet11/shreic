from django.contrib import admin
from .models import (
    MyUser, Gender, College, City, State, Country,
    Category, SubCategory1, SubCategory2,
    BookDet, NotesDet, BookReq,
    ChatRoom, ChatW, Notification,
    ShoppingCart, Order
)

# Registering each model
admin.site.register(MyUser)
admin.site.register(Gender)
admin.site.register(College)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)

admin.site.register(Category)
admin.site.register(SubCategory1)
admin.site.register(SubCategory2)

admin.site.register(BookDet)
admin.site.register(NotesDet)
admin.site.register(BookReq)

admin.site.register(ChatRoom)
admin.site.register(ChatW)
admin.site.register(Notification)
admin.site.register(ShoppingCart)
admin.site.register(Order)
