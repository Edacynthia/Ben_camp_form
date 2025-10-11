import csv
import io
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side
from .models import CampRegistration, ServiceUnit


@admin.register(ServiceUnit)
class ServiceUnitAdmin(admin.ModelAdmin):
    """Admin interface for Service Unit model"""

    list_display = ["name", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    list_editable = ["is_active"]
    readonly_fields = ["created_at"]

    fieldsets = (
        ("Unit Information", {"fields": ("name", "description", "is_active")}),
        ("System Information", {"fields": ("created_at",), "classes": ("collapse",)}),
    )


@admin.register(CampRegistration)
class CampRegistrationAdmin(admin.ModelAdmin):
    """Admin interface for Camp Registration model"""

    def get_work_units_display(self, obj):
        """Display work units as a comma-separated string"""
        return ", ".join([unit.name for unit in obj.work_units.all()])

    get_work_units_display.short_description = "Work Units"

    def export_to_csv(self, request, queryset):
        """Export selected registrations to CSV"""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="camp_registrations_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                "Registration ID",
                "Full Name",
                "Email",
                "Phone",
                "Gender",
                "Can Pay",
                "Work Units",
                "Allergies",
                "Allergy Details",
                "Health Challenges",
                "Health Details",
                "Location",
                "Arrival/Departure",
                "Emergency Contact",
                "Registration Date",
            ]
        )

        for obj in queryset:
            writer.writerow(
                [
                    obj.pk,
                    obj.fullname,
                    obj.email,
                    obj.phone,
                    obj.gender,
                    "Yes" if obj.can_pay == "yes" else "No",
                    ", ".join([unit.name for unit in obj.work_units.all()]),
                    "Yes" if obj.allergies == "yes" else "No",
                    getattr(obj, "allergy_details", "") or "",
                    "Yes" if obj.health_challenges == "yes" else "No",
                    getattr(obj, "health_challenge_details", "") or "",
                    obj.location,
                    obj.arrival_departure,
                    obj.emergency_contact,
                    obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                ]
            )

        return response

    export_to_csv.short_description = "Export selected registrations to CSV"

    def export_to_excel(self, request, queryset):
        """Export selected registrations to Excel"""
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            f'attachment; filename="camp_registrations_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
        )

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Camp Registrations"

        # Headers
        headers = [
            "Registration ID",
            "Full Name",
            "Email",
            "Phone",
            "Gender",
            "Can Pay",
            "Work Units",
            "Allergies",
            "Allergy Details",
            "Health Challenges",
            "Health Details",
            "Location",
            "Arrival/Departure",
            "Emergency Contact",
            "Registration Date",
        ]

        # Style headers
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(
            start_color="FF4757", end_color="FF4757", fill_type="solid"
        )

        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill

        # Data rows
        for row, obj in enumerate(queryset, 2):
            ws.cell(row=row, column=1, value=obj.pk)
            ws.cell(row=row, column=2, value=obj.fullname)
            ws.cell(row=row, column=3, value=obj.email)
            ws.cell(row=row, column=4, value=obj.phone)
            ws.cell(row=row, column=5, value=obj.gender)
            ws.cell(row=row, column=6, value="Yes" if obj.can_pay == "yes" else "No")
            ws.cell(
                row=row,
                column=7,
                value=", ".join([unit.name for unit in obj.work_units.all()]),
            )
            ws.cell(row=row, column=8, value="Yes" if obj.allergies == "yes" else "No")
            ws.cell(row=row, column=9, value=getattr(obj, "allergy_details", "") or "")
            ws.cell(
                row=row,
                column=10,
                value="Yes" if obj.health_challenges == "yes" else "No",
            )
            ws.cell(
                row=row,
                column=11,
                value=getattr(obj, "health_challenge_details", "") or "",
            )
            ws.cell(row=row, column=12, value=obj.location)
            ws.cell(row=row, column=13, value=obj.arrival_departure)
            ws.cell(row=row, column=14, value=obj.emergency_contact)
            ws.cell(
                row=row, column=15, value=obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
            )

        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width

        wb.save(response)
        return response

    export_to_excel.short_description = "Export selected registrations to Excel"

    def export_to_pdf(self, request, queryset):
        """Export selected registrations to PDF"""
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="camp_registrations_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
        )

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=16,
            spaceAfter=30,
            alignment=1,  # Center alignment
        )

        # Title
        title = Paragraph("Ben Camp Meeting Registrations", title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))

        # Table data
        data = [
            ["ID", "Full Name", "Email", "Phone", "Gender", "Can Pay", "Work Units"]
        ]

        for obj in queryset:
            data.append(
                [
                    str(obj.pk),
                    obj.fullname,
                    obj.email,
                    obj.phone,
                    obj.gender.title(),
                    "Yes" if obj.can_pay == "yes" else "No",
                    ", ".join([unit.name for unit in obj.work_units.all()]) or "None",
                ]
            )

        # Create table
        table = Table(data)
        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.Color(1, 0.28, 0.34),
                    ),  # #FF4757
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        elements.append(table)
        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    export_to_pdf.short_description = "Export selected registrations to PDF"

    actions = ["export_to_csv", "export_to_excel", "export_to_pdf"]

    list_display = [
        "pk",
        "fullname",
        "email",
        "phone",
        "gender",
        "can_pay",
        "get_work_units_display",
        "created_at",
    ]

    list_filter = [
        "gender",
        "can_pay",
        "allergies",
        "health_challenges",
        "created_at",
        "work_units",
    ]

    search_fields = ["fullname", "email", "phone"]

    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Basic Information", {"fields": ("fullname", "email", "phone", "gender")}),
        ("Camp Information", {"fields": ("can_pay", "work_units")}),
        ("Health Information", {"fields": ("allergies", "health_challenges")}),
        ("Travel & Emergency", {"fields": ("arrival_departure", "emergency_contact")}),
        (
            "System Information",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    ordering = ["-created_at"]
