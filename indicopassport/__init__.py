# coding=utf-8

from webassets import Bundle
import os

from indico.core.plugins import IndicoPlugin, IndicoPluginBlueprint
from indico.core import signals
from MaKaC.registration import GeneralField, GeneralSectionForm
from MaKaC.webinterface.pages.registrationForm import WPConfModifRegFormPreview, \
    WPRegistrationFormModify, WPRegistrationFormDisplay
from MaKaC.services.interface.rpc.handlers import importModule, endpointMap

blueprint = IndicoPluginBlueprint('indicopassport', __name__)


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
        print "Done"
        #bundle.build(self.assets,force=False,disable_cache=True)
        #self.assets.register(name, bundle)

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

