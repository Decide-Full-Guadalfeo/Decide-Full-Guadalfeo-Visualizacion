from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def post(self, request):

        voting = request.data

        # Adding voting statistics
        abstencion = {}
        abstencion["_0"] = round((100 - (voting["n_votantes"] / voting["n_personas_censo"] * 100)), 2)
        for i in [1,2,3,4,5]:
            abstencion["_"+str(i)] = round((100 - (voting["preguntas"][i]["n_votantes"] / voting["preguntas"][i]["n_personas_censo"] * 100)), 2)

        abstencion_m = {}
        abstencion_m["_0"] = round((100 - (voting["n_votantes_m"] / voting["n_hombres_censo"] * 100)), 2)
        for i in [1,2,3,4,5]:
            abstencion_m["_"+str(i)] = round((100 - (voting["preguntas"][i]["n_votantes_m"] / voting["preguntas"][i]["n_hombres_censo"] * 100)), 2)

        abstencion_f = {}
        abstencion_f["_0"] = round((100 - (voting["n_votantes_f"] / voting["n_mujeres_censo"] * 100)), 2)
        for i in [1,2,3,4,5]:
            abstencion_f["_"+str(i)] = round((100 - (voting["preguntas"][i]["n_votantes_f"] / voting["preguntas"][i]["n_mujeres_censo"] * 100)), 2)

        media_edad = {}
        media_edad["_0"] = voting["media_edad_votantes"]
        for i in [1,2,3,4,5]:
            media_edad["_"+str(i)] = voting["preguntas"][i]["media_edad_votantes"]

        voting["estadisticas"] = {"abstencion": abstencion, "abstencion_m": abstencion_m, "abstencion_f": abstencion_f, "media_edad": media_edad}
        
        
        for opt in voting["preguntas"][0]["opts"]:
            votos_censo = round(((opt["votes"]) / voting["n_personas_censo"] * 100), 2)
            votos_m = round((opt["voto_M"]/(opt["votes"]) * 100), 2)
            votos_f = round((opt["voto_F"]/(opt["votes"]) * 100), 2)
            votos_primero = round((opt["voto_curso"]["primero"]/(opt["votes"]) * 100), 2)
            votos_segundo = round((opt["voto_curso"]["segundo"]/(opt["votes"]) * 100), 2)
            votos_tercero = round((opt["voto_curso"]["tercero"]/(opt["votes"]) * 100), 2)
            votos_cuarto = round((opt["voto_curso"]["cuarto"]/(opt["votes"]) * 100), 2)
            votos_master = round((opt["voto_curso"]["master"]/(opt["votes"]) * 100), 2)

            opt["estadisticas"] = {"votos_censo": votos_censo, "votos_m": votos_m, "votos_f": votos_f, "votos_primero": votos_primero, "votos_segundo": votos_segundo,
             "votos_tercero": votos_tercero, "votos_cuarto": votos_cuarto, "votos_master": votos_master}
        
        for i in [1,2,3,4,5]:
            for opt in voting["preguntas"][i]["opts"]:
                votos_censo = round(((opt["votes"]) / voting["preguntas"][i]["n_personas_censo"] * 100), 2)
                votos_m = round((opt["voto_M"]/(opt["votes"]) * 100), 2)
                votos_f = round((opt["voto_F"]/(opt["votes"]) * 100), 2)

                opt["estadisticas"] = {"votos_censo": votos_censo, "votos_m": votos_m, "votos_f": votos_f}

        if voting["tipo"] == "VG":
            for opt in voting["preguntas"][6]["opts"]:
                votos_censo = round(((opt["votes"]) / voting["n_personas_censo"] * 100), 2)
                votos_m = round((opt["voto_M"]/(opt["votes"]) * 100), 2)
                votos_f = round((opt["voto_F"]/(opt["votes"]) * 100), 2)
                votos_primero = round((opt["voto_curso"]["primero"]/(opt["votes"]) * 100), 2)
                votos_segundo = round((opt["voto_curso"]["segundo"]/(opt["votes"]) * 100), 2)
                votos_tercero = round((opt["voto_curso"]["tercero"]/(opt["votes"]) * 100), 2)
                votos_cuarto = round((opt["voto_curso"]["cuarto"]/(opt["votes"]) * 100), 2)
                votos_master = round((opt["voto_curso"]["master"]/(opt["votes"]) * 100), 2)

                opt["estadisticas"] = {"votos_censo": votos_censo, "votos_m": votos_m, "votos_f": votos_f, "votos_primero": votos_primero, 
                "votos_segundo": votos_segundo, "votos_tercero": votos_tercero, "votos_cuarto": votos_cuarto, "votos_master": votos_master}

        return Response(voting)
