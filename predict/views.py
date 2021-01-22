from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from predict.instagram_api import FetchInstagramUser

from predict.models import Predictions

import requests
import json


class Predict(View):

    def get(self, request, userid):

        if self.checkDatabase(userid):
            return HttpResponse(json.dumps({
                'userid': userid,
                'is_real': Predictions.objects.filter(username=userid)[0].is_real
            }))
        else:
            insta = FetchInstagramUser()
            feature_array = {'input': insta.getFeatureArray(userid)}

            result = requests.post(
                'https://eogydkeql2.execute-api.us-east-1.amazonaws.com/default', data=json.dumps(feature_array))

            is_real = not bool(result.json()['result'])

            user = Predictions(username=userid, is_real=is_real)
            user.save()

            return HttpResponse(json.dumps({
                'userid': userid,
                'is_real': is_real
            }), content_type='application/json')



    def checkDatabase(self, userid):
        try:
            Predictions.objects.filter(username=userid)
            return True
        except Predictions.DoesNotExist:
            return False
