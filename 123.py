import os


def get_directory_structure(root_dir, ignored_folders):
    """
    遍历目录树并构建目录结构的字符串表示。
    忽略所有在 ignored_folders 列表中的文件夹。
    """
    directory_structure = ""
    for root, dirs, files in os.walk(root_dir):
        # 过滤要忽略的文件夹
        dirs[:] = [d for d in dirs if d not in ignored_folders]

        # 计算相对于根目录的缩进级别
        relative_root = os.path.relpath(root, root_dir)
        if relative_root == ".":
            level = 0
        else:
            level = relative_root.count(os.sep) + 1
        indent = ' ' * 4 * level
        directory_structure += f"{indent}{os.path.basename(root)}/\n"
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            directory_structure += f"{sub_indent}{file}\n"
    return directory_structure


def read_file_contents(file_path):
    """
    尝试读取文件内容。如果是文本文件，返回内容；否则返回错误信息。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        return f"[无法读取二进制文件或非UTF-8编码文件: {file_path}]\n"
    except Exception as e:
        return f"[读取文件时出错: {file_path} - {e}]\n"


def list_all_files(root_dir, ignored_folders):
    """
    列出所有文件的相对路径。
    忽略所有在 ignored_folders 列表中的文件夹，并排除 output.txt 本身。
    """
    files_list = []
    for root, dirs, files in os.walk(root_dir):
        # 过滤要忽略的文件夹
        dirs[:] = [d for d in dirs if d not in ignored_folders]

        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), root_dir)
            # 排除 output.txt 本身
            if os.path.abspath(os.path.join(root, file)) == os.path.join(root_dir, 'output.txt'):
                continue
            files_list.append(relative_path)
    return files_list


def prompt_excluded_files():
    """
    提示用户输入要排除的文件名、文件夹名和文件类型。
    """
    print("\n=== 排除文件内容的选项 ===\n")

    # 排除文件名
    file_names = set()
    file_names_input = input("请输入要排除的文件名（多个文件名用逗号分隔，留空跳过）： ").strip()
    if file_names_input:
        file_names = set(name.strip() for name in file_names_input.split(',') if name.strip())

    # 排除文件夹名
    folder_names = set()
    folder_names_input = input("请输入要排除的文件夹名（多个文件夹名用逗号分隔，留空跳过）： ").strip()
    if folder_names_input:
        folder_names = set(name.strip() for name in folder_names_input.split(',') if name.strip())

    # 排除文件类型
    file_types = set()
    file_types_input = input("请输入要排除的文件类型（扩展名，不含点，多个类型用逗号分隔，留空跳过）： ").strip()
    if file_types_input:
        file_types = set(ext.lower().lstrip('.') for ext in file_types_input.split(',') if ext.strip())

    # 显示用户选择的排除条件
    print("\n您选择的排除条件如下：")
    if file_names:
        print(" - 排除的文件名：")
        for name in file_names:
            print(f"   - {name}")
    else:
        print(" - 无排除的文件名。")

    if folder_names:
        print(" - 排除的文件夹名：")
        for folder in folder_names:
            print(f"   - {folder}")
    else:
        print(" - 无排除的文件夹名。")

    if file_types:
        print(" - 排除的文件类型：")
        for ext in file_types:
            print(f"   - .{ext}")
    else:
        print(" - 无排除的文件类型。")

    return file_names, folder_names, file_types


def prompt_ignored_folders():
    """
    提示用户输入要忽略的文件夹名称，这些文件夹将不会显示在目录结构中，也不会被遍历。
    """
    print("\n=== 额外忽略文件夹的选项 ===\n")
    ignored_folders = set()

    ignored_folders_input = input("请输入要额外忽略的文件夹名（多个文件夹名用逗号分隔，留空跳过）： ").strip()
    if ignored_folders_input:
        ignored_folders = set(name.strip() for name in ignored_folders_input.split(',') if name.strip())

    # 显示用户选择的忽略条件
    print("\n您选择要忽略的文件夹如下：")
    if ignored_folders:
        for folder in ignored_folders:
            print(f" - {folder}")
    else:
        print(" - 无额外忽略的文件夹。")

    return ignored_folders


def should_exclude(file_relative_path, file_names, folder_names, file_types):
    """
    判断一个文件是否应该被排除。
    """
    # 分离文件夹和文件名
    parts = file_relative_path.split(os.sep)
    file_name = parts[-1]
    folders = parts[:-1]

    # 检查文件名
    if file_name in file_names:
        return True

    # 检查文件夹名
    if any(folder in folder_names for folder in folders):
        return True

    # 检查文件类型
    _, ext = os.path.splitext(file_name)
    ext = ext.lstrip('.').lower()
    if ext in file_types:
        return True

    return False


def main():
    # 获取脚本所在的根目录
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # 默认要忽略的文件夹
    default_ignored_folders = {'node_modules'}

    # 提示用户输入要额外忽略的文件夹
    additional_ignored_folders = prompt_ignored_folders()

    # 合并默认和用户额外忽略的文件夹
    ignored_folders = default_ignored_folders.union(additional_ignored_folders)

    # 列出所有文件
    files_list = list_all_files(root_dir, ignored_folders)

    if not files_list:
        print("根目录下没有找到任何文件。")
        return

    print("\n以下是根目录及子目录中的所有文件：")
    for idx, file in enumerate(files_list, 1):
        print(f"{idx}. {file}")

    # 提示用户选择要排除的文件
    file_names, folder_names, file_types = prompt_excluded_files()

    # 获取目录结构
    directory_structure = get_directory_structure(root_dir, ignored_folders)

    # 初始化输出内容
    output_content = "目录结构:\n"
    output_content += directory_structure
    output_content += "\n文件内容:\n\n"

    # 遍历所有文件并读取内容
    excluded_files = []
    for file in files_list:
        if should_exclude(file, file_names, folder_names, file_types):
            excluded_files.append(file)
            continue  # 跳过被排除的文件
        file_path = os.path.join(root_dir, file)
        relative_path = file
        output_content += f"=== {relative_path} ===\n"
        file_contents = read_file_contents(file_path)
        output_content += file_contents + "\n\n"

    # 写入到output.txt
    output_file = os.path.join(root_dir, 'output.txt')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"\n所有信息已成功保存到 {output_file}")
    except Exception as e:
        print(f"写入文件时出错: {e}")

    # 显示被排除的文件
    if excluded_files:
        print("\n以下文件已被排除，不会输出内容：")
        for file in excluded_files:
            print(f"- {file}")
    else:
        print("\n没有文件被排除。")


if __name__ == "__main__":
    main()

# 请输入要额外忽略的文件夹名（多个文件夹名用逗号分隔，留空跳过）： node_modules,assets,uploads,routers,public

# 请输入要排除的文件名（多个文件名用逗号分隔，留空跳过）： scan_and_extract.py,.DS_Store,README.md,init.sql,123.py,.gitignore,20250123_cra_ai.py

# 请输入要排除的文件夹名（多个文件夹名用逗号分隔，留空跳过）： db,routers

# 请输入要排除的文件类型（扩展名，不含点，多个类型用逗号分隔，留空跳过）： json,mp4,sql,xml,svg,png,jpg,jpeg,json,md,txt,gitignore,iml,pyc
