from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import SignUpForm, LoginForm, BookForm, NotesForm, MessageForm, BookRequestForm
from .models import BookDet, NotesDet, ChatRoom, ChatW, MyUser, ShoppingCart, Order, BookReq
from django.db.models import Q, Max
from django.db import models, transaction

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # update this if you have a homepage
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # update this as needed
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    books = BookDet.objects.all()
    return render(request, 'core/home.html', {'books': books})

@login_required
def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'core/upload_book.html', {'form': form})

@login_required
def upload_notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST, request.FILES)
        if form.is_valid():
            notes = form.save(commit=False)
            notes.uploader = request.user
            notes.save()
            return redirect('home')
    else:
        form = NotesForm()
    return render(request, 'core/upload_notes.html', {'form': form})

def search_resources(request):
    query = request.GET.get('q', '')
    book_results = BookDet.objects.filter(title__icontains=query)
    notes_results = NotesDet.objects.filter(title__icontains=query)

    data = {
        'books': list(book_results.values('title')),
        'notes': list(notes_results.values('title'))
    }
    return JsonResponse(data)

@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(MyUser, id=user_id)

    # Find or create ChatRoom
    room, created = ChatRoom.objects.get_or_create(
        user1=min(request.user, other_user, key=lambda u: u.id),
        user2=max(request.user, other_user, key=lambda u: u.id)
    )

    messages = ChatW.objects.filter(room=room).order_by('timestamp')
    # mark all received messages as read
    messages.filter(sender=other_user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = room
            message.sender = request.user
            message.is_read = False
            message.save()
            return redirect('chat', user_id=other_user.id)
    else:
        form = MessageForm()

    return render(request, 'core/chat.html', {
        'room': room,
        'messages': messages,
        'form': form,
        'other_user': other_user
    })

def base_context(request):
    if request.user.is_authenticated:
        unread_count = ChatW.objects.filter(
            room__in=ChatRoom.objects.filter(
                models.Q(user1=request.user) | models.Q(user2=request.user)
            ),
            is_read=False
        ).exclude(sender=request.user).count()

        return {'unread_count': unread_count}
    return {}

@login_required
def user_list(request):
    User = get_user_model()
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'core/user_list.html', {'users': users})

@login_required
def chat_inbox(request):
    rooms = ChatRoom.objects.filter(
        models.Q(user1=request.user) | models.Q(user2=request.user)
    )

    inbox = []
    for room in rooms:
        # Get the other user
        other_user = room.user2 if room.user1 == request.user else room.user1
        # Get last message (if any)
        last_msg = ChatW.objects.filter(room=room).order_by('-timestamp').first()
        inbox.append({
            'room': room,
            'other_user': other_user,
            'last_msg': last_msg
        })

    return render(request, 'core/chat_inbox.html', {'inbox': inbox})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(BookDet, id=book_id)
    cart_item, created = ShoppingCart.objects.get_or_create(user=request.user, book=book)
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = ShoppingCart.objects.filter(user=request.user)
    return render(request, 'core/cart.html', {'cart_items': cart_items})

@login_required
@transaction.atomic
def place_order(request, book_id):
    book = get_object_or_404(BookDet, id=book_id)

    # Lock to avoid race condition (double click / multi-tab)
    existing_order = Order.objects.select_for_update().filter(
        buyer=request.user,
        book=book,
        status="Pending"
    ).first()

    if existing_order:
        # Already ordered while another tab was still submitting
        return redirect('view_cart')

    # ✅ Create the order
    Order.objects.create(
        buyer=request.user,
        seller=book.seller,
        book=book,
        status="Pending"
    )

    # 🛒 Clean up
    ShoppingCart.objects.filter(user=request.user, book=book).delete()
    BookReq.objects.filter(user=request.user, title__iexact=book.title).delete()

    return redirect('view_cart')

@login_required
def order_history(request):
    my_orders = Order.objects.filter(buyer=request.user).order_by('-timestamp')
    received_orders = Order.objects.filter(seller=request.user).order_by('-timestamp')

    return render(request, 'core/order_history.html', {
        'my_orders': my_orders,
        'received_orders': received_orders
    })

@login_required
def request_book(request):
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']

            # ✅ Check if user already requested this book
            already_requested = BookReq.objects.filter(
                user=request.user, 
                title__iexact=title
            ).exists()

            # ❌ Prevent duplicate request if it's still in list
            if already_requested:
                form.add_error('title', 'You have already requested this book.')
            else:
                # ✅ Allow new request
                req = form.save(commit=False)
                req.user = request.user
                req.save()
                return redirect('list_book_requests')
    else:
        form = BookRequestForm()

    return render(request, 'core/request_book.html', {'form': form})


@login_required
def list_book_requests(request):
    requests = (
        BookReq.objects
        .values('title')  # group by title
        .annotate(
            latest_time=Max('requested_on'),
            description=models.F('description'),
            username=models.F('user__username')
        )
        .order_by('-latest_time')
    )
    return render(request, 'core/book_requests.html', {'requests': requests})
