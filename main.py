import re
import streamlit as st
from googleapiclient.discovery import build

def extract_video_id(url):
    # Sử dụng regex để tìm ID video
    video_id = re.search(r'(?<=v=)[^&#]+', url)
    if not video_id:
        video_id = re.search(r'(?<=be/)[^&#]+', url)
    return video_id.group(0) if video_id else None

def video_comments(video_id):

    # empty list for storing reply
    replies = []
    comments = []

    # creating youtube resource object
    api_key = 'AIzaSyBP5BExPx1lN_wlS8uiITi1WKpBnQ9G_ig'
    youtube = build('youtube', 'v3', developerKey=api_key)

    # retrieve youtube video results
    video_response=youtube.commentThreads().list(part='snippet,replies', videoId=video_id).execute()

    # iterate video response
    while video_response:

        # extracting required info
        # from each result object
        for item in video_response['items']:

            # Extracting comments
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

            # counting number of reply of comment
            replycount = item['snippet']['totalReplyCount']

            # if reply is there
            if replycount>0:

                # iterate through all reply
                for reply in item['replies']['comments']:

                    # Extract reply
                    reply = reply['snippet']['textDisplay']

                    # Store reply is list
                    replies.append(reply)

            # empty reply list
            replies = []

        # Again repeat
        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                    part = 'snippet,replies',
                    videoId = video_id,
                      pageToken = video_response['nextPageToken']
                ).execute()
        else:
            break
    return comments

def cmt_processing(video_id):
    comment = video_comments(video_id)
    #clear_text = text_processing(comment)
    # clear_text_padded = comments_youtube.padding(tokenize(clear_text))
    return comment

# Giao diện Streamlit
st.title('YouTube Video ID Extractor')

# Nhập liên kết YouTube
link = st.text_input('Enter YouTube URL')

# Hiển thị ID video nếu liên kết hợp lệ
if link:
    vid_id = extract_video_id(link)
    if not vid_id:
        st.error('Invalid YouTube URL')
    else:
        st.success(f'Video ID: {vid_id}')
        comments = cmt_processing(vid_id)
        for i in comments:
            st.text(i)



