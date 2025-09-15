import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from .models import Quote
from django import forms

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
            'weight': forms.NumberInput(attrs={'min': 1, 'max': 100}),
        }

def show_quote(request, quote):
    return render(request, 'quotes/random_quote.html', {
        'quote': quote,
        'total_quotes': Quote.objects.count()
    })

def random_quote(request):
    """Главная страница со случайной цитатой"""
    # Получаем все цитаты с их весами
    quotes = list(Quote.objects.all())
    
    if quotes:
        # Создаем список с учетом весов (чем больше вес, тем больше шанс)
        selected_quote = random.choices(quotes, map(lambda x: x.weight, quotes))[0]
        
        # Увеличиваем счетчик просмотров
        selected_quote.views += 1
        selected_quote.save()
    else:
        selected_quote = None
    
    return show_quote(request, selected_quote)

def add_quote(request):
    """Добавление новой цитаты"""
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('random_quote')
    else:
        form = QuoteForm()
    
    return render(request, 'quotes/add_quote.html', {'form': form})

def like_quote(request, quote_id):
    """Лайк цитаты (AJAX)"""
    quote = get_object_or_404(Quote, id=quote_id)
    quote.likes += 1
    quote.save()
    return show_quote(request, quote)

def dislike_quote(request, quote_id):
    """Дизлайк цитаты (AJAX)"""
    quote = get_object_or_404(Quote, id=quote_id)
    quote.dislikes += 1
    quote.save()
    return show_quote(request, quote)

def popular_quotes(request):
    """10 самых популярных цитат по лайкам"""
    popular = Quote.objects.order_by('-likes')[:10]
    return render(request, 'quotes/popular_quotes.html', {
        'quotes': popular,
        'total_likes': Quote.objects.aggregate(Sum('likes'))['likes__sum'] or 0
    })