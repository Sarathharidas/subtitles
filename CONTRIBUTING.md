## Development Environment Setup
I use `conda` as my [python package and environment manager](https://www.sianbrooke.co.uk/dr-brookes-blog/coding-in-python-managing-packages-with-conda-and-pip) and so the setup instructions here uses conda. If you have an alternative preference, then please consider contributing to the CONTRIBUTING.md page. 

### Pre-requisites:
*  Cloned copy of the repository on your local machine.
*  [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installation at a preferred location. Here the default location is assumed to be the root directory. Generally on `/Users/<username>`
  
Before installing the packages required for this project, you'll need to make sure that your conda is configured to allow for maximum flexibility to resolve any dependency related conflicts. 

Learn more about conda configuration file [here](https://conda.io/projects/conda/en/latest/user-guide/configuration/use-condarc.html) or type `conda config -h` on your terminal.

Here's the conda config file or **~/.condarc** that's worked for me:

```yaml
restore_free_channel: true
report_errors: false
ssl_verify: false
auto_activate_base: false
channels:
  - defaults
  - pypi
  - conda-forge
channel_priority: true

```

At this point, change directory to local copy of the cloned repository and run the following command:

```bash
conda env create -n <env_name> --file environment.yml
```
where `<env_name>` is the environment name you'd like to use.

If you run into errors, don't hesitate to open an issue or a PR with a suggested fix!
