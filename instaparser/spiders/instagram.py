import json
import re
from copy import deepcopy
from urllib.parse import urlencode
from scrapy.http import FormRequest, HtmlResponse
from scrapy.spiders import Spider
from instaparser.items import InstaparserItem


class InstagramSpider(Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = '9085088121'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1631736455:AfdQAHpPJZuxWrEx+SJLY9Bd6DyIPCVMjr/0U1UgHX+Gmr5sY75D6BpFc3yoLH0Q6FF60nnZhMOwZ3qeiSlMgMhOsOYPwc5f7o6ie3o5cG+oaMptbLouO1cHQglCmu7seeEY4Ym6h0xL/jKUAcQdPsE='
    parse_user = ['ekaterinaermolenko198502', 'aleksandra_veis']

    def parse(self, response:HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login,
                      'enc_password': self.inst_pwd},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response:HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            for name_idx in range(len(self.parse_user)):
                yield response.follow(
                    f'/{self.parse_user[name_idx]}',
                    callback=self.user_parse,
                    cb_kwargs={'username': self.parse_user[name_idx]}
                )

    def user_parse(self, response:HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        max_id = 12
        followers_url = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&max_id={max_id}&search_surface=follow_list_page'
        yield response.follow(
            followers_url,
            callback=self.follower_parse,
            cb_kwargs={'username': username,
                        'user_id': user_id,
                        'max_id': max_id},
            headers={'User-Agent': 'Instagram 155.0.0.37.107'}
        )

    def follower_parse(self, response:HtmlResponse, username, user_id, max_id):
        j_data = response.json()
        if j_data.get('next_max_id'):
            max_id += 12
            followers_url = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&max_id={max_id}&search_surface=follow_list_page'
            yield response.follow(
                followers_url,
                callback=self.follower_parse,
                cb_kwargs={'username': username,
                            'user_id': user_id,
                            'max_id': max_id},
                headers={'User-Agent': 'Instagram 155.0.0.37.107'}
            )

        followers_array = j_data.get('users')
        for follower in followers_array:
            item = InstaparserItem(
                username=username,
                user_id=user_id,
                name=follower.get("full_name"),
                identifier=follower.get("pk"),
                photo=follower.get("profile_pic_url")
            )
            yield item

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
