from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, HttpResponse,reverse, redirect
from django.views.generic import TemplateView, View

import datetime
import os
import csv

from CatsManagement.models import Cat
from .maketables import WriteTables, WriteTablesNew
from .forms import SelectCatsForm
from weight.models import Measure, Participant

class WebtablesView(View):
    template_name = "tables/table.html"
    def get(self, request):
        headerwt, wt, headerst, st = WriteTablesNew(self.request, gdate = False)
        context = {'title': 'Measures',
                   'headermain': headerwt,
                   'headerst': headerst,
                   'maintable': wt,
                   'summarytable': st,
                   'stable_title': 'Average weights'}
        return render(request, "tables/table.html", context)

    def post(self, request):
        requestdict = dict(request.POST)
        ids = requestdict.get("selectw",None)
        request.session['selectby'] = 'ids'
        if not ids:
            return HttpResponseRedirect(reverse('tables:WebtablesView'))
        btn = request.POST['submitbtn']
        if btn == 'Delete':
            if request.user.is_authenticated:
                for i in ids:
                    try:
                        request.session['ids'].remove(i)
                        Measure.objects.get(id=i).delete()
                    except:
                        pass
            else:
                messages.warning(request, "You must login first")
            return redirect('/?next=/table/')
        request.session['ids'] = ids
        if btn == 'Redraw':
            return redirect('tables:WebtablesView')
        elif btn == 'CSV':
            return redirect('tables:csvweb')
        elif btn == 'Chart':
            return redirect('tables:ChartView')

def csvweb(request):
    headerwt,wt,headerst,st =  WriteTablesNew(request, gdate = False)
    datesuffix = datetime.datetime.now().strftime('_%Y_%m_%d')
    fn = 'CatsWeight' + datesuffix
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(fn)
    writer = csv.writer(response)
    writer.writerow(headerwt)
    writer.writerows(wt.values())
    writer.writerows([''])
    writer.writerow(headerst)
    writer.writerows(st)
    writer.writerows([''])
    return response

class SelectView(View):
    form_class = SelectCatsForm
    template_name = 'tables/testselect.html'
    def post(self,request, *args, **kwarg):
        form = SelectCatsForm(request.POST)
        if form.is_valid():
            catsset = form.cleaned_data.get("selectc")
            request.session['selectc'] = [c.id for c in catsset]
            request.session['fromdate'] = str(form.cleaned_data.get("fromdate"))
            request.session['todate'] = str(form.cleaned_data.get("todate"))
            request.session['selectby'] = 'cd'
            btn = request.POST['submitbtn']
            if btn == 'Table':
                return redirect('tables:WebtablesView')
            elif btn == 'CSV':
                return redirect('tables:csvweb')
            elif btn == 'Chart':
                return redirect('tables:ChartView')
        else:
            context = {'title': 'select',
                       'form': form
                       }
            return render(request, "tables/select.html", context)
    def get(self, request):
        form = SelectCatsForm()
        allcats = Cat.objects.all()
        context = {'title': 'select',
                   #'allcats': allcats,
                   'form': form
                   }
        return render(request, "tables/select.html", context)

class ChartView(TemplateView):
    template_name = "tables/chart.html"

    def get_context_data(self, **kwargs):
        headerwt, wt, headerst, st = WriteTablesNew(self.request, gdate = True)
        chartcol= headerwt[1:]
        # weights = [l[2:] for l in wt]
        # dates = [l[1] for l in wt]
        #data = [l[1:] for l in wt]

        context = {'title': 'Chart',
                   'charttitle':'Cats weight',
                   'chartcol': chartcol,
                   'data':wt
                   }
        return context
# class select(View):
#     def get(self, request):
#         allcats = Cat.objects.all()
#         context = {'title': 'select',
#                    'allcats': allcats
#                    }
#         return render(request, "tables/select.html", context)
#     def post(self, request):
#         requestdict = dict(request.POST)
#         fromdate = requestdict.get('fromdate',None)[0]
#         todate =requestdict.get('todate',None)[0]
#         currentdate = datetime.datetime.now().date()
#         todatedt = datetime.datetime.strptime(todate, "%Y-%m-%d").date()
#         fromdatedt = datetime.datetime.strptime(fromdate, "%Y-%m-%d").date()
#         if todatedt > currentdate:
#             messages.warning(request, "Nothing to do")
#             return HttpResponseRedirect('/')
#
#         request.session['selectc']= requestdict.get('selectc')
#         request.session['fromdate'] = requestdict.get('fromdate')
#         request.session['todate'] = requestdict.get('todate')
#
#         request.session['selection'] = True
#         return HttpResponseRedirect(reverse('tables:webtables'))