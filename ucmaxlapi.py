import sys
import json
import dicttoxml
import xmltodict
import requests

from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class RawAxl:
    """ A Very Basic AXL implementation

    The class will create the xml for the soap payload 'from scratch', using dicttoxml to create the calls and
    their arguments.
    The execute function will take the method name to be called, together with a dict of the arguments. The call
    will be executed and the returned xml will be returned as a dict using xmltodict
    """
    def __init__(self, username, password, server=None, version="10.5"):
        """ Initiate the AXL Client

        this will set the necessary user, passwd, server and version

        :param username (str):
        :param password (str):
        :param server (str): server name or IP where the AXL service is running
        :param version (str): version of CUCM, defaults to 10.5
        """
        self.username = username
        self.password = password
        self.server = server
        self.version = version

    def execute(self, call, args):
        # create the XML
        envelope = "<?xml version='1.0' encoding='utf8'?>"
        envelope += '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" ' \
                    'xmlns:ns1="http://www.cisco.com/AXL/API/{}">'.format(self.version)
        envelope += '<ns0:Header/>'
        envelope += '<ns0:Body>'
        envelope += '<ns1:{0} sequence="">'.format(call)

        # arguments from dict to xml
        envelope += dicttoxml.dicttoxml(args, attr_type=False, root=False).decode('utf-8')

        # closing tags
        envelope += '</ns1:{0}>'.format(call)
        envelope += '</ns0:Body>'
        envelope += '</ns0:Envelope>'

        # do the request (disable warnings)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        url = 'https://{}:8443/axl/'.format(self.server)
        r = requests.post(url, data=envelope,
                          auth=HTTPBasicAuth(self.username, self.password), verify=False)

        # into dict and return relevant parts
        ns0 = 'http://schemas.xmlsoap.org/soap/envelope/'
        ns1 = 'http://www.cisco.com/AXL/API/{}'.format(self.version)
        r_dict = xmltodict.parse(r.text, process_namespaces=True)
        body = r_dict['{}:Envelope'.format(ns0)]['{}:Body'.format(ns0)]

        if '{0}:{1}Response'.format(ns1, call).format(call) in body:
            return body['{0}:{1}Response'.format(ns1, call)]
        elif '{}:Fault'.format(ns0) in body:
            # clean it up a bit
            return {'fault': body['{}:Fault'.format(ns0)]}
        else:
            return body


if __name__ == '__main__':
    """
    test cases, goal is to give it a dict and get a dict back
    """
    axl = RawAxl(*sys.argv[1:])

    print('Test case 1:')
    response = axl.execute('executeSQLQuery',
                           {'sql': "select * from enduser where userid like '%{}%'".format(sys.argv[1])}
                           )
    print(json.dumps(response, sort_keys=True, indent=4))

    print('Test case 2:')
    response = axl.execute('getPhone', {'name': "jan-test"})
    print(json.dumps(response, sort_keys=True, indent=4))

    print('Test case 3:')
    response = axl.execute('listPhone',
                           {'searchCriteria': {
                               'name': "%test%"
                                },
                            'returnedTags': {
                                'name': '',
                                'model': ''
                                }
                            }
                           )
    print(json.dumps(response, sort_keys=True, indent=4))

    # print('Test case 4:')
    # response = axl.execute('addAarGroup', {'aarGroup': {'name': 'testAAR'}})
    # print(response)
    # print(json.dumps(response, sort_keys=True, indent=4))
