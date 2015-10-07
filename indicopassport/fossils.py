from indico.core.fossils.registration import IRegFormRegistrantBasicFossil
from iso3166 import countries
from indico.util.fossilize import IFossil


class IPassportFossil(IFossil):
    def getPersonalData(self):
        """
        Render the Personal data Form
        """
    getPersonalData.produce = lambda x: x.getConference().getRegistrationForm().getPersonalData().getRegistrantValues(x)

    def getPassportID(self):
        """
        Get the passport number
        """
    getPassportID.name = "passportId"


    def getPassportExpire(self):
        """
        Get the passport expiration date
        """
    getPassportExpire.produce = lambda x: x.getPassportExpire().date()


    def getPassportOrigin(self):
        """
        Get the passport issuing country
        """
    getPassportOrigin.produce = lambda x: countries.get(x.getPassportOrigin()).name


try:
    from indicopicture import IPictureFossil
    class IRegFormRegistrantPassportFossil(IRegFormRegistrantBasicFossil,IPassportFossil,IPictureFossil):
        pass
except:
    class IRegFormRegistrantPassportFossil(IRegFormRegistrantBasicFossil,IPassportFossil):
        pass
