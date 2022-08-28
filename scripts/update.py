import json
import os
import shutil
import requests


def main():
    # Paths
    mods_path = './mods/'
    pack_toml_path = './pack.toml'
    override_add_path = './scripts/override_add.json'
    override_remove_path = './scripts/override_remove.json'
    submissions_url = 'https://platform.modfest.net/submissions'

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
        os.system('packwiz mr add ' + (mod['slug'] if 'version_id' not in mod else 'https://modrinth.com/mod/' + mod['slug'] + '/version/' + mod['version_id']) + ' -y')

    for mod in overrides_remove:
        os.system('packwiz remove ' + mod['slug'])

    # Prompt
    print('Update complete! Next Steps:')
    print('1. CTRL+F for \"fail\" in the log')
    print('2. Bump pack version in pack.toml')
    print('3. `packwiz serve` and smoke test using local client+server')
    print('5. commit and push')
    print('6. smoke test using production client+server')


if __name__ == "__main__":
    main()
