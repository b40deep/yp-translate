import azure.cognitiveservices.speech as speechsdk
import os, time, queue, asyncio
from terminal_colors import _BLU, _GRY, _YLW, _PNK, _PPL, _RED, _GRN, _DBL, _RST

# Define your subscription key, region, and languages

from dotenv import load_dotenv, dotenv_values 
load_dotenv() 


SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")
speech_key = SPEECH_KEY
service_region = SPEECH_REGION
from_language = "en-US"  # Example: English (United States)
to_language = "ar"    
to_language2 = "es"     
to_language3 = "en"    
to_language4 = "cy" 
to_language5 = "ko" 
# ar	Arabic (Iraq)
# es	Spanish (Honduras)
# cy	Welsh (United Kingdom)
# en	English (United Kingdom)
# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=stt

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=speech_key, region=service_region)
translation_config.speech_recognition_language = from_language
translation_config.add_target_language(to_language)
translation_config.add_target_language(to_language2)
translation_config.add_target_language(to_language3)
# translation_config.add_target_language(to_language4)
# translation_config.add_target_language(to_language5)


def printr(evt):
    res1 = evt.result.translations[to_language]
    res2 = evt.result.translations[to_language2]
    res3 = evt.result.translations[to_language3]
    # res4 = evt.result.translations[to_language4]
    # res5 = evt.result.translations[to_language5]
    print('{}{}{}: {}{}{}'.format(_BLU,to_language,_RST, _GRN,res1,_RST))
    print('{}{}{}: {}{}{}'.format(_BLU,to_language2,_RST, _GRN,res2,_RST))
    print('{}{}{}: {}{}{}'.format(_BLU,to_language3,_RST, _GRN,res3,_RST))
    # print('{}{}{}: {}{}{}'.format(_BLU,to_language4,_RST, _GRN,res4,_RST))
    # print('{}{}{}: {}{}{}'.format(_BLU,to_language5,_RST, _GRN,res5,_RST))
    print("\n")

def yieldr(evt):
    res1 = evt.result.translations[to_language]
    res2 = evt.result.translations[to_language2]
    res3 = evt.result.translations[to_language3]
    # res4 = evt.result.translations[to_language4]
    # res5 = evt.result.translations[to_language5]
    return [res1, res2, res3]

async def get_text():
    # # Configure longer timeouts
    # translation_config.set_property(
    #     speechsdk.PropertyId.Speech_SegmentationSilenceTimeoutMs, 
    #     "10000"  # 4 seconds of silence before concluding
    # )
    # Increase end silence timeout
    translation_config.set_property(
        speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs,
        "10000"
    )
    # # Increase initial silence timeout (how long to wait for speech to start)
    # translation_config.set_property(
    #     speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs,
    #     "500"  # 10 seconds to start speaking
    # )

    translation_recognizer = speechsdk.translation.TranslationRecognizer(
            translation_config=translation_config)
    done = False
    result_queue = asyncio.Queue()
    loop = asyncio.get_event_loop()  # Get current event loop

    def recognizing_cb(evt):
        loop.call_soon_threadsafe(
            # lambda: asyncio.create_task(result_queue.put(('RECOGNIZING', evt.result.text)))
            lambda: asyncio.create_task(result_queue.put(('RECOGNIZING', evt.result)))
        )

    def recognized_cb(evt):
        loop.call_soon_threadsafe(
            lambda: asyncio.create_task(result_queue.put(('RECOGNIZED', evt.result.text)))
        )

    def stop_cb(evt):
        nonlocal done
        print(f"CLOSING on {evt}")
        # Schedule the async stop operation
        loop.call_soon_threadsafe(
            lambda: asyncio.create_task(translation_recognizer.stop_continuous_recognition_async())
        )
        done = True

    print("Speak into your microphone.")
    translation_recognizer.recognizing.connect(recognizing_cb)
    # translation_recognizer.recognized.connect(recognized_cb)
    translation_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    translation_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    translation_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    translation_recognizer.session_stopped.connect(stop_cb)
    translation_recognizer.canceled.connect(stop_cb)
    translation_recognizer.start_continuous_recognition_async().get()
    while not done or not result_queue.empty():
        try:
            kind, text = await asyncio.wait_for(result_queue.get(), timeout=0.5)
            yield kind, text
        except asyncio.TimeoutError:
            continue

# Call the function to run it
async def main():
    while True:
        async for tag, text in get_text():
            for lang in [to_language, to_language2, to_language3]:
                if lang in text.translations:
                    print("{} || {}: {}".format(tag, lang, text.translations[lang]))
            # print("{} || {}".format(tag, text.translations[to_language]))
            # print("{} || {}".format(tag, text.translations[to_language2]))
            # print("{} || {}".format(tag, text.translations[to_language3]))

    stream_result_looks_like_this = '''
    TranslationRecognitionEventArgs
    ( 
      session_id=8198a236e8f94020af7ea633c3a9e004, 
      result=TranslationRecognitionResult
        (
            result_id=e3d4b7f9d52d43548698325d62d6e3ce, 
            translations=
                {
                'es': 'Porque parecen ser', 
                'fr': 'Parce qu’ils semblent être'
                },
            reason=ResultReason.TranslatingSpeech
        )
    )
    '''

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
    # Uncomment the following line to run the get_text function directly
    # asyncio.run(get_text())
    
    # For testing purposes, you can also call yieldr with a mock event
    # mock_event = speechsdk.translation.TranslationRecognitionEventArgs(...)
    # print(yieldr(mock_event))