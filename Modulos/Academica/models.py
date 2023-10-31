from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Carrera (models.Model):
    codigo = models.CharField (max_length=3,primary_key=True)
    nombre =models.CharField(max_length=50)
    duracion=models.PositiveSmallIntegerField(default=5)
    def __str__(self):
        txt = "{0}(Duración: {1} año(s))"
        return txt.format(self.nombre,self.duracion)

class Estudiante (models.Model):
    dni =models.CharField(max_length=8, primary_key=True)
    apellidoPaterno = models.CharField(max_length=35)
    apellidoMaterno =models.CharField(max_length=35)
    nombres = models.CharField(max_length=35)
    fechaNacimiento = models.DateField()
    sexos =[
        ('F','Femenino'),
        ('M','Masculino')
    ]
    sexo = models.CharField(max_length=1, choices=sexos,default='F')
    carrera= models.ForeignKey(Carrera, null= False, on_delete=models.CASCADE)
    vigencia = models.BooleanField(default=True)
    def nombreCompleto(self):
        txt="{0}{1},{2}"
        return  txt.format(self.apellidoPaterno,self.apellidoMaterno,self.nombres)
    def __str__(self):
        txt = "{0}/ Carrera:{1} /{2}"
        if self.vigencia:
            estadoEstudiante ="VIGENTE"
        else:
            estadoEstudiante ="DE BAJA"
        return txt.format(self.nombreCompleto(),self.carrera,estadoEstudiante)    
class Curso(models.Model):
    codigo = models.CharField(max_length=6, primary_key=True)
    nombre = models.CharField(max_length=30)
    creditos = models.PositiveSmallIntegerField()
    docente = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.codigo}) / Docente: {self.docente}"

class Correlativas(models.Model):
    id_correlativa = models.CharField(max_length=6, primary_key=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='correlativas')
    curso_correlativo = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='requisitos')

    def __str__(self):
        return f"{self.curso} requiere {self.curso_correlativo}"



class Matricula (models.Model):
    id = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey (Estudiante, null=False,blank=False,on_delete=models.CASCADE)
    curso = models.ForeignKey (Curso, null=False,blank=False,on_delete=models.CASCADE)
    fechaMatricula = models.DateTimeField(auto_now_add=True)


def save(self, *args, **kwargs):
        
        # Verifica si el usuario logueado pertenece al grupo 'estudiantes'
        if self.estudiante.groups.filter(name='estudiantes').exists():
            self.estudiante = self.usuario
        else:
            # Obtén la carrera del estudiante
            carrera_estudiante = self.estudiante.carrera

            # Verifica si el curso pertenece a la misma carrera
            if self.curso.carrera != carrera_estudiante:
                raise Exception(f"No puedes matricularte en {self.curso} ya que no pertenece a tu carrera ({carrera_estudiante})")

            # Continúa con la verificación de correlativas
            correlativas = Correlativas.objects.filter(curso=self.curso)

            for correlativa in correlativas:
                curso_correlativo = correlativa.curso_correlativo
                if not Matricula.objects.filter(estudiante=self.estudiante, curso=curso_correlativo).exists():
                    raise Exception(f"No puedes matricularte en {self.curso} ya que no has aprobado {curso_correlativo}")

        super(Matricula, self).save(*args, **kwargs)



def __str__(self):
        txt = "{0} matriculad{1} en el curso {2} /fecha: {3}"
        if self.estudiante.sexo == "F":
            letraSexo = "a"
        else:
            letraSexo = "o"
        fecMat = self.fechaMatricula.strftime("%A %d/%m/%Y %H:%M:%S")
        return txt.format(self.estudiante.nombreCompleto(), letraSexo, self.curso ,fecMat)


    
    