from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse

import datetime

from CatsManagement.models import Cat
from .models import Measure, Participant

def EnterWeight(request):
    cats = Cat.objects.filter(active=True)

    context = {'cats': cats}
    return render(request, 'weight/EnterWeight.html', context)

@require_POST
def WeightConfirm(request):
    requestdict = dict(request.POST)
    selectedc = requestdict.get('selectc')
    mdate = requestdict.get('getdate')[0]
    try:
        datetime.datetime.strptime(mdate, "%Y-%m-%d")
    except ValueError:
        messages.warning(request, "Could not read the date")
        return HttpResponseRedirect(reverse('weight:EnterWeight'))
    if selectedc:
        selectedcats = Cat.objects.filter(pk__in=selectedc)
        cweight= requestdict.get('cweigth')
        header = ['Cat','Weight']
        zipped = zip(selectedcats, cweight)
        context = {
            'header': header,
            'zipped': zipped,
            'mdate': mdate
        }
        return render(request, 'weight/WeightConfirm.html', context)
    messages.warning(request, "No cat(s) selected!")
    return HttpResponseRedirect('/')

@require_POST
def SaveWeight(request):
    #try:
        requestdict = dict(request.POST)
        selectedcats = requestdict.get('selectedc')
        cweight = requestdict.get('cweight')
        mdate = datetime.datetime.strptime(requestdict.get('getdate')[0], "%Y-%m-%d").date()
        header = ['Cat','Weight']
        zipped = zip(selectedcats, cweight)
        m = Measure(date= mdate)
        m.save()
        for c, w in zipped:
            p = Participant(weight=w, cat= Cat.objects.get(id=c), measurement=m)
            p.save()
        measurments = {p.cat.name:p.weight for p in m.participant_set.all()}
        mnumber = Measure.objects.all().count()
        print(mnumber)
        context = {
            "header":header,
            "measurments": measurments,
            "mnumber":mnumber,
            "date": m.date,
        }
        return render(request, 'weight/Success.html', context)
    # except:
    #     messages.warning(request, "Sorry, something wrong happened entering data in the database")
    #     return HttpResponseRedirect('/')