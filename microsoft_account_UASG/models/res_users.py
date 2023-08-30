# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from datetime import datetime
import json
import logging

import requests
from werkzeug import urls

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

TIMEOUT = 20

DEFAULT_MICROSOFT_AUTH_ENDPOINT = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
DEFAULT_MICROSOFT_TOKEN_ENDPOINT = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

RESOURCE_NOT_FOUND_STATUSES = (204, 404)

class User(models.Model):
    _inherit = 'res.users'

    groups = fields.Char()


    @api.model
    def _do_request(self, uri, params=None, headers=None, method='POST', preuri="https://graph.microsoft.com", timeout=TIMEOUT):
        """ Execute the request to Microsoft API. Return a tuple ('HTTP_CODE', 'HTTP_RESPONSE')
            :param uri : the url to contact
            :param params : dict or already encoded parameters for the request to make
            :param headers : headers of request
            :param method : the method to use to make the request
            :param preuri : pre url to prepend to param uri.
        """
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        _logger.debug("Uri: %s - Type : %s - Headers: %s - Params : %s !" % (uri, method, headers, params))

        ask_time = fields.Datetime.now()
        try:
            if method.upper() in ('GET', 'DELETE'):
                res = requests.request(method.lower(), preuri + uri, headers=headers, params=params, timeout=timeout)
            elif method.upper() in ('POST', 'PATCH', 'PUT'):
                res = requests.request(method.lower(), preuri + uri, data=params, headers=headers, timeout=timeout)
            else:
                raise Exception(_('Method not supported [%s] not in [GET, POST, PUT, PATCH or DELETE]!', method))
            res.raise_for_status()
            status = res.status_code

            if int(status) in RESOURCE_NOT_FOUND_STATUSES:
                response = False
            else:
                # Some answers return empty content
                response = res.content and res.json() or {}

            try:
                ask_time = datetime.strptime(res.headers.get('date'), "%a, %d %b %Y %H:%M:%S %Z")
            except:
                pass
        except requests.HTTPError as error:
            if error.response.status_code in RESOURCE_NOT_FOUND_STATUSES:
                status = error.response.status_code
                response = ""
            else:
                _logger.exception("Bad microsoft request : %s !", error.response.content)
                raise error

        return (status, response, ask_time)
    @api.model
    def _get_token_endpoint(self):
        return self.env["ir.config_parameter"].sudo().get_param('microsoft_account.token_endpoint', DEFAULT_MICROSOFT_TOKEN_ENDPOINT)

    
    @api.model
    def action_get_Microsoft_groups(self, authorize_code, service = False , method='POST', preuri="https://graph.microsoft.com"):
        """ Call Microsoft API to exchange authorization code against token, with POST request, to
            not be redirected.
        """
        get_param = self.env['ir.config_parameter'].sudo().get_param
        base_url = get_param('web.base.url', default='http://www.odoo.com?NoBaseUrl')
        client_id = '2e98a997-764b-41e6-976f-4451a215e063'
        client_secret = get_param('microsoft_%s_client_secret' % (service,), default=False)
        scope = 'offline_access openid Group.Read.All'

        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {
            'code': authorize_code,
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'scope': scope,
            'redirect_uri': 'app.uasg.ae' + '/microsoft_account/authentication'
        }
        uri = self._get_token_endpoint()
        res = requests.request(method.lower(), preuri , data=data, headers=headers, timeout=TIMEOUT)
             
        # error_msg = str(data)
        # raise self.env['res.config.settings'].get_config_warning(error_msg) from requests.exceptions.RequestException 
        raise self.env['res.config.settings'].get_config_warning(str(res))
        try:
            dummy, response, dummy = self._do_request(self._get_token_endpoint(), params=data, headers=headers, method='POST', preuri='')
            raise self.env['res.config.settings'].get_config_warning(str(response))

            access_token = response.get('access_token')
            refresh_token = response.get('refresh_token')
            ttl = response.get('expires_in')
            self.env['res.users'].search([('id','=',request.session.uid)]).write({'groups' : response})
            return access_token, refresh_token, ttl
        except requests.HTTPError:
            error_msg = _("Something went wrong during your token generation. Maybe your Authorization Code is invalid")
            raise self.env['res.config.settings'].get_config_warning(str(authorize_code))

