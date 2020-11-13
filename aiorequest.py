from decimal import Decimal

import json as ujson
import aiohttp


class DecimalEncoder(ujson.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        else:
            return ujson.JSONEncoder.default(self, o)


def dumps(obj, ensure_ascii: bool = True) -> str:
    return ujson.dumps(obj, cls=DecimalEncoder, ensure_ascii=ensure_ascii)


def loads(string, default=None):
    if not string:
        return default
    return ujson.loads(string)


class Request:
    base_url = ''

    @classmethod
    async def get_json(cls, url, resp):
        text = await resp.text()
        if resp.status not in (200, 201):
            print(f'{url}: {resp.status} {text}')
            raise Exception(f'{url}：{resp.status} 网络错误!')
        return ujson.loads(text)

    @classmethod
    def get_data(cls, url: str, json: dict):
        return json['data']

    @classmethod
    def get_params(cls, params):
        return params

    @classmethod
    async def get(cls, url: str, params: object = None, content_type: str = 'application/json', **kwargs):
        url = cls.base_url + url
        if content_type:
            headers = kwargs.get('headers') or {}
            headers['Content-Type'] = content_type
            kwargs['headers'] = headers
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(
                url=url,
                params=cls.get_params(params) if params else None,
                **kwargs,
            ) as resp:
                print(resp.real_url)
                data = await cls.get_json(url, resp)
                return cls.get_data(url, data)

    @classmethod
    async def post(cls, url: str, json: object = None, content_type: str = 'application/json', **kwargs):
        url = cls.base_url + url
        if content_type:
            headers = kwargs.get('headers') or {}
            headers['Content-Type'] = content_type
            kwargs['headers'] = headers
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=url,
                data=dumps(cls.get_params(json) if json else json),
                **kwargs,
            ) as resp:
                data = await cls.get_json(url, resp)
                return cls.get_data(url, data)
