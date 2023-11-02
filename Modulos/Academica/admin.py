from django.contrib import admin
from django.contrib.auth.models import User  # Importa el modelo de usuario de Django

from Modulos.Academica.models import *
# Register your models here.
admin.site.register(Carrera)
admin.site.register(Correlativas)
admin.site.register(Matricula)
admin.site.register(Estudiante)
@admin.register(Curso)
class CursoAdmin (admin.ModelAdmin):
    
    list_display =('nombre','creditos')
    #ordering =('nombre',);
    #search_fields=('nombre',);
    list_editable = ['nombre']
    list_display_links = None  # Set list_display_links to None to allow 'nombre' to be editable
    #list_filter=('creditos',);
    #list_per_page = 3;