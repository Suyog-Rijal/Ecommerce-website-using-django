from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
import requests


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        User = get_user_model()
        email = sociallogin.account.extra_data.get('email')

        try:
            existing_user = User.objects.get(email=email)
            return existing_user

        except User.DoesNotExist:
            user = super().save_user(request, sociallogin, form)

            if sociallogin.account.provider == 'google':
                try:
                    extra_data = sociallogin.account.extra_data
                    user.firstname = extra_data.get('given_name', user.first_name)
                    user.lastname = extra_data.get('family_name', user.last_name)
                    user.email = extra_data.get('email', user.email)
                    user.gender = extra_data.get('gender', user.gender)
                    user.is_verified = True

                    picture_url = extra_data.get('picture')
                    if picture_url:
                        response = requests.get(picture_url)
                        if response.status_code == 200:
                            user.profile_pic.save(f"{user.email}_profile.jpg",
                                                  ContentFile(response.content),
                                                  save=True)

                    user.save()
                except Exception as e:
                    print(e)

            return user