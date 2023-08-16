# splunk-app-action
Github Action to automatically generate Splunk App and Add-on builds, run app-inspect checks (with the App-Inspect/Splunkbase API) on commit/push etc on GitHub repo. It also performs Splunk cloud checks.


## Capabilities & Usage

* You can get more information about GitHub workflow files [here](https://docs.github.com/en/actions/learn-github-actions/workflow-syntax-for-github-actions). As this document will not go in detail about it.


### Generate Splunk App/Add-on Build artifact
* The action automatically generates build artifact from github repo.
* Change file and directory permissions to avoid app-inspect failures.

```
- uses: VatsalJagani/splunk-app-action@v2
    with:
    app_dir: "my_app"
```
    * Here even app_dir is optional parameter if you want to generate the build.
    * See details about the inputs options under the `Inputs` section.


* Supports multiple Apps/Add-ons in single repository.
    ```
    - uses: VatsalJagani/splunk-app-action@v1
        with:
        app_dir: "my_splunk_app"

    - uses: VatsalJagani/splunk-app-action@v1
        with:
        app_dir: "my_splunk_add-on"
    ```

* #### Running Commands Before Generating App Build
    * If you wish to run the commands before generating the App build, set the environment variables `SPLUNK_APP_ACTION_<n>`.
        ```
        - uses: VatsalJagani/splunk-app-action@v1
            env:
            SPLUNK_APP_ACTION_1: "find my_app -type f -name *.sh -exec chmod +x '{}' \\;"
            with:
            app_dir: "my_app"
        ```
        * Above use-case is very common as if your App/Add-on has shell scripts in bin directory and you want to make sure it has executable permission.
        * Run the command in the context of your repo's root directory. (Assume current working directory is your repo's root directory.)
        * Maximum 100 commands can be executed. So from `SPLUNK_APP_ACTION_1` to `SPLUNK_APP_ACTION_99`.
        * The command will be executed in incremented order from `SPLUNK_APP_ACTION_1` to `SPLUNK_APP_ACTION_99`.

    * It allows you to run command before building the App build.
        * This could be useful if you wish to remove some files that you don't want in the build, change permission of some files before running the rest of the app build or app-inspect check.


### Run App-Inspect (with Splunkbase API)
* It runs app-inspect with Splunkbase API.
    * Past Story: I've tried to use CLI version of the App-inspect check, I've also tried to use github action with CLI version from Splunk, but all fails as they are always way behind the Splunkbase API. Hence you end up failing the checks when you try to upload a new version of Splunkbase.
* This is the automation of Splunkbase API or postman version of App-inspect checks.
* Fails the GitHub workflow if there is failure or error in App-inspect check or Cloud checks.

* It will generate the `reports in HTML format` and put it as `GitHub artifact`. You will find them under `Actions` tab in your repository.

* It also performs Splunk Cloud checks and SSAI checks for Splunk Cloud

* It requires to set inputs: splunkbase_username and splunkbase_password.

```
- uses: VatsalJagani/splunk-app-action@v2
    with:
        app_dir: "my_app"
        splunkbase_username: ${{ secrets.SPLUNKBASE_USERNAME }}
        splunkbase_password: ${{ secrets.SPLUNKBASE_PASSWORD }}
```


### Utilities
* Following are utilities provided by the splunk-app-action.
* Utilities make code changes in your repositories and create PR for you to view and merge if you deem ok.
* In order to do that all utilities require common input called `my_github_token`.


#### Utility that adds information about the App inside the README.md file
* The splunk-app-action has utility which automatically adds information about the App, like how many alerts does it have, how many dashboards does it have, etc inside the App's README.md file.
```
- uses: VatsalJagani/splunk-app-action@v2
    with:
        app_dir: "my_app"
        app_utilities: "whats_in_the_app"
        my_github_token: ${{ secrets.MY_GITHUB_TOKEN }}
```

#### Add Python Logger
* Auto adds python logger manager, including python file necessary, props.conf to assign right sourcetype for it under the internal logs.

```
- uses: VatsalJagani/splunk-app-action@v2
    with:
        app_dir: "my_app"
        app_utilities: "logger"
        my_github_token: ${{ secrets.MY_GITHUB_TOKEN }}
        logger_log_files_prefix: "my_app"
        logger_sourcetype: "my_app:logs"
```

#### Add Splunklib or Splunk SDK for Python and Auto Upgrades It
* This utility adds the splunklib or Splunk SDK for Python to the App and auto upgrades it whenever new version is available.

```
- uses: VatsalJagani/splunk-app-action@v2
    with:
        app_dir: "my_app"
        app_utilities: "splunk_python_sdk"
        my_github_token: ${{ secrets.MY_GITHUB_TOKEN }}
```

#### Add Common JavaScript Utilities File
* This utility adds a JavaScript file that contains commonly used functionality for a JavaScript code for a Splunk App.

