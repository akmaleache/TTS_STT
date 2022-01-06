import azure.cognitiveservices.speech as speechsdk
# from pygame import mixer, time
import io
subscription_key = "2129d8c1fe3a4d63973d9023ecc14a47"
region = "eastus"
# speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

# # Note: if only language is set, the default voice of that language is chosen.
# speech_config.speech_synthesis_language = "en-US" # e.g. "de-DE"
# # The voice setting will overwrite language setting.
# # The voice setting will not overwrite the voice element in input SSML.
# speech_config.speech_synthesis_voice_name ="en-US-ChristopherNeural"
# # output format
# # speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat["Audio16Khz32KBitRateMonoMp3"])

# ## create .wav flie of output
# # audio_config = AudioOutputConfig(filename="path/to/write/file.wav")
# # synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
# # synthesizer.speak_text_async("A simple test to write to a file.")

# # giving output to speaker
# def tts_main(use_tts,text):
# 	if use_tts == "yes":
# 		audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
# 		synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
# 		result = synthesizer.speak_text_async(text).get()
# 		print(type(result.audio_data))
# 		# sound = mixer.Sound(result.audio_data)
# 		stream = speechsdk.AudioDataStream(result)
# 		print(type(stream))
# 		res = result.audio_data
# 		print(stream)
# 		f = io.BytesIO(res)
# 		# print(f)
# 		# mixer.init()
# 		# sound = mixer.Sound(res)
# 		# audio = sound.play()
# 		# while audio.get_busy():
# 		#     time.Clock().tick(100)
# 		return(stream)
# 	else:
# 		return('nothing to do')

import requests




def get_token(subscription_key):
    fetch_token_url = 'https://eastus.api.cognitive.microsoft.com/sts/v1.0/issueToken'
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)
    return(access_token)
    # print(access_token)

def tts_main(use_tts,text):
	ACCESS_TOKEN = get_token(subscription_key)

	url = "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1"

	# url = "https://{}.tts.speech.microsoft.com/cognitiveservices/v1".format(location)
	header = {
	'Authorization': 'Bearer '+ACCESS_TOKEN,
	'Content-Type': 'application/ssml+xml',
	'X-Microsoft-OutputFormat': 'audio-24khz-160kbitrate-mono-mp3'
	}

	'''
	You can customise your speech output here
	by changing language, gender and name
	'''
	data = "<speak version='1.0' xml:lang='en-US'>\
			<voice xml:lang='en-US' xml:gender='Male' name='en-US-ChristopherNeural'>\
				{}\
			</voice>\
	   </speak>".format(text)
	res = requests.post(url, headers=header, data=data)
	
	# with open(r'C:\infiniticube\STT_TTS\Code\new.mp3', "wb") as file:
	# 		file.write(res.content)
	print(type(res.content))
	byte_file = res.content
	return(byte_file)
