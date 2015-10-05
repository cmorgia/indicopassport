from MaKaC.conference import ConferenceHolder
from indico.web.http_api import HTTPAPIHook
from indico.web.http_api.hooks.event import EventBaseHook
from indico.web.http_api.util import get_query_parameter
import json

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii')
    return dict(map(ascii_encode, pair) for pair in data.items())

@HTTPAPIHook.register
class UpdatePassportHook(EventBaseHook):
    PREFIX = "api"
    RE = r'(?P<event>[\w\s]+)/registrant/(?P<registrant_id>[\w\s]+)/updatepassport'
    METHOD_NAME = 'api_update_passport'
    NO_CACHE = True
    COMMIT = True
    HTTP_POST = True

    def _getParams(self):
        super(UpdatePassportHook, self)._getParams()
        raw_passport_info = str(get_query_parameter(self._queryParams, ["passport_info"]))
        self._passport_info = json.loads(raw_passport_info,object_hook=ascii_encode_dict)
        self._secret = get_query_parameter(self._queryParams, ["secret"])
        registrant_id = self._pathParams["registrant_id"]
        self._conf = ConferenceHolder().getById(self._pathParams['event'])
        self._registrant = self._conf.getRegistrantById(registrant_id)

    def _hasAccess(self, aw):
        return (self._conf.canManageRegistration(aw.getUser()) or self._conf.canModify(aw)) \
            and self._secret == self._registrant.getCheckInUUID()

    def api_update_passport(self, aw):
        try:
            self._registrant.updateFromPassportScan(self._passport_info)
            return {"status": "true"}
        except Exception as e:
            return {"status": "false"}

