import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import CampRegistration, ServiceUnit


def registration_form(request):
    """View to display the camp registration form and handle submission"""
    # Get active service units for the form
    service_units = ServiceUnit.objects.filter(is_active=True).order_by("name")

    if request.method == "POST":
        try:
            # Extract form data
            work_unit_names = request.POST.getlist("work_unit")  # Get multiple values
            form_data = {
                "fullname": request.POST.get("fullname", "").strip(),
                "email": request.POST.get("email", "").strip(),
                "phone": request.POST.get("phone", "").strip(),
                "gender": request.POST.get("gender", ""),
                "can_pay": request.POST.get("can_pay", ""),
                "allergies": request.POST.get("allergies", ""),
                "health_challenges": request.POST.get("health_challenges", ""),
                "location": request.POST.get("location", "").strip(),
                "arrival_departure": request.POST.get("arrival_departure", "").strip(),
                "emergency_contact": request.POST.get("emergency_contact", "").strip(),
            }

            # Handle conditional fields
            if form_data["allergies"] == "yes":
                allergy_details = request.POST.get("allergy_details", "").strip()
                if not allergy_details:
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return JsonResponse(
                            {
                                "success": False,
                                "message": "Please specify your allergies.",
                            }
                        )
                    messages.error(request, "Please specify your allergies.")
                    context = {"service_units": service_units}
                    return render(request, "camp_form.html", context)
                form_data["allergy_details"] = allergy_details

            if form_data["health_challenges"] == "yes":
                health_details = request.POST.get(
                    "health_challenge_details", ""
                ).strip()
                if not health_details:
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return JsonResponse(
                            {
                                "success": False,
                                "message": "Please specify your health challenges.",
                            }
                        )
                    messages.error(request, "Please specify your health challenges.")
                    context = {"service_units": service_units}
                    return render(request, "camp_form.html", context)
                form_data["health_challenge_details"] = health_details

            # Basic validation
            required_fields = [
                "fullname",
                "email",
                "phone",
                "gender",
                "can_pay",
                "allergies",
                "health_challenges",
                "location",
                "arrival_departure",
                "emergency_contact",
            ]

            missing_fields = [
                field for field in required_fields if not form_data[field]
            ]

            # Check if at least one work unit is selected
            if not work_unit_names:
                missing_fields.append("work_unit")

            if missing_fields:
                error_message = (
                    f"Please fill in all required fields: {', '.join(missing_fields)}"
                )
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "message": error_message})
                messages.error(request, error_message)
                context = {"service_units": service_units}
                return render(request, "camp_form.html", context)

            # Validate phone number format (only numbers and + character)
            phone_pattern = r"^[\+]?[0-9]+$"
            if not re.match(phone_pattern, form_data["phone"]):
                error_message = "Phone number can only contain numbers (e.g., +2341234567890 or 08012345678)."
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "message": error_message})
                messages.error(request, error_message)
                context = {"service_units": service_units}
                return render(request, "camp_form.html", context)

            # Check for duplicate email
            if CampRegistration.objects.filter(email=form_data["email"]).exists():
                error_message = "This email address is already registered. Please use a different email."
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "message": error_message})
                messages.error(request, error_message)
                context = {"service_units": service_units}
                return render(request, "camp_form.html", context)

            # Check for duplicate phone number
            if CampRegistration.objects.filter(phone=form_data["phone"]).exists():
                error_message = "This phone number is already registered. Please use a different phone number."
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "message": error_message})
                messages.error(request, error_message)
                context = {"service_units": service_units}
                return render(request, "camp_form.html", context)

            # Create and save registration (without work_units first)
            registration = CampRegistration.objects.create(**form_data)

            # Add work units using the ManyToMany relationship
            work_units = ServiceUnit.objects.filter(name__in=work_unit_names)
            registration.work_units.set(work_units)

            # Check if this is an AJAX request
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "success": True,
                        "registration_id": registration.pk,
                        "message": "Registration successful!",
                    }
                )

            # Regular form submission - redirect to success page
            return redirect("registration_success", registration_id=registration.pk)

        except Exception as e:
            # Check if this is an AJAX request
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "success": False,
                        "message": f"An error occurred during registration: {str(e)}",
                    }
                )

            messages.error(request, f"An error occurred during registration: {str(e)}")
            context = {"service_units": service_units}
            return render(request, "camp_form.html", context)

    # GET request - display the form
    context = {"service_units": service_units}
    return render(request, "camp_form.html", context)


def registration_success(request, registration_id):
    """View to display successful registration with ID"""
    try:
        # Verify the registration exists
        registration = CampRegistration.objects.get(pk=registration_id)

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
