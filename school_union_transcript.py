import asyncio

import requests

from aiorequest import Request

cookies = {'UBUS': '8Oa2Hbg6Iu2Cvt-I6dkrbi7xSypFudHOH-JZ_OauglljRmM6aMw_pH2g7_O9QA5k'}


async def get_schools(union_uid):
    data = await Request.get(f'http://api/school/list?union_uid={union_uid}', cookies=cookies)
    school_ids = [s['id'] for s in data if s['status'] > 0]
    return school_ids


async def download_transcript(union_uid, school_id):
    url = await Request.get(f'http://api/school/transcript/export?union_uid={union_uid}&school_id={school_id}',
                            cookies=cookies)

    name = url.rsplit('/', 1)[-1].split('?')[0]
    name = f'/Users/dong/Documents/{name}'
    r = requests.get(url, stream=True)
    with open(name, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print(f'{name} 下载完毕')


async def main(union_id):
    ids = {2018, 6482, 6493, 6515, 6519, 6541, 6622, 6717, 6835, 6956, 6966, 6968, 6978, 6980, 6996, 7002, 7702, 7703,
           7711, 7715, 7717, 7718}
    with open(f'{union_uid}_error_school_transcripts.json', 'w+') as f:
        # school_ids = await get_schools(union_uid)
        school_ids = ids
        for i, school_id in enumerate(school_ids, 1):
            print(f'{i} {school_id} 开始上传')
            try:
                await download_transcript(union_uid, school_id)
            except Exception as e:
                print('*' * 100, str(e))
                f.write(f',{school_id}')
            if i % 10 == 0:
                await asyncio.sleep(0.02)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    union_uid = 'ccb8588077d4445c8ce1'
    loop.run_until_complete(main(union_uid))
