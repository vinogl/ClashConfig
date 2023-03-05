from config_function import generate_groups, generate_rules
import json
import os


# 读取文件路径
with open('Files/files_path.json', 'r') as f:
    file_path = json.load(f)

logo_path = file_path["logo"]  # logo文件路径
groups_path = file_path["proxy_groups"]  # 代理组文件路径
rule_path = file_path["rule"]  # 规则文件路径
template_path = file_path["template"]  # 模板文件路径
config_filename = file_path["config_filename"]  # 生成的配置文件名


# 打印logo和使用方法
with open(logo_path, 'r') as f:
    print(f.read())
print(
    """
    使用方法：
    1. 分组将节点保存到%s，并将各代理组的规则保存到%s
    （注意：规则文件中的代理组名称必须与分组文件中的代理组名称一致）
    2. 运行脚本，输入保存路径，回车
    3. 生成的配置文件保存在指定路径，文件名为%s
    """
    % (groups_path, rule_path, config_filename)
)


# 获取保存路径
save_path = input('请输入保存路径(默认为当前路径): ')
if save_path == '':
    save_path = config_filename  # 默认保存到当前路径
else:
    save_path = os.path.join(save_path, config_filename)  # 保存到指定路径


# 生成代理配置和代理组信息，用于替换模板中的占位符
proxy_config, proxy_groups = generate_groups(groups_path)

# 生成规则，用于替换模板中的占位符
rule_str = generate_rules(rule_path)


# 读取模板，并替换占位符
with open(template_path, 'r') as f:
    template = f.read()
    template = template.replace('  $$PROXY_CONFIG$$', proxy_config.strip('\n'))
    template = template.replace('  $$PROXY_GROUPS$$', proxy_groups.strip('\n'))
    template = template.replace('  $$RULE$$', rule_str.strip('\n'))


# 保存配置文件到指定路径
with open(save_path, 'w') as f:
    f.write(template)
    print('保存成功')
