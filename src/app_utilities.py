
import os
import shutil
import helper_github_action as utils
from utilities.whats_inside_app import WhatsInsideTheAppUtility
from utilities.logger import LoggerUtility
from utilities.splunk_sdk_python import SplunkPythonSDKUtility
from utilities.common_splunk_js_utilities import CommonJSUtilitiesFile


class SplunkAppUtilities:
    def __init__(self, is_test=False) -> None:
        self.is_test = is_test
        # Get Inputs
        app_utilities = utils.get_input('app_utilities')
        if not app_utilities or app_utilities == "NONE" or app_utilities == "":
            self.app_utilities = []
        else:
            app_utilities = app_utilities.split(',')
            app_utilities = [u.strip() for u in app_utilities]

        os.chdir(utils.CommonDirPaths.MAIN_DIR)
        # copy folder to generate build, rather than affecting the original repo checkout
        utils.execute_system_command("rm -rf repodir_for_utilities")
        shutil.copytree('repodir', 'repodir_for_utilities')

        self.add_utilities(app_utilities)


    def add_utilities(self, app_utilities):
        utils.info(f"Adding utilities: {app_utilities}")
        for utility in app_utilities:
            if utility == "whats_in_the_app":
                WhatsInsideTheAppUtility()

            elif utility == "logger":
                LoggerUtility()

            elif utility == "splunk_python_sdk":
                SplunkPythonSDKUtility()

            elif utility == "common_js_utilities":
                CommonJSUtilitiesFile()

            else:
                utils.error("utility={} is not supported.".format(utility))
