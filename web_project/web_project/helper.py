import os, re
from django.conf import settings

class MyHelper():
    def __init__(self):
        pass

    def scs_url(self, cut=None, repl=None):
        sucess_url_para = list()
        print(f'constructing success url: {self.tgt_url_args}')
        for para, pk in self.tgt_url_args.items():
            if type(para) == int: sucess_url_para.append(str(pk))
            if type(para) == str: sucess_url_para.append(str(para)+'='+str(pk))
        success_url = '/'+'/'.join(sucess_url_para)
        if cut:
             success_url = success_url[:success_url.find(cut)]
        if repl:
            replaces = {'SUV01': ('/signups/signup/', '/blog/articles/')}
            success_url = success_url.replace(replaces[repl][0], replaces[repl][1])
        print(f'constructing success url: {success_url}')
        return success_url

    def parse_tgt_url(self, url):
        """
            splits in url by / and parses its arguments
            then outputs a dictionary of {argument: value} combinations
            if url argument has no value then, enumerate creates a int key
            INPUT  example: 'black-pelican.rocks/articles/Theme=0/Frame=0/'
            OUTPUT example: {0: 'black-pelican.rocks', 1: 'articles', 'Theme': 0, 'Frame': 0}
        """
        try:
            self.tgt_url_args = {}
            url_args = url.strip('/').split('/')
            arg_pattern = re.compile(r'([A-Z]\w+)=(\d+)')
            for idx, url_arg in enumerate(url_args):
                arg_match = arg_pattern.findall(url_arg)
                if arg_match:
                    self.tgt_url_args[arg_match[0][0]] = int(arg_match[0][1])
                else:
                    self.tgt_url_args[idx] = url_arg
            self.tgt_url_args['Frame'] = self.tgt_url_args.get('Frame', 0)
            print(f'\nparse_tgt_url in with: {url}, out with: {self.tgt_url_args}')
        except Exception as e:
            print(e)
        return self.tgt_url_args

    def get_context_metadata(self, view_args, request=None):
        context_meta = {}
        self.request = request if request else self.request
        context_meta['host_name'] = self.request.META['HTTP_HOST']
        context_meta['frame'] =  str(self.tgt_url_args.get('Frame', '0'))
        context_meta['template_name'] = view_args['template_name']
        context_meta['extension'] = view_args['extensions'][self.tgt_url_args['Frame']]
        context_meta['article_id'] = self.tgt_url_args.get('Article', '0')
        context_meta['theme'] = str(self.tgt_url_args.get('Theme', '0'))
        context_meta['step'] = str(self.tgt_url_args.get('Step', '0'))
        context_meta['page_title'] = view_args['page_title']
        context_meta['CHPID'] = settings.CHPID
        # web_sys changes web behavior (i.e. display page params)
        context_meta['web_sys'] = gbl_web_sys
        context_meta['web_sys_fix'] = os.environ.get('WEB_SYS_FIX', 'False')
        # web_mode changes web content displayed (i.e. texts articles)
        context_meta['web_mode'] = gbl_web_mode
        context_meta['web_mode_fix'] = os.environ.get('WEB_MODE_FIX', 'False')
        context_meta.update(MyHelper.get_web_modes(self,
                                                    context_meta['web_mode']))
        # web_style changes the css document
        print("in context_metadata with: {}".format(self.request.META['HTTP_HOST']))
        context_meta.update(MyHelper.get_web_styles(self,
                                                self.request.META['HTTP_HOST'],
                                                context_meta['frame']))
        print(f'\nget_context_metadate out with: {context_meta}')
        return context_meta

    def get_web_modes(self, web_mode):
        web_mode_dict = {'black-pelican.rocks':
            {
            'jumbo_head': 'Play hard',
            'jumbo_text': 'And leave nothing in, that could also be taken out!',
            'nav_1': 'THEMEN',
            'nav_2': 'Beiträge',
            'nav_3': 'Diskussion',
            'nav_4': '',
            'nav_5': 'Suchen',
            'nav_6': 'Neuer Artikel',
            'nav_7': 'Logout',
            'nav_8': 'Login',
            'nav_9': 'Anmelden',
            'button_1': 'Neu',
            'button_2': 'Kommentar Erstellen',
            'button_3': 'Zurück',
            'button_4': 'Ändern',
            'button_5': 'Löschen',
            'button_6': 'Zur Anmeldung',
            'button_7': 'Anmeldung Löschen!',
            'page_title_0': 'AI Maintenance',
            'page_title_1': 'Artikel Schreiben',
            'page_title_2': 'Artikel Übersicht',
            'page_title_3': 'Kommentar erstellen',
            'page_title_4': 'Unternehmen',
            'message_1': 'Sind Sie sicher, dass Sie den Artikel jetzt löschen wollen?',
            'message_2': 'Zum Kommentieren klicken Sie auf einen Artikel',
            'message_3': 'Schreiben sie uns!',
            'message_4': 'wird entgültig gelöscht !',
            'message_5': 'Kommentare zum Artikel',
            'message_6': 'Zm Kommentieren klicken Sie einen Artikel.',
            'form_ph_0': 'Thema eingeben...',
            'form_ph_1': 'Titel eingeben...',
            'form_ph_2': 'Text eingeben...',
            'form_lbl_0': 'Thema',
            'form_lbl_1': 'Titel',
            'form_lbl_2': 'localhost',
            'form_lbl_3': 'na',
            'form_lbl_4': 'na',
            'form_lbl_5': 'na',
            'form_lbl_6': 'na',
            'form_help_0': '',
            'form_help_1': 'Fassen Sie sich kurz!',
            'form_help_2': 'Achten Sie auf eine angemessene Sprechweise!',
            'form_btn_text1': 'Speichern',
            'user_views_msg_1': 'Sehr gut! Jetzt noch ein letzter Schritt!',
            'user_views_msg_2': 'Phuu, das hat gedauert. Jetzt kann`s losgehen',
            'user_views_msg_3': 'Anmeldung fehlgeschlagen',
            },
                    'wutmensch.de':
            {
            'jumbo_head': 'Don`t let it just happen',
            'jumbo_text': 'This is my view of the world',
            'nav_1': 'THEMEN',
            'nav_2': 'Artikel',
            'nav_3': 'Blog',
            'nav_4': '',
            'nav_5': 'Suchen',
            'nav_6': 'Neuer Artikel',
            'nav_7': 'Logout',
            'nav_8': 'Login',
            'nav_9': 'Anmelden',
            'button_1': 'Neu',
            'button_2': 'Kommentar Erstellen',
            'button_3': 'Zurück',
            'button_4': 'Ändern',
            'button_5': 'Löschen',
            'button_6': 'Anmeldung!',
            'button_7': 'Anmeldung Löschen!',
            'page_title_0': 'Themen',
            'page_title_1': 'Artikel Schreiben',
            'page_title_2': 'Artikel Übersicht',
            'page_title_3': 'Kommentar erstellen',
            'page_title_4': 'ups',
            'message_1': 'Sind Sie sicher, dass Sie den Artikel jetzt löschen wollen?',
            'message_2': 'Zum Kommentieren klicken Sie auf einen Artikel',
            'message_3': 'Sind Sie auch ein Wutmensch? Schreiben sie uns!',
            'message_4': 'wird entgültig gelöscht !',
            'message_5': 'Kommentare zum Artikel',
            'message_6': 'Zm Kommentieren klicken Sie einen Artikel.',
            'form_ph_0': 'Thema eingeben...',
            'form_ph_1': 'Titel eingeben...',
            'form_ph_2': 'Text eingeben...',
            'form_lbl_0': 'Thema',
            'form_lbl_1': 'Titel',
            'form_lbl_2': 'travel',
            'form_lbl_3': 'na',
            'form_lbl_4': 'na',
            'form_lbl_5': 'na',
            'form_lbl_6': 'na',
            'form_help_0': '',
            'form_help_1': 'Fassen Sie sich bitte kurz!',
            'form_help_2': 'Achten Sie auf eine angemessene Sprechweise!',
            'form_btn_text1': 'Speichern',
            'user_views_msg_1': 'Sehr gut! Jetzt noch ein letzter Schritt!',
            'user_views_msg_2': 'Phuu, das hat gedauert. Jetzt kann`s losgehen',
            'user_views_msg_3': 'Anmeldung fehlgeschlagen',
            },

                    'localhost:8000':
            {
            'jumbo_head': 'play hard',
            'jumbo_text': 'Perfection is not achived, if there is nothing more to put in.  But nothing left to take out!',
            'nav_1': 'THEMEN',
            'nav_2': 'Experten',
            'nav_3': 'Diskussion',
            'nav_4': '',
            'nav_5': 'Suchen',
            'nav_6': 'Neuer Artikel',
            'nav_7': 'Logout',
            'nav_8': 'Login',
            'nav_9': 'Anmelden',
            'button_1': 'Neu',
            'button_2': 'Kommentar Erstellen',
            'button_3': 'Zurück',
            'button_4': 'Ändern',
            'button_5': 'Löschen',
            'button_6': 'Anmeldung!',
            'button_7': 'Anmeldung Löschen!',
            'page_title_0': 'AI Maintenance',
            'page_title_1': 'Anmeldung',
            'page_title_2': 'Artikel Übersicht',
            'page_title_3': 'Kommentar erstellen',
            'page_title_4': 'Unternehmen',
            'message_1': 'Sind Sie sicher, dass Sie den Artikel jetzt löschen wollen?',
            'message_2': 'Zum Kommentieren klicken Sie auf einen Artikel',
            'message_3': 'Schreiben sie uns!',
            'message_4': 'wird entgültig gelöscht !',
            'message_5': 'Kommentare zum Artikel',
            'message_6': 'Um sich anzumelden klicken sie auf den Header der Veranstaltung!',
            'form_ph_0': 'Ein bis Zwei',
            'form_ph_1': 'Titel eingeben...',
            'form_ph_2': 'Text eingeben...',
            'form_lbl_0': 'Thema',
            'form_lbl_1': 'Straße',
            'form_lbl_2': 'Hausnummer',
            'form_lbl_3': 'Postleitzahl',
            'form_lbl_4': 'z.B. 80800',
            'form_lbl_5': 'Stadt',
            'form_lbl_6': 'Berlin',
            'form_help_0': '',
            'form_help_1': 'z.B.',
            'form_help_2': 'Achten Sie auf eine angemessene Sprechweise!',
            'form_btn_text1': 'Speichern',
            'user_views_msg_1': 'Sehr gut! Jetzt noch ein letzter Schritt!',
            'user_views_msg_2': 'Phuu, das hat gedauert. Jetzt kann`s losgehen',
            'user_views_msg_3': 'Anmeldung fehlgeschlagen',
            }
                        }
        print("this is web_mode: {}".format(web_mode))
        web_mode_params = web_mode_dict.get(web_mode, web_mode_dict.get('black-pelican.rocks', False))
        return web_mode_params

    def set_web_mode(self, hostname="localhost:8000"):
        """
            already run in auth_middleware to dynamically set web_mode
            web_mode is set to change content of the site (i.e. texts, articles)
            selects db fields depending on web_mode field
        """
        # default mode can be overwritten by fixted mode
        global gbl_web_mode
        if os.environ.get('WEB_MODE_FIX', 'False') == 'False':
            gbl_web_mode = hostname
            os.environ['WEB_MODE'] = gbl_web_mode
        else:
            gbl_web_mode = os.environ['WEB_MODE_FIX']
            os.environ['WEB_MODE'] = gbl_web_mode

    def get_web_styles(self, web_style='localhost:8000', frame='0'):
        """
            define style elements for each web_style
            other webstyles select specific css
        """
        web_styles = {'localhost:8000':
            {
            'form_btn_style1': 'btn-outline-info',
            'form_btn_style2': 'btn-outline-danger',
            '0': 'blog/main2.css',
            '1': 'blog/ifmain2.css',
            },

                        'black-pelican.rocks':
            {
            'form_btn_style1': 'btn-outline-success',
            'form_btn_style2': 'btn-outline-success',
            '0': 'blog/main.css',
            '1': 'blog/ifmain.css',
            },

                        'wutmensch.de':
            {
            'form_btn_style1': 'btn-outline-info',
            'form_btn_style2': 'btn-outline-danger',
            '0': 'blog/main2.css',
            '1': 'blog/ifmain2.css',
            }
                        }
        print("this is webstyle: {}".format(web_style))
        web_style_params = web_styles.get(web_style, web_styles['black-pelican.rocks'])
        web_style_params['css_style'] = web_style_params.pop(frame)
        return web_style_params

    def set_web_sys(self, hostname="black-pelican.rocks"):
        """
            gets systam parameters for current system (dev, test, prod)
            relevant for testing (i.e. in dev and test mode additional parameters are displayed)
        """
        global gbl_web_sys
        web_systems = {"wutmensch.de": "prod", "black-pelican.rocks": "prod", "localhost:8000": "dev"}
        if not os.environ.get('WEB_SYS_FIX', None):
            gbl_web_sys = web_systems.get(hostname, "prod")
            os.environ['WEB_SYS'] = gbl_web_sys
        else:
            gbl_web_sys = os.environ['WEB_SYS_FIX']
            os.environ['WEB_SYS'] = gbl_web_sys
        return gbl_web_sys

    def get_auth_actions(self):
        """
            provides additional parameters for authorisations
        """
        auth_actions = ['add', 'change', 'delete', 'view']
        return auth_actions

    def send_mail_to_user(self, request, subject, template, form, obj, event_name):
        from django.contrib.sites.shortcuts import get_current_site
        from django.core.mail import EmailMessage
        from django.template.loader import render_to_string
        current_site = get_current_site(request)
        connection = self.get_email_connection()
        message = render_to_string(template, {
            'event_name': event_name,
            'user': request.user,
            'domain': "https://" + request.META['HTTP_HOST'],
            'user_phone' : form.cleaned_data.get('phone'),
            'user_email' : form.cleaned_data.get('email'),
            'obj' : obj,
                    })
        from_email = settings.EMAIL_HOST_USER
        print(from_email,"email here")
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [to_email], connection=connection)
        email.send()
        return "checkmail"

    def get_email_connection(self):
        from django.core.mail import get_connection
        from django.conf import settings
        use_tls = True
        use_ssl = False
        fail_silently=False
        connection = get_connection(host=settings.EMAIL_HOST,
                            port=settings.EMAIL_PORT,
                            username=settings.EMAIL_HOST_USER,
                            password=settings.EMAIL_HOST_PASSWORD,
                            use_tls=use_tls,
                            use_ssl=use_ssl,
                            fail_silently=fail_silently)
        return connection

if __name__ == '__main__':
    helper = MyHelper()
    helper = helper.get_web_styles('0')
    print(helper)

