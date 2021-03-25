import os
import subprocess
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from .forms import *
from .models import *


def new(request):
    return render(request, 'new_job.html')


def newJob(confirmUrl, html, formClass, scriptArgument, request):
    if request.method == 'POST':
        form = formClass(request.POST, request.FILES)
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


def newEmap2Sec(request):
    return newJob('confirm_emap2sec', 'new_e2s.html', Emap2SecForm, 'emap2sec', request)


def confirmEmap2Sec(request, id):
    return confirmJob(Emap2SecJob, 'view_emap2sec', 'confirm_e2s.html', request, id)


def confirmMainmast(request, id):
    return confirmJob(MainmastJob, 'view_mainmast', 'confirm_mm.html', request, id)


def viewEmap2Sec(request, id):
    return viewJob('view_e2s.html', Emap2SecJob, request, id)


def newEmap2SecPlus(request):
    return newJob('confirm_emap2sec+', 'new_e2sp.html', Emap2SecPlusForm, 'emap2secplus', request)


def newMainmast(request):
    return newJob('confirm_mainmast', 'new_mm.html', MainmastForm, 'mainmast', request)


def viewMainmast(request, id):
    return viewJob('view_mm.html', MainmastJob, request, id)

def newMainmastSeg(request):
    return newJob('confirm_mainmastseg', 'new_mms.html', MainmastSegForm, 'mainmastseg', request)

