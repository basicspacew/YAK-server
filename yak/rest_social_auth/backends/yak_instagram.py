from instagram import InstagramAPI, helper
from social.backends.instagram import InstagramOAuth2
from yak.rest_social_auth.backends.base import ExtraDataAbstractMixin, ExtraActionsAbstractMixin


class Instagram(ExtraActionsAbstractMixin, ExtraDataAbstractMixin, InstagramOAuth2):
    @staticmethod
    def save_extra_data(response, user):
        if response['data']['bio']:
            user.about = response['data']['bio']

        user.save()

    @staticmethod
    def get_profile_image(strategy, details, response, uid, user, social, is_new=False, *args, **kwargs):
        image_url = response['data']['profile_picture']
        return image_url

    @staticmethod
    def post(user_social_auth, social_obj):
        return

    @staticmethod
    def get_friends(user_social_auth):
        return

    @staticmethod
    def get_posts(user_social_auth, **kwargs):
        api = InstagramAPI(access_token=user_social_auth.extra_data['access_token'])
        formatted_time = helper.datetime_to_timestamp(kwargs.get('last_updated_time', None))
        params = {
            'user_id': user_social_auth.uid,
            'min_timestamp': formatted_time
        }
        if 'limit' in kwargs:
            params.update({'count': kwargs['limit']})

        #TODO: Move the call to get the user's liked posts to a new function,
        # and call that function separately from the consumer.
        # This was coded for expediancy and low-cost.  It needs to be
        # changed if we decide we like this functionality (showing IG likes
        #   in the feed).
        recent_media, next_ = api.user_recent_media(**params)
        recent_likes = Instagram.get_likes(user_social_auth, **kwargs)
        return recent_media + recent_likes

    @staticmethod
    def get_likes(user_social_auth, **kwargs):
        api = InstagramAPI(access_token=user_social_auth.extra_data['access_token'])
        params = {
            'user_id': user_social_auth.uid,
        }
        if 'limit' in kwargs:
            params.update({'count': kwargs['limit']})

        recent_likes, next_ = api.user_liked_media(**params)
        return recent_likes
