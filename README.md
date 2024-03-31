# Ready Bot
Version 2.0 Ready Player Bot with Slash Commands

## Setup

Get discord server token and place into '.env' file in the root as:
```TOKEN=<Server Token>```

Start Server on Windows

```py bot.py```

Start Server on Ras Pi

```python3 bot.py```

Adding program to rc.local

```sudo nano /etc/rc.local/```

Add the following

```cd /home/ben2c/projects/ready-bot```
```python3 main.py```

Note: Ensure to install all dependencies under sudo

## Features/Fixes to Implement

1. Ensure that once queues are cleared, the timer is also reset.
2. Show the remainder time on players
