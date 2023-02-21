import asyncio
from datetime import datetime
import logging
import time
import simplejson as json
import re
from collections import Counter
from time import strftime
from time import gmtime
import traceback
import xlsxwriter
from aiohttp import ClientSession
import uuid
import requests
import math
from decimal import Decimal as dec
from tools.troublelogger.troubleloger import troublelog


clanlist = {'NOISY': '🧑‍🦽NOISY',
            '🧢': '🧢 • no cap',
            '•YRMUM•': '•YRMUM•',
            '🌵🪓': '🌵🪓',
            '💀': '💀',
            '🍇': '🍇',
            '•❔•': '•❔•',
            '🇺🇦': '🇺🇦',
            '💸ɢᴏᴠᴛ💸': '💸 ɢᴏᴠᴇʀɴᴍᴇɴᴛ 💸',
            'Ninja': '🎴Ninja Squad⛩',
            'pohui': 'pohui',
            'B4': '[🪓B4]',
            '🏴': '🏴S.I.T.',
            '🪬': '🪬',
            '⭕️': 'ЦАО | ⭕️',
            '🇳🇱': '🇳🇱•Cheapshot•🇳🇱',
            '🏴‍☠️': '🏴‍☠️',
            '❌': '❌Team❌',
            '•🐽•': '•🐽•',
            'Silent': 'Silent',
            'AİLE ❄️': 'AİLE ❄️',
            '.mp4': '.mp4',
            '𝔽𝕃𝔸𝕄𝔼𝔻': '⚔️𝔽𝕃𝔸𝕄𝔼𝔻⚔️',
            'В4': 'badclan'
            }

headers = {
    'Content-type': 'application/json',
    'Accept': 'text/plain',
    'Content-Encoding': 'utf-8'
}

api_url = 'http://141.8.199.204:9000/clanevent/newspaper'


async def get_player_clan(username, clanlist):
    claninfo = {}
    for unique, clanname in clanlist.items():
        if username.find(unique) != -1:
            if unique != 'В4':
                claninfo['clantag'] = unique
                claninfo['clanname'] = clanname
            else:
                claninfo['clantag'] = 'B4'
                claninfo['clanname'] = '[🪓B4]'
            break
        else:
            claninfo['clantag'] = 'None'
            claninfo['clanname'] = 'None'

    return claninfo


async def get_player_info(meta):
    # URL FOR META
    player_info = {}

    player_info['userpic'] = meta.get('userpic', '🤖')
    player_info['username'] = meta.get('name', 'ERROR')
    claninfo = await get_player_clan(player_info['username'], clanlist)
    player_info['clantag'] = claninfo.get('clantag', 'None')
    player_info['clanname'] = claninfo.get('clanname', 'None')
    player_info['date'] = meta.get('end_date', '00-00-00')

    return player_info


async def get_pdragon(kills):
    # URL FOR KILLS
    pdragons = 0
    if bool(kills["from"]) is not False:
        try:
            for i in kills["from"]["items"]:
                pdragons += sum(1 for b in i['stats'] if b["pic"] == "🐉")
        except:
            return pdragons
    return pdragons


async def get_destroy(destroys, playerdata):
    # URL FOR DESTROYS
    # playerdata from get_player_info(url)
    points = 0
    try:
        for i in destroys["from"]["items"]:
            buildings = []
            if 'name' in i:
                if i['name'].find(playerdata['clantag']) == -1:
                    for i in i["stats"]:
                        buildings.append(i)
                x = dec(0)
                for each in buildings:
                    x += dec(0.01)
                x *= len(buildings)
                points += x
        return points
    except:
        return points


