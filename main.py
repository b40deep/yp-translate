import gradio as gr

import asyncio
import random


css = """
.translated_text textarea{
    min-height: 28vh !important;
    font-size: 4em !important
    }
"""

str_arabic = ""
str_spanish = ""
str_english = ""

keep_running = True

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

with gr.Blocks(css=css) as demo:
    out1 = gr.Textbox(show_label=False, placeholder="ready to start...", interactive=False, autoscroll=True, max_lines=3, elem_classes="translated_text")
    out2 = gr.Textbox(show_label=False, placeholder="ready to start...", interactive=False, autoscroll=True, max_lines=3, elem_classes="translated_text")
    out3 = gr.Textbox(show_label=False, placeholder="ready to start...", interactive=False, autoscroll=True, max_lines=3, elem_classes="translated_text")
    btn = gr.Button("▶️")
    btn.click(update_outputs, inputs=None, outputs=[out1, out2, out3])

demo.launch()
