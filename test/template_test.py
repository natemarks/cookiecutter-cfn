"""Test variou executions of the cookiecutter
Each parametrize test case is a set of cookiecutter json overrides

"""
import logging
import os
import pytest
import testinfra  # pylint: disable=W0611
from cookiecutter.main import cookiecutter

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

PROJECT_DIR = os.getcwd()


@pytest.mark.parametrize(
    "ccinput",
    [
        (
            {
                "module_name": "fff",
                "github_user": "natemarks",
                "author": "Nate Marks"
            }),
        (
            {
                "module_name": "ggg",
                "github_user": "iainbanks",
                "author": "Iain M. Banks"
            }),
    ],
)
class TestClass:  # pylint: disable=R0903
    """Table test the cookiecutter options"""

    def test_(
        self, host, tmp_path, ccinput
    ):  # pylint: disable=R0201
        """Iterate on different cookiecutter json overrides"""
        role_dir=str(tmp_path) + "/" + "cfn-" + ccinput["module_name"]
        os.chdir(tmp_path)
        log.info("tmpdir: %s", str(tmp_path))
        cookiecutter(
            PROJECT_DIR,
            no_input=True,
            extra_context=ccinput,
        )
        #  check env file
        taskcat_cfg = host.file(role_dir + '/.taskcat.yml')
        assert taskcat_cfg.exists
        assert taskcat_cfg.contains('name: cfn-'+str(ccinput["module_name"]))
