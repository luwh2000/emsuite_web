import os
import subprocess
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from .forms import Emap2SecForm
from .models import Emap2SecJob


def new(request):
    return render(request, 'new_job.html')


def newJob(confirmUrl, html, request):
    if request.method == 'POST':
        form = Emap2SecForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save(commit=False)
            model.mrc_filename = form.cleaned_data['mrc_file'].name
            model.save()

            BASE_DIR = Path(__file__).resolve().parent.parent
            subprocess.call(" ".join((
                os.path.join(BASE_DIR, "scripts/queue_job.sh"),
                "emap2sec",
                str(model.id)
            )), shell=True)

            return HttpResponseRedirect(reverse(confirmUrl, kwargs={'id': str(model.id)}))
        else:
            pass
    else:
        form = Emap2SecForm()
    return render(request, html, {'form': form})


def confirmJob(viewUrl, html, request, id):
    job = Emap2SecJob.objects.get(id=id)
    return render(request, html, {'job': job, 'viewUrl': reverse(viewUrl, kwargs={'id': id})})


def viewJob(html, request, id):
    job = Emap2SecJob.objects.get(id=id)
    return render(request, html, {'job': job})


def newEmap2Sec(request):
    return newJob('confirm_emap2sec', 'new_e2s.html', request)


def confirmEmap2Sec(request, id):
    return confirmJob('view_emap2sec', 'confirm_e2s.html', request, id)


def viewEmap2Sec(request, id):
    job = Emap2SecJob.objects.get(id=id)
    return render(request, 'view_e2s.html', {'job': job})


def newEmap2SecPlus(request):
    return newJob('confirm_emap2sec+', 'new_e2sp.html', request)


def newMainmast(request):
    return newJob('confirm_mainmast', 'new_mm.html', request)


def newMainmastSeg(request):
    return newJob('confirm_mainmastseg', 'new_mms.html', request)
