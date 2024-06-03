
import requests

API_KEY = 'AIzaSyC3kacTRv0C0upRaUpU7spPU69DQAZHr5I'  # 替换为你的API密钥


class Video():
    def __init__(self,video_id,credit) -> None:

        self.video_id = video_id
        self.credit = credit
        
        pass

def get_links(SEARCH_QUERY:str) -> list[str]:
    links = []
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': SEARCH_QUERY,
        'type': 'video',  # 只搜索视频
        'key': API_KEY,
        #'videoCategoryId': "30",
        #'videoDuration':"medium",
        'maxResults': 25,  # 可以调整返回结果的数量，最大为50
    }
    response = requests.get(url, params=params)

    print(response.status_code)
    videos = response.json()

    videos_obj = []  # 存储原始视频
    for video in videos.get('items', []):
        #print(f"Title: {video['snippet']['title']}")
        #print(f"Description: {video['snippet']['description']}")
        video_id = video.get('id', {}).get('videoId', 'N/A')  # 更安全的方式来获取videoId
        if video_id != 'N/A':  # 确保videoId存在
            #print(f"Video ID: {video_id}")
            #print(f"Published At: {video['snippet']['publishedAt']}")
            #print(f"Video Link: https://www.youtube.com/watch?v={video_id}")
            videos_obj.append(Video(video_id, get_video_info(video_id)))
            #videos.append(f"https://www.youtube.com/embed/{video_id}")
        #print('------------------------------------------------------------------------------------------------------')

    # 使用sorted函数进行排序，指定key为lambda函数，以对象的credit属性为排序依据
    sorted_videos = sorted(videos_obj, key=lambda x: x.credit, reverse=True)

    for i in range(0,len(sorted_videos)):
        link = f"https://www.youtube.com/embed/{sorted_videos[i].video_id}"
        links.append(link)
    return links

    pass
def get_video_info(video_id) -> int:
    #API_KEY = 'YOUR_API_KEY'  # 将YOUR_API_KEY替换为你的YouTube Data API密钥
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet,contentDetails,statistics&key={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        video_data = data['items'][0]

        # 提取视频的基本信息
        title = video_data['snippet']['title']
        description = video_data['snippet']['description']
        publish_time = video_data['snippet']['publishedAt']

        # 提取内容详情
        duration = video_data['contentDetails']['duration']

        # 提取统计信息
        view_count = video_data['statistics']['viewCount']
        #print(type(view_count))
        like_count = video_data['statistics'].get('likeCount')  # 使用get是为了防止没有likeCount的情况
        #print(type(like_count))
        comment_count = video_data['statistics'].get('commentCount')  # 同上
        #print(type(comment_count))
        #print(f"Title: {title}")
        #print(f"Description: {description}")
        #print(f"Publish Time: {publish_time}")
        #print(f"Duration: {duration}")
        #print(f"Views: {view_count}")
        #print(f"Likes: {like_count}")
        #print(f"Comments: {comment_count}")

        view_count = convert_none_to_zero(view_count)
        like_count = convert_none_to_zero(like_count)
        comment_count = convert_none_to_zero(comment_count)

        return get_credit(view_count, like_count, comment_count)
    else:
        print("Video not found or access denied.")
        return 0

def get_video_comments(video_id):
    #API_KEY = 'YOUR_API_KEY'  # 替换为你的API密钥
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?key={API_KEY}&textFormat=plainText&part=snippet&videoId={video_id}&maxResults=20"

    response = requests.get(url)
    data = response.json()

    if 'items' in data:
        for item in data['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            print(f"Author: {author}\nComment: {comment}\n")
    else:
        print("No comments found or access denied.")


def get_credit(weight1,weight2,weight3) ->int:


    return 0.5*int(weight1) + 0.3*int(weight2) + 0.2*int(weight3)

def convert_none_to_zero(obj):
    if obj is None:
        return 0
    else:
        return obj


def get_np(touru,xianjinliu):

    return sum(xianjinliu) - touru
    pass
def get_roi(touru,xianjinliu):

    return (sum(xianjinliu) - touru)/touru

    pass

def get_npv(touru,xianjinliu):

    return 0.9259*xianjinliu[0] + 0.8573*xianjinliu[1] + 0.7938*xianjinliu[2] + 0.7350*xianjinliu[3] + 0.6806*xianjinliu[4] -touru
    
    pass

if __name__ == '__main__':
    # links = get_links('forest,river,car,channel')
    # print(links)

    ProjectA_np = get_np(100000, [30000, 30000, 30000, 30000, 25000])
    print("净利润:"+str(ProjectA_np))
    ProjectA_roi = get_roi(100000, [30000, 30000, 30000, 30000, 25000])
    print("投资回报率ROI:"+str(ProjectA_roi*100)+"%")
    ProjectA_npv = get_npv(100000, [30000, 30000, 30000, 30000, 25000])
    print("净现值:"+str(ProjectA_npv))
    print("----------------------------------------------------------------------")
    ProjectB_np = get_np(100000, [10000, 10000, 10000, 10000, 100000])
    print("净利润:"+str(ProjectB_np))
    ProjectB_roi = get_roi(100000, [10000, 10000, 10000, 10000, 100000])
    print("投资回报率ROI:"+str(ProjectB_roi*100)+"%")
    ProjectB_npv = get_npv(100000, [10000, 10000, 10000, 10000, 100000])
    print("净现值:"+str(ProjectB_npv))
    print("----------------------------------------------------------------------")

    ProjectC_np = get_np(130000, [40000, 40000, 50000, 30000, 10000])
    print("净利润:"+str(ProjectC_np))

    ProjectC_roi = get_roi(130000, [40000, 40000, 50000, 30000, 10000])
    print("投资回报率ROI:"+str(ProjectC_roi*100)+"%")
    ProjectC_npv = get_npv(130000, [40000, 40000, 50000, 30000, 10000])
    print("净现值:"+str(ProjectC_npv))
    print("----------------------------------------------------------------------")

    ProjectD_np = get_np(140000, [40000, 40000, 50000, 25000, 10000])
    print("净利润:"+str(ProjectD_np))
    ProjectD_roi = get_roi(140000, [40000, 40000, 50000, 25000, 10000])
    print("投资回报率ROI:"+str(ProjectD_roi*100)+"%")   
    projectD_npv = get_npv(140000, [40000, 40000, 50000, 25000, 10000])
    print("净现值:"+str(projectD_npv))


    pass
