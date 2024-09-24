# Tutoriel complet : django-elasticsearch-dsl et django-elasticsearch-dsl-drf

## 1. Introduction

Django-elasticsearch-dsl et django-elasticsearch-dsl-drf sont deux bibliothèques qui permettent d'intégrer Elasticsearch avec Django de manière transparente. Elles offrent une façon simple de synchroniser vos modèles Django avec Elasticsearch et de créer des API RESTful pour effectuer des recherches.

- django-elasticsearch-dsl (7.3.0) : Fournit une intégration entre Django et Elasticsearch.
- django-elasticsearch-dsl-drf (0.22.5) : Étend django-elasticsearch-dsl pour fournir des vues et des sérialiseurs compatibles avec Django REST Framework.

## 2. Configuration initiale

### 2.1 Installation

Installez les bibliothèques :

```bash
pip install django-elasticsearch-dsl==7.3.0 django-elasticsearch-dsl-drf==0.22.5
```

### 2.2 Configuration de Django

Ajoutez les applications à INSTALLED_APPS dans settings.py :

```python
INSTALLED_APPS = [
    # ...
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
]
```

Configurez la connexion à Elasticsearch :

```python
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}
```

## 3. Création d'un Document Elasticsearch

Un Document dans django-elasticsearch-dsl représente un modèle Django dans Elasticsearch.

Exemple avec un modèle Blog :

```python
# models.py
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# documents.py
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Blog

@registry.register_document
class BlogDocument(Document):
    class Index:
        name = 'blogs'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    title = fields.TextField()
    content = fields.TextField()
    created_at = fields.DateField()

    class Django:
        model = Blog
        fields = [
            'id',
        ]
```

## 4. Indexation des données

Pour indexer les données existantes :

```bash
python manage.py search_index --rebuild
```

## 5. Recherche de base

Vous pouvez maintenant effectuer des recherches :

```python
from elasticsearch_dsl import Q
from .documents import BlogDocument

# Recherche simple
results = BlogDocument.search().query("match", title="django")

# Recherche plus complexe
results = BlogDocument.search().query(
    Q("multi_match", query='django elasticsearch', fields=['title', 'content'])
)
```

## 6. Intégration avec Django REST Framework

### 6.1 Création d'un sérialiseur

```python
# serializers.py
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import BlogDocument

class BlogDocumentSerializer(DocumentSerializer):
    class Meta:
        document = BlogDocument
        fields = ('id', 'title', 'content', 'created_at')
```

### 6.2 Création d'une vue

```python
# views.py
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    SearchFilterBackend,
    OrderingFilterBackend,
)
from .documents import BlogDocument
from .serializers import BlogDocumentSerializer

class BlogDocumentView(DocumentViewSet):
    document = BlogDocument
    serializer_class = BlogDocumentSerializer
    filter_backends = [
        FilteringFilterBackend,
        SearchFilterBackend,
        OrderingFilterBackend,
    ]
    search_fields = ('title', 'content')
    filter_fields = {
        'title': 'title',
        'created_at': 'created_at',
    }
    ordering_fields = {
        'id': 'id',
        'title': 'title',
        'created_at': 'created_at',
    }
    ordering = ('id',)
```

### 6.3 Configuration des URLs

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogDocumentView

router = DefaultRouter()
router.register(r'blogs', BlogDocumentView, basename='blog')

urlpatterns = [
    path('', include(router.urls)),
]
```

## 7. Fonctionnalités avancées

### 7.1 Agrégations

```python
from django_elasticsearch_dsl_drf.filter_backends import FacetedSearchFilterBackend

class BlogDocumentView(DocumentViewSet):
    # ...
    filter_backends = [
        # ...
        FacetedSearchFilterBackend,
    ]
    faceted_search_fields = {
        'created_at': {
            'field': 'created_at',
            'facet': DateHistogramFacet,
            'options': {
                'interval': 'month'
            }
        }
    }
```

### 7.2 Suggestions

```python
from django_elasticsearch_dsl_drf.filter_backends import SuggesterFilterBackend

class BlogDocumentView(DocumentViewSet):
    # ...
    filter_backends = [
        # ...
        SuggesterFilterBackend,
    ]
    suggester_fields = {
        'title_suggest': {
            'field': 'title',
            'suggesters': [
                'completion',
            ],
        }
    }
```

## 8. Bonnes pratiques

1. Utilisez des index séparés pour chaque environnement (dev, staging, prod).
2. Configurez correctement le mapping des champs pour optimiser les performances.
3. Utilisez des tâches asynchrones pour l'indexation de grands volumes de données.
4. Mettez en place des tests pour vos documents et vues Elasticsearch.
5. Surveillez les performances de vos requêtes Elasticsearch.

## Conclusion

Django-elasticsearch-dsl et django-elasticsearch-dsl-drf offrent une intégration puissante entre Django, Django REST Framework et Elasticsearch. Elles permettent de créer rapidement des API de recherche performantes et flexibles. Avec ces outils, vous pouvez tirer parti de la puissance d'Elasticsearch tout en restant dans l'écosystème Django.

