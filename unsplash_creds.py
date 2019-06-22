client_id = 'replace with your Access key'
url = 'https://api.unsplash.com/photos/random'


def get_creds():
    """Returns the base url to get random photo and ACCESS key for application"""
    return(url, client_id)
