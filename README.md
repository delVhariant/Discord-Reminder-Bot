# A Simple Reminder bot for Docker

## Installation
For both docker and native, you must first create a .env file with your discord token:  
```echo DISCORD_TOKEN=TOKEN > .env```

### Docker
Compose file is provided for ease of use.  
```docker compose up -d```

### Native
Probably be to create a virtual env to prevent package issues.
```python3 -m venv bot-env
source bot-env/bin/activate
pip3 install -U requirements.txt
python3 bot.py
```

## Usage
Following commands are provided:
### !rem-create
Usage: `!rem-create <USER> <INTERVAL> <REMINDER>`

* USER should be an @mention of the target user  
    * ie: @myname
* INTERVAL should be wrapped in quotes and requires a datetime in format dd/mm/yyyy hh:mm and the recurrence interval (daily, weekly, monthly)
    * ie: "26/6/2022 9:00 daily" to remind at 9am daily.  
* REMINDER should be wrapped in quotes and is the reminder message
    * ie: "Take medicine"  

### !rem-list
Usage: `!rem-list`

Lists all reminders

### !rem-pause
Usage: `!rem-pause <ID>`
* ID is an integer and can be found from running !rem-list.
* Paused reminders will not execute

### !rem-unpause
Usage: `!rem-unpause <ID>`
* ID is an integer and can be found from running !rem-list.
* Unpausing a reminder will cause it to execute again.

### !rem-stop
Usage: `!rem-stop <ID>`
* Deletes a reminder from the db
* Reminders cannot be recovered
* ID is an integer and can be found from running !rem-list.


