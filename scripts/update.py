import json
import os
import shutil
import requests
import time
import subprocess


def packwiz_pretty_print(command, ignore_errors=False):
    try:
        output = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as err:
        output = err.output
        if not ignore_errors:
            print("Failed! - packwiz output:")
            print(output.decode('UTF-8').splitlines())
            return False

    lines = output.decode('UTF-8').splitlines()
    line_iter = iter(lines)
    for line in line_iter:
        if line.lower().startswith('dependency'):
            print("Installing " + line)
        elif line.lower().startswith('dependencies found'):
            while not next(line_iter, None).lower().startswith('would you like to'):
                pass
        elif line.lower().startswith(('found mod', 'finding dependencies', 'all dependencies', 'loading modpack', 'removing mod', 'you don\'t have this mod')):
            pass
        else:
            print(line)
    return True


def main():
    # Constants
    mods_path = './mods/'
    pack_toml_path = './pack.toml'
    override_add_path = './scripts/override_add.json'
    override_remove_path = './scripts/override_remove.json'
    submissions_url = 'https://platform.modfest.net/submissions'
    min_install_time = 0.6

    # Change working directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    os.chdir('../')

    # Check working directory
    if not os.path.exists(pack_toml_path):
        print("Couldn't find pack.toml - make sure you're running this from the pack directory!")
        return

    # Assert empty mods folder

    if os.path.exists(mods_path):
        shutil.rmtree(mods_path)
        os.makedirs(mods_path)

    # Refresh to keep log clean
    os.system('packwiz refresh')

    # Retrieve submissions for slugs and versions
    submissions = requests.get(submissions_url).json()

    # Retrieve override slugs and versions
    with open(override_add_path, 'r') as overrides_file:
        overrides_add = json.load(overrides_file)

    with open(override_remove_path, 'r') as overrides_file:
        overrides_remove = json.load(overrides_file)

    # Install mods based on slugs and versions
    for mod in overrides_add + submissions:
        before_time = time.time()
        if not packwiz_pretty_print('packwiz mr add ' + (mod['slug'] if 'version_id' not in mod else 'https://modrinth.com/mod/' + mod['slug'] + '/version/' + mod['version_id']) + ' -y'):
            print('Update failed. Please see above for error.')
            return
        elapsed_time = time.time() - before_time
        time.sleep(0 if elapsed_time >= min_install_time else min_install_time - elapsed_time)

    for mod in overrides_remove:
        packwiz_pretty_print('packwiz remove ' + mod['slug'], ignore_errors=True)

    # Copy in overriding jar files, you heretic
    shutil.copytree('./scripts/overrides', './mods', dirs_exist_ok=True)  # Python 3.8 :pineapple:

    # Prompt
    print('Update successful! Next Steps:')
    print('1. Bump pack version in pack.toml')
    print('2. `packwiz serve` and smoke test using local client+server')
    print('3. commit and push')
    print('4. smoke test using production client+server')


if __name__ == "__main__":
    main()
