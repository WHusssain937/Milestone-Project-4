from django.shortcuts import render


def index(request):
    """ View will return index page """

    return render(request, 'home/index.html')


def contact_us(request):
    """ View will return index page """

    return render(request, 'contact/contact_us.html')
