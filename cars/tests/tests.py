from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from cars.models import Article, Car


class ArticleModelArticle(TestCase):
    def test_article_has_attribute_titre(self):
        self.assertTrue(hasattr(Article(), 'Titre'))

    def test_first_char_titre_is_upper(self):
        art = Article.objects.create(Titre='Bmw')
        if art.Titre[0].isupper():
            self.assertTrue(art.Titre[0].isupper())
        else:
            self.fail('Première lettre doit être majuscule')

    def test_attribute_texte_article(self):
        self.assertTrue(hasattr(Article(), 'Texte'))

    def test_texte_should_be_blank(self):
        a = Article.objects.create(Titre='Bmw',
                                   Texte=None)
        try:
            a.full_clean()
        except ValidationError:
            self.fail('Texte doit pouroir être blanc')

class ArticleUrlTest(TestCase):
    def test_article_url_exists(self):
        reponse = self.client.get('/article/')
        self.assertEqual(reponse.status_code, 200)

    def test_url_accessible_by_name(self):
        reponse = self.client.get(reverse('cars:article'))
        self.assertEqual(reponse.status_code, 200)


class ArticleViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        nombre_article = 5

        for article_id in range(nombre_article):
            Article.objects.create(
                Titre=f'Titre {article_id}',
                Texte=f'Texte {article_id}'
            )

        nombre_voiture = 5

        for voiture_id in range(nombre_voiture):
            Car.objects.create(
                model=f'Voiture {voiture_id}',
                max_speed='300',
                description=f'Desc {voiture_id}'
            )

    def test_view_uses_correct_templates(self):
        reponse = self.client.get(reverse('cars:article'))
        self.assertTemplateUsed(reponse, 'cars/article.html')

    def test_one_article_per_car(self):
        self.assertEqual(Article.objects.count(), len(Car.objects.all()))

    def test_article_contains_titre(self):
        reponse = self.client.get(reverse('cars:article'))
        art = Article.objects.get(id=2)
        self.assertContains(reponse, art.Titre)


class ArticleTemplatesTest(TestCase):
    def test_get_button_return(self):
        reponse = self.client.get(reverse('cars:article'))

        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, '<button>Retour</button>', html=True)