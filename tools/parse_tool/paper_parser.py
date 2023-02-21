import datetime
import re
from time import strftime, gmtime

from aiohttp import ClientSession


# https://press.cheapshot.co/view.html?id=ddb27ad5713275159e522e8a3d909252%2F98ce05f52e8fca5f9ff2e3747d76dc84

# https://press.cheapshot.co/data/ddb27ad5713275159e522e8a3d909252/98ce05f52e8fca5f9ff2e3747d76dc84/kills

# https://press.cheapshot.co/view.html?id=38c28847663e706a5e7fc29e41b6ce42%2F4362aee1c76bb8e32aad7b73e64b01af

# https://press.cheapshot.co/data/38c28847663e706a5e7fc29e41b6ce42/4362aee1c76bb8e32aad7b73e64b01af/kills

async def paper_parse(paper):
    paper_re = re.sub('%2F','/',paper)
    pattern = re.compile(r'(.*=)(.*)(/)(.*)')
    urls = paper_re.split("\n")
    urls_res = []

    for i in urls:
        res = pattern.search(i)
        try:
            url = f"https://press.cheapshot.co/data/{res.group(2)}/{res.group(4)}"
            urls_res.append(str(url))
        except:
            pass


    return await run(urls_res,paper_re.split("\n"))


async def run(urls, urls_in):
    owners = []
    lst = []
    for url in urls_in:
        if url.startswith('https://press.cheapshot.co/'):
            owners.append(url)
    async with ClientSession() as session:

        for url in urls:
            url_for_kills = f'{url}/kills'
            url_for_meta = f'{url}/meta'

            async with session.get(url_for_meta) as response:
                page_content = await response.json()
                item = page_content
                async with session.get(url_for_kills) as response:
                    page_content = await response.json()

                    item2 = page_content["from"]["category"]

                    item2["date"]= item["end_date"]
                    item2["userpic"] = item["userpic"]
                    item2["username"] =  item["name"]

                    lst.append(item2)


    result = {}
    for i in range(0, len(owners)):
        result[owners[i]] = lst[i]
    return result
# worksheet.write(0, 0, 'Это A1!')


async def epit(raw_papers,call_user_id):
    import xlsxwriter
    timestamp = strftime("%H-%M-%S", gmtime())
    filename = f'res_{call_user_id}_{str(timestamp)}.xlsx'
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    name_format = workbook.add_format()
    name_format.set_align('center')
    count = 1
    for owner, items in raw_papers.items():
        worksheet.write_url(0, count, owner,name_format, string=items['username'])
        worksheet.set_column(1, count, 25)
        count += 1

    count = 1
    lst = ['👾 alien',
           '💀 attacker',
           '🐝 birdie',
           '🐍 defender',
           '🐉 dragon',
           '🦀 ordinary',
           '👮 police',
           '🚔 police_car',
           '🚁 police_heli',
           '🐀 rat',
           '⛄ snö',
           '📅 date']
    worksheet.set_column(0, count, 13)
    for i in lst:
        worksheet.write(count, 0, i)
        count += 1

    count = 1
    num_format = workbook.add_format()
    num_format.set_num_format('0')
    date_format = workbook.add_format({'num_format': 'dd.mm.yyyy'})
    for owner, items in raw_papers.items():
        worksheet.write(1, count, int(items['alien']) if 'alien' in items else 0,num_format)
        worksheet.write(2, count, int(items['attacker']) if 'attacker' in items else 0,num_format)
        worksheet.write(3, count, int(items['birdie']) if 'birdie' in items else 0,num_format)
        worksheet.write(4, count, int(items['defender']) if 'defender' in items else 0,num_format)
        worksheet.write(5, count, int(items['dragon']) if 'dragon' in items else 0,num_format)
        worksheet.write(6, count, int(items['ordinary']) if 'ordinary' in items else 0,num_format)
        worksheet.write(7, count, int(items['police']) if 'police' in items else 0,num_format)
        worksheet.write(8, count, int(items['police_car']) if 'police_car' in items else 0,num_format)
        worksheet.write(9, count, int(items['police_heli']) if 'police_heli' in items else 0,num_format)
        worksheet.write(10, count, int(items['rat']) if 'rat' in items else 0,num_format)
        worksheet.write(11, count, int(items['snö']) if 'snö' in items else 0,num_format)
        date_time = datetime.datetime.strptime(items['date'] if 'date' in items else '11-11-11', '%Y-%m-%d')

        worksheet.write_datetime(12, count, date_time, date_format)
        count += 1
    workbook.close()

    return filename


