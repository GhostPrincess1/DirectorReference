from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()


#全局的client对象，可以使用其他函数调用openai api，如果不需要全局的client对象，可以使用client = OpenAI(api_key=os.environ.
client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )



def get_clips(prompt:str):
    

    completion = client.chat.completions.create(
    model="gpt-4-0125-preview",
    messages=[
        {"role": "user", "content": f"{prompt}"}
    ]
    )


    return completion.choices[0].message.content



    pass

def get_image(prompt:str):
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"{prompt}",
        n=1,
        size="1024x1024",

    )
    return response.data[0].url

    pass


if __name__ == '__main__':
    
    pass