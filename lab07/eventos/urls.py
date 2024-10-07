from django.urls import path
from eventos import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home, name='home'),
    path('listar_eventos/', views.listar_eventos, name='listar_eventos'),
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('crear_evento/', views.crear_evento, name='crear_evento'),
    path('ver_evento/<int:evento_id>/', views.ver_evento, name='ver_evento'),
    path('editar_evento/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('eliminar_evento/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('ver_usuario/<int:usuario_id>/', views.ver_usuario, name='ver_usuario'),
    path('editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('registrar_usuario_evento/<int:evento_id>/', views.registrar_usuario_evento, name='registrar_usuario_evento'),
    path('filtrar_eventos/', views.filtrar_eventos, name='filtrar_eventos'),
]