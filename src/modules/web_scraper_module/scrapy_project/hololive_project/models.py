from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from .....utils.database_utils import Base

class HoloSchedulesModel(Base):
    __tablename__ = 'hololive_schedules'

    # Stream fields
    stream_id = Column(String(20), primary_key=True)
    stream_link = Column(String(50))
    stream_title = Column(String(100))
    stream_description = Column(String(100))
    stream_thumbnail = Column(String(100))
    stream_type = Column(String(20))
    stream_state = Column(String(20))
    stream_duration = Column(String(20))

    # Datetime fields
    datetime_scheduled_start = Column(DateTime)
    datetime_actual_start = Column(DateTime)
    datetime_actual_end = Column(DateTime)

    # Streamer fields
    # channel_id = Column(String(50), ForeignKey('hololive_channels.channel_id'))
    channel_id = Column(String(50))
    channel_name = Column(String(50))
    channel_short_name = Column(String(50))
    channel_collabs = Column(String(100))

    # Define the relationship with the Channels table
    # hololive_channels = relationship('HololiveChannelsModel', back_populates='hololive_schedules')

class HololiveChannelsModel(Base):
    __tablename__ = 'hololive_channels'

    channel_id = Column(String(20), primary_key=True)
    channel_name = Column(String(50))
    channel_short_name = Column(String(50))

    # hololive_schedules = relationship('HoloSchedulesModel', back_populates='hololive_channels')