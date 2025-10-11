from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from .models import CampRegistration


def registration_form(request):
    """View to display the camp registration form and handle submission"""
    if request.method == "POST":
        try:
            # Extract form data
            form_data = {
                "fullname": request.POST.get("fullname", "").strip(),
                "email": request.POST.get("email", "").strip(),
                "phone": request.POST.get("phone", "").strip(),
                "gender": request.POST.get("gender", ""),
                "can_pay": request.POST.get("can_pay", ""),
                "work_unit": request.POST.get("work_unit", "").strip(),
                "allergies": request.POST.get("allergies", ""),
                "health_challenges": request.POST.get("health_challenges", ""),
                "arrival_departure": request.POST.get("arrival_departure", "").strip(),
                "emergency_contact": request.POST.get("emergency_contact", "").strip(),
            }

            # Basic validation
            required_fields = [
                "fullname",
                "email",
                "phone",
                "gender",
                "can_pay",
                "work_unit",
                "allergies",
                "health_challenges",
                "arrival_departure",
                "emergency_contact",
            ]

            missing_fields = [
                field for field in required_fields if not form_data[field]
            ]

            if missing_fields:
                messages.error(
                    request,
                    f"Please fill in all required fields: {', '.join(missing_fields)}",
                )
                return render(request, "camp_form.html")

            # Create and save registration
            registration = CampRegistration.objects.create(**form_data)

            # Redirect to success page with registration ID
            return redirect(
                "registration_success", registration_id=registration.registration_id
            )

        except Exception as e:
            messages.error(request, f"An error occurred during registration: {str(e)}")
            return render(request, "camp_form.html")

    # GET request - display the form
    return render(request, "camp_form.html")


def registration_success(request, registration_id):
    """View to display successful registration with ID"""
    try:
        # Verify the registration exists
        registration = CampRegistration.objects.get(registration_id=registration_id)

        context = {
            "registration_id": registration_id,
            "fullname": registration.fullname,
        }

        return render(request, "success.html", context)

    except CampRegistration.DoesNotExist:
        messages.error(request, "Registration not found.")
        return redirect("registration_form")


def registration_list(request):
    """View to display all registrations (for admin purposes)"""
    registrations = CampRegistration.objects.all().order_by("-created_at")

    context = {
        "registrations": registrations,
        "total_count": registrations.count(),
    }

    return render(request, "registration_list.html", context)
