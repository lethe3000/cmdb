#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header


class AuthOrAnonymousAuthentication(authentication.TokenAuthentication):
    """
    未提供token header则返回匿名用户
    """
    keyword = "Bearer"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return AnonymousUser(), None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
