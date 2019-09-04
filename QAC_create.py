# -*- coding: UTF-8 -*-
import os


def create(project_path, CCT):
    acf = r'C:\Perforce\Helix-QAC-2019.1\config\acf\default.acf'  # ACF文件路径
    rcf = r'C:\Perforce\Helix-QAC-2019.1\config\rcf\default-en_US.rcf'  # RCF文件路径
    cct = r'C:\Perforce\Helix-QAC-2019.1\config\cct\\' + CCT
    cmd = 'qacli admin -P ' + project_path + ' --qaf-project-config -A ' + acf + ' -R ' + rcf + ' -C ' + cct
    os.system(cmd)


def find_code(project_path):
    code_list = []
    for home, dirs, files in os.walk(project_path):  # 检索project_path文件夹下的源文件
        for filename in files:
            if filename.endswith('.c') | filename.endswith('.cpp') | filename.endswith('.cc'):
                code_list.append('"' + os.path.join(home) + '\\' + filename + '"')
    path = project_path + '\\code_list.txt'
    with open(path, 'w') as f:  # 将源文件路径输出到code_list.txt文件中
        for list_mem in code_list:
            f.write(list_mem + '\n')


def find_header(project_path):
    home1 = None
    header_list = []
    for home, dirs, files in os.walk(project_path):  # 检索project_path文件夹下的头文件，将其路径存放在header_list列表中
        for filename in files:
            if filename.endswith('.h'):
                if home != home1:
                    header_list.append('"' + os.path.join(home) + '"')
                    home1 = home
    return header_list


def add_files(project_path, path):
    cmd1 = 'qacli admin -P "' + project_path + '" --add-files "' + project_path + '\\code_list.txt"'
    os.system(cmd1)
    acf_path = project_path + r'\prqa\configs\Initial\config\project.acf'
    with open(acf_path) as f:  # 判断find_header检索到的头文件路径是否已经被添加，如果没有则进行添加
        acf_list = f.read()
        for inc in path:
            if inc not in acf_list:
                cmd2 = 'qacli pprops -c qac-9.6.0 -o i --set ' + inc + ' -P "' + project_path + '"'  # 为qac分析模块添加头文件
                # cmd3 = 'qacli pprops -c qacpp-4.4.0 -o i --set ' + inc + ' -P "' + project_path + '"' #为qacpp添加头文件
                os.system(cmd2)


def configure(component):
    cmd = 'qacli admin --set-license-server 5055@localhost'
    # 添加分析模块，eg:qac-9.6.0 qacpp-4.4.0 rcma-2.2.0 m2cm-3.3.7 m3cm-2.3.6 mcpp-1.5.5 mcppx-1.4.8 
    cmd1 = 'qacli pprops -c ' + component + ' --add -T C -P .'
    os.system(cmd)
    os.system(cmd1)


def analysis():
    cmd = 'qacli analyze -P . -c --file-based-analysis'  # test
    os.system(cmd)


def upload(project_path, db_name, version):
    user_m = ' --upload-source ALL -U http://localhost:8080 --username admin --password admin '
    list_path = '"' + project_path + '\\code_list.txt"'
    cmd = 'qacli upload -P "' + project_path + '" -q --files ' + list_path + ' --upload-project ' + db_name + ' --snapshot' \
                                                                                                              '-name ' + \
          version + user_m
    os.system(cmd)


if __name__ == "__main__":
    project = os.path.abspath('.')  # 指定工程路径
    cct_name = 'Helix_Generic_C.cct'
    if not os.path.exists(project + r'\prqaproject.xml'):
        create(project, cct_name)
    find_code(project)
    include_path_list = find_header(project)
    add_files(project, include_path_list)
    configure('rcma-2.2.0')
    configure('m3cm-3.3.7')
    analysis()
    upload(project, 'Jenkins_addfile', '1.7')
