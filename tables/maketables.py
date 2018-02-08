import csv
import datetime
import io

from CatsManagement.models import Cat
from weight.models import Measure, Participant
from .simplestats import mean, pstdev

def main():
    WriteTables('All', [12,13])

def WriteTables(request, gdate = False):
    wt = []
    session = request.session
    datefrom = Measure.objects.order_by('-date').last().date
    dateto = datetime.datetime.now().date()
    if request.session['selection']:
        catsset = session.get('selectc', None)
        # datefrom = session.get('fromdate', None)
        # print(datefrom)
        # if datefrom:
        #     print(datefrom)
        #     datefrom = datetime.datetime.strptime(datefrom, "%Y-%m-%d").date()
        if session.get('todate') != "None":
            dateto = session.get('todate')
        if session.get('fromdate') != "None":
            datefrom = session.get('fromdate')
        request.session['selection'] = False
    else:
        allcats = Cat.objects.all()
        catsset = [c.id for c in allcats]

    qmeas = Measure.objects.filter(participant__cat__in=catsset,
                                   date__lte=dateto,
                                   date__gte=datefrom
                                   ).distinct()
    allcats = Cat.objects.filter(id__in=catsset)
    catsmeasured = [c for c in allcats]
    # distinct measure with selected cats (catsset)
    # Measure.objects.filter(participant__cat__in=[12,13,14]).distinct()
    # if 'All' in measureset:
    #     qmeas = Measure.objects.all()
    # else:
    #     qmeas = Measure.objects.filter(id__in=measureset)


    for m in qmeas:
        weights = m.get_weigths()
        mdate = m.date.strftime("%Y-%m-%d")
        if gdate:
            gdatelist = mdate.split('-')
            "Date(Year, Month, Day)"
            gdatelist[1] = str(int(gdatelist[1]) - 1)
            mdate = "new Date({0}, {1}, {2})".format(m.date.year, m.date.month-1,m.date.day)#'new Date({0},{1},{2})'.format(*gdatelist)
        wt.append([mdate] + _wranking(weights, catsmeasured))
    st = _summary_table(wt,len(catsmeasured), 1) #1 for date
    headerwt = ['Date'] + catsmeasured
    headerst = [' '] + catsmeasured
    return headerwt, wt, headerst, st

def WriteTablesNew(request, gdate = False):

    wt = {}
    #request.session['selectby'] = None
    session = request.session
    datefrom = Measure.objects.order_by('-date').last().date
    dateto = datetime.datetime.now().date()
    selectby = session.get('selectby', None)
    # selectby:
    # id: get Measure by id
    # cd: get Measure by Catset and Date rage

    if selectby == 'ids':
        ids = session.get('ids', None)
        request.session['selectby'] = None
        qmeas = Measure.objects.filter(id__in=ids)
        catsset_temp = []
        for m in qmeas:
            catsset_temp = catsset_temp + m.get_all_cats()
            catsset = list(set(catsset_temp))
    else:
        if selectby =='cd':
            #catsset = session.get('selectc', None)
            if session.get('todate') != "None":
                dateto = session.get('todate')
            if session.get('fromdate') != "None":
                datefrom = session.get('fromdate')
            request.session['selectby'] = None
        else:
            allcats = Cat.objects.all()
            request.session['selectc'] = [c.id for c in allcats]
            #catsset = [c.id for c in allcats]

        catsset = session.get('selectc', None)
        qmeas = Measure.objects.filter(participant__cat__in=catsset,
                                       date__lte=dateto,
                                       date__gte=datefrom,
                                       ).distinct()
        request.session['ids'] = [str(q.id) for q in qmeas]
    allcats = Cat.objects.filter(id__in=catsset)
    catsmeasured = [c for c in allcats]
    for m in qmeas:
        weights = m.get_weigths()
        mdate = m.date.strftime("%Y-%m-%d")
        if gdate:
            gdatelist = mdate.split('-')
            "Date(Year, Month, Day)"
            gdatelist[1] = str(int(gdatelist[1]) - 1)
            mdate = "new Date({0}, {1}, {2})".format(m.date.year, m.date.month-1,m.date.day)

        wt[m.id] = [mdate] + _wranking(weights, catsmeasured)
            #wt.append([mdate] + _wranking(weights, catsmeasured))

    st = _summary_table_new(wt,len(catsmeasured), 1) #1 for date
    headerwt = ['Date'] + catsmeasured
    headerst = [' '] + catsmeasured
    return headerwt, wt, headerst, st

def _wranking(weigths, cats):
    """
    Format the weigths from the weigths dict in the proper order of
    all cats in all measurments (cats
    Returns a list of the weigths
    [10, 14, None, 9]
    """
    result = [None for i in range(len(cats))]
    for w in weigths:
        if w in cats:
            result[cats.index(w)]=weigths[w]
    return result

def _summary_table_new(dict,m, n):
    '''
        ll is a list of lists from the build_table function
        m is the number of individuals
        n is the number of columns to skip
        This function will create a summary table with the average weigths
        for each cat in all measurements.
        The output will be a list of list like:
            [[''   	PP	HH18	HH22],
             [Mean	42	42	41],
             [STDev	6.32	6.4	5.83]]
    '''
    temp = [[] for i in range(m)]
    for key, value in dict.items():
        for i, v in enumerate(value[n:]):
            temp[i].append(v)

    result = [['Mean']+[0 for i in range(m)], ['STDev']+[0 for i in range(m)]]
    for i in range(0, m):
        cleaned_temp = list(filter(None, temp[i]))
        result[0][i + 1] = "{0:0.2f}".format(mean(cleaned_temp))
        result[1][i + 1] = "{0:0.2f}".format(pstdev(cleaned_temp))
    return result

def _summary_table(ll,m, n):
    '''
        ll is a list of lists from the build_table function
        m is the number of individuals
        n is the number of columns to skip
        This function will create a summary table with the average weigths
        for each cat in all measurements.
        The output will be a list of list like:
            [[''   	PP	HH18	HH22],
             [Mean	42	42	41],
             [STDev	6.32	6.4	5.83]]
    '''
    temp = [list(_transpose(ll, n+i)) for i in range(m)]
    result = [['Mean']+[0 for i in range(m)], ['STDev']+[0 for i in range(m)]]
    for i in range(0, m):
        cleaned_temp = list(filter(None, temp[i]))
        result[0][i + 1] = "{0:0.2f}".format(mean(cleaned_temp))
        result[1][i + 1] = "{0:0.2f}".format(pstdev(cleaned_temp))
    return result

def _transpose(ll,p):
    '''
        This function will transpose the elements of a peculiar position
        in a list of lists
        ll is a list of lists
        p is the position to be transpose
        [[1,2,3],[1,2,3]] -> [1,1] or [2,2] or [3,3] according to p
    '''
    for l in ll:
        yield l[p]

if __name__ == "__main__":
    main()