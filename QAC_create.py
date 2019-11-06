# -*- coding: UTF-8 -*-
import os
import db_version


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
    with open(path, 'w') as file:  # 将源文件路径输出到code_list.txt文件中
        for list_mem in code_list:
            file.write(list_mem + '\n')


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
    with open(acf_path) as file:  # 判断find_header检索到的头文件路径是否已经被添加，如果没有则进行添加
        acf_list = file.read()
        for inc in path:
            if inc not in acf_list:
                cmd2 = 'qacli pprops -c qac-9.6.0 -o i --set ' + inc + ' -P "' + project_path + '"'  # 为qac分析模块添加头文件
                # cmd3 = 'qacli pprops -c qacpp-4.4.0 -o i --set ' + inc + ' -P "' + project_path + '"' #为qacpp添加头文件
                os.system(cmd2)


# def add_configure(component): # 分析模块添加程序
#     # 添加分析模块，eg:qac-9.6.0 qacpp-4.4.0 rcma-2.0.0 m2cm-3.3.7 m3cm-2.3.6 mcpp-1.5.5 mcppx-1.4.8
#     acf_path = project_path + r'\prqa\configs\Initial\config\project.acf'
#     C_comp = ['qac-9.6.0', 'm2cm-3.3.7', 'm3cm-2.3.6', 'cweccm-1.0.6']
#     Cpp_comp = ['qacpp-4.4.0', 'mcpp-1.5.5', 'mcppx-1.4.8', 'cwecppcm-1.0.1', 'ascm-2.0.0', 'jcm-1.3.8']
#     C_CPP_comp = ['rcma-2.0.0', 'mta-2.0.0']
#     for comp in component:
#         if comp in C_comp:
#             target.append('C')
#         elif comp in Cpp_comp:
#             target.append('C++')
#         elif comp in C_CPP_comp:
#             target.append('C/C++')
#
#     cmd = 'qacli pprops -c ' + component + ' --add -T ' + target + ' -P .'
#     os.system(cmd)


def delete_svn(project_path):  # 删除通过svn将源码同步到Jenkins工作目录时svn添加的.svn文件
    cmd = '"' + project_path + '\\delete.bat"'
    os.system(cmd)


def analysis():
    cmd = 'qacli admin --set-license-server 5055@localhost'
    cmd1 = 'qacli analyze -P . -c --file-based-analysis'  # test
    os.system(cmd)
    os.system(cmd1)


def upload(project_path, db_name, v):
    list_path = '"' + project_path + '\\code_list.txt"'
    user_m = ' --upload-source ALL -U http://localhost:8080 --username admin --password admin '
    cmd = 'qacli upload -P "' + project_path + '" -q --files ' + list_path + ' --upload-project ' + db_name + ' --snapshot' \
                                                                                                              '-name ' + \
          v + user_m
    flag = os.popen(cmd)
    if 'done' in flag.read():
        return 1
    else:
        return 0


if __name__ == "__main__":
    change_version = 0
    project = os.path.abspath('.')  # 指定工程路径
    cct_name = 'Helix_Generic_C.cct'
    if not os.path.exists(project + r'\prqaproject.xml'):
        create(project, cct_name)
    find_code(project)  # 检索当前工作目录下是否新增了源文件，并添加源文件到QAC工作
    include_path_list = find_header(project)  # 检索当前工作目录下是否新增了头文件
    add_files(project, include_path_list)  # 添加头文件到QAC工程中
    #delete_svn(project)
    analysis()  # 执行QAC分析
    version = db_version.calculate(project, change_version)  # 读取之前dashboard工程辨别编号，如何是第一次上传会将版本编号指定为1.0
    f = upload(project, 'hello_auto', version)  # 将结果上传到dashboard
    if f:  # 判断QAC是否成功将结果上传到dashboard
        db_version.write(project, version)  # 将当前dashboard版本编号写入version.txt中
