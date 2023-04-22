# pytrojan
This project provide command line inference for ubuntu.


## Install 

```bash 
pip install -r requirements.txt
# -v means verbose, or more output.
# -e means installing a project in editable mode.
pip install -v -e .

python setup.py develop
```

## Usage
### cli
```bash
clash version
clash update --url <SUBSCRIBE>
clash list
clash connect -n <NODEID>
```

### check state
```bash
ps aux | grep trojan | grep -v grep
```


### Use proxy
```bash
# curl proxy
curl google.com --socks5 127.0.0.1:1080
curl google.com -x socks5://127.0.0.1:1080

# git proxy
git config --global http.proxy 'socks5://127.0.0.1:1080'
git config --global https.proxy 'socks5://127.0.0.1:1080'
git config --global --unset http.proxy
git config --global --unset https.proxy

# global proxy
export ALL_PROXY="socks5://127.0.0.1:1080"
unset ALL_PROXY
```

### proxychains
```
apt install proxychains
```
edit `/etc/proxychains.conf` and comment `socks4`, add `socks5 127.0.0.1 1080` in `ProxyList`.
Then use `proxychains cmd`, e.g. `proxychains curl -4 ip.sb`.


## Mechanism
1. Install trojan
```bash
apt update
apt install trojan -y
```
2. Modifying the configuration file

Open `/etc/trojan/config.json` and modify it.
```
{
    "run_type": "client",
    "local_addr": "127.0.0.1",
    "local_port": 1080,
    "remote_addr": "REMOTE ADDR",
    "remote_port": 443,
    "password": [
        "PASSWORD"
    ],
    "log_level": 1,
    "ssl": {
        "verify": false,
        "verify_hostname": false,
        "cert": "",
        "cipher": "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES128-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:AES128-SHA:AES256-SHA:DES-CBC3-SHA",
        "cipher_tls13": "TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_256_GCM_SHA384",
        "sni": "SNI",
        "alpn": [
            "h2",
            "http/1.1"
        ],
        "reuse_session": true,
        "session_ticket": false,
        "curves": ""
    },
    "tcp": {
        "no_delay": true,
        "keep_alive": true,
        "reuse_port": false,
        "fast_open": false,
        "fast_open_qlen": 20
    }
}
```

3. start trojan
```bash
trojan -t
systemctl start trojan
systemctl status trojan
```

```
~~/pyclash
├── config.json
├── links.cache
├── pyclash
│   ├── cli.py
│   ├── connect.py
│   ├── __init__.py
│   ├── update.py
│   └── utils.py
├── pyproject.toml
├── README.md
├── requirements.txt
└── setup.py
```

## Q&A
1. ERROR `requests.exceptions.InvalidSchema: Missing dependencies for SOCKS support.`
```
pip install -U 'requests[socks]'
```

## Reference

- https://docs.python.org/zh-cn/3.9/library/urllib.parse.html
- https://xbsj9729.website/pagesv2/download-linux.html
- https://ip-api.com
- https://www.ipify.org
- https://ipinfo.io