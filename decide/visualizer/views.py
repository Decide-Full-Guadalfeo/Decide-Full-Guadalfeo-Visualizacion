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

    # whatsappResultsMessage="https://api.whatsapp.com/send?text="+msg.replace("<b>","").replace("</b>","")
    # whatsapp_results_keyboard = telegram.InlineKeyboardButton(text="Share Results in WhatsApp", url=whatsappResultsMessage)

    custom_keyboard = [[telegram_keyboard,twitter_keyboard],[telegram_results_keyboard,whatsapp_keyboard]]
    reply_markup = telegram.InlineKeyboardMarkup(custom_keyboard)

    bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='HTML',reply_markup=reply_markup)

class BotResponse(TemplateView):

    template_name = 'visualizer/botResponse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        
        if self.request.user.is_staff:
            try:
                r = mods.get('voting', params={'id': vid})
                context['voting'] = json.dumps(r[0]["postproc"],indent=4)

                voting_id=str(r[0]["postproc"]['id'])
                message="<b>Votación: "+ r[0]["postproc"]['titulo']+"</b>  " + r[0]["postproc"]['fecha_inicio']+" - "+ r[0]["postproc"]['fecha_fin']+"\n"+"Descripción: "+r[0]["postproc"]['desc']+"\n"+"Personas censadas: "+str(r[0]["postproc"]['n_personas_censo'])+" / Votantes: "+str(r[0]["postproc"]['n_votantes'])+"\n"
                preguntas=r[0]["postproc"]['preguntas']
                for pregunta in preguntas:
                    message=message+"<b>·"+pregunta['titulo']+": "+ str(pregunta['numero_candidatos'])+" candidatos</b>\n"
                    candidatos=pregunta['opts']
                    for candidato in candidatos:
                        votos=int(candidato["voto_F"])+int(candidato["voto_M"])
                        message=message+"-"+candidato['nombre']+":"+str(votos)+"\n"
                bot(voting_id,message)
            except:
                raise Http404
        else:
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
            #context['voting_completo'] = json.dumps(r[0])
            #context["fecha_de_comienzo"]=json.dumps(r[0]["start_date"])
            #context["fecha_de_fin"]=json.dumps(r[0]["end_date"])
            context['botUrl']="http://localhost:8000/visualizer/botResults/"+str(r[0]['id'])
            context['whatsappUrl']="https://api.whatsapp.com/send?text=Puedes%20ver%20los%20resultados%20de%20la%20votación%20en%20el%20siguiente%20enlace:%20http://localhost:8000/visualizer/botResults/"+str(r[0]['id'])
            context['twitterUrl']="https://twitter.com/intent/tweet?text=Puedes%20ver%20los%20resultados%20de%20la%20votación%20en%20el%20siguiente%20enlace:%20http://localhost:8000/visualizer/botResults/"+str(r[0]['id'])
            context['facebookUrl']="http://www.facebook.com/sharer.php?u=http://localhost:8000/visualizer/botResults/"+str(r[0]['id'])
        except:
            raise Http404

        return context

class Prueba(TemplateView):
    try:
        template_name = 'visualizer/prueba.html'
    except:
        raise Http404

class ContactUs(TemplateView):
    try:
        template_name = 'visualizer/contactUs.html'
    except:
        raise Http404

class AboutUs(TemplateView):
    try:
        template_name = 'visualizer/aboutUs.html'
    except:
        raise Http404