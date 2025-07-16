# 📚 Shreic - Django-Based Educational Resource Sharing Website

This is a web platform built using Django, based on the research paper *“A Django Based Educational Resource Sharing Website: Shreic”* by Shyam et al. It allows students to upload, search, request, and share academic books and notes.

---

## 🚀 Features

- 👤 Custom user registration (with gender, college, location)
- 📤 Upload books and notes (with image/PDF)
- 📬 Real-time chat between users
- 🛒 Add to cart and place orders (COD)
- 📄 Request unavailable books
- 🔔 Notifications for unread messages
- 🔎 Live search with results dropdown

---

## ⚙️ Installation

1. **Clone the repo**
   git clone https://github.com/yourusername/shreic-clone.git
   cd shreic-clone
2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate  # On Windows
3. Install dependencies
   pip install -r requirements.txt
4. Run migrations
   python manage.py makemigrations
   python manage.py migrate
5. Create superuser
   python manage.py createsuperuser
6. Run the development server
   python manage.py runserver

🗃️ Project Structure
   core/
│   views.py
│   models.py
│   forms.py
│   urls.py
│
├── templates/core/
│   base.html
│   home.html
│   upload_book.html
│   ...

🧪 Test Credentials
You can create your own users or login as:
   Username: admin
   Password: admin123 (if set during createsuperuser)

 🧠 Author
   Sujeet Singh

  📄 License
  This project is for academic use and educational purposes only.

  
---

### ✅ Result

You now have:
- `requirements.txt` to install your environment
- `README.md` to explain how your project works

---

Let me know if you want help with:
- ☁️ Deploying this live (Render, PythonAnywhere)
- 🧪 Final test checklist
- 📁 Zip project + submit for grading

You're almost done, Sujeet — and you've built something great! 💯👏
