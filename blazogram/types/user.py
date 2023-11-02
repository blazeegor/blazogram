from dataclasses import dataclass


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: str = None
    username: str = None
    language_code: str = None
    is_premium: bool = False
    added_to_attachment_menu: bool = False
    can_join_groups: bool = None
    can_read_all_group_messages: bool = None
    supports_inline_queries: bool = None

    @property
    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name if self.last_name else self.first_name