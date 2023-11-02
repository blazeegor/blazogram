from dataclasses import dataclass
from .photo import ChatPhoto


@dataclass
class Chat:
    id: int
    type: str
    title: str = None
    username: str = None
    first_name: str = None
    last_name: str = None
    is_forum: bool = None
    bio: str = None
    photo: ChatPhoto = None


@dataclass
class ChatAdministratorRights:
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: bool = False
    can_edit_messages: bool = False
    can_pin_messages: bool = False
    can_post_stories: bool = False
    can_edit_stories: bool = False
    can_delete_stories: bool = False
    can_manage_topics: bool = False