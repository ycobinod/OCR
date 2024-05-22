import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView

search_url = settings.ELASTIC_URL+ settings.ELASTIC_INDEX + "/_search/"
headers = { "Authorization": "ApiKey "+ settings.ELASTIC_API_KEY}

class Search(APIView):
    def post(self , request):
        data = request.data
        keyword = data['keyword']
        search_query = {
            "query": {
                "wildcard": {
                    "book_name.keyword": {
                        "value" : "*"+ keyword +"*"
                    }
                }
            }
        }
        try:
            search_response = requests.post(search_url, headers=headers, json=search_query , verify=False)
            resp = search_response.json()
        except Exception as er:
            print('search err-----' , er)

        value = resp['hits']['total']['value']
        print('---value---------' , value)
        matched_data = []
        for hits_position in range(value):  
            objects = resp['hits']['hits'][hits_position]['_source']
            matched_data.append(objects)
                
        return JsonResponse({'data' : matched_data})