from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from .forms import licuefacForm, moliendaForm
from django.core.mail import send_mail
from .forms import IncidenteForm
from .forms import DatosForm
from .models import Datos, licuefac, molienda
from django.core.mail import EmailMessage
from .forms import CorreoForm



def programar_apertura(request):
    return render(request, 'programar_apertura.html')

def enviar_correo(request):
    if request.method == 'POST':
        form = CorreoForm(request.POST)
        if form.is_valid():
            asunto = form.cleaned_data['asunto']
            cuerpo = form.cleaned_data['cuerpo']

            # Lógica para enviar el correo
            email = EmailMessage(asunto, cuerpo, 'no_reply@bio4.com.ar', ['rodrigoimaz@outlook.com'])
            email.send()

            return render(request, 'exito.html')  # Página de éxito o redirección
    else:
        form = CorreoForm()

    return render(request, 'formulario_correo.html', {'form': form})

def last_five_rows(request):
    # Query the database to get the last 5 rows
    last_five_rows = Datos.objects.all().order_by('-fecha_creacion')[:5]

    # Render the template with the data
    return render(request, 'last_five_rows.html', {'last_five_rows': last_five_rows})

@login_required
def ingresar_datos(request):
    if request.method == 'POST':
        form = DatosForm(request.POST)
        if form.is_valid():
            datos = form.save(commit=False)
            datos.id_usuario = request.user
            datos.usuario = request.user.username
            datos.save()
            return redirect('exito')  # redirigir a la misma página después de guardar
    else:
        form = DatosForm()
    
    return render(request, 'ingresar_datos.html', {'form': form})


def incidente_form(request):
    if request.method == 'POST':
        form = IncidenteForm(request.POST)
        if form.is_valid():
            # Guardar el incidente en la base de datos
            incidente = form.save()

            # Enviar un correo electrónico
            send_mail(
                'Nuevo incidente reportado',
                f'Título: {incidente.titulo}\nDescripción: {incidente.descripcion}',
                'no_reply@bio4.com.ar',  # Reemplaza con tu dirección de correo electrónico
                ['rodrigoimaz@outlook.com'],  # Reemplaza con la dirección del destinatario
                fail_silently=False,
            )

            return redirect('home.html')  # Reemplaza con la URL de tu página de confirmación
    else:
        form = IncidenteForm()

    return render(request, 'incidente_form.html', {'form': form})


@login_required
def molienda(request):
    if request.method == 'POST':
        form = moliendaForm(request.POST)
        if form.is_valid():
            molineda = form.save(commit=False)
            molineda.id_usuario = request.user
            molineda.usuario = request.user.username
            molineda.save()
            return redirect('exito')  
    else:
        form = moliendaForm()
    return render(request, 'molienda.html', {'form': form})



def v_licuefac(request):
    success_message = None

def v_licuefac(request):
    success_message = None

    if request.method == 'POST':
        form = licuefacForm(request.POST)
        if form.is_valid():
            # Validar y guardar la instancia del formulario
            licuefac_instancia = form.save(commit=False)
            licuefac_instancia.id_usuario = request.user
            licuefac_instancia.usuario = request.user.username
            licuefac_instancia.save()

            # Establecer el mensaje de éxito
            success_message = "Datos guardados correctamente."

            # Redirigir a la misma vista con el mensaje de éxito
            return redirect('licuefac')  # Reemplaza 'nombre_de_la_vista_actual' con el nombre de tu vista

    else:
        form = licuefacForm()

    # Obtener los últimos 5 objetos guardados
    ult5 = licuefac.objects.all().order_by('-fecha_creacion')[:5]

    # Renderizar la plantilla con el formulario y los últimos 5 registros
    return render(request, 'licuefac.html', {'form': form, 'ult5': ult5, 'success_message': success_message})


def exito(request):
    return render(request, 'exito.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'carga_datos.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'carga_datos.htmll', {"form": TaskForm, "error": "Error creating task."})


def home(request):
    return render(request, 'home.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('tasks')

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def mlf(request):
    # Lógica para la vista mlf
    return render(request, 'mlf.html')

@login_required
def dest(request):
    # Lógica para la vista dest
    return render(request, 'dest.html')