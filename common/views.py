import requests
from django.contrib.messages import success
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.defaultfilters import title
from src import settings
from .models import *
import random
from django.db.models import Q
from django.core.paginator import Paginator


def index(request):

    # qabul_qiluvchilar = ["ergashevazamera8@gmail.com"]
    #
    # send_mail(
    #     subject="Sizda Xabar bor!",
    #     message="Bu xabar sizga News yangiliklar saytidan yuborildi ",
    #     from_email=settings.EMAIL_HOST_USER,
    #     recipient_list=qabul_qiluvchilar,
    # )
    # print("\n\n", "Xabar yuborib bo'lindi", "\n\n")

    news = New.objects.all().order_by('-create')
    random_news = [news[random.randint(0, len(news)-1)], news[random.randint(0, len(news)-1)]]
    actual = New.objects.filter(Q(title__icontains="Mashina") | Q(short_desc__icontains="mashina"))[:3]
    ctx = {
        'news': news,
        'random_news': random_news,
        'actual': actual,
    }
    return render(request, 'index.html', ctx)



def category(request, slug):
    one_ctg = Category.objects.filter(slug=slug).first()
    if not one_ctg:
        return render(request, 'category.html', {"error": 404})


    news  = New.objects.filter(ctg=one_ctg).order_by('-id')
    if not news:
        return render(request, 'category.html', {"error": 404})


    paginator = Paginator(news, 2)
    page = request.GET.get("page", 1)
    result = paginator.get_page(page)

    ctx = {
        'one_ctg': one_ctg,
        'news': result,
        'len': len(news),
        'paginator': paginator,
        'page': int(page)
    }
    return render(request, 'category.html', ctx)



def search(request):
    key = request.GET.get('search', None)

    if not key:
        return render(request, "search.html", {'error': 404})

    news = New.objects.filter(Q(title__icontains=key) |
                              Q(short_desc__icontains=key) |
                              Q(description__icontains=key) |
                              Q(tags__icontains=key))

    paginator = Paginator(news, 3)
    page = request.GET.get('page', 1)
    result = paginator.get_page(page)


    ctx = {
        'news': result,
        'count' : paginator.count,
        'paginator': paginator,
        'page': page,
        'key': key,

    }
    return render(request, 'search.html', ctx)



def contact(request):

    if request.POST:
        try:
            cnt = Contact.objects.create(
                ism=request.POST['ism'],
                phone=request.POST['phone'],
                xabar=request.POST['xabar'],
            )

            request.session['success'] = 'Xabaringiz Qabul qilindi'

            message = f"Saytdan Yangi Kontakt\n" \
                      f"Ism :{cnt.ism}\n" \
                      f"Telefon Raqam :{cnt.phone}\n" \
                      f"Xabar :{cnt.xabar}\n"

            url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={6717501063}&text={message}"
            requests.get(url)



        except: ... #pass == ...


        return redirect('contact')


    success = request.session.get('success', None)
    try:
        del request.session['success']
    except: ...

    ctx = {
        "success" : success or ""

    }
    return render(request, 'contact.html', ctx)




def view(request, pk):
    one_new = New.objects.filter(id=pk).first()
    if not one_new:
        return render(request, 'view.html', {"error": 404})

    one_new.views += 1
    one_new.save()

    if request.method == "POST":
        user = request.POST.get("user")
        message = request.POST.get("message")
        parent_id = request.POST.get("parent_id")

        if user and message:
            parent = Comment.objects.filter(id=parent_id).first() if parent_id and parent_id != "0" else None
            Comment.objects.create(
                new=one_new,
                user=user,
                message=message,
                parent=parent,
                is_sub=bool(parent)
            )
        return redirect("view", pk=pk)

    news = New.objects.filter(ctg=one_new.ctg)

    comments = Comment.objects.filter(new=one_new, parent__isnull=True).order_by("-post")
    # count = Comment.objects.filter(new=one_new,parent__isnull=True).count()



    ctx = {
        "one_new": one_new,
        "comments": comments,
        "count": comments.count(),
    }

    if news.count() > 2:
        ctx["random_news"] = [
            news[random.randint(0, news.count() - 1)],
            news[random.randint(0, news.count() - 1)]
        ]

    return render(request, "view.html", ctx)




def add_to_subs(request, next):
    if request.method == "POST":
        try:
            Subscribe.objects.create(
                email=request.POST['email']
            )
        except:
            pass

    return redirect(next)
