from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


class Source(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    link = models.URLField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        if self.author:
            return f"{self.author}: {self.title}"
        return self.title


class Term(models.Model):
    term = models.CharField(max_length=120, unique=True, db_index=True)
    slug = models.SlugField(max_length=140, unique=True)
    short_definition = models.CharField(max_length=255)
    full_definition = models.TextField(validators=[MinLengthValidator(30)])
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="terms",
    )
    source = models.ForeignKey(
        Source,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="terms",
    )
    synonyms = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["term"]
        indexes = [
            models.Index(fields=["term"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.term

    def get_absolute_url(self):
        return reverse("term_detail", kwargs={"slug": self.slug})


class UserSuggestion(models.Model):
    STATUS_NEW = "new"
    STATUS_REVIEWED = "reviewed"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_NEW, "New"),
        (STATUS_REVIEWED, "Reviewed"),
        (STATUS_REJECTED, "Rejected"),
    ]

    candidate_term = models.CharField(max_length=120)
    candidate_definition = models.TextField()
    contact_email = models.EmailField(blank=True)
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.candidate_term} ({self.status})"
