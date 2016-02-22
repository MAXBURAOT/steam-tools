#!/usr/bin/env python
#
# Lara Maia <dev@lara.click> 2015
#
# The Steam Tools is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# The Steam Tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#

from time import sleep
from logging import getLogger

import requests

agent = {'user-agent': 'unknown/0.0.0'}
logger = getLogger('root')

def tryConnect(url, cookies="", data=False):
    while True:
        try:
            if data:
                response = requests.post(url, data=data, cookies=cookies, headers=agent, timeout=10)
                response.raise_for_status()
                return response
            else:
                response = requests.get(url, cookies=cookies, headers=agent, timeout=10)
                response.raise_for_status()
                # Check if the cookies remains valid.
                if str(response.content).find('https://steamcommunity.com/login/home/?goto=id') != -1:
                    raise requests.exceptions.TooManyRedirects
                return response
        except requests.exceptions.TooManyRedirects:
            logger.critical("Too many redirects. Please, check your configuration.")
            logger.critical("(Invalid or expired cookie?)")
            exit(1)
        except(requests.exceptions.HTTPError, requests.exceptions.RequestException):
            logger.error("The connection is refused or fails. Trying again...")
            sleep(3)

    logger.critical("Cannot access the internet! Please, check your internet connection.")
    exit(1)