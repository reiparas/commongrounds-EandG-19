import datetime
from django import forms
from .models import Book, BookReview, Borrow

class BookReviewForm(forms.ModelForm):

    class Meta:
        model = BookReview
        fields = ["anonymous_reviewer", "title", "comment"]

    def __init__(self, *args, **kwargs):
        reviewer_name = kwargs.pop("reviewer_name", None)
        super().__init__(*args, **kwargs)
        if reviewer_name:
            self.fields["anonymous_reviewer"].initial = reviewer_name
            self.fields["anonymous_reviewer"].widget.attrs["readonly"] = True
            self.fields["anonymous_reviewer"].label = "Name"
    
class BookContributeForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = ["title", "genre", "author", "synopsis", "publication_year", "available_to_borrow"]
        widgets = {"genre": forms.Select()}

class BookUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = ["title", "genre", "author", "synopsis", "publication_year", "available_to_borrow"]
        widgets = {"genre": forms.Select()}

class BorrowForm(forms.ModelForm):

    class Meta:
        model = Borrow
        fields = ["name", "date_borrowed"]
        widgets = {
            "date_borrowed": forms.DateInput(attrs={"type": "date"}),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.date_to_return = instance.date_borrowed + datetime.timedelta(days=14)
        if commit:
            instance.save()
        return instance

class BookFormFactory:
    @classmethod
    def get_form(cls, context, **kwargs):
        data = kwargs.get("data", None)
        instance = kwargs.get("instance", None)

        if context == "review":
            reviewer_name = kwargs.get("reviewer_name", None)
            return BookReviewForm(data, reviewer_name=reviewer_name)
        elif context == "contribute":
            return BookContributeForm(data) 
        elif context == "update":
            return BookUpdateForm(data, instance=instance)
        else:
            raise ValueError(f"Unknown form context: {context}")   