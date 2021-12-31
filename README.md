This cookiecutter template is used to start cloudformation module projects. The important features of the template project are:

make lint : run aws cloudformation validate-template against the project templates


make test  : tuns taskcat to test the template files directly

The limitation of task cat is that it doesn't really pause to let you look at the stack. To address that problem, I added scripts/run_tests.sh. This script runs the template directly.  It pauses for manual inspection when the stack is built, then deletes the stack.


TODO:
The next challenge is using test stacks.  As an example, the cfn-vpc project has a stack template that just creates a VPC.  You can't really test it without  attaching hosts to the subnets, though.  So i need to create a standard way to test/run nested stacks. This means that I have to figure out some naming to keep the various versions of template files unique (probably the  git commit). Then I need to upload the stacks to a bucket and pass the bucket url to  a root stack which then calls the stack under test. So  my root stack would call the vpc stack and use the vpc stack output to spin up an EC2 instance to actually test the various subnets.