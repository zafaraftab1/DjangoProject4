import csv

from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import UpdateData


def customerData(request):
    if request.method == "POST":
        try:
            name = (request.POST.get("name") or "").strip()
            email = (request.POST.get("email") or "").strip()
            phone = (request.POST.get("phone") or "").strip()
            website = (request.POST.get("website") or "").strip()
            message = (request.POST.get("message") or "").strip()

            if not name or not email:
                messages.error(request, "Name and email are required.")
                return redirect("home")

            UpdateData.objects.create(
                name=name,
                email=email,
                phone=phone,
                website=website,
                message=message
            )

            messages.success(request, "Your message has been sent successfully!")
            return redirect("home")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, "updateAPI/index.html")


def success(request):
    return render(request, "updateAPI/save_data.html")


def submissions(request):
    query = (request.GET.get("q") or "").strip()
    sort = (request.GET.get("sort") or "id").strip()
    order = (request.GET.get("order") or "desc").strip().lower()
    per_page = request.GET.get("per_page", "10")

    allowed_sort_fields = {"id", "name", "email"}
    if sort not in allowed_sort_fields:
        sort = "id"

    if order not in {"asc", "desc"}:
        order = "desc"

    try:
        per_page_value = int(per_page)
    except ValueError:
        per_page_value = 10

    if per_page_value not in {10, 25, 50}:
        per_page_value = 10

    ordering = sort if order == "asc" else f"-{sort}"
    records = UpdateData.objects.all().order_by(ordering)
    total_count = records.count()

    if query:
        records = records.filter(
            Q(name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
            | Q(message__icontains=query)
        )
    filtered_count = records.count()

    paginator = Paginator(records, per_page_value)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "updateAPI/submissions.html",
        {
            "page_obj": page_obj,
            "query": query,
            "total_count": total_count,
            "filtered_count": filtered_count,
            "sort": sort,
            "order": order,
            "per_page": per_page_value,
        },
    )


def export_submissions_csv(request):
    records = UpdateData.objects.all().order_by("-id")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="submissions.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Name", "Email", "Phone", "Website", "Message"])
    for row in records:
        writer.writerow(
            [row.id, row.name, row.email, row.phone, row.website, row.message]
        )

    return response
