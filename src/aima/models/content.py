from pydantic import BaseModel

class SocialMediaPost(BaseModel):
    platform: str
    post_type: str
    text: str
    hashtags: list[str] = []
    cta: str = ""

class AdCopy(BaseModel):
    headline: str
    body: str
    cta: str
    target_audience: str

class GeneratedContent(BaseModel):
    social_media_posts: list[SocialMediaPost] = []
    ad_copies: list[AdCopy] = []
    email_subject_lines: list[str] = []
    key_talking_points: list[str] = []
