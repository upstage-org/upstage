# coding: iso8859-15
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AssetType(Base):
    __tablename__ = 'asset_type'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('asset_type_id_seq'::regclass)"))
    name = Column(Text, nullable=False)
    description = Column(Text)
    file_location = Column(Text, nullable=False)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))


class Config(Base):
    __tablename__ = 'config'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('config_id_seq'::regclass)"))
    name = Column(Text, nullable=False)
    value = Column(Text)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, server_default=text("nextval('events_id_seq'::regclass)"))
    performance_id = Column(Integer, index=True)
    topic = Column(Text, nullable=False)
    mqtt_timestamp = Column(Float(53), nullable=False)
    created = Column(DateTime, nullable=False, index=True, server_default=text("CURRENT_TIMESTAMP"))
    payload = Column(JSON, nullable=False)


class JwtNoList(Base):
    __tablename__ = 'jwt_no_list'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('jwt_no_list_id_seq'::regclass)"))
    token = Column(Text, nullable=False, unique=True)
    token_type = Column(Text, nullable=False)
    remove_after = Column(DateTime, server_default=text("timezone('utc'::text, now())"))


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('tag_id_seq'::regclass)"))
    name = Column(Text, nullable=False)
    color = Column(Text)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))


class UpstageGroup(Base):
    __tablename__ = 'upstage_group'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('upstage_group_id_seq'::regclass)"))
    description = Column(Text)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))


class UpstageUser(Base):
    __tablename__ = 'upstage_user'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('upstage_user_id_seq'::regclass)"))
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    email = Column(Text, unique=True)
    bin_name = Column(Text, nullable=False)
    role = Column(Integer, nullable=False, server_default=text("0"))
    first_name = Column(Text)
    last_name = Column(Text)
    display_name = Column(Text)
    active = Column(Boolean, nullable=False, server_default=text("false"))
    validated_via_portal = Column(Boolean, nullable=False, server_default=text("false"))
    agreed_to_terms = Column(Boolean, nullable=False, server_default=text("false"))
    firebase_pushnot_id = Column(Text)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))
    deactivated_on = Column(DateTime)
    upload_limit = Column(Integer)
    intro = Column(Text)
    can_send_email = Column(Boolean, server_default=text("false"))


class AdminOneTimeTotpQrUrl(Base):
    __tablename__ = 'admin_one_time_totp_qr_url'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('admin_one_time_totp_qr_url_id_seq'::regclass)"))
    user_id = Column(ForeignKey('upstage_user.id'), nullable=False, unique=True, server_default=text("0"))
    url = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    recorded_time = Column(DateTime, server_default=text("timezone('utc'::text, now())"))
    active = Column(Boolean, nullable=False, server_default=text("true"))

    user = relationship('UpstageUser', uselist=False)


class AppleProfile(Base):
    __tablename__ = 'apple_profile'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('apple_profile_id_seq'::regclass)"))
    user_id = Column(ForeignKey('upstage_user.id'))
    apple_id = Column(Text, nullable=False, server_default=text("''::text"))
    apple_phone = Column(Text)
    apple_email = Column(Text)
    apple_first_name = Column(Text)
    apple_last_name = Column(Text)
    apple_username = Column(Text)
    other_profile_json = Column(Text)
    received_datetime = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    user = relationship('UpstageUser')


class Asset(Base):
    __tablename__ = 'asset'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('asset_id_seq'::regclass)"))
    name = Column(Text, nullable=False)
    asset_type_id = Column(ForeignKey('asset_type.id'), nullable=False)
    owner_id = Column(ForeignKey('upstage_user.id'), nullable=False)
    description = Column(Text)
    file_location = Column(Text, nullable=False)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))
    updated_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))
    size = Column(BigInteger, nullable=False, server_default=text("0"))
    copyright_level = Column(Integer, server_default=text("0"))

    asset_type = relationship('AssetType')
    owner = relationship('UpstageUser')


class FacebookProfile(Base):
    __tablename__ = 'facebook_profile'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('facebook_profile_id_seq'::regclass)"))
    user_id = Column(ForeignKey('upstage_user.id'))
    facebook_id = Column(Text, nullable=False, server_default=text("''::text"))
    facebook_phone = Column(Text)
    facebook_email = Column(Text)
    facebook_first_name = Column(Text)
    facebook_last_name = Column(Text)
    facebook_username = Column(Text)
    other_profile_json = Column(Text)
    received_datetime = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    user = relationship('UpstageUser')