async def get_monuments_destroyed(page_content, allmonuments):
    # URL FOR DESTROYS
    monuments = page_content["special"]
    monument_list = []
    monument_points = 0

    for i, b in monuments.items():
        if type(b) != int:
            for monument in b:
                picname = f"{monument['pic']}{monument['name']}"

                with open("destroyedmonuments.txt", 'r', encoding="utf-8") as f:
                    destroyed_list = [line.rstrip('\n') for line in f]

                if picname not in destroyed_list:
                    cur_monument = {"pic": monument["pic"], "name": monument["name"],
                                    "picname": f"{monument['pic']}{monument['name']}"}
                    if monument['name'] != 'Mystery Box':
                        monument_list.append(cur_monument)
                        with open("destroyedmonuments.txt", 'a', encoding="utf-8") as destroyed:
                            destroyed.write(f"{cur_monument['picname']}\n")
                    else:
                        monument_points += 3

    for i in monument_list:
        for dict_ in allmonuments:
            if dict_["picname"] == i['picname']:
                monument_points += int(dict_['diff']) + 2
    return monument_points


async def get_all_monuments(page_content):
    all_monuments = []
    for i in page_content:
        for monument in i['monuments']:
            if monument['difficulty'] == "":
                all_monuments.append({"pic": monument["pic"], "name": monument["name"], "diff": 1,
                                      "picname": f"{monument['pic']}{monument['name']}"})
            else:
                star_count = dict(Counter(monument['difficulty']))
                all_monuments.append({"pic": monument["pic"], "name": monument["name"], "diff": star_count.get('⭐'),
                                      "picname": f"{monument['pic']}{monument['name']}"})

    return all_monuments


async def get_upgrades(page_content):
    if bool(page_content) is not False:
        builds = dict(Counter(page_content['buildings']))
        for k, i in builds.items():
            builds[k] = i
        return builds
    else:
        builds = {}
        return builds


async def get_bot_kills(page_content):
    # URL_FOR_KILLS
    if bool(page_content['from']) is not False:
        return page_content["from"]["category"]
    else:
        empty = {}
        return empty


async def paper_parse_clan(paper, mode):
    pattern = re.compile(r'(id=)(.*)(\/|%2F)(.*)')
    urls = paper.split(",")
    urls = [ele for ele in urls if ele.strip()]
    urls_res = []

    for i in urls:
        res = pattern.search(i)
        try:
            url = f"https://press.cheapshot.co/data/{res.group(2)}/{res.group(4)}"
            urls_res.append(str(url))
        except Exception:
            e = traceback.format_exc()
            await troublelog("CLANPARSER", e, {i})

    if mode != "registration":
        return await run(urls_res, "event")
    else:
        return await run(urls_res, "registration")


async def send_to_exp(url,content, session):
    try:
        string1 = json.dumps(content,indent=4, sort_keys=True, separators=(',', ': '), use_decimal=True)
        state = requests.post(url, data=string1, headers=headers)
        return state.status_code
    except Exception as e:
        e = traceback.format_exc()
        return e


async def create_dict(result, jsons):
    allmonuments = await get_all_monuments(jsons['allmonuments'])
    playerdata = await get_player_info(jsons['meta'])
    result.update(playerdata)
    result.update(await get_bot_kills(jsons['kills']))
    result['pdragon'] = await get_pdragon(jsons['kills'])
    result['destroy'] = await get_destroy(jsons['destroys'], playerdata)
    result['monument'] = await get_monuments_destroyed(jsons['destroys'], allmonuments)
    upgrades = await get_upgrades(jsons['builds'])

    result['buildings'] = [{'count': v, 'pic': k} for k,v in upgrades.items()]
    result['sno'] = result.pop('snö', 0)
    result['pkill'] = result.pop('user', 0)
    # result['uuid'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, result['url']))


    
    cat_pops_int = [
        'police', 'police_car', 'police_heli', 'rat', 'birdie', 'ordinary', 'alien', 'dragon', 'pdragons', 'destroy', 'monument','pkill'
    ]

    for cat in cat_pops_int:
        result[cat] =  result.pop(cat, 0)

    cat_pops_str = [
        'clantag', 'clanname', 'date', 'userpic', 'username'
    ]

    for cat in cat_pops_str:
        result[cat] =  result.pop(cat, 'Error')

    return result


