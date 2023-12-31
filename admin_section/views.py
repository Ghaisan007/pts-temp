from django.shortcuts import render, get_object_or_404, redirect
from main.models import Book
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core import serializers
# from admin_section.forms import BookForm
from django.urls import reverse

# Create your views here.
def show_admin(request):
    context = {}

    return render(request, "admin.html", context)

def show_book_list_admin(request):
    p = Paginator(Book.objects.all(), 20)
    page = request.GET.get('page')

    top5 = Book.objects.all()[:5]
    books = p.get_page(page)
    print(top5)
    context = {
        'books': books,
        'top5': top5,
    }

    return render(request, "book_list_admin.html", context)

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users':users})

def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_section:user_list')
    return render(request, 'user_list.html', {'user': user})

def get_book_json(request):
    book_item = Book.objects.all()
    return HttpResponse(serializers.serialize('json', book_item))

@csrf_exempt
def add_book_ajax(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        author = request.POST.get("author")
        average_rating = request.POST.get("average_rating")
        isbn = request.POST.get("isbn")
        isbn13 = request.POST.get("isbn13")
        language_code = request.POST.get("language_code")
        num_pages = request.POST.get("num_pages")
        rating_count = request.POST.get("rating_count")
        text_review_count = request.POST.get("text_review_count")
        publication_date = request.POST.get("publication_date")
        publisher = request.POST.get("publisher")
    
        new_book = Book(title=title, author=author, average_rating=average_rating, isbn=isbn, isbn13=isbn13, language_code=language_code, 
            num_pages=num_pages, rating_count=rating_count, text_review_count=text_review_count, 
            publication_date=publication_date, publisher=publisher)
        new_book.save()

        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()

# def edit_book(request, id):
#     book = Book.objects.get(pk = id)

#     form = BookForm(request.POST or None, instance=book)

#     if form.is_valid() and request.method == "POST":
#         form.save()
#         return HttpResponseRedirect(reverse('admin_section:show_book_list_admin'))

#     context = {'form': form}
#     return render(request, "edit_book.html", context)

def delete_book(request, id):
    book = Book.objects.get(pk = id)
    book.delete()
    return HttpResponseRedirect(reverse('admin_section:show_book_list_admin'))