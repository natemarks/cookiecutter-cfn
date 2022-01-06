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
        #  check taskcat file
        taskcat_cfg = host.file(role_dir + '/.taskcat.yml')
        assert taskcat_cfg.exists
        assert taskcat_cfg.contains('name: cfn-'+str(ccinput["module_name"]))
        #  check create_and_teardown.sh
        create_and_teardown = host.file(role_dir + '/scripts/create_and_teardown.sh')
        assert create_and_teardown.exists
        assert create_and_teardown.contains('STACK_NAME="deleteme-cfn-'+str(ccinput["module_name"]))
        #  check create_and_teardown.sh
        create_only = host.file(role_dir + '/scripts/create_only.sh')
        assert create_only.exists
        assert create_only.contains('STACK_NAME="deleteme-cfn-'+str(ccinput["module_name"]))
        #  check Makefile
        makefile = host.file(role_dir + '/Makefile')
        assert makefile.exists
        assert makefile.contains('PROJECT := cfn-'+str(ccinput["module_name"]))