async def fetch(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            response.raise_for_status()
        return await response.json()


async def fetch_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def exp_fetch(session, url, result):
    async with session.post(url, data=result, headers=headers) as response:
        return response.status


async def exp_fetch_all(url, session, results_json):
    tasks = []
    for result_json in results_json:
        task = asyncio.create_task(exp_fetch(session, url, result_json))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def run(urls, mode):
    t = time.perf_counter()

    pattern2 = re.compile(r'(data\/)(.*)(\/)(.*)')

    results = []
    results_json = []

    async with ClientSession() as session:
        for url in urls:
            result = {}
            url = re.sub('%20', '', url)
            res = pattern2.search(url)

            try:
                result["url"] = f"https://press.cheapshot.co/view.html?id={res.group(2)}/{res.group(4)}"
            except Exception:
                e = traceback.format_exc()
                await troublelog("CLANPARSER",e,{url})

            
            urls = [
                f'{url}/kills',
                f'{url}/meta',
                f'{url}/destroys',
                f'{url}/builds',
                'https://cheapshot.app/monument'
                ]
            
            htmls = await fetch_all(session, urls)
            jsons = {
                'kills': htmls[0],
                'meta': htmls[1],
                'destroys': htmls[2],
                'builds': htmls[3],
                'allmonuments': htmls[4]
                }
            
            if mode == "registration":
                return  await get_player_info(json['meta'], session)
                
            results.append(await create_dict(result, jsons))
            results_json.append(json.dumps(result,indent=4, sort_keys=True, separators=(',', ': '), use_decimal=True))

        responces = await exp_fetch_all(api_url, session, results_json)
        logging.warning(f'[{results[0]["clanname"]}] sent [{responces.count(200)} / {len(responces)}] to api. Elapsed time: [{{0:.3f}}] sec.'.format(time.perf_counter() - t))

        return results


async def epit_clan(raw_papers, unique, building):
    timestamp = strftime("%H-%M", gmtime())
    filename = f'{raw_papers[0]["clanname"]}-{unique}_{str(timestamp)}.xlsx'
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    name_format = workbook.add_format()
    name_format.set_align('center')
    count = 1


    for paper in raw_papers:
        worksheet.write_url(0, count, paper["url"], name_format, string=paper['username'])
        worksheet.set_column(1, count, 25)
        count += 1

    count = 1
    categories = ['police',
           'police_heli',
           'birdie',
           'ordinary',
           'dragon',
           'pdragon',
           'alien',
           'police_car',
           'monument',
           'rat',
           'destroy',
           f'{building}',
           'date']

    worksheet.set_column(0, count, 13)

    for category in categories:
        worksheet.write(count, 0, category)
        count += 1

    count = 1

    offset = 1

    cell_format = workbook.add_format()
    cell_format.set_pattern(1)  # This is optional when using a solid fill.
    cell_format.set_bg_color('#666666')
    cell_format.set_font_size(11)

    for paper in raw_papers:
        for category in categories:
            if category is not building:
                worksheet.write(offset, count, paper.get(category, 0), cell_format)
            else:
                for i in paper['buildings']:
                    if i['pic'] == building:
                        worksheet.write(offset, count, i['count'], cell_format)
                        break
                    else:
                        worksheet.write(offset, count, 0, cell_format)
            offset += 1
        count += 1
        offset = 1

    workbook.close()

    return filename

                # settings = {}
                # settings['s_police'] = 5000
                # settings['s_police_heli'] = 1000
                # settings['s_police_car'] = 250
                # settings['s_ordinary'] = 750
                # settings['s_dragons'] = 30
                # settings['s_pdragon'] = 25
                # settings['s_alien'] = 20
                # settings['s_rat'] = 2500
                # result['settings'] = [{'type': type, 'count': count} for type, count in settings.items()]