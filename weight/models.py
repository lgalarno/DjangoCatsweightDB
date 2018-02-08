from django.db import models
from django.db.models.signals import pre_save

from CatsManagement.models import Cat

class Measure(models.Model):
    date        = models.DateField()
    #number      = models.IntegerField()
    class Meta:
        ordering = ['date']
    def __str__(self):
        return "{0}".format(self.date)
    def get_all_cats(self):
        return [cat.cat.id for cat in self.participant_set.all()]
    def get_number_of_cats(self):
        return len(self.get_all_cats())
    def get_weigths(self):
        return {c.cat : c.weight for c in self.participant_set.all()}

class Participant(models.Model):
    weight      = models.IntegerField()
    cat         = models.ForeignKey(Cat, on_delete = models.CASCADE)
    measurement  = models.ForeignKey(Measure, on_delete = models.CASCADE)
    def __str__(self):
        return "{0}".format(self.cat)

# def pre_save_measure_receiver(sender, instance, *args, **kwargs):
#     if instance.pk:
#         return
#     instance.number = Measure.objects.all().count() + 1
#
# pre_save.connect(pre_save_measure_receiver, sender=Measure)
