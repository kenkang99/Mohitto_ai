from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = 'user_table'
    user_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    email = Column(Text, unique=True, index=True, nullable=False)
    password = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    requests = relationship("Request", back_populates="user")
    hair_recommendations = relationship("HairRecommendation", back_populates="user")
    hairshop_recommendations = relationship("HairshopRecommendation", back_populates="user")

class Request(Base):
    __tablename__ = 'request_table'
    request_id = Column(BigInteger, primary_key=True, index=True)
    user_image_url = Column(Text)
    hair_length = Column(String(20))
    hair_type = Column(String(20))
    sex = Column(String(20))
    location = Column(String(20))
    cheekbone = Column(String(20))
    mood = Column(Text)
    dyed = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    forehead_shape = Column(String(20))
    difficulty = Column(String(20))
    has_bangs = Column(Integer)
    user_id = Column(BigInteger, ForeignKey('user_table.user_id'))
    user = relationship("User", back_populates="requests")
    results = relationship("Result", back_populates="request")
    hair_recommendations = relationship("HairRecommendation", back_populates="request")

class Result(Base):
    __tablename__ = 'result_table'
    result_id = Column(BigInteger, primary_key=True, index=True)
    face_type = Column(String(20))
    skin_tone = Column(String(20))
    forehead = Column(String(20))
    sex = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())
    request_id = Column(BigInteger, ForeignKey('request_table.request_id'))
    request = relationship("Request", back_populates="results")

class Hairstyle(Base):
    __tablename__ = 'hairstyle_table'
    hair_id = Column(BigInteger, primary_key=True, index=True)
    hairstyle_name = Column(String(20), nullable=False)
    hairstyle_image_url = Column(Text)
    hairstyle_explanation = Column(Text)
    hair_recommendations = relationship("HairRecommendation", back_populates="hairstyle")

class HairRecommendation(Base):
    __tablename__ = 'hair_recommendation_table'
    hair_rec_id = Column(BigInteger, primary_key=True, index=True)
    simulation_image_url = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    explanation = Column(Text)
    color = Column(Text)
    is_saved = Column(Integer, default=0)
    request_id = Column(BigInteger, ForeignKey('request_table.request_id'))
    hair_id = Column(BigInteger, ForeignKey('hairstyle_table.hair_id'))
    user_id = Column(BigInteger, ForeignKey('user_table.user_id'))
    request = relationship("Request", back_populates="hair_recommendations")
    hairstyle = relationship("Hairstyle", back_populates="hair_recommendations")
    user = relationship("User", back_populates="hair_recommendations")
    hairshop_recommendations = relationship("HairshopRecommendation", back_populates="hair_recommendation")

class Hairshop(Base):
    __tablename__ = 'hairshop_table'
    hairshop_id = Column(BigInteger, primary_key=True, index=True)
    hairshop_name = Column(Text, nullable=False)
    address = Column(Text)
    menu = Column(Text)
    phone = Column(String(20))
    intro = Column(Text)
    latitude = Column(Text)
    longitude = Column(Text)
    hairshop_recommendations = relationship("HairshopRecommendation", back_populates="hairshop")

class HairshopRecommendation(Base):
    __tablename__ = 'hairshop_recommendation_table'
    hairshop_rec_id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    is_saved = Column(Integer, default=0)
    hair_rec_id = Column(BigInteger, ForeignKey('hair_recommendation_table.hair_rec_id'))
    hairshop_id = Column(BigInteger, ForeignKey('hairshop_table.hairshop_id'))
    user_id = Column(BigInteger, ForeignKey('user_table.user_id'))
    hair_recommendation = relationship("HairRecommendation", back_populates="hairshop_recommendations")
    hairshop = relationship("Hairshop", back_populates="hairshop_recommendations")
    user = relationship("User", back_populates="hairshop_recommendations") 