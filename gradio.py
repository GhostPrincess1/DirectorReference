import gradio as gr

def process_data(input1, input2, input3, input4, input5):
    # 这里是你的数据处理逻辑
    # 返回值应该包括9个文本结果，1个图片链接和10个视频链接
    text_outputs = ["文本结果1", "文本结果2", "文本结果3", "文本结果4", "文本结果5",
                    "文本结果6", "文本结果7", "文本结果8", "文本结果9"]
    image_output = "https://example.com/image.jpg"  # 示例图片链接
    video_outputs = [
        "https://example.com/video1.mp4",  # 示例视频链接
        "https://example.com/video2.mp4",
        # 添加更多视频链接
    ]
    return text_outputs + [image_output] + video_outputs

inputs = [gr.inputs.Textbox(lines=2, label=f"输入 {i}") for i in range(1, 6)]
outputs = [gr.outputs.Textbox(label=f"文本结果 {i}") for i in range(1, 10)] + \
          [gr.outputs.Image(label="图片结果")] + \
          [gr.outputs.Video(label=f"视频结果 {i}") for i in range(1, 11)]

iface = gr.Interface(fn=process_data, inputs=inputs, outputs=outputs, title="数据处理界面")
iface.launch()
