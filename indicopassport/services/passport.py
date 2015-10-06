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

from MaKaC.user import AvatarHolder
from indico.core.config import Config

from MaKaC.services.implementation.base import ServiceBase
from iso3166 import countries

class Redirect(ServiceBase):

    def _checkParams(self):
        ServiceBase._checkParams(self)
        self.firstName = self._params['First Name'] if 'First Name' in self._params else None
        self.lastName = self._params['Surname'] if 'Surname' in self._params else None
        self.birthDate = self._params['Birth Date'] if 'Birth Date' in self._params else None
        self.passportID = self._params['Passport ID'] if 'Passport ID' in self._params else None
        self.passportOrigin = self._params['Passport Origin'] if 'Passport Origin' in self._params else None
        self.passportOrigin = countries.get(self.passportOrigin).alpha2

    def _getAnswer(self):
        avs = AvatarHolder().match({'passport': self.passportOrigin+self.passportID})
        if len(avs)<1:
            return {"error":"Avatar not found"}

        av = avs[0]
        registrantList = av.getRegistrantList()
        registrantList = filter(lambda reg: reg.canEnterPremises()[0],registrantList)

        if len(registrantList)<1:
            return {"error":"Avatar found but no valid registration"}

        registrant = registrantList[0]

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
