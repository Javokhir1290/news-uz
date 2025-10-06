from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from common.models.auth import User

@login_required
def user_list(request):

    User = get_user_model()
    users = User.objects.filter(is_active=True).order_by('-id')
    paginator = Paginator(users, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/pages/user_list.html', {'page_obj': page_obj})




@login_required
def toggle_user_status(request, pk):
    user = get_object_or_404(User, id=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect("user_list")