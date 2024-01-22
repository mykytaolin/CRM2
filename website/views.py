from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from .models import Lead, Agent, Category
from .forms import LeadModelForm, LeadForm, CustomBaseUserCreationForm, AssignAgentForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganiserAndLoginRequiredMixin


class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomBaseUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


def landing_page(request):
    return render(request, "landing.html")


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "website/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        # initially queryset of leads for all entire organisation
        if user.is_organiser:  # checking if the organiser
            queryset = Lead.objects.filter(organisation=user.userprofile,
                                           agent__isnull=False)  # checking the organisation by userprofile
            # which we get by referencing user.userprofile in user model
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation,
                                           agent__isnull=False)  # if we are an agents
            # we can access to agent by request.user and pole organisation which agent model consist

            # filtering the leads for the current agent
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True,
            )
            context.update({
                "unassigned_leads": queryset,
            })
        return context


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "object_list": leads
    }
    return render(request, "website/lead_list.html", context)


class LeadUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "website/lead_update.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("website:lead-update")

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/website")
    context = {
        'form': form,
        "lead": lead
    }
    return render(request, "website/lead_update.html", context)


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "website/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user

        # initially queryset of leads for all entire organisation
        if user.is_organiser:  # checking if the organiser
            queryset = Lead.objects.filter(organisation=user.userprofile)  # checking the organisation by userprofile
            # which we get by referencing user.userprofile in user model
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)  # if we are an agents
            # we can access to agent by request.user and pole organisation which agent model consist

            # filtering the leads for the current agent
            queryset = queryset.filter(agent__user=user)

        return queryset


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "website/lead_detail.html", context)


class LeadCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "website/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("website:lead-list")

    def form_valid(self, form):
        # To send email
        send_mail(
            subject="A lead has been created",
            message="go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

    def get_queryset(self):
        user = self.request.user

        # initially queryset of leads for all entire organisation
        if user.is_organiser:  # checking if the organiser
            queryset = Lead.objects.filter(organisation=user.userprofile)  # checking the organisation by userprofile
            # which we get by referencing user.userprofile in user model
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)  # if we are an agents
            # we can access to agent by request.user and pole organisation which agent model consist

            # filtering the leads for the current agent
            queryset = queryset.filter(agent__user=user)

        return queryset


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


class LeadDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "website/lead_delete.html"

    def get_success_url(self):
        return reverse("website:lead-list")

    def get_queryset(self):
        user = self.request.user

        # initially queryset of leads for all entire organisation
        if user.is_organiser:  # checking if the organiser
            queryset = Lead.objects.filter(organisation=user.userprofile)  # checking the organisation by userprofile
            # which we get by referencing user.userprofile in user model
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)  # if we are an agents
            # we can access to agent by request.user and pole organisation which agent model consist

            # filtering the leads for the current agent
            queryset = queryset.filter(agent__user=user)

        return queryset


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/website")


class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
    template_name = "website/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):  # clean and easy way to pass the args into the form
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def form_valid(self, form):
        agent = (form.cleaned_data["agent"])
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

    def get_success_url(self):
        return reverse("website:lead-list")


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "website/category_list.html"

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )

        return queryset


# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return redirect("/website")
#     context = {
#         'form': form,
#         "lead": lead
#     }
#     return render(request, "website/lead_update.html", context)


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