class GoogleProfile(Base):
    __tablename__ = 'google_profile'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('google_profile_id_seq'::regclass)"))
    user_id = Column(ForeignKey('upstage_user.id'))
    google_id = Column(Text, nullable=False, server_default=text("''::text"))
    google_phone = Column(Text)
    google_email = Column(Text)
    google_first_name = Column(Text)
    google_last_name = Column(Text)
    google_username = Column(Text)
    other_profile_json = Column(Text)
    received_datetime = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    user = relationship('UpstageUser')


class Stage(Base):
    __tablename__ = 'stage'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('stage_id_seq'::regclass)"))
    name = Column(Text, nullable=False)
    description = Column(Text)
    owner_id = Column(ForeignKey('upstage_user.id'), nullable=False)
    file_location = Column(String, nullable=False)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))
    last_access = Column(DateTime)

    owner = relationship('UpstageUser')


class UserGroup(Base):
    __tablename__ = 'user_group'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('user_group_id_seq'::regclass)"))
    notes = Column(Text)
    group_id = Column(ForeignKey('upstage_group.id'), nullable=False, server_default=text("0"))
    user_id = Column(ForeignKey('upstage_user.id'), nullable=False, server_default=text("0"))
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    group = relationship('UpstageGroup')
    user = relationship('UpstageUser')


class UserPortalConfig(Base):
    __tablename__ = 'user_portal_config'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('user_portal_config_id_seq'::regclass)"))
    user_id = Column(ForeignKey('upstage_user.id'), nullable=False, unique=True, server_default=text("0"))
    json_config = Column(Text, nullable=False, server_default=text("'{\"viewing_timezone\":\"US/Eastern\"}'::text"))

    user = relationship('UpstageUser', uselist=False)


class UserPushnot(Base):
    __tablename__ = 'user_pushnot'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('user_pushnot_id_seq'::regclass)"))
    user_id = Column(ForeignKey('upstage_user.id'), nullable=False, server_default=text("0"))
    push_notification = Column(Text, nullable=False)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    user = relationship('UpstageUser')


class UserSession(Base):
    __tablename__ = 'user_session'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('user_session_id_seq'::regclass)"))
    user_id = Column(ForeignKey('upstage_user.id'), nullable=False, server_default=text("0"))
    access_token = Column(Text, nullable=False, server_default=text("''::text"))
    refresh_token = Column(Text, nullable=False, server_default=text("''::text"))
    recorded_time = Column(DateTime, server_default=text("timezone('utc'::text, now())"))
    app_version = Column(Text)
    app_os_type = Column(Text)
    app_os_version = Column(Text)
    app_device = Column(Text)

    user = relationship('UpstageUser')


