import os
import subprocess

branches = [
    'env_dev', 'env_qa', 'master',
    'package_sie', 'package_cbkyt', 
    'app_zend_django', 'app_reports', 'app_calendar_events',
]

file = "pull_updates.txt"
broken = False

def main():
    with open(file, 'w') as stdout_file:
        code = subprocess.call(
            ['git', 'fetch', 'upstream'],
            stdout=stdout_file,
            stderr=stdout_file)
        if code != 0:
            print("Ocurrio un error obtiendo las actualizaciones")
        else:
            for branch in branches:
                code = subprocess.call(
                    ['git', 'checkout', f'upstream/{branch}'],
                    stdout=stdout_file,
                    stderr=stdout_file)
                if code != 0:
                    print(
                        f"Error accesando al branch upstream/{branch}")
                    continue
                code = subprocess.call(
                    ['git', 'checkout', '-b', branch],
                    stdout=stdout_file,
                    stderr=stdout_file)
                if code == 0:
                    print(f"Branch creado: {branch}")
                elif code == 128:
                    code = subprocess.call(
                        ['git', 'checkout', branch],
                        stdout=stdout_file,
                        stderr=stdout_file)
                    print(f"Branch accesado: {branch}")
                    code = subprocess.call(
                        ['git', 'merge', f'upstream/{branch}'],
                        stdout=stdout_file,
                        stderr=stdout_file)
                    if code != 0:
                        print(f"Erro al ejecutar merge para con {branch}")
                        broken = True
                        break
                else:
                    print("Error")
                    broken = True
                    break

    print("====================================")
    with open(file, 'r') as stdout_file:
        print("".join(stdout_file.readlines()))
    print("====================================")
    os.remove(file)

    if not broken:
        subprocess.call(['git', 'checkout', 'env_dev'])
        subprocess.call(['git', 'status'])

if __name__ == "__main__":
    main()
