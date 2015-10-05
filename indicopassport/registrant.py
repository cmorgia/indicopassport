from MaKaC.registration import Registrant, PersonalDataForm


def updateValues(self, params):
        _mapFields = {
            'givenNames': 'firstName',
            'surNames': 'surname',
            'dayOfBirth': 'birthDate',
            'documentNumber': 'passportId',
            'expirationDate': 'passportExpire',
            'countryCode': 'passportOrigin'
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

        passport_info['expirationDate'] = datetime.strptime(passport_info['expirationDate'], '%y%m%d').strftime('%d/%m/%Y')
        passport_info['dayOfBirth'] = datetime.strptime(passport_info['dayOfBirth'], '%y%m%d').strftime('%d/%m/%Y')

        passport_info['countryCode']=countries.get(passport_info['countryCode']).alpha2
        self.setPassportExpire(passport_info['expirationDate'])
        self.setPassportOrigin(passport_info['countryCode'])
        self.setPassportId(passport_info['documentNumber'])
        self.setFirstName(passport_info['givenNames'])
        self.setSurName(passport_info['surNames'])
        self.setBirthDate(passport_info['dayOfBirth'])

        if self.getAvatar():
            self.getAvatar().setPassportId(passport_info['documentNumber'])
            self.getAvatar().setPassportOrigin(passport_info['countryCode'])
            self.getAvatar().setPassportExpire(passport_info['expirationDate'])
            self.getAvatar().setName(passport_info['givenNames'])
            self.getAvatar().setSurName(passport_info['surNames'])
            self.getAvatar().setBirthDate(passport_info['dayOfBirth'])

        self.updateValues(passport_info)

Registrant.updateFromPassportScan = updateFromPassportScan
