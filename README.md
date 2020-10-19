<h2 align="center"><b>Owner: <a href="https://telegram.dog/deleteduser420">𝚂𝚢𝚗𝚝𝚊𝚡 ░ Σrr♢r</a></b></h2>

<br>
<h2 align="center"><b>Çeviri: <a href="https://telegram.dog/hozansahin">Hozan Şahin</a></b></h2>
<br>
<p align="center">
    <a href="https://github.com/code-rgb/USERGE-X"><img src="https://i.imgur.com/53mdl2v.png" alt="Userge-x" width=400px></a>
    <br>
    <br>
</p>

<h1>USERGE-X</h1>
<b>Kullanıcı Dostu Telegram UserBot'u</b>
<br>
<br>

[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/code-rgb/userge-x)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg?&style=flat-square)](https://github.com/code-rgb/USERGE-X#copyright--license)
[![Stars](https://img.shields.io/github/stars/code-rgb/USERGE-X?&style=flat-square)](https://github.com/code-rgb/USERGE-X/stargazers)
[![Forks](https://img.shields.io/github/forks/code-rgb/USERGE-X?&style=flat-square)](https://github.com/code-rgb/USERGE-X/network/members)
[![Issues Open](https://img.shields.io/github/issues/code-rgb/USERGE-X?&style=flat-square)](https://github.com/code-rgb/USERGE-X/issues)
[![Issues Closed](https://img.shields.io/github/issues-closed/code-rgb/USERGE-X?&style=flat-square)](https://github.com/code-rgb/USERGE-X/issues?q=is:closed)
[![PR Open](https://img.shields.io/github/issues-pr/code-rgb/USERGE-X?&style=flat-square)](https://github.com/code-rgb/USERGE-X/pulls)
[![PR Closed](https://img.shields.io/github/issues-pr-closed/code-rgb/USERGE-X?&style=flat-square)](https://github.com/code-rgb/USERGE-X/pulls?q=is:closed)
![Repo Size](https://img.shields.io/github/repo-size/code-rgb/userge-x?style=flat-square)
[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen?&style=flat-square)](https://sourcery.ai)
[![CodeFactor](https://www.codefactor.io/repository/github/code-rgb/userge-x/badge?&style=flat-square)](https://www.codefactor.io/repository/github/code-rgb/userge-x)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod&style=flat-square)](https://gitpod.io/#https://github.com/code-rgb/userge-x)
[![Vercel](https://img.shields.io/badge/Vercel-click%20to%20open-black?&logo=vercel&style=flat-square)](http://userge-x.vercel.app/)
[![Telegram](https://img.shields.io/badge/Support%20Group-USERGE--X-blue?&logo=telegram&style=social)](https://telegram.dog/x_xtests)
<br>

 **USERGE-X** _Python_ [Pyrogram](https://github.com/pyrogram/pyrogram) kullanılarak yazılmış Güçlü, _Kullanıcı Dostu_ Telegram UserBot (Kullanıcı) Botudur.
<br>
<br>

## feragatname

                
   ```

/**
    ⚠️USERGE-X Userbot kullanımından dolayı; Telegram hesabınız yasaklanabilir.⚠️          
    Bu açık kaynaklı bir projedir, yaptığınız her işlemden (siz)kendiniz sorumlusunuz. Kesinlikle  yöneticiler sorumluluk kabul etmemektedir.
    USERGE-X kullanarak bu sorumlulukları kabul etmiş sayılırsınız.
/**
```


## Gereksinimler 

* Python 3.8 veya üstü
* Telegram [API Anahtarı](https://my.telegram.org/apps)
* Google Drive [API Anahtarı](https://console.developers.google.com/)
* MongoDB [Veritabanı URL](https://cloud.mongodb.com/)


## Nasıl Kurulur
* HEROKU Methodu:

<p align="center">
<a href = "https://heroku.com/deploy?template=https://github.com/code-rgb/USERGE-X/tree/alpha"><img src="https://telegra.ph/file/57c4edb389224c9cf9996.png" alt="Kullanım İçin Tıklayın" width="490px"></a></p>
<br>

  > **NOT** : İhtiyacınız olan diğer değişkenleri ekleyebilirsiniz ve bu isteğinize bağlıdır.. (Ayarlar(settings) -> reveal config vars)
  * İlk önce Yukarıdaki Düğmeye tıklayın.
  * `API_ID`, `API_HASH`, `DATABASE_URL` ve `LOG_CHANNEL_ID` ve `HEROKU_APP_NAME` alanlarını Doldurun (**Zorunludur**)
  * Ardından Dual Mode değişkenlerini doldurun: `OWNER_ID`, `BOT_TOKEN` ve `HU_STRING_SESSION`
  * Sonra [**isteğe bağlı** diğer değişkenleri doldurun](https://telegra.ph/Heroku-Vars-for-USERGE-X-08-25)
  * Sonunda **deploy** düğmesine basın


## Daha fazla Detau
<details>
  <summary><b>Detaylar ve Klavuzlar</b></summary>

## Other Ways

* Docker ile çalıştırın 🐳 
    <a href="https://github.com/code-rgb/USERGE-X/blob/alpha/resources/readmeDocker.md"><b>Detaylı Kılavuza Bakın</b></a>

* With Git, Python and pip 🔧
  ```bash
  # Repoyu klonlayın
  git clone https://github.com/code-rgb/userge-x.git
  cd userge-x

  # virtualenv oluşturun
  virtualenv -p /usr/bin/python3 venv
  . ./venv/bin/activate

  # Gerekli bağımlılıkları yükleyin
  pip install -r requirements.txt

  # Create config.env as given config.env.sample and fill that
  cp config.env.sample config.env

  # string session oluşturun ve config.env dosyanıza ekleyin
  bash genStr

  # Artık botunuzu kullanabilirsiniz ;)
  bash run
  ```

  
<h2>Fork(Klon)'lanmış Repo için kullanım Kılavuzuo</h2>
<a href="https://telegra.ph/Upstream-Userge-Forked-Repo-Guide-07-04"><b>Fork(Klon)'lanmış Repo</b></a>
<br>
<br>

<h3 align="center">Youtube Anlatımı<h3>
<p align="center"><a href="https://youtu.be/M4T_BJvFqkc"><img src="https://i.imgur.com/VVgSk2m.png" width=250px></a>
</p>


## Özellikler

* Güçlü ve **Çok Kullanışlı** yerleşik Eklentiler
  * gdrive [ yükleme / indirme / vb. ] ( Ortak Drive Desteği! ) 
  * zip / tar / unzip / untar / unrar
  * telegram yükleme / indirme
  * pmpermit / afk
  * notlar / filtreler
  * birleştirme / tamamlama
  * gadmin
  * Eklenti yönetimi
  * ...Ve Çok daha fazlası
* Kanal & Gruo Kayıt alma desteği
* Veritabanı Desteği
* Yerleşik yardım desteği
* Kurulumu ve Kullanımı Kolay
* Eklentiler / yerleşik eklentiler
* Değiştirilebilen Taban ile modülleri yazmak kolay

## Örnek Plugin

```python
from userge import userge, Message, filters

LOG = userge.getLogger(__name__)  # logger object
CHANNEL = userge.getCLogger(__name__)  # channel logger object

# add command handler
@userge.on_cmd("test", about="help text to this command")
async def test_cmd(message: Message):
   LOG.info("starting test command...")  # log to console
   # some other stuff
   await message.edit("testing...", del_in=5)  # this will be automatically deleted after 5 sec
   # some other stuff
   await CHANNEL.log("testing completed!")  # log to channel

# add filters handler
@userge.on_filters(filters.me & filters.private)  # filter my private messages
async def test_filter(message: Message):
   LOG.info("starting filter command...")
   # some other stuff
   await message.reply(f"you typed - {message.text}", del_in=5)
   # some other stuff
   await CHANNEL.log("filter executed!")
```

</details> 


### Proje Tabanları

* [Pyrogram Assistant](https://github.com/pyrogram/assistant)
* [PyroGramBot](https://github.com/SpEcHiDe/PyroGramBot)
* [PaperPlane](https://github.com/RaphielGang/Telegram-Paperplane)
* [Uniborg](https://github.com/SpEcHiDe/UniBorg)


### Telif Hakkı & Lisans 

[**GNU General Public License v3.0**](https://github.com/code-rgb/USERGE-X/blob/alpha/LICENSE) Standartlarına göre lisanslanmıştır.
