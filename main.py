from flask import Flask, render_template, request,jsonify,render_template
from flask_cors import CORS
import chatgpt
import json
import youtube
app = Flask(__name__)
CORS(app)

control_prompt_for_videoprompt = ("你是一个导演，我将提供给你视频画面的设计描述，它们已经按照<scene>、<charactor>、<motion>、<view>、<atmosphere>等xml标签标记出来了,这些标签标记的是视频的不同维度的描述。"
                  '所有xml标签标记的内容在"""这种三引号内。'
                  "你要仔细阅读这些描述，经过深思熟虑和复杂的思考，然后设计9段分镜画面来实现这个视频，每个分镜用不超过50个中文描述，这9个分镜在时间线上要有连续性和关联性。"
                  "你有足够的时间来设计，请确保设计出来的分镜是富有新意和出圈能力的，并且必须符合xml标签标记的描述。"
                  '最终你要给我一个完整的json格式的数据输出，json数据格式必须符合{"clip1":"","clip2":"",...,"clip9":""}这种格式要求。'
                  '请务必注意，你给我的回答中，有且仅有一个json格式数据的字符串，以{开头，以}结尾，内容为"clip1":"","clip2":"",...,"clip9":""这种格式要求，不得有其它东西。')

control_prompt_for_image = "你是一个电影分镜草图绘画师，我提供给你9段分镜的自然语言描述，这9段分镜包含在一个json格式的字符串内。请你仔细阅读这9段分镜的内容，精心设计和画出这9段分镜的草图。你要画出9宫格形状的彩色草图，9宫格按照从左到右、从上到下的顺序分别对应9段分镜描述的顺序，还要确保9宫格的每个格子大小一样。输出尺寸为长方形图片。你要帮助我写出来一个向dalle3输入的prompt，这个prompt要完全符合9段分镜描述的内容和上述提出的格式要求。你仅给我一个完整的prompt，不要夹杂多余的，只需要给我一个独立完整的prompt。"

control_prompt_for_search_video = '我想制作一个电影画面，我将提供给你视频画面的设计描述，它们已经按照<scene>、<charactor>、<motion>、<view>、<atmosphere>等xml标签标记出来了,这些标签标记的是视频设计的不同维度的描述。所有xml标签标记的内容在"""这种三引号内。这是一段我想设计的电影画面，请推荐一个符合这种画面内容的电影。你要告诉我推荐的电影的标题，以及与电影内容相关的若干关键词。最终你要给我一个完整的json格式的数据输出，json数据格式必须符合{"title":"","keyword":""}这个格式要求，json中的数据必须为英文。请务必注意，你给我的回答中，有且仅有一个json格式数据的字符串，这个字符串要能直接解析为json格式，不得有其它东西。'
@app.route('/biubiu',methods = ['POST','GET'])
def get_result():

    print("前端请求进入")
    #获取场景描述，按照不同的维度插入xml标签中
    scene = "<scene>"+request.form['scene']+"</scene>"
    charactor = "<charactor>"+request.form['charactor']+"</charactor>"
    motion = "<motion>"+request.form['motion']+"</motion>"
    view = "<view>"+request.form['view']+"</view>"
    atmosphere = "<atmosphere>"+request.form['atmosphere'] +"</atmosphere>"

    
    paragraph = "\n".join([scene, charactor, motion, view, atmosphere])
    paragraph = '"""' + paragraph + '"""'

    #print(paragraph)

    #step:向gpt获取9个clip分镜片段的描述，返回值应该为json格式
    

    get_clips_prompt = control_prompt_for_videoprompt + paragraph
    clips_for_image = chatgpt.get_clips(get_clips_prompt)  #作为向dalle3输入的一部分
    clips = json.loads(clips_for_image)   #作为最后输出的一部分

    #step:用dalle3画分镜草图

    dalle3_prompt = control_prompt_for_image + clips_for_image
    
    image_url = chatgpt.get_image(dalle3_prompt)


    #step:使用多维输入，产生视频参考推荐

    video_reference = chatgpt.get_clips(control_prompt_for_search_video+paragraph)

    print(video_reference)
    video_reference = json.loads(video_reference)


    #step:搜索youtube 视频链接

    links = youtube.get_links(video_reference['title']+","+video_reference['keyword'])
    #links = youtube.get_links(video_reference['title'])

    result = {
        "clip":clips,
        "video_reference":video_reference,
        "links":links,
        "image_url":image_url,
    }




    


    
    return jsonify(result) 

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/hello', methods=['GET', 'POST'])
# def hello():
#     if request.method == 'POST':
#         name = request.form['name']
#         return render_template('hello.html', name=name)
#     return render_template('hello_form.html')


@app.route('/',methods = ['POST','GET'])
def index():
    return render_template('index.html')
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1017)


    