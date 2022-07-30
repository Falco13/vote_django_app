from django.shortcuts import render, redirect
from contact.forms import ContactForm, ContactUserForm
from django.contrib import messages
from contact.models import Contact


def contact_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ContactUserForm(request.POST)
            if form.is_valid():
                Contact.objects.create(name_user=request.user,
                                       first_name=request.user.first_name,
                                       email=request.user.email,
                                       text=form.cleaned_data.get('text'))
            else:
                messages.error(request, form.errors)
                return redirect('poll_app:home')
        else:
            form = ContactForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                Contact.objects.create(**data)
            else:
                messages.error(request, form.errors)
                return redirect('poll_app:home')
        return render(request, 'contact/send_contact.html', {'form': form})
    else:
        form = ContactForm()
        return render(request, 'contact/contact.html', {'form': form})
