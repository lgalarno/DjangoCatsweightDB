from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from .forms import CatForm
from .models import Cat

class CatsListView(ListView):
    template_name = 'CatsManagement/list.html'

    def get_queryset(self):
        return Cat.objects.all()

class CatDetailView(DetailView):
    model = Cat
    template_name = 'CatsManagement/detail.html'
    def get_object(self):
        object = get_object_or_404(Cat, id=self.kwargs['id'])
        return object

class CreateCatView(CreateView):
    template_name = 'CatsManagement/cat_form.html'
    form_class = CatForm
    context_object_name = 'Create'
    # model = Cat
    # fields = ['name',
    #           'birth',
    #           'description',
    #           'picture',
    #           'active']
    # def form_valid(self, form):
    #     # obj = form.save(commit=False)
    #     # obj.user = self.request.user
    #     # #instance.save()
    #     return super(CreateCatView, self).form_valid(form)

    # context_object_name = 'Create'
    # model = Cat
    # fields = ['name', 'birth', 'description', 'picture', 'active']

class CatUpdateView(UpdateView):
    context_object_name = 'Update'
    model = Cat
    fields = ['name','birth', 'description', 'picture', 'active']
    def get_object(self):
        object = get_object_or_404(Cat, id=self.kwargs['id'])
        return object
    def get_context_data(self, **kwargs):
        context = super(CatUpdateView, self).get_context_data(**kwargs)
        context['update_view'] = True
        return context

class CatDeleteView(DeleteView):
    model = Cat
    success_url = reverse_lazy('CatsManagement:CatsListView')
    def get_object(self):
        object = get_object_or_404(Cat, id=self.kwargs['id'])
        return object