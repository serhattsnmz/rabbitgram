import  json
import  requests
from    datetime import datetime

import  rabbitgram.statics  as st
import  rabbitgram.functions as fn
from    rabbitgram.logger import Logger

class Rabbitgram:

    def __init__(self):
        self.session        = requests.Session()
        self.logger         = Logger().create_logger("base")
        self.login_status   = False

    def check_login_status(func):
        def wrapper(self, *args, **kwargs):
            if not self.login_status:
                self.logger.error("You must be login before getting user data!")
                return
            return func(self, *args, **kwargs)
        return wrapper

    def login(self, username, password):
        session     = self.session
        post_data   = {'username': username, 'password': password}

        try:
            with session.get(st.INSTAGRAM_HOMEPAGE) as res:
                token = fn.get_shared_data(res.text)['config']['csrf_token']
                session.headers.update({'X-CSRFToken': token})

            with session.post(st.INSTAGRAM_LOGIN_URL, post_data, allow_redirects=True) as login:
                token = next(c.value for c in login.cookies if c.name == 'csrftoken')
                session.headers.update({'X-CSRFToken': token})
                if not login.ok:
                    raise SystemError("Login error: check your connection!")
                data = json.loads(login.text)
                if not data.get('authenticated', False):
                    raise ValueError('Login error: check your username and password!')

            with session.get(st.INSTAGRAM_HOMEPAGE) as res:
                if res.text.find(username) == -1:
                    raise ValueError('Login error: check your username and password!')
            
            if "X-CSRFToken" in self.session.headers:
                self.logger.info("Login successful.")
                self.login_status = True

        except ValueError as exp:
            self.logger.error(exp)
        except Exception as exp:
            self.logger.exception("System Error!")

    @check_login_status
    def get_user_data(self, username):
        url = st.INSTAGRAM_USER_PAGE % username
        try:
            with self.session.get(url) as res:
                data = fn.get_shared_data(res.text)

                if 'ProfilePage' not in data['entry_data']:
                    raise ValueError()

                self.logger.info(f"User found: '{username}'")
                return data

        except (ValueError, AttributeError):
            self.logger.error(f"User not found: '{username}'")
        except Exception as exp:
            self.logger.exception("System Error!")

    @check_login_status
    def get_user_information(self, username):
        try:
            base_data   = self.get_user_data(username)
            user_data   = base_data['entry_data']['ProfilePage'][0]['graphql']['user']
            
            user_info   = {
                "user_id"               : user_data["id"],
                "is_private"            : user_data['is_private'],
                "followed_by_viewer"    : user_data['followed_by_viewer'],
                "blocked_by_viewer"     : user_data["blocked_by_viewer"],
                "biography"             : user_data["biography"],
                "profile_pic"           : user_data["profile_pic_url_hd"],
                "followed_by"           : user_data["edge_followed_by"]["count"],
                "follow"                : user_data["edge_follow"]["count"]
            }
            self.logger.debug("USER INFO   >>> \n" + json.dumps(user_info))
            self.logger.debug("COOKIE INFO >>> \n" + json.dumps(self.session.cookies.items()))
            
            if user_info['is_private'] and not user_info['followed_by_viewer']:
                raise RuntimeError(f"User '{username}' has private account.")
            
            self.logger.info(f"User information found: '{username}'")
            return user_info

        except (ValueError, RuntimeError) as exp:
            self.logger.error(exp)
        except Exception as exp:
            self.logger.exception("System Error!")
    
    @check_login_status
    def get_user_media(self, username):
        try:
            user_id         = self.get_user_information(username)["user_id"]
            end_cursor      = None
            media_list      = []

            while True:
                payload_json = {
                    "id"    : user_id,
                    "first" : 10,
                    "after" : end_cursor,
                }
                payload = json.dumps(payload_json, separators=(',', ':'))

                req     = self.session.get(st.INSTAGRAM_QUERY_URL.format(payload))
                data    = req.json()["data"]["user"]["edge_owner_to_timeline_media"]

                has_next_page   = data["page_info"]["has_next_page"]
                end_cursor      = data["page_info"]["end_cursor"]
                count           = len(data["edges"])

                for edge in data["edges"]:
                    node = edge["node"]

                    media = {
                        "id"            : node.get("id", None),
                        "media_like"    : node.get("edge_media_preview_like").get("edge_media_preview_like"),
                        "timestamp"     : node.get("taken_at_timestamp"),
                        "date"          : str(datetime.fromtimestamp(node.get("taken_at_timestamp"))),
                        "media_list"    : []
                    }

                    if "edge_sidecar_to_children" in node:
                        for inline in node["edge_sidecar_to_children"]["edges"]:
                            inline_node = inline["node"]
                            media["media_list"].append({
                                "id"            : inline_node.get("id", None),
                                "is_video"      : inline_node.get("is_video", None),
                                "video_url"     : inline_node.get("video_url", None),
                                "picture_url"   : inline_node.get("display_url"),
                                "dimensions"    : f'{inline_node["dimensions"]["width"]} x {inline_node["dimensions"]["height"]}'
                            })
                    else:
                        media["media_list"].append({
                            "id"            : node.get("id", None),
                            "is_video"      : node.get("is_video", None),
                            "video_url"     : node.get("video_url", None),
                            "picture_url"   : node.get("display_url"),
                            "dimensions"    : f'{node["dimensions"]["width"]} x {node["dimensions"]["height"]}'
                        })

                    media_list.append(media)

                if not has_next_page:
                    break
            
            self.logger.info(f"User all media parsed. (Total found media : {len(media_list)} )")
            return media_list

        except (ValueError, RuntimeError) as exp:
            self.logger.error(exp)
        except Exception as exp:
            self.logger.exception("System Error!")
        

        
