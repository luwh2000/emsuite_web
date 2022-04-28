import os
import subprocess
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.base import RedirectView

from .forms import *
from .models import *


import mimetypes
from wsgiref.util import FileWrapper
from django.db.models import TextField
from django.db.models.functions import Cast

def get(request):
    return render(request, 'new_job.html')


def find(request):
    return render(request, 'find.html')


def newJob(confirmUrl, html, formClass, scriptArgument, request):
    if request.method == 'POST':
        form = formClass(request.POST, request.FILES)
        print(formClass)
        if form.is_valid():
            model = form.save(commit=False)
            model.map_filename = form.cleaned_data['map_file'].name
            model.save()

            BASE_DIR = Path(__file__).resolve().parent.parent
            subprocess.call(" ".join((
                os.path.join(BASE_DIR, "scripts/queue_job.sh"),
                scriptArgument,
                str(model.id)
            )), shell=True)

            return HttpResponseRedirect(reverse(confirmUrl, kwargs={'id': str(model.id)}))
        else:
            for field in form:
                print(field.name)
                print(field.errors)
            pass
    else:
        form = formClass()
    return render(request, html, {'form': form})


def confirmJob(jobClass, viewUrl, html, request, id):
    job = jobClass.objects.get(id=id)
    return render(request, html, {'job': job, 'viewUrl': reverse(viewUrl, kwargs={'id': id})})


def viewJob(html, jobClass, request, id):
    job = jobClass.objects.get(id=id)
    return render(request, html, {'job': job})


def findJob(request):
    type = request.GET.get('type')
    return render(request, 'find_job.html', {'type': type})


def find2view(request):
    id = request.GET.get('id')
    type = request.GET.get('type')
    jobClass = None
    html = ''
    if type == 'Emap2Sec':
        jobClass = Emap2SecJob
        html = 'view_e2s.html'
    elif type == 'Emap2Sec+':
        jobClass = Emap2SecPlusJob
        html = 'view_e2sp.html'
    elif type == 'MAINMAST':
        jobClass = MainmastJob
        html = 'view_mm.html'
    elif type == 'MAINMASTseg':
        jobClass = MainmastSegJob
        html = 'view_mms.html'
    return viewJob(html, jobClass, request, id)


def newEmap2Sec(request):
    print("Emap2Sec")
    return newJob('confirm_emap2sec', 'new_e2s.html', Emap2SecForm, 'emap2sec', request)


def confirmEmap2Sec(request, id):
    return confirmJob(Emap2SecJob, 'view_emap2sec', 'confirm_e2s.html', request, id)


def viewEmap2Sec(request, id):
    return viewJob('view_e2s.html', Emap2SecJob, request, id)


def confirmMainmast(request, id):
    return confirmJob(MainmastJob, 'view_mainmast', 'confirm_mm.html', request, id)


def newEmap2SecPlus(request):
    print("Emap2SecPlus")
    return newJob('confirm_emap2sec+', 'new_e2sp.html', Emap2SecPlusForm, 'emap2sec_plus', request)

def confirmEmap2SecPlus(request, id):
    return confirmJob(Emap2SecPlusJob, 'view_emap2sec+', 'confirm_e2sp.html', request, id)

def viewEmap2SecPlus(request, id):
    return viewJob('view_e2sp.html', Emap2SecPlusJob, request, id)

def newMainmast(request):
    return newJob('confirm_mainmast', 'new_mm.html', MainmastForm, 'mainmast', request)


def viewMainmast(request, id):
    return viewJob('view_mm.html', MainmastJob, request, id)


def newMainmastSeg(request):
    return newJob('confirm_mainmastseg', 'new_mms.html', MainmastSegForm, 'mainmastseg', request)
