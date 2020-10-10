from django.shortcuts import render


def profile(request):
    """ Display's the user's profile """
    template = 'profile/profile.html'
    context = {}

    return render(request, template, context)
