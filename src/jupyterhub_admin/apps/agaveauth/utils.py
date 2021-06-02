from jupyterhub_admin.metadata import get_config_metadata, write_config_metadata


def add_admin_user(username):
    metadata = get_config_metadata()
    if 'admin_users' not in metadata['value']:
        metadata['value']['admin_users'] = [username]
    else:
        if username in metadata['value']['admin_users']:
            raise Exception('%s is already an admin user' % username)
        metadata['value']['admin_users'].append(username)
    write_config_metadata(metadata['value'])
    

def remove_admin_user(username):
    metadata = get_config_metadata()
    if 'admin_users' not in metadata['value'] or username not in metadata['value']['admin_users']:
        raise Exception('%s is not an admin user' % username)
    metadata['value']['admin_users'].remove(username)
    write_config_metadata(metadata['value'])