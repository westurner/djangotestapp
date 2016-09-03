import factory
import factory.fuzzy

from django.conf import settings
from django_factory_boy import auth

from faker import Factory as FakerFactory

from .models import ResourceEdgeType, ResourceEdge, Resource

fake = FakerFactory.create('en_US')

FACTORY_BASE_CLS = factory.DjangoModelFactory

class ResourceEdgeTypeFactory(FACTORY_BASE_CLS):
    class Meta:
        model = ResourceEdgeType


class ResourceEdgeFactory(FACTORY_BASE_CLS):
    class Meta:
        model = ResourceEdge


class ResourceFactory(FACTORY_BASE_CLS):
    # id = UUID4
    url = fake.url()
    name = fake.catch_phrase()
    description = fake.paragraphs()  # note: html
    # description_html(): safe_htmlify(self.descripton)
    data = fake.pydict()
    # context_url = models.URLField() # TODO: what is this for

    class Meta:
        model = Resource

