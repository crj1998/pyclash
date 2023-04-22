"""
The Command Line Interface (CLI) for the downloader
"""
import os
import sys
import argparse
import logging
import subprocess

shell = lambda cmd: subprocess.Popen(cmd, shell=True, stdout=None, stderr=None).wait()

from .utils import get_file_path
from .connect import write_config
from .update import fetch, parse


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)-5s] [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG)

    logger.addHandler(console)


def main():
    setup_logger()
    logging.info("🚀 Start...")
    parser = argparse.ArgumentParser(description="A fancy downloader for slut.")
    # parser.add_argument('-v', '--version', )
    subparsers = parser.add_subparsers(help='sub-command help')

    install_parser = subparsers.add_parser('install', help='version')
    install_parser.set_defaults(func=install)

    status_parser = subparsers.add_parser('status', help='version')
    status_parser.set_defaults(func=status)

    start_parser = subparsers.add_parser('start', help='version')
    start_parser.set_defaults(func=start)

    version_parser = subparsers.add_parser('version', help='version')
    version_parser.set_defaults(func=version)

    update_parser = subparsers.add_parser('update', help='update profiles')
    update_parser.add_argument("--url", type=str, help="The URL of the subscribe link.", required=True)
    update_parser.add_argument("--force", action="store_true", help="Force update profile file.")
    update_parser.add_argument("-o", "--output", 
        default=os.getcwd(),
        help=("Destination local file path. If not set, the resource "
                "will be downloaded to the current working directory, with filename "
                "same as the basename of the URL")
    )
    update_parser.set_defaults(func=update)

    list_parser = subparsers.add_parser('list', help='update profiles')
    list_parser.set_defaults(func=listnodes)

    connect_parser = subparsers.add_parser('connect', help='connect node')
    connect_parser.add_argument("-n", "--node", type=int, help="Index of the node", default=0)
    connect_parser.add_argument("-o", "--output", 
        default="/etc/trojan/config.json",
        help=("Destination local file path. If not set, the resource "
                "will be downloaded to the current working directory, with filename "
                "same as the basename of the URL")
    )
    connect_parser.set_defaults(func=connect)

    test_parser = subparsers.add_parser('test', help='version')
    test_parser.set_defaults(func=test)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        logging.info("README.md for usage")



def install(args):
    shell('apt update')
    shell('apt install trojan systemctl -y')
    shell('apt show trojan')
    logging.info(f"Success install trojan!")

def start(args):
    shell('systemctl start trojan')

def stop(args):
    shell('systemctl stop trojan')

def status(args):
    shell('systemctl status trojan')

def version(args):
    logging.info(f"OS: {sys.platform}")
    logging.info(f"Python: {sys.version}")
    logging.info(f"Package path: {get_file_path('')}")

def update(args):
    fetch(args.url, timeout=0 if args.force else 15 * 24)

def connect(args):
    stop(args)
    cfg = parse()[args.node]
    write_config(cfg, args.output)
    logging.info(f"write config file to {args.output}!")
    start(args)

def listnodes(args):
    cfgs = parse()
    if cfgs is not None:
        for i, cfg in enumerate(cfgs):
            print(f'    {i:2d} ', cfg['name'])

def test(args):
    import requests
    url = "https://ipinfo.io/json"
    r = requests.get(url)
    d = r.json()
    logging.info(f"No proxy : {d['city']}({d['ip']}) in {r.elapsed.microseconds/1000:.1f} ms")

    proxies = {"http": "socks5://127.0.0.1:1080","https": "socks5://127.0.0.1:1080"}
    r = requests.get(url, proxies=proxies)
    if r.status_code == 200:
        d = r.json()
        logging.info(f"Local proxy : {d['city']}({d['ip']}) in {r.elapsed.microseconds/1000:.1f} ms")
    else:
        logging.error(f"Failed proxy {r.status_code} for local!")
        return

    import socket
    import socks
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
    socket.socket = socks.socksocket
    r = requests.get(url)
    if r.status_code == 200:
        d = r.json()
        logging.info(f"Global proxy : {d['city']}({d['ip']}) in {r.elapsed.microseconds/1000:.1f} ms")
    else:
        logging.error(f"Failed proxy {r.status_code} for local!")
        return

    shell("curl google.com -x socks5://127.0.0.1:1080")

if __name__ == "__main__":
    main()