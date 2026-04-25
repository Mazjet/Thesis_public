from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .forms import UserSuggestionForm
from .models import Category, Term


def home(request):
    latest_terms = Term.objects.select_related("category").order_by("-created_at")[:6]
    popular_categories = Category.objects.annotate(term_total=Count("terms")).order_by("-term_total", "name")[:6]
    category_count = Category.objects.count()
    term_count = Term.objects.count()
    return render(
        request,
        "dictionary/home.html",
        {
            "latest_terms": latest_terms,
            "popular_categories": popular_categories,
            "category_count": category_count,
            "term_count": term_count,
        },
    )


def term_list(request):
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    terms = Term.objects.select_related("category", "source")
    if query:
        terms = terms.filter(
            Q(term__icontains=query)
            | Q(short_definition__icontains=query)
            | Q(full_definition__icontains=query)
            | Q(synonyms__icontains=query)
        )
    if category_slug:
        terms = terms.filter(category__slug=category_slug)
    categories = Category.objects.all()
    return render(
        request,
        "dictionary/term_list.html",
        {
            "terms": terms,
            "categories": categories,
            "query": query,
            "selected_category": category_slug,
        },
    )


def term_detail(request, slug):
    term = get_object_or_404(Term.objects.select_related("category", "source"), slug=slug)
    return render(request, "dictionary/term_detail.html", {"term": term})


def category_list(request):
    categories = Category.objects.prefetch_related("terms")
    return render(request, "dictionary/category_list.html", {"categories": categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    terms = category.terms.select_related("source")
    return render(
        request,
        "dictionary/category_detail.html",
        {"category": category, "terms": terms},
    )


def about_project(request):
    return render(request, "dictionary/about.html")


def submit_suggestion(request):
    if request.method == "POST":
        form = UserSuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "dictionary/suggestion_success.html")
    else:
        form = UserSuggestionForm()
    return render(request, "dictionary/suggestion_form.html", {"form": form})
