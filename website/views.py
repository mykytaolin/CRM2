from django.shortcuts import render, redirect
from .models import Lead, Agent
from .forms import LeadModelForm, LeadForm


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, "website/lead_list.html", context)


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadForm
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            lead.first_name = first_name
            lead.last_name = last_name
            lead.age = age
            lead.save()
            return redirect("/website")
    context = {
        'form': form,
        "lead": lead
    }
    return render(request, "website/lead_update.html", context)


# def lead_create(request):
#   form = LeadForm
#   if request.method == "POST":
#       form = LeadForm(request.POST)
#       if form.is_valid():
#           first_name = form.cleaned_data['first_name']
#           last_name = form.cleaned_data['last_name']
#           age = form.cleaned_data['age']
#           agent = form.cleaned_data['agent']
#           Lead.objects.create(
#               first_name=first_name,
#               last_name=last_name,
#               age=age,
#               agent=agent,
#           )
#           return redirect("/website")
#   context = {
#       'form': LeadForm()
#   }
#   return render(request, "website/lead_create.html", context)


def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/website")
    context = {
        'form': form
    }
    return render(request, "website/lead_create.html", context)


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "website/lead_update.html", context)
