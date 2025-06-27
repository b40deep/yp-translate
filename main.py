import gradio as gr
import asyncio
import random

keep_running=True

# Your shared data-generating function
async def get_text():
    while keep_running:
        yield f"Random Value: {random.randint(1, 100)}"
        await asyncio.sleep(1)

async def update_outputs(output1='', output2='', output3=''):
    async for val in get_text():
        output1 += f" {val}"
        output2 += f" {val}"
        output3 += f" {val}"
        yield output1, output2, output3       


with gr.Blocks() as demo:
    out1 = gr.Textbox(show_label=False, interactive=False, autoscroll=True, max_lines=4)
    out2 = gr.Textbox(show_label=False, interactive=False, autoscroll=True, max_lines=4)
    out3 = gr.Textbox(show_label=False, interactive=False, autoscroll=True, max_lines=4)
    demo.load(update_outputs, inputs=None, outputs=[out1, out2, out3])
    
demo.launch()
