from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from predict.instagram_api import FetchInstagramUser

import requests
import json


class Predict(View):

    def get(self, request, userid):

        insta = FetchInstagramUser()
        feature_array = {'input': insta.getFeatureArray(userid)}

        result = requests.post(
            'https://eogydkeql2.execute-api.us-east-1.amazonaws.com/default', data=json.dumps(feature_array))

        return HttpResponse(json.dumps({
            'userid': userid,
            'is_real': not bool(result.json()['result'])
        }), content_type='application/json')
