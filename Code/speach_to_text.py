## pip install azure-cognitiveservices-speech

# import azure.cognitiveservices.speech as speechsdk
subscription_key = "2129d8c1fe3a4d63973d9023ecc14a47"
region = "eastus"

# speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

# def from_mic():
#     speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
#     speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    
#     print("Speak into your microphone.")
#     result = speech_recognizer.recognize_once_async().get()
#     return(result.text)

# from_mic()



def from_file():
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    audio_input = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    
    result = speech_recognizer.recognize_once_async().get()
    return(result.text)

def stt_main(use_stt):
	if use_stt:
		return(from_file())
	else:
		return('nothing to perform')

# def from_file():
#     speech_config = speechsdk.SpeechConfig(subscription="<paste-your-speech-key-here>", region="<paste-your-speech-location/region-here>")
#     audio_input = speechsdk.AudioConfig(filename="your_file_name.wav")
#     speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    
#     result = speech_recognizer.recognize_once_async().get()
#     print(result.text)

# from_file()

# ### directly from mic example 2

# print("Say something...")


# # Starts speech recognition, and returns after a single utterance is recognized. The end of a
# # single utterance is determined by listening for silence at the end or until a maximum of 15
# # seconds of audio is processed.  The task returns the recognition text as result. 
# # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# # shot recognition like command or query. 
# # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
# result = speech_recognizer.recognize_once()

# # Checks result.
# if result.reason == speechsdk.ResultReason.RecognizedSpeech:
#     print("Recognized: {}".format(result.text))
# elif result.reason == speechsdk.ResultReason.NoMatch:
#     print("No speech could be recognized: {}".format(result.no_match_details))
# elif result.reason == speechsdk.ResultReason.Canceled:
#     cancellation_details = result.cancellation_details
#     print("Speech Recognition canceled: {}".format(cancellation_details.reason))
#     if cancellation_details.reason == speechsdk.CancellationReason.Error:
#         print("Error details: {}".format(cancellation_details.error_details))
# # </code>

## REST 
# Request module must be installed.
# Run pip install requests if necessary.
import requests




def get_token(subscription_key):
    fetch_token_url = 'https://eastus.api.cognitive.microsoft.com/sts/v1.0/issueToken'
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)
    # print(access_token)


# ACCESS_TOKEN = get_token(subscription_key)

# url = "https://eastus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US"

# headers = {
#   'Content-type': 'audio/wav;codec="audio/pcm";',
#   'Ocp-Apim-Subscription-Key': subscription_key,
#   'Content-type': 'audio/wav'
#   # 'Authorization: Bearer ACCESS_TOKEN'
# }

# with open('welcome.wav','rb') as payload:
#     response = requests.request("POST", url, headers=headers, data=payload)
#     print(response.text)