```
- uses: VatsalJagani/splunk-app-action@v2
    with:
        app_dir: "my_app"
        app_utilities: "common_js_utilities"
        my_github_token: ${{ secrets.MY_GITHUB_TOKEN }}
```


## Inputs

#### app_dir
* description: "Provide app directory inside your repository. Do not provide the value if the repo's root directory itself if app directory."
* required: false
* default: ".", meaning root folder of the repository.

#### is_generate_build
* description: "Whether to generate the App Build or not."
* required: false
* default: true

#### to_make_permission_changes
* description: "Whether to apply file and folder permission changes according to Splunk App Inspect expectation before generating the build."
* required: false
* default: true

#### is_app_inspect_check
* description: "Whether to perform the Splunk app-inspect checks or not. This would include cloud-inspect checks as well."
* required: false
* default: true

#### splunkbase_username
* description: "Username required to call the Splunkbase API for App-Inspect. Required when is_app_inspect_check is set to true."
* required: false

#### splunkbase_password
* description: "Password required to call the Splunkbase API for App-Inspect. Required when is_app_inspect_check is set to true. Strongly recommend to use via GitHub secrets only and specify like `{{secrets.MY_SPLUNK_PASSWORD}}`."
* required: false

#### app_build_path
* description: "Full App build path. Used only when is_generate_build is set to false."
* required: false

#### app_utilities
* description: "Add comma separated list of utilities to use. You need to enable read and write permission for workflow to create Pull Requests. Valid options: whats_in_the_app, logger, splunk_python_sdk, common_js_utilities"
* required: false
* default: "", meaning no utilities

#### my_github_token
* description: "GitHub Secret Token to automatically create Pull request. (Make sure to put it in the Repo secret on GitHub as `MY_GITHUB_TOKEN` and then use it like `{{ secrets.MY_GITHUB_TOKEN }}`. Do not write it in plain text.) Only required if app_utilities is being used."
* required: false

#### default_branch_name
* description: "It auto detects the default branch, but if you want to use different branch then write branch name in this input. This branch will be used to create new branch and create PR."
* required: false

#### logger_log_files_prefix
* description: "Log files prefix. Only required for logger utility."
* required: false

#### logger_sourcetype
* description: "Sourcetype for the internal app logs. Required only for logger utility."
* required: false



## Troubleshooting
* You see below error on GitHub workflow with action.

    ```
    Unable to push changes into the branch=splunk_app_action_bbe00a4a32a796cc84b73b09abc09922
    ```

    * Enable GitHub workflow to create pull request.
    * Go to your Repo `Setting` > `Actions` > `General`.
        * ![Workflow Permission 1](/images/workflow_permission_for_pr_1.png)
    * Enable read and write permission under `Workflow permissions`.
        * ![Workflow Permission 2](/images/workflow_permission_for_pr_2.png)


## Examples
* **Cyences App for Splunk**
  * Has App and Add-on in the same repo.
  * Uses user defined command execution before generating the Add-on build. (To give executable permissions to bash (`.sh`) files in the Add-on automatically.)
  ![image](/images/cyences_workflow_3.PNG)
  * Executes workflow action whenever a new pull request is created. It also runs on any changes to `master` branch.
  ![image](/images/cyences_workflow_1.PNG)
  * [Splunkbase App](https://splunkbase.splunk.com/app/5351/)
  * [Splunkbase Add-on](https://splunkbase.splunk.com/app/5659/)
  * [Workflow file](https://github.com/VatsalJagani/Splunk-Cyences-App-for-Splunk/blob/master/.github/workflows/main.yml)
[](images/cyences_workflow.png)


* **3CX PhoneSystem App**
  * Has github repo's root directory as the App's root directory.
  * Executes on all changes in all branches. Also, option to manually execute the workflow from GitHub UI.
  ![image](/images/3cx_app_workflow.PNG)
  * [Workflow file](https://github.com/VatsalJagani/Splunk-3CX-App/blob/master/.github/workflows/main.yml)


* **Sample run app-inspect checks directly on previously generated build**
  * ![image](/images/sample_to_use_on_already_generated_build.PNG)


* **MaxMind Database Auto Update App**
  * Removing unnecessary files from build.
    ![image](/images/max_mind_database_update_app_workflow.PNG)
  * [Workflow file](https://github.com/VatsalJagani/Splunk-App-Auto-Update-MaxMind-Database/blob/master/.github/workflows/main.yml)


* **Lansweeper App and Add-on**
  * [Workflow file](https://github.com/VatsalJagani/Splunk-Integration-for-Lansweeper/blob/master/.github/workflows/main.yml)



## Contribute
* If you are developer and want to contribute to this project, please submit a Pull Request.
* If you find a bug or have a request for enhancement, create a Github Issue in this project.
* If you wish to share Feedback or success story, please add comment in [this issue](https://github.com/VatsalJagani/splunk-app-action/issues/19).


# TODO - Update screenshots and/or provide link
# TODO - examples to update.
