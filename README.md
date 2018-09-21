# Wallpaper
I've long wanted a lightweight tool to change my wallpaper automatically without taking up much space.

This script grabs a random image from [SimpleDesktops](http://simpledesktops.com/) and saves to a local buffer. It will override the same image everytime. You can put `python wallpaper.py` in your crontab to automate the changing.

## Next Step
1. I want a script that pre-calculates the "perceived brightness" and saves them locally in sqlite. This way I can skip the bright ones at night.

2. I should upload the new wallpapers to my nextcloud drive.


## Ackowledgement
Spencer Woo's [original script](https://github.com/spencerwoo98/spencer-simple-desktop-api) for his blog.

[CronScheduler](https://unix.stackexchange.com/questions/363376/how-do-i-add-remove-cron-jobs-by-script)