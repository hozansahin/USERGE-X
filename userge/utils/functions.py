import os
from ..config import Config
from .tools import take_screen_shot, runcmd
from .progress import progress
import re
import html


# For Downloading & Checking Media then Converting to Image.
# RETURNS an "Image".
async def media_to_image(message):
    replied = message.reply_to_message
    if not (replied.photo or replied.sticker or replied.animation or replied.video):
        await message.err("<code>Medya Türü Geçersiz! YARDIM'a bakın.</code>")
        return
    if not os.path.isdir(Config.DOWN_PATH):
        os.makedirs(Config.DOWN_PATH)
    await message.edit("Kahretsin, Yine Başlıyoruz...")
    dls = await message.client.download_media(
        message=message.reply_to_message,
        file_name=Config.DOWN_PATH,
        progress=progress,
        progress_args=(message, "Verilen içeriğe sahip olmaya çalışıyorum")
    )
    dls_loc = os.path.join(Config.DOWN_PATH, os.path.basename(dls))
    if replied.sticker and replied.sticker.file_name.endswith(".tgs"):
        await message.edit("Animasyonlu Stikır Görüntüye Dönüştürülüyor ...")
        png_file = os.path.join(Config.DOWN_PATH, "image.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {dls_loc} {png_file}"
        stdout, stderr = (await runcmd(cmd))[:2]
        os.remove(dls_loc)
        if not os.path.lexists(png_file):
            await message.err("Bu çıkartma Gey, Görev Başarıyla Başarısız Oldu ≧ω≦")
            raise Exception(stdout + stderr)
        dls_loc = png_file
    elif replied.sticker and replied.sticker.file_name.endswith(".webp"):
        stkr_file = os.path.join(Config.DOWN_PATH, "stkr.png")
        os.rename(dls_loc, stkr_file)
        if not os.path.lexists(stkr_file):
            await message.err("```Çok Aradık Ama Sticker bulunamadı...```")
            return
        dls_loc = stkr_file
    elif replied.animation or replied.video:
        await message.edit("Medya Görüntüye Dönüştürülüyor...")
        jpg_file = os.path.join(Config.DOWN_PATH, "image.jpg")
        await take_screen_shot(dls_loc, 0, jpg_file)
        os.remove(dls_loc)
        if not os.path.lexists(jpg_file):
            await message.err("Bu Gif Gey'dir (｡ì _ í｡), Görev Başarıyla Başarısız Oldu!")
            return
        dls_loc = jpg_file
    await message.edit("Neredeyse bitti...😎")
    return dls_loc


# Removes Emoji From Text
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats 
    "]+")

# RETURNS a "string" so don't use with await
def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, '', inputString)

# from NANA-REMIX --------
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html)


def escape_markdown(text):
    """Helper function to escape telegram markup symbols."""
    escape_chars = r'\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def mention_html(user_id, name):
    return u'<a href="tg://user?id={}">{}</a>'.format(user_id, html.escape(name))


def mention_markdown(user_id, name):
    return u'[{}](tg://user?id={})'.format(escape_markdown(name), user_id)

#------------------------

def thumb_from_audio(audio_path, output):
    os.system(f'ffmpeg -i {audio_path} -filter:v scale=500:500 -an {output}')
    return