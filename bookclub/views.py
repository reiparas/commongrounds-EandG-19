from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Bookmark
from .forms import BookFormFactory, BorrowForm


def book_list(request):
    all_books = Book.objects.all()

    contributed = Book.objects.none()
    bookmarked = Book.objects.none()
    reviewed = Book.objects.none()

    if request.user.is_authenticated:
        profile = request.user.profile
        contributed = Book.objects.filter(contributor=profile)
        bookmarked = Book.objects.filter(bookmarks__profile=profile)
        reviewed = Book.objects.filter(reviews__user_reviewer=profile)

        user_book_ids = (
            contributed | bookmarked | reviewed 
        ).values_list("id", flat=True)
        all_books = all_books.exclude(id__in=user_book_ids)

    context = {
        "all_books":all_books,
        "contributed": contributed,
        "bookmarked": bookmarked,
        "reviewed":reviewed,
    }

    return render(request, "bookclub/book_list.html", context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    bookmark_count = book.bookmarks.count()
    profile = request.user.profile if request.user.is_authenticated else None

    reviewer_name = profile.displayName if profile else None
    review_form = BookFormFactory.get_form("review", reviewer_name=reviewer_name)

    if request.method == "POST" and "submit_review" in request.POST:
        review_form = BookFormFactory.get_form("review", 
                                               data=request.POST, 
                                               reviewer_name=reviewer_name)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            if profile:
                new_review.user_reviewer = profile
            new_review.save()
            return redirect("bookclub:book_detail", pk=pk)
        
    if request.method == "POST" and "toggle_bookmark" in request.POST:
        if profile:
            existing = Bookmark.objects.filter(profile=profile, book=book)
            if existing.exists():
                existing.delete()
            else:
                Bookmark.objects.create(profile=profile, book=book)
        return redirect("bookclub:book_detail", pk=pk)
        
    is_bookmarked = profile and Bookmark.objects.filter(profile=profile, 
                                                        book=book).exists()
    is_contributor = profile and book.contributor == profile

    context = {
        "book": book,
        "bookmark_count": bookmark_count,
        "is_bookmarked": is_bookmarked,
        "is_contributor": is_contributor,
        "review_form": review_form,
        "reviews": book.reviews.all(),
    }

    return render(request, "bookclub/book_detail.html", context)

@login_required
def book_create(request):
    form = BookFormFactory.get_form("contribute")
    if request.method == "POST":
        form = BookFormFactory.get_form("contribute", data=request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.contributor = request.user.profile
            book.save()
            return redirect("bookclub:book_detail", pk=book.pk)
    return render(request, "bookclub/book_form.html", {"form": form, 
                                                       "action": "Add"})

@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookFormFactory.get_form("update", instance=book)
    if request.method == "POST":
        form = BookFormFactory.get_form("update", data=request.POST, 
                                        instance=book)
        if form.is_valid():
            book = form.save()
            return redirect("bookclub:book_detail", pk=book.pk)
    return render(request, "bookclub/book_form.html", {"form": form, 
                                                       "action": "Edit"})

def book_borrow(request, pk):
    book = get_object_or_404(Book, pk=pk)
    profile = request.user.profile if request.user.is_authenticated else None

    initial ={}
    if profile:
        initial["name"] = profile.displayName

    form = BorrowForm(initial=initial)
    if request.method == "POST":
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.book = book
            if profile:
                borrow.borrower = profile
            borrow.save()
            book.available_to_borrow = False
            book.save()
            
            return redirect("bookclub:book_detail", pk=pk)
    return render(request, "bookclub/book_borrow.html", {"book": book, 
                                                         "form": form})