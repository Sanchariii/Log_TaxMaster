from django.http import HttpResponse
# from streamlit_django_integration import st_django_component

def hello_world(request):
    return HttpResponse("Hello, World!")
