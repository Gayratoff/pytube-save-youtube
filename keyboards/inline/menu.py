from aiogram import types


class Keyboards:
    def main(self, video_url, audio_url):
        menu = types.InlineKeyboardMarkup(row_width=3)
        video = types.InlineKeyboardButton("📹 Video",callback_data=f"video;{video_url}")
        Audio = types.InlineKeyboardButton("🔊 MP3",callback_data=f"audio:{audio_url}")
        Off = types.InlineKeyboardButton("❌",callback_data=f"off")
        return menu.add(video,Audio,Off)
kb = Keyboards()