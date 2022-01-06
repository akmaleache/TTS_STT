import sys
from django.shortcuts import render
import json
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

sys.path.append('./Code')
from speach_to_text import stt_main
from text_to_speach import tts_main


@api_view(['GET', 'POST'])
def main_stt(request):
	if request.method == 'GET':
		return Response({"message": "Got some data!"})

	elif request.method == 'POST':
		# print(request.data)
		use_stt = request.data['start_stt']
		result = stt_main(use_stt = use_stt)
		return Response({"message": result})

@api_view(['GET', 'POST'])
def main_tts(request):
	if request.method == 'GET':
		return Response({"message": "Got some data!"})

	elif request.method == 'POST':
		# print(request.data)
		use_stt = request.data['start_tts']
		text = request.data['text']
		result = tts_main(use_tts = use_stt,text = text)
		# return Response({'byte':result})
		return HttpResponse(result, content_type='application/octet-stream')