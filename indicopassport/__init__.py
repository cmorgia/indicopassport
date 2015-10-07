# coding=utf-8

from webassets import Bundle
import os
from MaKaC.common.indexes import Index, IndexesHolder
from MaKaC.conference import ConferenceHolder
from indico.core.db import DBMgr

from indico.core.plugins import IndicoPlugin, IndicoPluginBlueprint
from indico.core import signals
from MaKaC.registration import GeneralField, GeneralSectionForm, TextInput, DateInput, CountryInput
from MaKaC.webinterface.pages.registrationForm import WPConfModifRegFormPreview, \
    WPRegistrationFormModify, WPRegistrationFormDisplay
from MaKaC.services.interface.rpc.handlers import importModule, endpointMap
from indico.web.http_api.hooks.registration import RegistrantFetcher
import indicopassport.registrant
from indicopassport.fossils import IRegFormRegistrantPassportFossil
import indicopassport.http_api.hooks

blueprint = IndicoPluginBlueprint('indicopassport', __name__)


def addIndex(self,name,index):
    if not name in self._IndexesHolder__allowedIdxs:
        DBMgr.getInstance().startRequest()
        self._IndexesHolder__allowedIdxs.append(name)
        self._getIdx()["registrants"] = RegistrantIndex()
        DBMgr.getInstance().commit()


class IndicoPassportPlugin(IndicoPlugin):
    """Indico Passport Plugin

    """
    configurable = False

    def init(self):
        super(IndicoPassportPlugin, self).init()

        # Inject the JS and CSS, should be in limited pages
        self.inject_js('indicopassport_js', WPRegistrationFormDisplay)
        self.inject_js('indicopassport_js', WPRegistrationFormModify)
        self.inject_js('indicopassport_js', WPConfModifRegFormPreview)

        self.connect(signals.event.created,self.conf_created)

        endpointMap["passport"]=importModule("indicopassport.services.passport")
        IndexesHolder.addIndex = addIndex
        IndexesHolder().addIndex("registrants",RegistrantIndex())

        RegistrantFetcher.DETAIL_INTERFACES["passport"]= IRegFormRegistrantPassportFossil

    def register_assets(self):
        self.register_js_bundle('indicopassport_js', 'js/indicopassport.js')
        self.register_jars_bundle('indico_jars', 'jars/swipeapplet.jar','jars/mmmreader.jar')

    def register_jars_bundle(self, name, *files):
        import shutil
        bundle = Bundle(*files, output='jars')
        dirName = bundle.resolve_output(self.assets)
        if os.path.isdir(dirName):
            shutil.rmtree(dirName)
        os.makedirs(dirName)
        contents = bundle.resolve_contents(self.assets)

        for (orig,content) in contents:
            shutil.copy2(content,dirName)

    def get_blueprints(self):
        return blueprint

    @signals.app_created.connect
    def _config(app, **kwargs):
        pass

    def conf_created(self,conf,parent):
        _sectionHeader = dict()
        _sectionHeader["title"] = "Passport"
        _sectionHeader["description"] = "Passport"
        regForm = conf.getRegistrationForm()
        pos = next((i for i, f in enumerate(regForm.getSortedForms()) if not f.isEnabled()), None)
        section = GeneralSectionForm(regForm, data=_sectionHeader)
        section.directives = "nd-passport-section"

        fields = [
            {
                "disabled": False,
                "caption": "Passport ID",
                "mandatory": True
            },
            {
                "input": "date",
                "dateFormat": "%d/%m/%Y",
                "disabled": False,
                "caption": "Passport Expire",
                "mandatory": True
            },
            {
                "input": "country",
                "disabled": False,
                "caption": "Passport Origin",
                "mandatory": True
            }
        ]

        for item in fields:
            field = GeneralField(section, data=item)
            pos = next((i for i, f in enumerate(section.getSortedFields()) if f.isDisabled()), None)
            section.addToSortedFields(field, i=pos)

        regForm.addGeneralSectionForm(section, preserveTitle=True, )

        print "Section ID is %s" % section.getId()

class RegistrantIndex(Index):
    _name = "registrants"

    def getLocator(self,registrant):
        return {
            'confId': registrant.getConference().getId(),
            'registrantId': registrant.getId()
        }

    def index(self, registrant):
        passInfo = registrant.getPassportInfo()
        if passInfo:
            locator = self.getLocator(registrant)
            self._addItem(passInfo, locator)

    def unindex(self, registrant):
        passInfo = registrant.getPassportInfo()
        if passInfo:
            locator = self.getLocator(registrant)
            self._withdrawItem(passInfo, locator)

    def match(self, passportID, passportExpire, passportOrigin, cs=0, exact=0, accent_sensitive=True):
        """this match is an approximative case insensitive match"""

        passportInfo = "{}-{}-{}".format(passportID,passportExpire,passportOrigin)
        locator = self._match(passportInfo, cs, exact)
        registrant = ConferenceHolder().getById(locator['confId']).getRegistrantById(locator['registrantId'])
        return registrant

def decorateSetValue(fn):
    def new_funct(*args, **kwargs):
        ret = fn(*args, **kwargs)
        self = args[0]
        item = args[1]
        params = args[2]
        registrant = args[3]
        caption = item.getGeneralField().getCaption()
        value = item.getValue()
        if caption=='Passport ID':
            registrant.setPassportID(value,item)
        elif caption=='Passport Origin':
            registrant.setPassportOrigin(value,item)
        elif caption=='Passport Expire':
            registrant.setPassportExpire(value,item)
        return ret
    return new_funct

TextInput._setResponseValue = decorateSetValue(TextInput._setResponseValue)
DateInput._setResponseValue = decorateSetValue(DateInput._setResponseValue)
CountryInput._setResponseValue = decorateSetValue(CountryInput._setResponseValue)