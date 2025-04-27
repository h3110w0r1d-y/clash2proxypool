import os
import signal
from time import sleep
from subprocess import DEVNULL, Popen
import yaml
import shutil


GLIDER_CONFIG = f"""
verbose=True
listen=127.0.0.1:7899
strategy=rr

"""

MIHOMO_START_PORT = 10000
MIHOMO_PROCESS: list[Popen] = []
MIHOMO_TEMPLATE = {
    'mode': 'rule',
    # 'mixed-port': 10000,
    'bind-address': '127.0.0.1',
    # 'log-level': 'warning',
    # 'proxies': [],
    'proxy-groups': [{
        'name': 'DefaultGroup',
        'type': 'select',
        # 'proxies': [],
    }],
    'rules': ['MATCH,DefaultGroup']
}


def gen_config():
    with open('mihomo.yaml', 'r') as f:
        clash: dict[str, dict] = yaml.safe_load(f)

    if os.path.exists('config'):
        shutil.rmtree('config')
    os.mkdir('config')

    for i, proxy in enumerate(clash.get('proxies', [])):
        proxy_name = f"Proxy-{i}"
        proxy_port = MIHOMO_START_PORT + i
        proxy['name'] = proxy_name

        new_proxy = MIHOMO_TEMPLATE.copy()
        new_proxy.update({
            'mixed-port': proxy_port,
            'proxies': [proxy],
        })
        new_proxy['proxy-groups']['proxies'] = [proxy_name]

        result = yaml.dump(new_proxy)

        with open(f'config/{proxy_name}.yaml', 'w') as f:
            f.write(result)

        GLIDER_CONFIG += f'forward=http://127.0.0.1:{proxy_port}\n'

    with open('glider.conf', 'w') as f:
        f.write(GLIDER_CONFIG)


def start_mihomo():
    config_files = os.listdir('config')
    for config_file in config_files:
        config_path = os.path.join('config', config_file)
        command = f'./mihomo -f {config_path}'
        process = Popen(command, shell=True, stdout=DEVNULL, stderr=DEVNULL)
        MIHOMO_PROCESS.append(process)


def start_glider():
    command = './glider -config glider.conf'
    process = Popen(command, shell=True, stdout=DEVNULL, stderr=DEVNULL)
    MIHOMO_PROCESS.append(process)


def kill_processes():
    for process in MIHOMO_PROCESS:
        process.kill()
    print("\nAll processes terminated.")


if __name__ == '__main__':
    print("Generating config files...")
    gen_config()
    print("Starting Mihomo...")
    start_mihomo()
    print("Starting Glider...")
    start_glider()
    signal.signal(signal.SIGINT, kill_processes)
    signal.signal(signal.SIGTERM, kill_processes)
    try:
        while True:
            print("\rMihomo and Glider are running...", end='', flush=True)
            for process in MIHOMO_PROCESS:
                if process.poll() is not None:
                    print('\n', process.args, 'stopped')
                    MIHOMO_PROCESS.remove(process)
            sleep(1)
    except KeyboardInterrupt:
        kill_processes()
