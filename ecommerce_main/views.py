from django.shortcuts import render

def home(request):
  context={
    'title':"Home | Asha Fashion"
  }
  return render(request,"index.html", context)