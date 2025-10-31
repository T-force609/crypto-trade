from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from .serializers import SupportTicketSerializer
from .models import SupportTicket


@api_view(["POST"])
@permission_classes([AllowAny])
def contact_support(request):
    serializer = SupportTicketSerializer(data=request.data)
    if serializer.is_valid():
        ticket = serializer.save(
            user=request.user if request.user.is_authenticated else None
        )

        # Send email to admin
        send_mail(
            subject=f"New Support Message: {ticket.subject}",
            message=f"From: {ticket.email}\n\n{ticket.message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.SUPPORT_EMAIL_RECEIVER],
            fail_silently=False,
        )

        return Response({"message": "Your message has been sent successfully!"}, status=200)
    return Response(serializer.errors, status=400)
