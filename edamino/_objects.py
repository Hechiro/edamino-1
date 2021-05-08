from pydantic import BaseModel


class AvatarFrame(BaseModel):
    frameId: str = None
    frameType: int = None
    icon: str = None
    name: str
    ownershipStatus: str or int = None
    resourceUrl: str = None
    status: int = None
    version: int = None


class Account(BaseModel):
    activation: int = None
    advancedSettings: dict = None
    aminoIdEditable: bool = None
    appleID: str or int = None
    createdTime: str = None
    email: str = None
    emailActivation: int = None
    extensions: dict = None
    facebookID: str or int = None
    googleID: str = None
    icon: str = None
    mediaList: list = None
    membership: str or int or bool = None
    modifiedTime: str = None
    nickname: str = None
    phoneNumber: str or int = None
    phoneNumberActivation: int = None
    role: int = None
    securityLevel: int = None
    status: int = None
    twitterID: str or int = None
    uid: str = None
    username: str = None


class UserProfile(BaseModel):
    accountMembershipStatus: int = None
    aminoId: str = None
    blogsCount: int = None
    commentsCount: int = None
    consecutiveCheckInDays: bool = None
    content: str = None
    createdTime: str = None
    extensions: dict = None
    followingStatus: int = None
    icon: str = None
    isGlobal: bool = None
    isNicknameVerified: bool = None
    itemsCount: int = None
    joinedCount: int = None
    level: int = None
    mediaList: list = None
    membersCount: int = None
    membershipStatus: int = None
    modifiedTime: str = None
    mood: str or bool = None
    moodSticker: str or int = None
    ndcId: int = None
    nickname: str = None
    notificationSubscriptionStatus: int = None
    onlineStatus: int = None
    postsCount: int = None
    pushEnabled: bool = None
    reputation: int = None
    role: int = None
    status: int = None
    storiesCount: int = None
    uid: str = None
    visitorsCount: int = None
    visitPrivacy: int = None


class Login(BaseModel):
    account: Account = None
    api_duration: str = None
    api_message: str = None
    api_status_code: int = None
    api_timestamp: str = None
    user_id: str = None
    secret: str = None
    sid: str = None
    profile: UserProfile = None


class Author(BaseModel):
    accountMembershipStatus: int = None
    icon: str = None
    level: int = None
    nickname: str = None
    reputation: int = None
    role: int = None
    status: int
    uid: str = None
    avatarFrameId: str = None
    followingStatus: int = None
    avatarFrame: AvatarFrame = None


class Message(BaseModel):
    author: Author = None
    clientRefId: int = None
    content: str = ""
    createdTime: str = None
    extensions: dict = None
    includedInSummary: bool = None
    isHidden: bool = None
    mediaType: int = None
    messageId: str = None
    threadId: str = None
    type: int = None
    uid: str = None
    mediaValue: str = None


class Event(BaseModel):
    alertOption: int = None
    membershipStatus: int = None
    ndcId: str = None
    message: Message


class GetFromCode(BaseModel):
    ndcId: str = None
    objectId: str = None
    objectType: int = None
    shortCode: str = None
    targetCode: int = None
    fullPath: str = None
    content: str = None
    name: str = None
    icon: str = None
    link: str = None
    shareURLShortCode: str = None
    shareURLFullPath: str = None


class Member(BaseModel):
    icon: str
    membershipStatus: int = None
    nickname: str
    role: int
    status: int
    uid: str


class Thread(BaseModel):
    alertOption: int = None
    author: Author = None
    condition: int = None
    content: str = None
    createdTime: str = None
    extensions: dict = None
    icon: str = None
    isPinned: bool = None
    keywords: dict or str = None
    lastMessageSummary: dict = None
    lastReadTime: str = None
    latestActivityTime: str = None
    membersCount: int
    membersQuota: int = None
    membersSummary: list[Member]
