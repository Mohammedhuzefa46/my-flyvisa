from django.shortcuts import render
from .models import Email
from .forms import EmailForm

def submit_email(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()  # Save the email to the database
            return render(request, 'thank_you.html')  # Redirect to a thank you page
    else:
        form = EmailForm()
    return render(request, 'index.html', {'form': form})
