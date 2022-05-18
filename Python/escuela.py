from email.policy import default
from sqlite3 import Timestamp
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Sequence,ForeignKey,DateTime,Time,CheckConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased,relationship
from sqlalchemy.sql import exists ##Importo la clase exists para preguntar si existe
from sqlalchemy import Table,Text
from datetime import datetime,date,time

##Declaro la Base Declarativa
Base=declarative_base()

##Creo el motor de base de datos
engine= create_engine('sqlite:///:memory:')

##Relación Profesores por Curso
profesoresPorCurso=Table('profesoresPorCurso',Base.metadata,
                Column('profesor_id',ForeignKey('profesores.id'),primary_key=True),
                Column('curso_id',ForeignKey('cursos.id'),primary_key=True)
                )

##Clase Alumnos
class Alumnos(Base):
    __tablename__='alumnos'

    id=Column(Integer,Sequence('alumnos_id_seq'),primary_key=True)
    nombre=Column(String)
    apellido=Column(String)
    fechaIngreso=Column(DateTime)
    fechaNacimiento=Column(DateTime)
    #Relación uno a uno con un curso
    curso_id=Column(Integer,ForeignKey('cursos.id'))

    curso=relationship('Cursos',back_populates='alumnos')

    def __repr__(self):
        return "{} {} {} {} {}".format(self.id,self.nombre,self.apellido,self.fechaIngreso,self.fechaNacimiento)

##Clase Profesores
class Profesores(Base):
    __tablename__='profesores'
    id=Column(Integer,Sequence('profesores_id_seq'),primary_key=True)
    nombre=Column(String)
    apellido=Column(String)
    fechaNacimiento=Column(DateTime)
    materia=Column(String)

    horario_id=Column(Integer,ForeignKey('horarios.id'))
    
    horario=relationship('Horarios',back_populates='profesores')

    cursosp=relationship('Cursos',secondary=profesoresPorCurso,
                        back_populates='profesoresc')

    
    def __repr__(self):
        return "{} {} {} {} {}".format(self.id,self.nombre,self.apellido,self.fechaNacimiento,self.materia)

##Clase Cursos
class Cursos(Base):
    __tablename__='cursos'
    id=Column(Integer,Sequence('cursos_id_seq'),primary_key=True)
    nombre=Column(String)
    
    alumnos=relationship('Alumnos',order_by='Alumnos.id',uselist=False,back_populates='curso')

    profesoresc=relationship("Profesores",secondary=profesoresPorCurso,back_populates='cursosp')

    def __repr__(self):
        return "{}".format(self.nombre)
    
class Horarios(Base):
    __tablename__='horarios'
    id=Column(Integer,Sequence('horarios_id_seq'),primary_key=True)
    ##Dia de la semana siendo 0 Domingo 6 Sabado
    dia=Column(Integer,CheckConstraint('dia > 0','dia < 6'))
    horaInicio=Column(Time)
    horaFin=Column(Time)

    profesores=relationship("Profesores",back_populates='horario',uselist=False)

    def __repr__(self) :
        return "{} {} {} {}".format(self.id,self.dia,self.horaInicio,self.horaFin)

##Creo la base metadata
Base.metadata.create_all(engine)

##Declaro la sesión
Session=sessionmaker(bind=engine)

#Instancio la sesion
session=Session()

curso1=Cursos(nombre='Curso1')
curso2=Cursos(nombre='Curso2')
curso3=Cursos(nombre='Curso3')

session.add_all([curso1,curso2,curso3])

alumno1=Alumnos(nombre='Ignacio',apellido='Acosta',fechaIngreso=date.fromisoformat('2021-03-03'),fechaNacimiento=date.fromisoformat('1989-08-18'),curso_id=1)
alumno2=Alumnos(nombre='Rodrigo',apellido='Perez',fechaIngreso=date.fromisoformat('2021-03-03'),fechaNacimiento=date.fromisoformat('1989-04-12'),curso_id=1)
alumno3=Alumnos(nombre='Melisa',apellido='Rodriguez',fechaIngreso=date.fromisoformat('2021-03-03'),fechaNacimiento=date.fromisoformat('1989-05-25'),curso_id=2)
alumno4=Alumnos(nombre='Leandro',apellido='Paredez',fechaIngreso=date.fromisoformat('2021-03-03'),fechaNacimiento=date.fromisoformat('1992-02-12'),curso_id=1)
alumno5=Alumnos(nombre='Liones',apellido='Lopez',fechaIngreso=date.fromisoformat('2021-03-03'),fechaNacimiento=date.fromisoformat('1989-12-25'),curso_id=2)

