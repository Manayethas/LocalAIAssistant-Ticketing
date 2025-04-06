import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///../instance/tickets.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AD Settings
    AD_SERVER = os.getenv('AD_SERVER', 'ldap://your-ad-server:389')
    AD_DOMAIN = os.getenv('AD_DOMAIN', 'yourdomain.com')
    AD_BASE_DN = os.getenv('AD_BASE_DN', 'DC=yourdomain,DC=com')
    AD_USER_SEARCH_FILTER = os.getenv('AD_USER_SEARCH_FILTER', '(sAMAccountName={})')
    AD_GROUP_SEARCH_FILTER = os.getenv('AD_GROUP_SEARCH_FILTER', '(memberOf=CN=Technicians,OU=Groups,DC=yourdomain,DC=com)')
    AD_USERNAME = os.getenv('AD_USERNAME', 'service_account')
    AD_PASSWORD = os.getenv('AD_PASSWORD', 'service_account_password') 