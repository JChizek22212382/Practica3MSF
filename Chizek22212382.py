"""
Práctica 2: Sistema Cardiovascular

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Josué Chizek Espinoza
Número de control: 22212382
Correo institucional: 22212382@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Modulos (consola) y libreria para sistemas de control
#!pip install control
#!pip install slycot
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl
from scipy import signal
import pandas as pd

x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
n= round((tend - t0)/dt) + 1 
t = np.linspace(t0, tend, n)
u = np.zeros(n); u[round(1/dt):round(2/dt)] =1

def musculo (Cs,Cp,R,a):
    num = [Cs*R,1-a]
    den = [R*(Cp+Cs),1]
    sys=ctrl.tf(num,den)
    return sys
#Funcion de transferencia: Control
Cs,Cp,R,a = 10E-6,100E-6,100,0.25
syscontrol = musculo(Cs,Cp,R,a)
print(f'Funcion de transferencia del Control: {syscontrol}')

#Funcion de transferencia: Caso
Cs,Cp,R,a = 10E-6,100E-6,10E3,0.25
syscaso = musculo(Cs,Cp,R,a)
print(f'Funcion de transferencia del caso: {syscaso}')

_,Fs1 = ctrl.forced_response(syscontrol,t,u,x0)
_,Fs2 = ctrl.forced_response(syscaso,t,u,x0)

fgl= plt.figure()
plt.plot(t,u,'-',linewidth = 1, color =[0.569,0.392,0.235],label='F(s)')
plt.plot(t,Fs1,'-',linewidth = 1, color =[0.902,0.224,0.274],label='Fs1(t):Control')
plt.plot(t,Fs2,'-',linewidth = 1, color =[0.114,0.208,0.341],label='Fs2(t):Caso')

plt.grid(False) #Para poner una cuadricula en la grafica
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.6,1.4); plt.yticks(np.arange(-0.6,1.6,0.2))
plt.xlabel('t[s]')
plt.ylabel('Fs[V]')
plt.legend(bbox_to_anchor = (0.5,-0.2),loc = 'center', ncol = 3)
plt.show()
fgl.set_size_inches(w,h)
fgl.tight_layout()
fgl.savefig('Sistema Musculoesqueletico en lazo abierto python.png',dpi=600,bbox_inches='tight')
fgl.savefig('Sistema Musculoesqueletico en lazo abierto python.pdf')

def controlador (kP,kI,sys):
    Cr = 1E-6
    Re = 1/(kI*Cr)
    Rr = kP*Re
    numPI = [Rr*Cr,1]
    denPI = [Re*Cr,0]
    PI = ctrl.tf(numPI,denPI)
    X = ctrl.series(PI, sys)
    sysPI = ctrl.feedback(X,1,sign=-1)
    return sysPI
TratamientoPI = controlador (0.0216974155806455,41824.9323264174,syscaso)

_,Fs3 = ctrl.forced_response(TratamientoPI,t,Fs1,x0)

fgl= plt.figure()
plt.plot(t,u,'-',linewidth = 1, color =[0.569,0.392,0.235],label='F(s)')
plt.plot(t,Fs1,'-',linewidth = 1, color =[0.902,0.224,0.274],label='Fs1(t):Control')
plt.plot(t,Fs2,'-',linewidth = 1, color =[0.114,0.208,0.341],label='Fs2(t):Caso')
plt.plot(t,Fs3,':',linewidth = 1.5, color =[0.271,0.482,0.616],label='Fs3(t):Tratamiento')
plt.grid(False) #Para poner una cuadricula en la grafica
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.6,1.4); plt.yticks(np.arange(-0.6,1.6,0.2))
plt.xlabel('Pp(t)[V]')
plt.ylabel('t[s]')
plt.legend(bbox_to_anchor = (0.5,-0.2),loc = 'center', ncol = 3)
plt.show()
fgl.tight_layout()
fgl.savefig('Sistema Musculoesqueletico en lazo cerrado python.png',dpi=600,bbox_inches='tight')
fgl.savefig('Sistema Musculoesqueletico en lazo cerrado python.pdf')