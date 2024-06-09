# -*- coding: iso8859-15 -*-
import os,sys
import json
import requests
import unittest

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

class GQLTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.BASE_URL = 'https://qmu.upstage.live/'
        self.LOGIN_URL = f'{self.BASE_URL}api/access_token/'
        self.WMI = f'{self.BASE_URL}api/studio_graphql/'

    def test1_call_whoami(self):
        headers = {'Content-Type': 'application/json'}
        data = {'username': "", 'password': ""}
        r = requests.post(self.LOGIN_URL, data=json.dumps(data), headers=headers)
        print(r.text)
        result = json.loads(r.text)
        headers = {'Content-Type': 'application/json','X-ACCESS-TOKEN':result['access_token']}
        query = {"query":"query whoami{whoami{id,username,password,email,binName,role,firstName,lastName,displayName,active,createdOn,firebasePushnotId,deactivatedOn,uploadLimit,intro,canSendEmail,lastLogin,dbId,roleName}}","variables":{}}
        #"User{id,username,password,email,binName,role,firstName,lastName,displayName,active,createdOn,firebasePushnotId,deactivatedOn,uploadLimit,intro,canSendEmail,lastLogin,dbId,roleName}","operationName":"whoami"}
        import pdb;pdb.set_trace()
        r = requests.post(self.WMI, data=json.dumps(query), headers=headers)
        print(r.text)

if __name__ == '__main__':
    unittest.main()

