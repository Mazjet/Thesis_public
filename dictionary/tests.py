from django.test import TestCase
from django.urls import reverse

from .models import Category, Source, Term, UserSuggestion


class DictionaryViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Базові поняття",
            slug="bazovi-ponyattia",
            description="Основні терміни інформаційних технологій.",
        )
        self.source = Source.objects.create(
            title="Сучасні ІТ-системи",
            author="І. Петренко",
            year=2024,
        )
        self.term = Term.objects.create(
            term="Алгоритм",
            slug="algorytm",
            short_definition="Скінченна послідовність чітких дій.",
            full_definition=(
                "Алгоритм - це формалізований опис кроків, "
                "які виконуються для отримання потрібного результату."
            ),
            category=self.category,
            source=self.source,
        )

    def test_home_page_returns_success(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тлумачний словник")

    def test_term_search_filters_results(self):
        response = self.client.get(reverse("term_list"), {"q": "Алгоритм"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Алгоритм")

    def test_term_detail_page_exists(self):
        response = self.client.get(reverse("term_detail", kwargs={"slug": "algorytm"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Скінченна послідовність")

    def test_create_user_suggestion(self):
        response = self.client.post(
            reverse("submit_suggestion"),
            {
                "candidate_term": "Парсер",
                "candidate_definition": (
                    "Програма, що аналізує текст і виділяє структуру "
                    "за заданими правилами."
                ),
                "contact_email": "student@example.com",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserSuggestion.objects.count(), 1)
