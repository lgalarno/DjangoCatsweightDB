from django.test import TestCase

from CatsManagement.models import Cat
from .maketables import WriteTables

class MakeTablesTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        print('Hello')
        allcats = Cat.objects.all()
        catsset = [c.id for c in allcats]
        print(catsset)
        x = WriteTables(datesset='All', catsset=catsset)




