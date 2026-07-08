from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, model_validator
from .models import MentorshipType, MentorshipStatus


class MentorshipBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: MentorshipType
    # LIVE fields
    start_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    streaming_link: Optional[str] = None
    max_slots: Optional[int] = None
    # RECORDED fields
    video_url: Optional[str] = None
    video_duration_seconds: Optional[int] = None
    thumbnail_url: Optional[str] = None

    @model_validator(mode='after')
    def validate_type_specific_fields(self) -> 'MentorshipBase':
        if self.type == MentorshipType.LIVE:
            if not self.start_time:
                raise ValueError('start_time is required for live mentorships')
            if not self.streaming_link:
                raise ValueError(
                    'streaming_link is required for live mentorships'
                )
            if not self.duration_minutes:
                raise ValueError(
                    'duration_minutes is required for live mentorships'
                )
        elif self.type == MentorshipType.RECORDED:
            if not self.video_url:
                raise ValueError(
                    'video_url is required for recorded mentorships'
                )
            if not self.video_duration_seconds:
                raise ValueError(
                    'video_duration_seconds is required for recorded mentorships'
                )
        return self


class MentorshipCreate(MentorshipBase):
    status: MentorshipStatus = MentorshipStatus.SCHEDULED


class MentorshipUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[MentorshipStatus] = None
    start_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    streaming_link: Optional[str] = None
    max_slots: Optional[int] = None
    video_url: Optional[str] = None
    video_duration_seconds: Optional[int] = None
    thumbnail_url: Optional[str] = None


class MentorshipResponse(MentorshipBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: MentorshipStatus
    created_at: datetime
    updated_at: datetime
