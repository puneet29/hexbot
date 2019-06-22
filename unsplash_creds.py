client_id = '5ed0cb1155b5863f743841b836890a0731cf906dc41faafd6d2a62418780e2c8'
url = 'https://api.unsplash.com/photos/random'


def get_creds():
    """Returns the base url to get random photo and ACCESS key for application"""
    return(url, client_id)
