from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber
import json

@csrf_exempt 
def unsubscribe(request):
    if request.method == 'POST':
        try:
            # reteriving json data from the reqbody
            data = json.loads(request.body.decode('utf-8'))
            # reteriving email from json data
            email = data.get('email')

            if email:
                try:
                    # reteriving object with email
                    subscriber = Subscriber.objects.get(email=email)
                    # marking isActive as false
                    subscriber.isActive = False
                    subscriber.save()
                    return JsonResponse({'message': 'Subscriber unsubscribed successfully.'})
                except Subscriber.DoesNotExist:
                    return JsonResponse({'error': 'Subscriber with this email does not exist.'}, status=404)
            else:
                return JsonResponse({'error': 'Email is required.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)