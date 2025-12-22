from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Dict, Set
from enum import Enum
import uuid

# =============== ENUMS ===============
class MessageStatus(Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    EDITED = "edited"
    DELETED = "deleted"


class UserStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    AWAY = "away"
    BUSY = "busy"


class ChatType(Enum):
    PRIVATE = "private"
    GROUP = "group"
    CHANNEL = "channel"
    SUPERGROUP = "supergroup"


# =============== ABSTRACT CLASSES ===============
class Identifiable(ABC):
    """Abstract class for all entities that have an ID"""
    
    @abstractmethod
    def get_id(self) -> str:
        pass
    
    @abstractmethod
    def get_display_name(self) -> str:
        pass


class Content(ABC):
    """Abstract class for different types of content"""
    
    @abstractmethod
    def get_content(self) -> str:
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict:
        pass
    
    @abstractmethod
    def can_be_forwarded(self) -> bool:
        pass


class Searchable(ABC):
    """Abstract class for entities that can be searched"""
    
    @abstractmethod
    def search(self, query: str) -> List:
        pass
    
    @abstractmethod
    def index_content(self) -> Dict:
        pass


class Notifiable(ABC):
    """Abstract class for entities that can receive notifications"""
    
    @abstractmethod
    def notify(self, notification: str) -> None:
        pass
    
    @abstractmethod
    def get_notification_preferences(self) -> Dict:
        pass


class Serializable(ABC):
    """Abstract class for entities that can be serialized"""
    
    @abstractmethod
    def to_dict(self) -> Dict:
        pass
    
    @abstractmethod
    def from_dict(self, data: Dict) -> None:
        pass


# =============== CONCRETE CLASSES ===============
class User(Identifiable, Notifiable):
    """Represents a Telegram user"""
    
    def __init__(self, username: str, phone_number: str, first_name: str, 
                 last_name: str = "", bio: str = ""):
        self._id = str(uuid.uuid4())
        self.username = username
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.bio = bio
        self.status = UserStatus.OFFLINE
        self.contacts: List[User] = []
        self.blocked_users: Set[str] = set()
        self.notification_prefs = {
            "messages": True,
            "calls": True,
            "groups": True,
            "channels": False
        }
        self.last_seen = datetime.now()
    
    def get_id(self) -> str:
        return self._id
    
    def get_display_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def notify(self, notification: str) -> None:
        print(f"[Notification for {self.username}]: {notification}")
    
    def get_notification_preferences(self) -> Dict:
        return self.notification_prefs
    
    def update_status(self, new_status: UserStatus) -> None:
        self.status = new_status
        self.last_seen = datetime.now()
    
    def add_contact(self, user: 'User') -> None:
        if user.get_id() not in [u.get_id() for u in self.contacts]:
            self.contacts.append(user)
    
    def block_user(self, user_id: str) -> None:
        self.blocked_users.add(user_id)
    
    def is_blocked(self, user_id: str) -> bool:
        return user_id in self.blocked_users


class TextMessage(Content, Serializable):
    """Represents a text message"""
    
    def __init__(self, text: str, sender_id: str):
        self._id = str(uuid.uuid4())
        self.text = text
        self.sender_id = sender_id
        self.timestamp = datetime.now()
        self.edited = False
        self.edit_history: List[Dict] = []
    
    def get_content(self) -> str:
        return self.text
    
    def get_metadata(self) -> Dict:
        return {
            "id": self._id,
            "sender": self.sender_id,
            "timestamp": self.timestamp,
            "edited": self.edited,
            "length": len(self.text)
        }
    
    def can_be_forwarded(self) -> bool:
        return True
    
    def edit(self, new_text: str) -> None:
        self.edit_history.append({
            "old_text": self.text,
            "timestamp": datetime.now()
        })
        self.text = new_text
        self.edited = True
    
    def to_dict(self) -> Dict:
        return {
            "id": self._id,
            "text": self.text,
            "sender_id": self.sender_id,
            "timestamp": self.timestamp.isoformat(),
            "edited": self.edited,
            "edit_history": self.edit_history
        }
    
    def from_dict(self, data: Dict) -> None:
        self._id = data["id"]
        self.text = data["text"]
        self.sender_id = data["sender_id"]
        self.timestamp = datetime.fromisoformat(data["timestamp"])
        self.edited = data["edited"]
        self.edit_history = data["edit_history"]


class MediaMessage(Content):
    """Represents a media message (photo, video, etc.)"""
    
    def __init__(self, file_url: str, media_type: str, caption: str = "", 
                 sender_id: str = ""):
        self._id = str(uuid.uuid4())
        self.file_url = file_url
        self.media_type = media_type
        self.caption = caption
        self.sender_id = sender_id
        self.timestamp = datetime.now()
        self.file_size: Optional[int] = None
        self.dimensions: Optional[tuple] = None
    
    def get_content(self) -> str:
        return f"[{self.media_type.upper()}] {self.caption}"
    
    def get_metadata(self) -> Dict:
        return {
            "id": self._id,
            "type": self.media_type,
            "url": self.file_url,
            "sender": self.sender_id,
            "timestamp": self.timestamp,
            "caption": self.caption
        }
    
    def can_be_forwarded(self) -> bool:
        return True
    
    def get_file_info(self) -> str:
        return f"{self.media_type} - {self.file_size or 'Unknown'} bytes"


class Chat(Identifiable, Searchable):
    """Abstract base for all chat types"""
    
    def __init__(self, chat_type: ChatType, title: str = ""):
        self._id = str(uuid.uuid4())
        self.chat_type = chat_type
        self.title = title
        self.messages: List[Content] = []
        self.participants: List[User] = []
        self.created_at = datetime.now()
        self.pinned_messages: List[str] = []
    
    def get_id(self) -> str:
        return self._id
    
    def get_display_name(self) -> str:
        return self.title or f"Chat {self._id[:8]}"
    
    def search(self, query: str) -> List[Content]:
        results = []
        for message in self.messages:
            if query.lower() in message.get_content().lower():
                results.append(message)
        return results
    
    def index_content(self) -> Dict:
        return {
            "chat_id": self._id,
            "message_count": len(self.messages),
            "participant_count": len(self.participants),
            "last_message": self.messages[-1].get_content() if self.messages else None
        }
    
    def add_message(self, message: Content) -> None:
        self.messages.append(message)
    
    def add_participant(self, user: User) -> None:
        if user not in self.participants:
            self.participants.append(user)
    
    def get_recent_messages(self, count: int = 10) -> List[Content]:
        return self.messages[-count:] if self.messages else []


class PrivateChat(Chat):
    """One-on-one private chat"""
    
    def __init__(self, user1: User, user2: User):
        super().__init__(ChatType.PRIVATE, f"{user1.get_display_name()} ↔ {user2.get_display_name()}")
        self.user1 = user1
        self.user2 = user2
        self.add_participant(user1)
        self.add_participant(user2)
    
    def get_other_user(self, current_user: User) -> Optional[User]:
        if current_user.get_id() == self.user1.get_id():
            return self.user2
        elif current_user.get_id() == self.user2.get_id():
            return self.user1
        return None


class GroupChat(Chat):
    """Group chat with multiple participants"""
    
    def __init__(self, title: str, creator: User):
        super().__init__(ChatType.GROUP, title)
        self.creator = creator
        self.admins: List[User] = [creator]
        self.add_participant(creator)
    
    def add_admin(self, user: User) -> None:
        if user not in self.admins:
            self.admins.append(user)
    
    def is_admin(self, user: User) -> bool:
        return user in self.admins
    
    def remove_participant(self, admin: User, user_to_remove: User) -> bool:
        if admin in self.admins and user_to_remove in self.participants:
            self.participants.remove(user_to_remove)
            if user_to_remove in self.admins:
                self.admins.remove(user_to_remove)
            return True
        return False


class Channel(Chat):
    """Broadcast channel"""
    
    def __init__(self, title: str, creator: User, description: str = ""):
        super().__init__(ChatType.CHANNEL, title)
        self.creator = creator
        self.description = description
        self.subscribers: List[User] = []
        self.is_public = True
    
    def add_subscriber(self, user: User) -> None:
        if user not in self.subscribers:
            self.subscribers.append(user)
    
    def broadcast_message(self, message: Content) -> None:
        self.add_message(message)
        for subscriber in self.subscribers:
            subscriber.notify(f"New message in channel {self.title}: {message.get_content()[:50]}...")


class Bot(Identifiable):
    """Telegram bot"""
    
    def __init__(self, username: str, token: str, description: str = ""):
        self._id = str(uuid.uuid4())
        self.username = username
        self.token = token
        self.description = description
        self.commands: Dict[str, callable] = {}
        self.webhook_url: Optional[str] = None
    
    def get_id(self) -> str:
        return self._id
    
    def get_display_name(self) -> str:
        return f"🤖 {self.username}"
    
    def register_command(self, command: str, handler: callable) -> None:
        self.commands[command] = handler
    
    def handle_message(self, message: str, user: User) -> str:
        if message.startswith('/'):
            command = message.split()[0]
            if command in self.commands:
                return self.commands[command](user, message)
            else:
                return f"Unknown command: {command}"
        else:
            return f"Echo: {message}"
    
    def set_webhook(self, url: str) -> None:
        self.webhook_url = url


class Call(Notifiable, Serializable):
    """Voice/Video call"""
    
    def __init__(self, caller: User, receiver: User, is_video: bool = False):
        self._id = str(uuid.uuid4())
        self.caller = caller
        self.receiver = receiver
        self.is_video = is_video
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.duration: Optional[float] = None
        self.status = "ringing"
    
    def notify(self, notification: str) -> None:
        self.receiver.notify(f"📞 Call from {self.caller.get_display_name()}: {notification}")
    
    def get_notification_preferences(self) -> Dict:
        return {"calls": True}
    
    def answer(self) -> None:
        self.status = "active"
        self.start_time = datetime.now()
    
    def end(self) -> None:
        self.status = "ended"
        self.end_time = datetime.now()
        if self.start_time:
            self.duration = (self.end_time - self.start_time).total_seconds()
    
    def to_dict(self) -> Dict:
        return {
            "id": self._id,
            "caller": self.caller.get_id(),
            "receiver": self.receiver.get_id(),
            "is_video": self.is_video,
            "status": self.status,
            "duration": self.duration
        }
    
    def from_dict(self, data: Dict) -> None:
        self._id = data["id"]
        self.is_video = data["is_video"]
        self.status = data["status"]
        self.duration = data["duration"]


class Sticker(Content):
    """Sticker content"""
    
    def __init__(self, sticker_id: str, emoji: str = "", pack_id: str = ""):
        self._id = sticker_id
        self.emoji = emoji
        self.pack_id = pack_id
        self.sender_id: Optional[str] = None
    
    def get_content(self) -> str:
        return f"[Sticker: {self.emoji or 'No emoji'}]"
    
    def get_metadata(self) -> Dict:
        return {
            "id": self._id,
            "emoji": self.emoji,
            "pack": self.pack_id,
            "sender": self.sender_id
        }
    
    def can_be_forwarded(self) -> bool:
        return True


# =============== MAIN APPLICATION DEMO ===============
class TelegramDemo:
    """Demonstrates the Telegram-like messaging system"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.chats: Dict[str, Chat] = {}
        self.bots: Dict[str, Bot] = {}
        
    def run_demo(self):
        print("=== Telegram-like Messaging System Demo ===\n")
        
        # Create users
        print("1. Creating users...")
        alice = User("alice_wonder", "+1234567890", "Alice", "Wonderland", "Down the rabbit hole")
        bob = User("bob_builder", "+0987654321", "Bob", "Builder", "Can we fix it?")
        charlie = User("charlie_choco", "+1112223333", "Charlie", "Chocolate", "Golden ticket hunter")
        diana = User("diana_prince", "+4445556666", "Diana", "Prince", "Amazon warrior")
        
        self.users = {u.get_id(): u for u in [alice, bob, charlie, diana]}
        
        alice.update_status(UserStatus.ONLINE)
        bob.update_status(UserStatus.AWAY)
        
        print(f"   Created: {alice.get_display_name()}, {bob.get_display_name()}, "
              f"{charlie.get_display_name()}, {diana.get_display_name()}")
        
        # Add contacts
        print("\n2. Adding contacts...")
        alice.add_contact(bob)
        alice.add_contact(charlie)
        bob.add_contact(alice)
        print(f"   {alice.get_display_name()}'s contacts: {[c.get_display_name() for c in alice.contacts]}")
        
        # Create private chat
        print("\n3. Creating private chat...")
        alice_bob_chat = PrivateChat(alice, bob)
        self.chats[alice_bob_chat.get_id()] = alice_bob_chat
        print(f"   Created private chat: {alice_bob_chat.get_display_name()}")
        
        # Send messages in private chat
        print("\n4. Sending messages...")
        msg1 = TextMessage("Hi Bob! How are you?", alice.get_id())
        alice_bob_chat.add_message(msg1)
        
        msg2 = TextMessage("Hi Alice! I'm good, working on a new project.", bob.get_id())
        alice_bob_chat.add_message(msg2)
        
        # Edit a message
        print("\n5. Editing a message...")
        msg3 = TextMessage("Let's meet tomorrow at 3 PM", alice.get_id())
        alice_bob_chat.add_message(msg3)
        print(f"   Original message: {msg3.get_content()}")
        msg3.edit("Let's meet tomorrow at 4 PM")
        print(f"   Edited message: {msg3.get_content()}")
        print(f"   Edit history: {msg3.edit_history}")
        
        # Create group chat
        print("\n6. Creating group chat...")
        study_group = GroupChat("Study Group", alice)
        study_group.add_participant(bob)
        study_group.add_participant(charlie)
        study_group.add_admin(bob)
        self.chats[study_group.get_id()] = study_group
        print(f"   Created group: {study_group.get_display_name()}")
        print(f"   Participants: {[p.get_display_name() for p in study_group.participants]}")
        print(f"   Admins: {[a.get_display_name() for a in study_group.admins]}")
        
        # Send media message
        print("\n7. Sending media message...")
        photo_msg = MediaMessage("https://example.com/photo.jpg", "photo", 
                                 "Check out this beautiful sunset!", alice.get_id())
        study_group.add_message(photo_msg)
        print(f"   Sent: {photo_msg.get_content()}")
        print(f"   Metadata: {photo_msg.get_metadata()}")
        
        # Create channel
        print("\n8. Creating channel...")
        news_channel = Channel("Tech News", diana, "Latest technology updates")
        news_channel.add_subscriber(alice)
        news_channel.add_subscriber(bob)
        self.chats[news_channel.get_id()] = news_channel
        
        channel_msg = TextMessage("Breaking: New AI model achieves human-level reasoning", diana.get_id())
        news_channel.broadcast_message(channel_msg)
        print(f"   Created channel: {news_channel.get_display_name()}")
        print(f"   Subscribers: {len(news_channel.subscribers)}")
        print(f"   Broadcasted: {channel_msg.get_content()}")
        
        # Create and use a bot
        print("\n9. Creating and using a bot...")
        echo_bot = Bot("echo_bot", "bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11", "Simple echo bot")
        
        def help_command(user: User, message: str) -> str:
            return "Available commands: /help, /time, /echo"
        
        def time_command(user: User, message: str) -> str:
            return f"Current time: {datetime.now().strftime('%H:%M:%S')}"
        
        echo_bot.register_command("/help", help_command)
        echo_bot.register_command("/time", time_command)
        
        print(f"   Bot: {echo_bot.get_display_name()}")
        print(f"   Bot response to '/help': {echo_bot.handle_message('/help', alice)}")
        print(f"   Bot response to '/time': {echo_bot.handle_message('/time', bob)}")
        print(f"   Bot response to 'Hello': {echo_bot.handle_message('Hello', charlie)}")
        
        # Make a call
        print("\n10. Making a call...")
        call = Call(alice, bob, is_video=True)
        print(f"   Call from {call.caller.get_display_name()} to {call.receiver.get_display_name()}")
        call.notify("Incoming video call")
        call.answer()
        print(f"   Call answered, status: {call.status}")
        call.end()
        print(f"   Call ended, duration: {call.duration:.1f} seconds")
        
        # Search in chat
        print("\n11. Searching messages...")
        alice_bob_chat.add_message(TextMessage("Let's discuss the project tomorrow", alice.get_id()))
        alice_bob_chat.add_message(TextMessage("The project deadline is next week", bob.get_id()))
        
        search_results = alice_bob_chat.search("project")
        print(f"   Search for 'project' found {len(search_results)} messages:")
        for msg in search_results:
            print(f"     - {msg.get_content()}")
        
        # Demonstrate notifications
        print("\n12. Notification system...")
        alice.notify("New message from Bob")
        bob.notify("Diana added you to a channel")
        
        # Demonstrate SOLID principles (brief explanation)
        print("\n13. SOLID Principles in this design:")
        print("   - Single Responsibility: Each class has one main responsibility")
        print("   - Open/Closed: Easy to extend with new content types")
        print("   - Liskov Substitution: All Content types can be used interchangeably")
        print("   - Interface Segregation: Multiple focused interfaces")
        print("   - Dependency Inversion: High-level modules depend on abstractions")
        
        # Statistics
        print("\n14. System Statistics:")
        print(f"   Total users: {len(self.users)}")
        print(f"   Total chats: {len(self.chats)}")
        print(f"   Total messages in alice-bob chat: {len(alice_bob_chat.messages)}")
        print(f"   Alice's status: {alice.status.value}")
        print(f"   Bob's last seen: {bob.last_seen.strftime('%Y-%m-%d %H:%M:%S')}")


# =============== SOLID PRINCIPLES EXPLANATION ===============
"""
SOLID Principles in this Telegram implementation:

1. SINGLE RESPONSIBILITY:
   - User class handles only user-related operations
   - Chat class handles only chat management
   - Message classes handle only content representation
   - Bot class handles only bot functionality

2. OPEN/CLOSED PRINCIPLE:
   - Easy to add new message types (AudioMessage, LocationMessage, etc.) 
     by extending Content class
   - Easy to add new chat types by extending Chat class
   - New features can be added without modifying existing code

3. LISKOV SUBSTITUTION:
   - All Content subclasses (TextMessage, MediaMessage, Sticker) 
     can be used interchangeably
   - All Chat subclasses can be used wherever Chat is expected
   - All Identifiable objects can be identified uniformly

4. INTERFACE SEGREGATION:
   - Small, focused interfaces (Identifiable, Content, Searchable, etc.)
   - Classes implement only interfaces they need
   - No fat interfaces forcing unnecessary implementations

5. DEPENDENCY INVERSION:
   - High-level modules depend on abstractions (Content, Identifiable)
   - Low-level modules also depend on these abstractions
   - Dependency injection through constructors
"""

if __name__ == "__main__":
    demo = TelegramDemo()
    demo.run_demo()
