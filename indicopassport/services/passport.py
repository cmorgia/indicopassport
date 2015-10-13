# This file is part of Indico.
# Copyright (C) 2002 - 2015 European Organization for Nuclear Research (CERN).
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# Indico is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Indico; if not, see <http://www.gnu.org/licenses/>.
from MaKaC.common.indexes import IndexesHolder

from MaKaC.user import AvatarHolder
from indico.core.config import Config

from MaKaC.services.implementation.base import ServiceBase
from iso3166 import countries

class Redirect(ServiceBase):

    def _checkParams(self):
        ServiceBase._checkParams(self)
        self.passportID = self._params['passportID'] if 'passportID' in self._params else None
        self.passportExpire = self._params['passportExpire'] if 'passportExpire' in self._params else None
        self.passportOrigin = self._params['passportOrigin'] if 'passportOrigin' in self._params else None
        self.passportOrigin = countries.get(self.passportOrigin).alpha2

    def _getAnswer(self):
        idx = IndexesHolder().getById("registrants")
        registrant = idx.match(self.passportID,self.passportExpire,self.passportOrigin)
        if not registrant:
            return {"error":"Registrant not found"}

        url = '{}/event/{}/manage/registration/users/{}/misc/0'.format(
            Config.getInstance().getBaseURL(),
            registrant.getConference().getId(),
            registrant.getId()
        )
        response = {
            'location': url
        }

        return response


methodMap = {
    "redirect": Redirect
}
