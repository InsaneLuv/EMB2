import asyncio
import re
from time import strftime
from time import gmtime
from tools.parse_tool_clan.paper_parser_clan import fetch_all, get_player_info
from tools.troublelogger.troubleloger import troublelog
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build




import re
import aiohttp
import asyncio


class Parser:
    def __init__(self, url):
        self.url = url
        self.pattern = re.compile(r'(id=)(.*)(\/|%2F)(.*)')
        self.unique_player_id = ''
        self.unique_paper_id = ''
        self.urls = []
        self.htmls = {}
        self.jsons = {}
        self.result = {}
        self.player_info = {}
    
    async def parse(self):
        self.extract_ids()
        async with aiohttp.ClientSession() as session:
            self.generate_urls()
            self.htmls = await self.fetch_all(session, self.urls)
            self.generate_jsons()
            # await self.get_player_info(self.jsons['meta'])
            await self.extract_result_data()
        return self.result
    
    def extract_ids(self):
        tokens = self.pattern.search(self.url)
        self.unique_player_id = tokens.group(2)
        self.unique_paper_id = tokens.group(4)
    
    def generate_urls(self):
        self.urls = [
            f'https://press.cheapshot.co/data/{self.unique_player_id}/{self.unique_paper_id}/kills',
            f'https://press.cheapshot.co/data/{self.unique_player_id}/{self.unique_paper_id}/meta',
            f'https://press.cheapshot.co/data/{self.unique_player_id}/{self.unique_paper_id}/destroys'
        ]
    
    async def fetch(self, session, url):
        async with session.get(url) as response:
            if response.status != 200:
                response.raise_for_status()
            return await response.json()

    async def fetch_all(self, session, urls):
        tasks = []
        for url in urls:
            task = asyncio.create_task(self.fetch(session, url))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results
    
    def generate_jsons(self):
        self.jsons = {
            'kills': self.htmls[0],
            'meta': self.htmls[1],
            'destroys': self.htmls[2]
        }
    
    async def get_destroy(self) -> int:
        points = 0
        try:
            for item in self.jsons['destroys']['from']['items']:
                if item.get('name') == 'Squi':
                    for building, stat in item['stats'].items():
                        if building == '🕋':
                            points += stat * 2
                        elif building == '⛩':
                            points += stat * 5
        except KeyError:
            pass
        return points
    
    async def get_building_count(self, desired) -> int:
        stat = 0
        try:
            for item in self.jsons['destroys']['from']['items']:
                if item.get('name') == 'Squi':
                    for building, count in item['stats'].items():
                        if building == desired:
                            return count
        except KeyError:
            pass
        return stat
    
    async def get_player_info(self, meta_json):
        self.player_info['userpic'] = meta_json.get('userpic','❓')
        self.player_info['username'] = meta_json.get('name','❓')
        self.player_info['date'] = meta_json.get('end_date','❓')
        return self.player_info
    
    async def extract_result_data(self):
        player_data = await self.get_player_info(self.jsons['meta'])

        self.result['userpic'] = player_data['userpic']
        self.result['username'] = player_data['username']
        self.result['unique_player_id'] = self.unique_player_id
        self.result['unique_paper_id'] = self.unique_paper_id
        self.result['date'] = player_data['date']
        self.result['points'] = await self.get_destroy()
        self.result['🕋'] = await self.get_building_count('🕋')
        self.result['⛩'] = await self.get_building_count('⛩')



class SheetsClient:
    def __init__(self):
        self.SERVICE_ACCOUNT_FILE = 'tablewriter-379418-eabbc27e7d3f.json'
        self.spreadsheet_id = '1ylRjNBxrdCQmzZVSsOv8r4h7q3IMEJ-AARKz2PGfXyo'
        self.creds = Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE)
        self.DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        self.service = build('sheets', 'v4', credentials=self.creds, discoveryServiceUrl=self.DISCOVERY_SERVICE_URL)

    async def insert_result(self, result):
        dates = {
            '2023-03-05': 'WEEK1️⃣',
            '2023-03-12': 'WEEK2️⃣',
            '2023-03-19': 'WEEK3️⃣',
            '2023-03-26': 'WEEK4️⃣',
            '2023-04-02': 'WEEK5️⃣'
        }
        try:
            range_name = dates[str(result['date'])]
        except:
            range_name = 'TECHNICAL'

        player = "{userpic} {username}".format(userpic=result['userpic'], username=result['username'])
        paper_link = 'https://press.cheapshot.co/view.html?id={unique_player_id}/{unique_paper_id}'.format(
            unique_player_id=result["unique_player_id"], unique_paper_id=result["unique_paper_id"])
        hyperlink = '=HYPERLINK("{0}"; "{1}")'.format(paper_link, player)

        values = [
            [
                hyperlink,
                result['⛩'],
                result['🕋'],
                result['points']
            ]
        ]

        requests = [
            {
                'insertDimension': {
                    'range': {
                        'sheetId': 0,
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': 0
                    },
                    'inheritFromBefore': False
                }
            }
        ]

        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body={'requests': requests}).execute()
        self.service.spreadsheets().values().append(
                                                    spreadsheetId=self.spreadsheet_id,
                                                    range=range_name,
                                                    valueInputOption='USER_ENTERED',
                                                    insertDataOption='INSERT_ROWS',
                                                    body={'values': values}
                                                    ).execute()