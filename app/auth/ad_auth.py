from ldap3 import Server, Connection, ALL, SUBTREE
from flask import current_app
import re

def authenticate_ad_user(username, password):
    """Authenticate a user against Active Directory"""
    try:
        # Create server object
        server = Server(current_app.config['AD_SERVER'], get_info=ALL)
        
        # Create connection for service account
        conn = Connection(
            server,
            user=f"{current_app.config['AD_USERNAME']}@{current_app.config['AD_DOMAIN']}",
            password=current_app.config['AD_PASSWORD'],
            auto_bind=True
        )
        
        # Search for the user
        search_filter = current_app.config['AD_USER_SEARCH_FILTER'].format(username)
        conn.search(
            current_app.config['AD_BASE_DN'],
            search_filter,
            search_scope=SUBTREE,
            attributes=['sAMAccountName', 'memberOf']
        )
        
        if not conn.entries:
            return None, "User not found in Active Directory"
            
        user_dn = conn.entries[0].entry_dn
        
        # Try to bind as the user to verify credentials
        user_conn = Connection(
            server,
            user=user_dn,
            password=password,
            auto_bind=True
        )
        user_conn.unbind()  # Close the connection after successful bind
        
        # Check if user is in technicians group
        is_technician = False
        if 'memberOf' in conn.entries[0]:
            for group in conn.entries[0]['memberOf']:
                if re.search(current_app.config['AD_GROUP_SEARCH_FILTER'], str(group)):
                    is_technician = True
                    break
        
        return {
            'username': username,
            'is_technician': is_technician
        }, None
        
    except Exception as e:
        return None, str(e) 