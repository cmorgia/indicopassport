from MaKaC.common.indexes import IndexesHolder
from MaKaC.registration import Registrant, PersonalDataForm


def updateValues(self, params):
        _mapFields = {
            'givenNames': 'firstName',
            'surNames': 'surname',
            'dayOfBirth': 'birthDate'
            #'documentNumber': 'passportId',
            #'expirationDate': 'passportExpire',
            #'countryCode': 'passportOrigin'
        }
        params = dict([(_mapFields[k],v) for (k,v) in params.iteritems() if k in _mapFields])

        gsList = self.getRegistrationForm().getGeneralSectionFormsList()
        pds = [i for i in gsList if isinstance(i,PersonalDataForm)]
        pd = pds[0]
        mg = self.getMiscellaneousGroupById(pd.getId())
        for f in pd.getSortedFields():
            if params.has_key(f.getPDField()):
                val = params[f.getPDField()]
                fakeParams = {f.getInput().getHTMLName(): val}
                f.getInput().setResponseValue(mg.getResponseItemById(f.getId()), fakeParams, self, mg, override=True, validate=False)


def updateFromPassportScan(self, passport_info):
        from datetime import datetime
        from iso3166 import countries

        passport_info['expirationDate'] = datetime.strptime(passport_info['expirationDate'], '%y%m%d')
        passport_info['dayOfBirth'] = datetime.strptime(passport_info['dayOfBirth'], '%y%m%d').strftime('%d/%m/%Y')

        passport_info['countryCode']=countries.get(passport_info['countryCode']).alpha2
        self.setPassportExpire(passport_info['expirationDate'])
        self.setPassportOrigin(passport_info['countryCode'])
        self.setPassportID(passport_info['documentNumber'])
        self.setFirstName(passport_info['givenNames'])
        self.setSurName(passport_info['surNames'])
        self.setBirthDate(passport_info['dayOfBirth'])

        if self.getAvatar():
            self.getAvatar().setName(passport_info['givenNames'])
            self.getAvatar().setSurName(passport_info['surNames'])
            self.getAvatar().setBirthDate(passport_info['dayOfBirth'])

        self.updateValues(passport_info)

Registrant.updateFromPassportScan = updateFromPassportScan
Registrant.updateValues = updateValues

def setPassportID(self,value,item=None):
    index = IndexesHolder().getById("registrants")
    index.unindex(self)

    self._passportID = value
    if item:
        self._passportID_item = item
    elif self._passportID_item:
        self._passportID_item.setValue(value)

    index.index(self)


def setPassportExpire(self,value,item=None):
    index = IndexesHolder().getById("registrants")
    index.unindex(self)

    self._passportExpire = value
    if item:
        self._passportExpire_item = item
    elif self._passportExpire_item:
        self._passportExpire_item.setValue(value)

    index.index(self)


def setPassportOrigin(self,value,item=None):
    index = IndexesHolder().getById("registrants")
    index.unindex(self)

    self._passportOrigin = value
    if item:
        self._passportOrigin_item = item
    elif self._passportOrigin_item:
        self._passportOrigin_item.setValue(value)

    index.index(self)


def getPassportID(self):
    return self._passportID


def getPassportExpire(self):
    return self._passportExpire


def getPassportOrigin(self):
    return self._passportOrigin


def getPassportInfo(self):
    try:
        return "{}-{}-{}".format(self.getPassportID(),self.getPassportExpire(),self.getPassportOrigin())
    except AttributeError:
        return None


Registrant.setPassportID = setPassportID
Registrant.setPassportExpire = setPassportExpire
Registrant.setPassportOrigin = setPassportOrigin
Registrant.getPassportID = getPassportID
Registrant.getPassportExpire = getPassportExpire
Registrant.getPassportOrigin = getPassportOrigin
Registrant.getPassportInfo = getPassportInfo