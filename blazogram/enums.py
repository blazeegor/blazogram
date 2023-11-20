from enum import Enum


class ParseMode(Enum):
    HTML = 'HTML'
    MARKDOWN = 'MARKDOWN'
    MARKDOWN_V2 = 'MARKDOWN_V2'


class ChatAction(Enum):
    TYPING = 'typing'
    UPLOAD_PHOTO = 'upload_photo'
    RECORD_VIDEO = 'record_video'
    UPLOAD_VIDEO = 'upload_video'
    RECORD_VOICE = 'record_voice'
    UPLOAD_VOICE = 'upload_voice'
    UPLOAD_DOCUMENT = 'upload_document'
    CHOOSE_STICKER = 'choose_sticker'
    FIND_LOCATION = 'find_location'
    RECORD_VIDEO_NOTE = 'record_video_note'
    UPLOAD_VIDEO_NOTE = 'upload_video_note'


class Languages(Enum):
    RUSSIAN = 'ru'
    ENGLISH = 'en'
    FRENCH = 'fr'


class ContentTypes(Enum):
    TEXT = 'text'
    PHOTO = 'photo'
    VIDEO = 'video'