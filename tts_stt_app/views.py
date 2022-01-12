import sys
from django.shortcuts import render
import json
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

sys.path.append('./Code')
from syllable_count import logic_flow

@api_view(['GET', 'POST'])
def main_spell_check(request):
	if request.method == 'GET':
		return Response({"message": "Got some data!"})

	elif request.method == 'POST':
		# print(request.data)
		user_id = request.data['user_id']
		age = request.data['age']
		co_ordinate = request.data['co_ordinate']
		user_text = request.data['user_text']
		result = logic_flow(user_id = user_id, age = age, user_text = user_text,co_ordinate = co_ordinate)
		return Response({"message": result})