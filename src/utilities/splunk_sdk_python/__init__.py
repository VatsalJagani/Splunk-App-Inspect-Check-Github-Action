
import os
import re
import shutil

import helpers.github_action_utils as utils
from utilities.base_utility import BaseUtility


class SplunkPythonSDKUtility(BaseUtility):

    def _get_splunklib_version(self, file_path):
        try:
            with open(file_path, 'r') as f:
                match = re.search(
                    r"\n__version_info__\s*=\s*([^\n]+)", f.read())
                version = match.group(1)
                return version
        except:
            utils.info("Error with getting the splunklib version.")


    def remove_pycache(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".pyc"):
                    os.remove(os.path.join(root, file))
            for dir in dirs:
                if dir == "__pycache__":
                    shutil.rmtree(os.path.join(root, dir))


    def implement_utility(self):
        utils.info("Adding SplunkPythonSDKUtility")

        splunk_python_sdk_install_path = utils.get_input('splunk_python_sdk_install_path')
        utils.info(f"splunk_python_sdk_install_path: {splunk_python_sdk_install_path}")
        if not splunk_python_sdk_install_path or splunk_python_sdk_install_path == "NONE":
            splunk_python_sdk_install_path = "bin"

        is_remove_pyc_from_splunklib_dir = utils.str_to_boolean_default_true(
            utils.get_input('is_remove_pyc_from_splunklib_dir'))
        utils.info(f"is_remove_pyc_from_splunklib_dir: {is_remove_pyc_from_splunklib_dir}")

        folder_to_install_splunklib = os.path.join(
            self.app_write_dir, splunk_python_sdk_install_path)

        if not os.path.exists(folder_to_install_splunklib):
            os.mkdir(folder_to_install_splunklib)

        os.chdir(folder_to_install_splunklib)

        # Check if splunklib exist already
        already_exist = False
        previous_version = None

        splunklib_dir = os.path.join(folder_to_install_splunklib, 'splunklib')
        init_file = os.path.join(splunklib_dir, '__init__.py')

        print(f"init_file inside code = {init_file}")

        if os.path.exists(splunklib_dir) and os.path.isdir(splunklib_dir) and os.path.isfile(init_file):
            already_exist = True
            previous_version = self._get_splunklib_version(init_file)
            utils.info(f"Previous splunklib version = {previous_version}")

        if already_exist:
            utils.info(
                f"splunklib already present under {folder_to_install_splunklib} directory of the App, upgrading...")
            utils.execute_system_command(
                f'pip install splunk-sdk --upgrade --target "{folder_to_install_splunklib}"')
        else:
            utils.info(
                f"splunklib not present under {folder_to_install_splunklib} directory of the App, installing...")
            utils.execute_system_command(
                f'pip install splunk-sdk --target "{folder_to_install_splunklib}"')

        # Removing .pyc and __pycache__
        if is_remove_pyc_from_splunklib_dir:
            self.remove_pycache(folder_to_install_splunklib)

        new_version = self._get_splunklib_version(init_file)
        utils.info(f"New splunklib version = {new_version}")

        if not already_exist or previous_version != new_version:
            return init_file
