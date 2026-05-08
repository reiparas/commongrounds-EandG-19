from django.contrib import admin
from .models import Genre, Book, BookReview, Bookmark, Borrow


admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(BookReview)
admin.site.register(Bookmark)
admin.site.register(Borrow)
