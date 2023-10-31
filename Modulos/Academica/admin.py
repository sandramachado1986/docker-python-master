from django.contrib import admin
from django.contrib.auth.models import User  # Importa el modelo de usuario de Django

from Modulos.Academica.models import *


# Register your models here.
admin.site.register(Carrera)
admin.site.register(Correlativas)

admin.site.register(Curso)
admin.site.register(Estudiante)
admin.site.register(Matricula)



