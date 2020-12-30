import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from pathlib import Path

from base import mods

import telegram

BOT_TOKEN="1458371772:AAHu7wPpi_gZNSIvwQfUeMndzffycghAVaw"
BOT_CHAT_ID="@guadalfeo_visualizacion"
BOT_URL="https://api.telegram.org/bot"+BOT_TOKEN+"/sendMessage?chat_id="+BOT_CHAT_ID+"&text=Hello+world"

def bot(voting_id, msg,chat_id=BOT_CHAT_ID, token=BOT_TOKEN):
    bot=telegram.Bot(token=token)
    telegram_keyboard = telegram.InlineKeyboardButton(text="Share Link in Telegram", switch_inline_query="Puedes ver los resultados de la votación en el siguiente enlace: http://localhost:8000/visualizer/botResults/"+voting_id)
    telegram_results_keyboard = telegram.InlineKeyboardButton(text="Share Results in Telegram", switch_inline_query=msg.replace("<b>","").replace("</b>",""))

    twitterMessage="https://twitter.com/intent/tweet?text=Puedes%20ver%20los%20resultados%20de%20la%20votación%20en%20el%20siguiente%20enlace:%20http://localhost:8000/visualizer/botResults/"+voting_id
    twitter_keyboard = telegram.InlineKeyboardButton(text="Share Link in Twitter", url=twitterMessage)

    whatsappMessage="https://api.whatsapp.com/send?text=Puedes%20ver%20los%20resultados%20de%20la%20votación%20en%20el%20siguiente%20enlace:%20http://localhost:8000/visualizer/botResults/"+voting_id
    whatsapp_keyboard = telegram.InlineKeyboardButton(text="Share Link in WhatsApp", url=whatsappMessage)

    whatsappResultsMessage="https://api.whatsapp.com/send?text="+msg.replace("<b>","").replace("</b>","")
    whatsapp_results_keyboard = telegram.InlineKeyboardButton(text="Share Results in WhatsApp", url=whatsappResultsMessage)

    custom_keyboard = [[telegram_keyboard,twitter_keyboard],[whatsapp_keyboard,telegram_results_keyboard],[whatsapp_results_keyboard]]
    reply_markup = telegram.InlineKeyboardMarkup(custom_keyboard)

    bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='HTML',reply_markup=reply_markup)

class BotResponse(TemplateView):

    template_name = 'visualizer/botResponse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
            r[0]={
                "id":"2",
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
            voting_id=str(r[0]['id'])
            message="<b>Votación: "+ r[0]['titulo']+"</b>  " + r[0]['fecha_inicio']+" - "+ r[0]['fecha_fin']+"\n"+"Descripción: "+r[0]['desc']+"\n"+"Personas censadas: "+r[0]['n_personas_censo']+"\n"
            preguntas=r[0]['preguntas']
            for pregunta in preguntas:
                message=message+"·"+pregunta['titulo']+":\n"
                candidatos=pregunta['opts']
                for candidato in candidatos:
                    votos=int(candidato["voto_F"])+int(candidato["voto_M"])
                    message=message+"-"+candidato['nombre']+":"+str(votos)+"\n"
            bot(voting_id,message)
        except:
            raise Http404
            
        return context

class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            script_location = Path(__file__).absolute().parent
            file_location = script_location / 'API_vGeneral.json'
            with file_location.open() as json_file:
                context['voting'] = json.load(json_file)
            r = mods.get('voting', params={'id': vid})
            # context['voting'] = json.dumps(r[0])
            context['botUrl']="http://localhost:8000/visualizer/botResults/"+str(r[0]['id'])
        except:
            raise Http404

        return context

class Prueba(TemplateView):
    try:
        template_name = 'visualizer/prueba.html'
    except:
        raise Http404