from django.http import HttpResponse

class StripWH_Handler:
    """ Handles Stripe Webhooks """

    def __init__(self, request):
        self.request = request
    
    def handle_event(self, event):
        """ 
        Handles a generic/unknown/unexpected webhook event 
        """
        return HttpResponse(
            content=f'Webhook recieved: {event["type"]}',
            status=200)