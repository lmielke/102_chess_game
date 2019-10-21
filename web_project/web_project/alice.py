
'''
    this class is a temporary adapter to alice
'''
from PIL import Image


class alice():
    def __init__(self):
        pass

    def do_shorten_text(self, posts, max_len=100, nr_sentences=2):
        '''
            takes a text creates a preview i.e. depending on the length
            shortens the text to the specified number of sentences
        '''
        for obj in posts:
            obj.readmore = 'weiterlesen'
            if len(obj.content) > max_len:
                obj.content = '.'.join(obj.content.split('.')[:nr_sentences]) + '.'
                obj.more = True
            else:
                obj.more = False
        # posts = {'values': posts}
        # print(f'---> posts: {posts}')
        # print('---> posts values:'.format(posts['values']))
        return posts

    def do_define_themes(self):
        '''
            takes a text creates a preview i.e. depending on the length
            shortens the text to the specified number of sentences
        '''
        themes = {
            'p_title': 'Home',
            'themes': [{
                'theme': '0',
                'do_button': 'enter',
                'title': 'Politik',
                'description': 'Bridge imaging and maintenance process and controll.',
                'image': '/media/card_pics/img_bridgecard01.jpg'
            },

                {
                'theme': '0',
                'do_button': 'enter',
                'title': 'Tunnnels',
                'description': 'Tunnnel imaging and maintenance process and controll.',
                'image': '/media/card_pics/img_tunnelcard01.jpg'
            },
                {
                'theme': '0',
                'do_button': 'enter',
                'title': 'Buildings',
                'description': 'Building imaging and maintenance process and controll.',
                'image': '/media/card_pics/img_buildingcard01.jpg'
            },
                {
                'theme': '0',
                'do_button': 'enter',
                'title': 'Parks',
                'description': 'Park imaging and maintenance process and controll.',
                'image': '/media/card_pics/img_parkscard01.jpg'
            },
                {
                'theme': '0',
                'do_button': 'enter',
                'title': 'Railways',
                'description': 'Railway imaging and maintenance process and controll.',
                'image': '/media/card_pics/img_railscard01.jpg'
            },
                {
                'theme': '0',
                'do_button': 'enter',
                'title': 'Industrial',
                'description': 'Industrial facility imaging and maintenance process and controll.',
                'image': '/media/card_pics/img_industrialcard01.jpg'
            },

            ]}
        return themes
