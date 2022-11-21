from django.utils import timezone


def year(request):
    dt = timezone.now().year
    return {
        'year': dt
    }
