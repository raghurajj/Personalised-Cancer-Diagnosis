from django.shortcuts import render
import json


# Create your views here.

def home(request):
    gene = request.GET.get('gene')
    variation = request.GET.get('variation')
    research = request.GET.get('research')

    print(gene, variation, research)

    class_title=" "
    interpretation= " "

    return render(request, 'pcd/index.html', {"class":class_title,"interpretation":interpretation})
