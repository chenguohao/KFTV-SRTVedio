import loadSRT
from MergeSRTVideo import strFloatTime, RealizeAddSubtitles, GenBlur

videoTitle = '最强超能王'
language = '越南语'
lan = ''
if language == '越南语':
    lan = 'Vim'
for i in range(2,11):
    videoPath = f'/Volumes/SSD/TV/{videoTitle}/{videoTitle}_中文_{i}.mp4'
    srtPath = f'/Volumes/SSD/TV-{lan}/{videoTitle}/SRT/{i}.srt'
    outFolder = f'/Volumes/SSD/TV-{lan}/{videoTitle}'
    RealizeAddSubtitles(videoPath, srtPath, language,videoTitle,i,outFolder)
