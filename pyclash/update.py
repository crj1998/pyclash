import os
import time
import logging
import base64
import requests

from urllib.parse import unquote, urlparse, parse_qs, parse_qsl

from .utils import get_file_path

def fetch(url, timeout=24):
    cache_file = get_file_path("links.cache")
    now = time.time()
    if os.path.exists(cache_file) and now - os.path.getmtime(cache_file) <= timeout * 3600:
        t = os.path.getmtime(cache_file)
        ts = time.localtime(t)
        logging.info(f"Exist cache file created at: {time.strftime('%Y-%m-%d %H:%M:%S', ts)}")
        return True

    r = requests.get(url, timeout=5)
    content = r.content
    ret = base64.b64decode(content)
    ret = ret.decode('utf-8')
    ret = unquote(ret).strip()
    with open(cache_file, "w") as f:
        f.write(ret)
    ts = time.localtime()
    logging.info(f"cache file created at: {time.strftime('%Y-%m-%d %H:%M:%S', ts)}", )
    return True

def parse():
    cache_file = get_file_path("links.cache")
    logger = logging.getLogger('root')
    if not os.path.exists(cache_file):
        logger.error(f"{cache_file} not exists!")
        return None

    with open(cache_file, "r") as f:
        data = f.read()
    cfgs = []
    for line in data.split("\n"):
        # scheme://netloc/path;parameters?query#fragment
        qs = urlparse(line)
        scheme = qs.scheme
        netloc = qs.netloc
        query = {k: v for k, v in parse_qsl(qs.query)}
        fragment = qs.fragment
        hostname = qs.hostname
        port = qs.port
        username = qs.username
        cfg = {
            'name': fragment,
            'type': scheme,
            'server': hostname,
            'port': port, 
            'password': username, 
            'udp': query['type'] != 'ws', 
            'sni': query['sni'], 
            'skip-cert-verify': query['allowInsecure'] == '1'
        }
        if cfg['udp']:
            cfgs.append(cfg)
    logger.info(f'Total {len(cfgs)} configs find!')
    return cfgs


"""
{ name: '🇭🇰香港 01 | 专线', 
type: trojan, 
server: hk1.cf4589a1-71ec-429f-b46a-892af2259b8e.yiyuan.cyou, 
port: 443, 
password: 22b49ebb-0cc4-4b1a-bf38-a35c6c751f94, udp: true, sni: 13-251-128-188.nhost.00cdn.com, skip-cert-verify: true }

"""

if __name__ == '__main__':
    # res = fetch("https://sub1.smallstrawberry.com/api/v1/client/subscribe?token=9d305264dbe9596335a427906a026399")
    res = parse()
    print(res)