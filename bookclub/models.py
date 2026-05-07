from django.db import models
from django.urls import reverse
from accounts.models import Profile


class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    contributor = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contributed_books",
    )

    author = models.CharField(max_length=255)
    synopsis = models.TextField(blank=True)
    publication_year = models.IntegerField()
    available_to_borrow = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-publication_year"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("bookclub:book_detail", kwargs={"pk": self.pk})
    

class BookReview(models.Model):

    user_reviewer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews",
    )
    anonymous_reviewer = models.CharField(max_length=255, blank=True, default="Anonymous")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        name = self.user_reviewer.displayName if self.user_reviewer else self.anonymous_reviewer
        return f"{self.title} - {name}"
    

class Bookmark(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )
    date_bookmarked = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.displayName} bookmarked {self.book.title}"


class Borrow(models.Model):
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name="borrows",
    )
    borrower = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="borrows",
    )

    name = models.CharField(max_length=255)
    date_borrowed = models.DateField()
    date_to_return = models.DateField()

    def __str__(self):
        return f"{self.name} borrowed {self.book.title}"

