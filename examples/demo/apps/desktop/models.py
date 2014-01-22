#coding=utf-8

from uliweb.orm import *

class LoginUser(Model):
    name = Field(CHAR, max_length=255)
    site = Field(CHAR, max_length=100)
    uid = Field(CHAR, max_length=100)
    avatar = Field(CHAR, max_length=255)
    
