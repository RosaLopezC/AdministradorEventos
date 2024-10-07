from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Evento, Usuario, RegistroEvento
from .forms import EventoForm, UsuarioForm, RegistroEventoForm
from django.utils import timezone
from django.db.models import Count

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UsuarioForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home(request):
    eventos = Evento.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'home.html', {'eventos': eventos, 'usuarios': usuarios})

@login_required
def listar_eventos(request):
    eventos = Evento.objects.all()
    
    organizador_id = request.GET.get('organizador', '')
    if organizador_id:
        eventos = eventos.filter(organizador_id=organizador_id)
    
    return render(request, 'listar_eventos.html', {'eventos': eventos, 'total_eventos': eventos.count()})

@login_required
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    
    filtro_participacion = request.GET.get('filtro_participacion', '')
    if filtro_participacion == 'mas_eventos':
        usuarios = usuarios.annotate(num_eventos=Count('registroevento')).order_by('-num_eventos')
    
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios, 'total_usuarios': usuarios.count()})

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_eventos')
    else:
        form = EventoForm()
    return render(request, 'crear_evento.html', {'form': form})

@login_required
def ver_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    registros = RegistroEvento.objects.filter(evento=evento)
    
    if request.method == 'POST':
        registro_id = request.POST.get('registro_id')
        accion = request.POST.get('accion')
        
        if accion == 'eliminar':
            registro = get_object_or_404(RegistroEvento, id=registro_id)
            registro.delete()
        elif accion == 'editar':
            registro = get_object_or_404(RegistroEvento, id=registro_id)
            form = RegistroEventoForm(request.POST, instance=registro)
            if form.is_valid():
                form.save()
    
    return render(request, 'ver_evento.html', {'evento': evento, 'registros': registros})

@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('listar_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'editar_evento.html', {'form': form})

@login_required
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    evento.delete()
    return redirect('listar_eventos')

@login_required
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'registrar_usuario.html', {'form': form})

@login_required
def ver_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    registros = RegistroEvento.objects.filter(usuario=usuario)
    
    if request.method == 'POST':
        registro_id = request.POST.get('registro_id')
        accion = request.POST.get('accion')
        
        if accion == 'eliminar':
            registro = get_object_or_404(RegistroEvento, id=registro_id)
            registro.delete()
    
    return render(request, 'ver_usuario.html', {'usuario': usuario, 'registros': registros})

@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form})

@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('listar_usuarios')

@login_required
def registrar_usuario_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        form = RegistroEventoForm(request.POST)
        if form.is_valid():
            usuario_existente = form.cleaned_data['usuario_existente']
            nuevo_usuario = form.cleaned_data['nuevo_usuario']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            if nuevo_usuario:
                usuario = Usuario.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            else:
                usuario = usuario_existente

            RegistroEvento.objects.create(usuario=usuario, evento=evento)
            return redirect('ver_evento', evento_id=evento.id)
    else:
        form = RegistroEventoForm()
    return render(request, 'registrar_usuario_evento.html', {'form': form, 'evento': evento})

@login_required
def filtrar_eventos(request):
    filtro = request.GET.get('filtro', '')
    if filtro == 'hoy':
        eventos = Evento.objects.filter(fecha_inicio__date=timezone.now().date())
    elif filtro == 'proximos':
        eventos = Evento.objects.filter(fecha_inicio__gt=timezone.now())
    elif filtro == 'pasados':
        eventos = Evento.objects.filter(fecha_fin__lt=timezone.now())
    else:
        eventos = Evento.objects.all()
    
    mes = request.GET.get('mes', '')
    if mes:
        eventos = eventos.filter(fecha_inicio__year=timezone.now().year, fecha_inicio__month=mes)
    
    organizador_id = request.GET.get('organizador', '')
    if organizador_id:
        eventos = eventos.filter(organizador_id=organizador_id)
    
    meses_disponibles = Evento.objects.filter(fecha_inicio__year=timezone.now().year).dates('fecha_inicio', 'month')
    
    organizadores = Usuario.objects.filter(eventos_organizados__isnull=False).distinct()
    
    return render(request, 'listar_eventos.html', {
        'eventos': eventos,
        'total_eventos': eventos.count(),
        'meses_disponibles': meses_disponibles,
        'organizadores': organizadores,
    })