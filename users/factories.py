import factory
import faker

from .models import User

fake = faker.Factory.create()


class UserFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = User

    email = factory.lazy_attribute(lambda o: fake.email())
