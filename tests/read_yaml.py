import yaml
import os


script_path = os.path.abspath(__file__) #  获取脚本的绝对路径(__file__ 是当前脚本的路径)包含文件本身
print(f"当前脚本的绝对路径: {script_path}")
# 获取脚本所在目录
script_dir = os.path.dirname(os.path.dirname(script_path))
print(f"project_root: {script_dir}")
yaml_file_path = os.path.join(script_dir, "config.yaml")
def read_yaml(yaml_file_path):
    with open(yaml_file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config



if __name__ == "__main__":
    yaml_content = read_yaml(yaml_file_path)
    print(yaml_content)
    host = yaml_content["mysql"]["host"]
    print(host)