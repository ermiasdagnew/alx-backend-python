from django.http import JsonResponse
from .models import ChatMessage

def send_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        ChatMessage.objects.create(user=request.user, message=message_text)
        return JsonResponse({'status': 'Message sent'})
    return JsonResponse({'error': 'Invalid request'}, status=400)