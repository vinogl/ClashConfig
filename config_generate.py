from config_function import url2config, direct_rule
import json
import os


# 读取文件路径
with open('Files/files_path.json', 'r') as f:
    file_path = json.load(f)

logo_path = file_path["logo"]
vmess_path = file_path["vmess"]
rule_path = file_path["rule"]
template_path = file_path["template"]
config_filename = file_path["config_filename"]


# 打印logo和使用方法
with open(logo_path, 'r') as f:
    print(f.read())
print(
    """
    使用方法：
    1. 将vmess节点链接保存到%s中，每个链接占一行
    2. 按需求修改%s内的代理规则
    3. 运行脚本，输入保存路径，回车
    4. 生成的配置文件保存在指定路径，文件名为%s
    """
    % (vmess_path, rule_path, config_filename)
)


# 获取保存路径
save_path = input('请输入保存路径(默认为当前路径): ')
if save_path == '':
    save_path = config_filename  # 默认保存到当前路径
else:
    save_path = os.path.join(save_path, config_filename)  # 保存到指定路径


# 读取节点链接，并保存到node_list列表中
with open(vmess_path, 'r') as f:
    node_list = f.read().splitlines()
node_list = [x for x in node_list if x]  # 去除空行


# 解析节点链接，并保存为字符串，用于替换模板(template.yaml)中的占位符
proxy_config_str = ''  # 用于保存节点配置
proxy_name_str = ''  # 用于保存节点名称
for node_url in node_list:
    proxy_config_str += '  ' + url2config(node_url)[0] + '\n'
    proxy_name_str += '      - ' + url2config(node_url)[1] + '\n'


# 生成规则，用于替换模板(template.yaml)中的占位符
direct_group_name, proxy_group_name, rule_str = direct_rule(rule_path)


# 读取模板(template.yaml)，并替换占位符
with open(template_path, 'r') as f:
    template = f.read()
    template = template.replace('  $$PROXY_CONFIG$$', proxy_config_str.strip('\n'))
    template = template.replace('      $$PROXY_NAME$$', proxy_name_str.strip('\n'))
    template = template.replace('$$DIRECT_GROUP_NAME$$', direct_group_name)
    template = template.replace('$$PROXY_GROUP_NAME$$', proxy_group_name)
    template = template.replace('  $$RULE$$', rule_str.strip('\n'))


# 保存配置文件到指定路径
with open(save_path, 'w') as f:
    f.write(template)
    print('保存成功')
