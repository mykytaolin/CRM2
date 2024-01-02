from django.shortcuts import render
from .models import Lead


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads,
    }
    return render(request, "website/lead_list.html", context)