session.add_all([alumno1,alumno2,alumno3,alumno4,alumno5])

print(session.query(Alumnos).all())



horarios1=Horarios(dia=1,horaInicio=time.fromisoformat('08:00:00'),horaFin=time.fromisoformat('10:00:00'))
horarios2=Horarios(dia=2,horaInicio=time.fromisoformat('08:00:00'),horaFin=time.fromisoformat('10:00:00'))
horarios3=Horarios(dia=3,horaInicio=time.fromisoformat('08:00:00'),horaFin=time.fromisoformat('10:00:00'))
horarios4=Horarios(dia=4,horaInicio=time.fromisoformat('08:00:00'),horaFin=time.fromisoformat('10:00:00'))
horarios5=Horarios(dia=1,horaInicio=time.fromisoformat('14:15:00'),horaFin=time.fromisoformat('15:45:00'))
horarios6=Horarios(dia=2,horaInicio=time.fromisoformat('10:15:00'),horaFin=time.fromisoformat('12:15:00'))

session.add_all([horarios1,horarios2,horarios3,horarios4,horarios5,horarios6])

print(session.query(Horarios).all())

Profesor1=Profesores(nombre='Carlos',apellido='Augusto',fechaNacimiento=date.fromisoformat('1989-01-18'),materia='Matematica',horario_id=1)
Profesor2=Profesores(nombre='Maria',apellido='Martinez',fechaNacimiento=date.fromisoformat('1989-02-12'),materia='Geografia',horario_id=2)
Profesor3=Profesores(nombre='Martin',apellido='Fernandez',fechaNacimiento=date.fromisoformat('1989-03-25'),materia='Fisica',horario_id=3)
Profesor4=Profesores(nombre='Diego',apellido='Martinez',fechaNacimiento=date.fromisoformat('1989-02-12'),materia='Geografia',horario_id=4)
Profesor5=Profesores(nombre='Pedro',apellido='Troglio',fechaNacimiento=date.fromisoformat('1989-03-25'),materia='Fisica',horario_id=5)

session.add_all([Profesor1,Profesor2,Profesor3,Profesor4,Profesor5])

print(session.query(Profesores).all())


##Verifico que la tabla no tenga ningun resultado
print(session.query(profesoresPorCurso).all())

##Obtengo los cursos
cursos=session.query(Cursos).all()
profesores=session.query(Profesores).all()

##inserto los profesores a los cursos
cursos[0].profesoresc.append(profesores[0])
cursos[0].profesoresc.append(profesores[1])
cursos[1].profesoresc.append(profesores[2])
cursos[1].profesoresc.append(profesores[3])
cursos[0].profesoresc.append(profesores[4])


print(session.query(profesoresPorCurso).all())

##Ver Profesores para el Lunes
print('Profesores del día Lunes')
print(session.query(Profesores).outerjoin(Horarios,Profesores.horario_id==Horarios.id).filter(Horarios.dia==1).all())

##Ver Alumnos del Curso 2
print('Alumnos del Curso 2')
print(session.query(Alumnos).outerjoin(Cursos,Alumnos.curso_id==Cursos.id).filter(Cursos.nombre=='Curso2').all())

##Ver todos los Alumnos del curso 1
print('Alumnos del Curso 1')
AlumnosCurso1=session.query(Alumnos).outerjoin(Cursos,Alumnos.curso_id==Cursos.id).filter(Cursos.nombre=='Curso1').all()
for Alumno in AlumnosCurso1:
    print(Alumno)

##Ver Horario de los profesores del curso 1
print('Horarios de los profesores del Curso 1')
ProfesoresCurso=session.query(Profesores).outerjoin(Horarios,Profesores.horario_id==Horarios.id).outerjoin(profesoresPorCurso).outerjoin(Cursos).filter(Cursos.nombre=='Curso1').all()
for Profesor in ProfesoresCurso:
    print(Profesor)
    print("{} {} {}".format(Profesor.horario.dia,Profesor.horario.horaInicio,Profesor.horario.horaFin))
