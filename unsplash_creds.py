client_id = 'update with your own Access Key'
url = 'https://api.unsplash.com/photos/random'


def get_creds():
    """Returns the base url to get random photo and ACCESS key for application"""
    return(url, client_id)
