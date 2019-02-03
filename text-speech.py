import gtts
import os
tts = gtts.gTTS(text='你好', lang='zh-cn')
tts.save("good.mp3")
os.system("good.mp3")
