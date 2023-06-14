import requests
import pandas as pd

apiKey = 'RGAPI-a6530184-33eb-4dbd-9e0f-4cc7cf937c6d'
matchId = 'KR_6540176483'
puuid = 'PKukybj5IXCRVMxF84LyipuwD8LEiweTVXW-EIoTHir--V-e0SJ15OtP7GZ4hcF6lq8CKMagfsjzfA'
timelineUrl = 'https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline?api_key={apiKey}'

response = requests.get(timelineUrl)

if response.status_code == 200:
    data = response.json()
    if 'frames' in data:
        frames = data['frames']
        
        # Riot API에서 받은 데이터를 가정합니다
        YourId = 'PKukybj5IXCRVMxF84LyipuwD8LEiweTVXW-EIoTHir--V-e0SJ15OtP7GZ4hcF6lq8CKMagfsjzfA'

        # 데이터를 저장하기 위한 빈 리스트를 초기화합니다
        kills = []
        deaths = []
        paths = []

        # 각 프레임을 순회합니다
        for frame in frames:
            minute = frame['timestamp'] // 60000  # 분을 계산합니다

            # 각 이벤트를 순회합니다
            for event in frame['events']:
                event_type = event['type']

                if event_type == 'CHAMPION_KILL':
                    killer_id = event['killerId']
                    victim_id = event['victimId']
                    position = event['position']

                    # 원하는 소환사의 킬 정보만 필터링합니다
                    if killer_id == YourId or victim_id == YourId:
                        kills.append((killer_id, victim_id, position.x, position.y, minute))

                elif event_type == 'CHAMPION_DEATH':
                    killer_id = event['killerId']
                    victim_id = event['victimId']
                    position = event['position']

                    # 원하는 소환사의 데스 정보만 필터링합니다
                    if killer_id == YourId or victim_id == YourId:
                        deaths.append((killer_id, victim_id, position.x, position.y, minute))

                elif event_type == 'CHAMPION_LOCATION':
                    participant_id = event['participantId']
                    position = event['position']

                    # 원하는 소환사의 위치 정보만 필터링합니다
                    if participant_id == YourId:
                        paths.append((participant_id, position.x, position.y, minute))

        # 수집한 데이터로부터 데이터프레임을 생성합니다
        kills_df = pd.DataFrame(kills, columns=['킬러ID', '피해자ID', 'X', 'Y', '분'])
        deaths_df = pd.DataFrame(deaths, columns=['킬러ID', '피해자ID', 'X', 'Y', '분'])
        paths_df = pd.DataFrame(paths, columns=['참가자ID', 'X', 'Y', '분'])
        
        # 생성한 데이터프레임을 사용하여 분석 또는 시각화 등의 작업을 수행합니다
        
    else:
        print("'frames' 필드가 존재하지 않습니다.")
else:
    print('API 요청이 실패하였습니다. 상태 코드:', response.status_code)
