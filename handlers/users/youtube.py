from pytube import YouTube



async def Download(link,media, x):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()

    try:
        youtubeObject.download(output_path=media,filename=x)
    except:
        print("Xatolik yuz berdi")
    print("Yuklab olish muvaffaqiyatli yakunlandi")

    data = youtubeObject.url
    if data:
        return data
    return None


async def Download_audio(link,audio, f):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_audio_only()
    try:
        youtubeObject.download(output_path=audio,filename=f)
    except:
        print("Xatolik yuz berdi")
    print("Yuklab olish muvaffaqiyatli yakunlandi")

    datas = youtubeObject.url
    if datas:
        return datas
    return None


