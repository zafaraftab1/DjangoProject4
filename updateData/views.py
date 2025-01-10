from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UpdateData


def customerData(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            website = request.POST.get("website")
            message = request.POST.get("message")

            # Save data to the database
            UpdateData.objects.create(
                name=name,
                email=email,
                phone=phone,
                website=website,
                message=message
            )

            # Success message
            messages.success(request, "Your message has been sent successfully!")
            return redirect('/')  # Update the URL as needed
        except Exception as e:
            # Error message
            messages.error(request, f"An error occurred: {str(e)}")

    # Render the template for GET request
    return render(request, 'updateAPI/index.html')

from django.shortcuts import render

def success(request):
    return render(request, 'updateAPI/save_data.html')  # Adjust the template name/path if needed
