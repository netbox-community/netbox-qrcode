[<< Back to README start](/README.md)
# Development
## Contributing
Developing tools for this project based on [ntc-netbox-plugin-onboarding](https://github.com/networktocode/ntc-netbox-plugin-onboarding) repo.

Issues and pull requests are welcomed.

## Recommended extensions for VSCode:
With the extension ID you can search for the extension more easily.
- GitHub Pull Request (Extension ID: GitHub.vscode-pull-request-github)
- Docker (Extension ID: ms-azuretools.vscode-docker)
- Python (Extension ID: ms-python.python)
- Python Debugger (Extension ID: ms-python.debugpy)
- Django (Extension ID: batisteo.vscode-django)
- Makefile-Tools (extension ID: ms-vscode.makefile-tools)

## Easy start of the development environment
Take a look at the topic "Makefile" and pay attention to the "Makefile" file in the project to be able to quickly start Netbox with the Docker-Compose.

## Default Login (Netbox, DB, PostgreSQL, Redis)
If the project is started via Docker-Compose, the first login to Netbox is possible with the login data from the makesuperuser.py file.
Other login data for the database, PostgreSQL and Redis can be found in the dev.env file.

Default Netbox Login (When start via Docker-Compose):
- User: admin
- PW: admin

## Debugging with Breakpoint in VSCode
The following describes how to start the debugging mode in VSCode.

*Start Container*
Write "make debug-vscode" without quotation marks in terminal window of VSCode (See also Makefile)
Wait until all containers are started and Starting development server at http://0.0.0.0:8000/ is displayed.

*Start Debug:*
- Go to "Run and Debug" and start the debug "Docker: Python -Django" (The footer of vsCode should become Orang.)
- Set a breakpoint in the code 
- Open the NetBox page with the plugin.
- VSCode will stop at the stopping point.

If you change something in an HTML file, this will be displayed immediately after a reload of the website. If you change something in a *.py file, the web server is automatically restarted after saving the file. It may be advisable to deactivate this in VSCode under File --> Auto Save so that the web server does not restart so often.

*Helpful documentary:*
- https://medium.com/django-unleashed/debug-django-application-in-docker-container-using-vscode-ca5967340262
- https://testdriven.io/blog/django-debugging-vs-code/
- https://github.com/microsoft/debugpy
- https://docs.python.org/3/using/cmdline.html#cmdoption-X

[<< Back to README start](/README.md)