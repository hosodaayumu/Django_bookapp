from django.shortcuts import render
from django.views import generic
from .models import Shelf, Review
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.core.paginator import Paginator

# レビューの表示

class ListBookView(generic.ListView):
    template_name = 'book/book_list.html'
    model = Shelf
    context_object_name = 'Shelf'
    queryset = Shelf.objects.all().order_by('-id')  # 登録順（降順）に並べ替え

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # レビュー平均でソートして上位3冊を取得
        ranking_list = (
            Shelf.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')[:3]
        )
        context['ranking_list'] = ranking_list
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # レビュー平均でソートして上位3冊を取得
        ranking_list = (
            Shelf.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')[:3]
        )
        context['ranking_list'] = ranking_list
        return context


class DetailBookView(generic.DetailView):
    template_name = 'book/book_detail.html'
    model = Shelf
    context_object_name = 'Shelf'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 本に関連するレビューを取得
        reviews = Review.objects.filter(book=self.object).order_by('-id')  # 最新のレビュー順
        paginator = Paginator(reviews, 3)  # 1ページに3件表示
        page_number = self.request.GET.get('page')
        context['reviews'] = paginator.get_page(page_number)
        return context 
        
        
class CreateBookView(LoginRequiredMixin,generic.CreateView):
    template_name = 'book/book_create.html'
    model = Shelf
    context_object_name = 'Shelf'
    fields = ('title', 'text', 'category','thumbnail')
    success_url = reverse_lazy('list-book')
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # ログイン中のユーザーを設定
        return super().form_valid(form)
    
class DeleteBookView(LoginRequiredMixin,generic.DeleteView):
    template_name = 'book/book_confirm_delete.html'
    model = Shelf
    context_object_name = 'Shelf'
    success_url = reverse_lazy('list-book')
    
class UpdateBookView(LoginRequiredMixin,generic.UpdateView):
    template_name = 'book/book_update.html'
    model = Shelf
    context_object_name = 'Shelf'
    fields = ('title', 'text', 'category','thumbnail')
    success_url = reverse_lazy('list-book')   
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied('編集権限がありません。')
        return super(UpdateBookView, self).dispatch(request, *args, **kwargs)

    
class CreateReviewView(LoginRequiredMixin,generic.CreateView):
    model = Review
    fields = ('book', 'text', 'rate')
    template_name = 'book/review_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Shelf.objects.get(pk=self.kwargs['book_id'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.title = form.instance.text
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk':self.object.book.id})  

    
    
    
    
    
    
# Create your views here.
