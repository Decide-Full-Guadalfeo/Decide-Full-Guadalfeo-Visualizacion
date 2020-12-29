import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods

import telegram
import requests
from django.shortcuts import render


BOT_TOKEN="1458371772:AAHu7wPpi_gZNSIvwQfUeMndzffycghAVaw"
BOT_CHAT_ID="-406008177"
BOT_URL="https://api.telegram.org/bot"+BOT_TOKEN+"/sendMessage?chat_id="+BOT_CHAT_ID+"&text=Hello+world"


def bot(msg,chat_id=BOT_CHAT_ID, token=BOT_TOKEN):
    bot=telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='HTML')

class BotResponse(TemplateView):

    template_name = 'visualizer/botResponse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
            r[0]={
                "titulo":"Votación primaria dentro de una candidatura",
                "desc":"Votación primaria dentro de una candidatura",
                "fecha_inicio":"23/12/2020",
                "fecha_fin":"31/12/2020",
                "tipo":"VP",
                "n_personas_censo":"465",
                "preguntas":[
                    {
                        "titulo": "Delegado de centro",
                        "opts":[
                                {
                                "nombre": "Primer candidato (nombre de la persona)",
                                "numero": "3 (numero de opcion)",
                                "voto_F": "24",
                                "voto_M":"23",
                                "media_Edad": "22.12 (media de edad de los votantes de la opción)",
                                "voto_curso":{"primero": "2","segundo":"3" ,"tercero":"3", "cuarto":"5", "master":"4"}
                                },
                            ]
                        },
                    {
                        "titulo":"Primarias de primer curso",
                        "opts":[
                            {
                                "nombre": "Primer candidato (nombre de la persona)",
                                "numero": "3 (numero de opcion)",
                                "voto_F": "24",
                                "voto_M":"23",
                                "media_Edad": "22.12 (media de edad de los votantes de la opción)",
                                },
                        ]
                    },
                    {
                        "titulo":"Primarias de segundo curso",
                        "opts":[
                            {
                                "nombre": "Primer candidato (nombre de la persona)",
                                "numero": "3 (numero de opcion)",
                                "voto_F": "24",
                                "voto_M":"23",
                                "media_Edad": "22.12 (media de edad de los votantes de la opción)",
                                },
                        ]
                    }
                ]
            }
            message="<b>Votación: "+ r[0]['titulo']+"</b>  " + r[0]['fecha_inicio']+" - "+ r[0]['fecha_fin']+"\n"+"Descripción: "+r[0]['desc']+"\n"+"Personas censadas: "+r[0]['n_personas_censo']+"\n"
            preguntas=r[0]['preguntas']
            for pregunta in preguntas:
                message=message+"·"+pregunta['titulo']+":\n"
                candidatos=pregunta['opts']
                for candidato in candidatos:
                    votos=int(candidato["voto_F"])+int(candidato["voto_M"])
                    message=message+"-"+candidato['nombre']+":"+str(votos)+"\n"
            bot(message)
        except:
            raise Http404

        return context

class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        return context

class Prueba(TemplateView):
    try:
        template_name = 'visualizer/prueba.html'
    except:
        raise Http404