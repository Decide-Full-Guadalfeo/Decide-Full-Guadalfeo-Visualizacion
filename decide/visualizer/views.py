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


def bot(request,msg,chat_id=BOT_CHAT_ID, token=BOT_TOKEN):
    bot=telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)

def botResponse(request):
    bot(request,"Hola")
    return render(request,"visualizer/botResponse.html")


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
