import gradio as gr
import asyncio
import random
import azure.speechtranslate_stream_final as speechsdk
import threading, queue

keep_running=True

# Your shared data-generating function
async def get_text2():
    while keep_running:
        yield f"Random Value: {random.randint(1, 100)}"
        await asyncio.sleep(1)

async def update_outputs(output1='', output2='', output3=''):
    async for val in get_text2():
        output1 += f" {val}"
        output2 += f" {val}"
        output3 += f" {val}"
        yield output1, output2, output3       


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

def get_delta(old_string, new_string):
    res = ""
    if new_string.startswith(old_string):
        res = new_string[len(old_string):]
        print("AF Old || {}".format(old_string))
        print("AF Old >> {}".format(res))
    else:
        res = new_string
        print("AF New || {}".format(old_string))
        print("AF New >> {}".format(res))
    return res  # If no common prefix, return the whole new string

async def update_outputs2():
    global str_arabic, str_spanish, str_english
    while True:
        async for tag, output in speechsdk.get_text():
            res = []
            if tag == 'RECOGNIZING':
                print("Recognizing:")
            if tag == 'RECOGNIZED':
                print("Recognized:")
            for lang in [ to_english, to_spanish, to_arabic ]:
                if lang in output.translations:
                    text = output.translations[lang]
                    # print("{} || {} ||>> {}".format(tag, lang, text))
                    if lang == to_english:
                        str_english += text
                        res.append(str_english)
                    elif lang == to_spanish:
                        str_spanish += text
                        res.append(str_spanish)
                    elif lang == to_arabic:
                        str_arabic += text
                        res.append(str_arabic)
            yield res

with gr.Blocks(css=css) as demo:
    out1 = gr.Textbox(show_label=False, placeholder="ready to start...", interactive=False, autoscroll=True, max_lines=3, elem_classes="translated_text")
    out2 = gr.Textbox(show_label=False, placeholder="ready to start...", interactive=False, autoscroll=True, max_lines=3, elem_classes="translated_text")
    out3 = gr.Textbox(show_label=False, placeholder="ready to start...", interactive=False, autoscroll=True, max_lines=3, elem_classes="translated_text")
    btn = gr.Button("▶️")
    btn.click(update_outputs2, inputs=None, outputs=[out1, out2, out3])
    
demo.launch()
