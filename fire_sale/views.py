from django.shortcuts import render

# Create your views here.
def index(request):
    current_user = request.user
    return render(request, 'fire_sale/frontpage.html', {
        'current_user': current_user
    })