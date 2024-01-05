from django.shortcuts import render
from .models import Lead
from django.http import HttpResponse


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, "lead_list.html", context)


def lead_detail(request, pk):
    print(pk)
    lead = Lead.objects.get(id=pk)
    print(lead)
    return HttpResponse("here is a detail view")