class AssetAttribute(Base):
    __tablename__ = 'asset_attribute'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('asset_attribute_id_seq'::regclass)"))
    asset_id = Column(ForeignKey('asset.id'), nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    asset = relationship('Asset')


class AssetGroup(Base):
    __tablename__ = 'asset_group'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('asset_group_id_seq'::regclass)"))
    description = Column(Text)
    group_id = Column(ForeignKey('upstage_group.id'), nullable=False, server_default=text("0"))
    asset_id = Column(ForeignKey('asset.id'), nullable=False, server_default=text("0"))
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    asset = relationship('Asset')
    group = relationship('UpstageGroup')


class AssetLicense(Base):
    __tablename__ = 'asset_license'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('asset_license_id_seq'::regclass)"))
    asset_id = Column(ForeignKey('asset.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    created_on = Column(DateTime, index=True, server_default=text("timezone('utc'::text, now())"))
    level = Column(Integer, nullable=False)
    permissions = Column(Text)

    asset = relationship('Asset')


class AssetUsage(Base):
    __tablename__ = 'asset_usage'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('asset_usage_id_seq'::regclass)"))
    asset_id = Column(ForeignKey('asset.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    user_id = Column(ForeignKey('upstage_user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    approved = Column(Boolean, nullable=False, server_default=text("false"))
    seen = Column(Boolean, nullable=False, server_default=text("false"))
    note = Column(Text)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    asset = relationship('Asset')
    user = relationship('UpstageUser')


class MediaTag(Base):
    __tablename__ = 'media_tag'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('media_tag_id_seq'::regclass)"))
    asset_id = Column(ForeignKey('asset.id'), nullable=False)
    tag_id = Column(ForeignKey('tag.id'), nullable=False)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    asset = relationship('Asset')
    tag = relationship('Tag')


class ParentAsset(Base):
    __tablename__ = 'parent_asset'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('parent_asset_id_seq'::regclass)"))
    asset_id = Column(ForeignKey('asset.id'), nullable=False)
    child_asset_id = Column(ForeignKey('asset.id'), nullable=False)

    asset = relationship('Asset', primaryjoin='ParentAsset.asset_id == Asset.id')
    child_asset = relationship('Asset', primaryjoin='ParentAsset.child_asset_id == Asset.id')


class ParentStage(Base):
    __tablename__ = 'parent_stage'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('parent_stage_id_seq'::regclass)"))
    stage_id = Column(ForeignKey('stage.id'), nullable=False)
    child_asset_id = Column(ForeignKey('asset.id'), nullable=False)

    child_asset = relationship('Asset')
    stage = relationship('Stage')


class Performance(Base):
    __tablename__ = 'performance'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('performance_id_seq'::regclass)"))
    name = Column(Text)
    description = Column(Text)
    stage_id = Column(ForeignKey('stage.id'), nullable=False)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))
    saved_on = Column(DateTime)
    recording = Column(Boolean, nullable=False, server_default=text("false"))

    stage = relationship('Stage')


class Scene(Base):
    __tablename__ = 'scene'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('scene_id_seq'::regclass)"))
    name = Column(Text, nullable=False)
    scene_order = Column(Integer, nullable=False, index=True, server_default=text("0"))
    scene_preview = Column(Text)
    payload = Column(Text, nullable=False)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))
    active = Column(Boolean, nullable=False, server_default=text("true"))
    owner_id = Column(ForeignKey('upstage_user.id'), nullable=False, server_default=text("0"))
    stage_id = Column(ForeignKey('stage.id'), nullable=False)

    owner = relationship('UpstageUser')
    stage = relationship('Stage')


class StageAttribute(Base):
    __tablename__ = 'stage_attribute'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('stage_attribute_id_seq'::regclass)"))
    stage_id = Column(ForeignKey('stage.id'), nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    stage = relationship('Stage')


class StageGroup(Base):
    __tablename__ = 'stage_group'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('stage_group_id_seq'::regclass)"))
    description = Column(Text)
    group_id = Column(ForeignKey('upstage_group.id'), nullable=False, server_default=text("0"))
    stage_id = Column(ForeignKey('stage.id'), nullable=False, server_default=text("0"))
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    group = relationship('UpstageGroup')
    stage = relationship('Stage')


class UserAsset(Base):
    __tablename__ = 'user_asset'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('user_asset_id_seq'::regclass)"))
    notes = Column(Text)
    asset_id = Column(ForeignKey('asset.id'), nullable=False, server_default=text("0"))
    user_id = Column(ForeignKey('upstage_user.id'), nullable=False, server_default=text("0"))
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    asset = relationship('Asset')
    user = relationship('UpstageUser')


class UserStage(Base):
    __tablename__ = 'user_stage'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('user_stage_id_seq'::regclass)"))
    notes = Column(Text)
    stage_id = Column(ForeignKey('stage.id'), nullable=False, server_default=text("0"))
    user_id = Column(ForeignKey('upstage_user.id'), nullable=False, server_default=text("0"))
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))

    stage = relationship('Stage')
    user = relationship('UpstageUser')


class LivePerformanceMqttConfig(Base):
    __tablename__ = 'live_performance_mqtt_config'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('live_performance_mqtt_config_id_seq'::regclass)"))
    name = Column(Text, nullable=False)
    owner_id = Column(ForeignKey('upstage_user.id'), nullable=False, server_default=text("0"))
    ip_address = Column(Text, nullable=False)
    websocket_port = Column(Integer, nullable=False, server_default=text("0"))
    webclient_port = Column(Integer, nullable=False, server_default=text("0"))
    topic_name = Column(Text, nullable=False, unique=True)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    created_on = Column(DateTime, server_default=text("timezone('utc'::text, now())"))
    expires_on = Column(DateTime)
    performance_id = Column(ForeignKey('performance.id'), nullable=False)

    owner = relationship('UpstageUser')
    performance = relationship('Performance')
