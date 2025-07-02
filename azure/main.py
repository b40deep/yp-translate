import gradio as gr
import asyncio
import random
import azure.speechtranslate_stream_final as speechsdk
import threading, queue

keep_running=True

css = """
.translated_text textarea{
    min-height: 28vh !important;
    font-size: 4em !important
    }
"""

to_arabic = speechsdk.to_language
to_spanish = speechsdk.to_language2
to_english = speechsdk.to_language3

str_arabic = ""
str_spanish = ""
str_english = ""

async def update_outputs2():
    global str_arabic, str_spanish, str_english
    while True:
        async for tag, output in speechsdk.get_text():
            res = ['', '', '']
            if tag == 'RECOGNIZING':
                print("Recognizing:")
            if tag == 'RECOGNIZED':
                print("Recognized:")
            for lang in [ to_english, to_spanish, to_arabic ]:
                if lang in output.translations:
                    text = output.translations[lang]
                    # print("{} || {} ||>> {}".format(tag, lang, text))
                    if lang == to_english:
                        res[0] = text
                    elif lang == to_spanish:
                        res[1] = text
                    elif lang == to_arabic:
                        res[2] = text
            yield res

with gr.Blocks(css=css) as demo:
    out1 = gr.Textbox(show_label=False, placeholder="ready to start...", interactive=False, autoscroll=True, max_lines=3, elem_classes="translated_text")
    out2 = gr.Textbox(show_label=False, placeholder="ready to start...", interactive=False, autoscroll=True, max_lines=3, elem_classes="translated_text")
    out3 = gr.Textbox(show_label=False, placeholder="ready to start...", interactive=False, autoscroll=True, max_lines=3, elem_classes="translated_text")
    btn = gr.Button("▶️")
    btn.click(update_outputs2, inputs=None, outputs=[out1, out2, out3])
    
demo.launch()
