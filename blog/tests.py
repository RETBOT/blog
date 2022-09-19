import email
import imp
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Publicaciones

# Create your tests here.


class PruebasBlog(TestCase): 
    def setUp(self): 
        self.usuario = get_user_model().objects.create_user(
            username = 'usuarioprueba',
            email = 'prueba@email.com',
            password = 'secreto'
        )

        self.pub = Publicaciones.objects.create(
            titulo = 'Un buen titulo',
            cuerpo = 'Muy buen contenido',
            autor = self.usuario
        )

    def test_representacion_cademas(self):
        pub = Publicaciones(titulo='Un titulo simple')
        self.assertEqual(str(pub), pub.titulo)

    def test_contenido_publicaciones(self):
        self.assertEqual(f'{self.pub.titulo}','Un buen titulo')
        self.assertEqual(f'{self.pub.autor}','usuarioprueba')
        self.assertEqual(f'{self.pub.cuerpo}','Muy buen contenido')
    

    def test_vista_lista_publicaciones(self):
        respuesta = self.client.get(reverse('inicio'))
        self.assertEqual(respuesta.status_code,200),
        self.assertContains(respuesta,'Muy buen contenido'),
        self.assertTemplateUsed(respuesta,'inicio.html')

    def test_vista_detalle_publicacion(self):
        respuesta = self.client.get('/pub/1/')
        sin_respuesta = self.client.get('/pub/1000000/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(sin_respuesta.status_code, 404)
        self.assertContains(respuesta, 'Un buen titulo')
        self.assertTemplateUsed(respuesta, 'detalle_publicaciones.html')