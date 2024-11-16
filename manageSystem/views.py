from django.shortcuts import render,redirect
from manageSystem import models
# Create your views here.

def academy_list(request):
    academy = models.Academy.objects.all()
    return render(request, 'academy_list.html', {'academy_list': academy})


def edit_academy(request):
    if request.method == 'POST':
        edit_id = request.GET.get('id')
        edit_obj = models.Academy.objects.get(id=edit_id)
        new_name = request.POST.get('edit_name')
        edit_obj.name = new_name
        edit_obj.save()
        return redirect('/academy_list/')

    edit_id = request.GET.get('id')
    edit_obj = models.Academy.objects.get(id=edit_id)
    return render(request, 'academy_edit.html', {'academy': edit_obj})


def add_academy(request):
    if request.method == 'POST':
        new_academy_name = request.POST.get('name')
        models.Academy.objects.create(name=new_academy_name)
        return redirect('/academy_list/')
    return render(request, 'academy_add.html')


def drop_academy(request):
    drop_id = request.GET.get('id')
    drop_obj = models.Academy.objects.get(id=drop_id)
    drop_obj.delete()
