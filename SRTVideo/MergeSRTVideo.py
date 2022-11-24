

from os.path import splitext, isfile
import unicodedata
import urwid.old_str_util
from moviepy.editor import (VideoFileClip,
                            TextClip,
                            CompositeVideoClip)
from scipy.ndimage import gaussian_filter
from skimage.filters import difference_of_gaussians, gaussian


# 读取字幕文件
def read_srt(path):
    content = ""
    with open(path, 'r', encoding='UTF-8') as f:
        content = f.read()
        return content


# 字幕拆分
def get_sequences(content):
    sequences = content.split('\n\n')
    sequences = [sequence.split('\n') for sequence in sequences]
    # 去除每一句空值
    sequences = [list(filter(None, sequence)) for sequence in sequences]
    # 去除整体空值
    return list(filter(None, sequences))


def strFloatTime(tempStr):
    xx = tempStr.split(':')
    hour = int(xx[0])
    minute = int(xx[1])
    second = int(xx[2].split(',')[0])
    minsecond = int(xx[2].split(',')[1])
    allTime = hour * 60 * 60 + minute * 60 + second + minsecond / 1000
    return allTime

class RealizeAddSubtitles():
    '''
    合成字幕与视频
    '''



    FontSize_Malai=55
    FontSize_Thai =45


    def __init__(self, videoFile, txtFile,language,videoTitle,index,outFolder):
        self.src_video = videoFile
        self.sentences = txtFile

        if not (isfile(self.src_video) and self.src_video.endswith(('.avi', '.mp4')) and isfile(
                self.sentences) and self.sentences.endswith('.srt')):
            print('视频仅支持avi以及mp4，字幕仅支持srt格式')
        else:
            video = VideoFileClip(self.src_video)
            # 获取视频的宽度和高度
            w, h = video.w, video.h
            # 所有字幕剪辑
            txts = []
            blurbgs = []
            content = read_srt(self.sentences)
            sequences = get_sequences(content)



            i = 100
            list = TextClip.list('font')
            for line in sequences:
                if len(line)<3:
                    continue
                sentences = line[2]
                start = line[1].split(' --> ')[0]
                end = line[1].split(' --> ')[1]

                # if len(list) > i:
                #     i = i + 1
                start=strFloatTime(start)
                end=strFloatTime(end)

                start, end = map(float, (start, end))
                span=end-start

                font = 'Courier-New-Bold'
                if language == '泰语':
                    font = 'Ayuthaya'#'Leelawadee'
                posy = h - 463

                pos = (5, posy)
                txt = (TextClip(sentences, fontsize=45,bg_color='white', stroke_color='black', stroke_width=1,
                                font= font, size=(w, 0),method='caption',
                                align='South', color='white')
                       .set_position(pos)
                       .set_duration(span)
                       .set_start(start))
                posy = getPosy(videoTitle,h,txt.h)
                pos = (5, posy)
                clipbg = video.subclip(start, end).set_pos(pos).crop(5, posy, txt.w, posy+txt.h).set_start(start)
                clipbg_blurred = clipbg.fl_image(blur)


                txt2 = (TextClip((sentences).encode('utf-8'), fontsize=45, stroke_color='blue', stroke_width=1,
                                font= font, size=(w-33, 0),method='caption',
                                align='South', color='white')
                       .set_position(pos)
                       .set_duration(span)
                       .set_start(start))

                blurbgs.append(clipbg_blurred)
                txts.append(txt2)

            # 合成视频，写入文件

            video = CompositeVideoClip([video, *blurbgs , *txts])
            fn, ext = splitext(self.src_video)
            video.write_videofile(f'{outFolder}/{videoTitle}_{language}_{index}{ext}',audio_codec='aac')
            # audio = video.audio
            # audio.close()
            # video.close()

def getPosy(videoTitle,screenH,textH):
    if videoTitle == '最豪废婿':
        return int(screenH - 335 - textH)
    elif videoTitle == '最强超能王':
        return int(screenH - 510)


def blur(image):
        """ Returns a blurred (radius=2 pixels) version of the image """
        return gaussian(image.astype(float), sigma=10)
if __name__ == '__main__':
    '''调用方法示例'''
    srt_path = './1.srt'



    addSubtitles = RealizeAddSubtitles('.1.mp4', srt_path)

def GenBlur():
    clip1 = VideoFileClip("1.mp4").subclip(0, 9)

    clip2 = VideoFileClip("1.mp4").subclip(2, 4).crop(0,300,540,660).set_pos((50,50)).set_start(2)
    clip2_blurred = clip2.fl_image(blur)

    clip3 = VideoFileClip("1.mp4").subclip(5, 7).crop(0, 350, 440, 660).set_pos((50,150)).set_start(5)
    clip3_blurred = clip3.fl_image(blur)

    clips = []
    clips.append(clip2_blurred)
    clips.append(clip3_blurred)

    video = CompositeVideoClip([clip1, *clips])
    video.write_videofile(f'clip.mp4')