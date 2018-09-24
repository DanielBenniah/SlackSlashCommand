# SlackSlashCommand
Slash Commands for Slack with local server (python, flask)

## Steps to follow

1. Ensure that Python version 3.6 is installed.
2. Run node-v8.12.0-x64.exe
3. Run requirements_lt.bat and requirements_py.bat
4. Run server.bat
5. Edit ConnectToInternet.bat and replace <custom_subdomain> with a name of your choice. Run ConnectToInternet.bat
	Make sure the prompt reads "https://<custom_subdomain>.localtunnel.me/"

6. In the command prompt run the following

> python --version

> npm --version

> lt --version

Ensure that the levels are equal or higher than the following

> Python version 3.6.6

> Nnpm version 6.4.1

> npm localtunnel version 1.9.1
	
## Slash Commands
### /shorturl <Long URL>
	Shortens a given URL
	Example: /shorturl http://facebook.com
	
### /definition <word>
	Returns the definition of a word
	Example: /definition integrate
	
### /rps <rock/papers/scissors>
	Play Rock, Papers, Scissors with the computer!
	Example: /rps rock
	
### /thumbsup
	Provide feedback on the slash commands
	Example: /thumbsup

## Log Messages

All log messages will be sotred in logs.log and all error messages will be stored in errors.log

## Troubleshooting common errors

#### Time_out_error:
	Please check if "ConnectToInternet" and "Server" are up and running. Ensure that "ConnectToInternet" prompt displays 
	"https://<custom_subdomain>.localtunnel.me/". Run the commmand again. If error persists, restart both "ConnectToInternet" and 
	"Server"
	
#### 404_Error:
	Occurs when "ConnectToInternet" does not display "https://<custom_subdomain>.localtunnel.me/". It means the local server connects
	to the internet, but through a different address. Restart the "ConnectToInternet" batch file.
	
#### Error_when_receiving_message_from_peers:
	Common error when receiving message from local server. Re-run the command.
	 
