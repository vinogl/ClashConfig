from urllib.parse import urlsplit
from base64 import b64decode
import json
import yaml


def url2config(node_url):
    """
    将vmess的节点转换为clash配置
    """
    url = urlsplit(node_url)

    # 解析vmess链接
    if url.scheme == 'vmess':
        config = json.loads(b64decode(url.netloc).decode('utf-8'))
    else:
        return None

    # 根据解析的vmess链接生成clash配置
    clash_config = {
        'name': config['ps'],
        'server': config['add'],
        'port': config['port'],
        'type': 'vmess',
        'uuid': config['id'],
        'alterId': config['aid'],
        'cipher': 'auto' if config['type'] == 'none' else config['type'],
        'tls': True if config['tls'] == 'tls' else False,
        'network': config['net'],
        'skip-cert-verify': 'false',
        'udp': 'true'
    }

    # 将clash配置转换为字符串
    config_str = '- { '
    for key, value in clash_config.items():
        if key == list(clash_config.keys())[-1]:
            config_str += '%s: %s' % (key, value)
        else:
            config_str += '%s: %s, ' % (key, value)
    config_str += ' }'

    # 返回clash配置字符串和节点名称
    return config_str, clash_config['name']


def direct_rule(direct_path):
    """
    生成直连规则，用于替换模板(template.yaml)中的占位符
    """
    with open(direct_path, 'r') as f:
        direct_list = yaml.safe_load(f)

    rule_str = ''  # 用于保存规则
    proxy_group_name = ''  # 用于保存代理组名称
    for group_name, rule_list in direct_list.items():
        if group_name != 'DIRECT' or 'REJECT' or 'GLOBAL':
            # 如果group_name不是DIRECT、REJECT、GLOBAL，则为代理组名称
            proxy_group_name = group_name

        for key, value in rule_list.items():
            # 遍历规则列表，添加规则
            if value is None:
                # 如果value为None，则直接添加规则
                rule_str += '  - %s,%s\n' % (key, group_name)
            else:
                # 如果value不为None，则遍历value，添加规则
                for item in value:
                    rule_str += '  - %s,%s,%s\n' % (key, item, group_name)

    # 返回代理组名称和规则字符串
    return proxy_group_name, rule_str
