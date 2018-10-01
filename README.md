# Wallpaper
I've long wanted a lightweight tool to change my wallpaper automatically without taking up much space. This is a collection of python scripts that can be added to the crontab to download them locally or save them on your cloud drive.

# Usage
`sh wallpaper_scheduler add goes.py` or `sh wallpaper_scheduler add simpledesktop.py`

`simpleDesktop.py` grabs a random image from [SimpleDesktops](http://simpledesktops.com/) and saves to a local buffer. It will override the same image everytime.

`goes.py` grabs the current image of the GOES-16 satellite from [NOAA.gov](noaa.gov), crops it to 16:9 and centers around the atlantic coast.

`batchJob.py` is a script that uses `futures` to upload collections of images from [SimpleDesktops](http://simpledesktops.com/) to your NextCloud drive.

## Next Steps
- [x] Pre-calcualte brightness of all images, stores to sqlite and analyze
- [ ] Update wallpaper from NextCloud
- [x] Upload in batches to NextCloud
- [x] Calcualte the brightness of one image
- [x] Near real time image of the earth

## Ackowledgement
Spencer Woo's [original script](https://github.com/spencerwoo98/spencer-simple-desktop-api) for his blog.

[CronScheduler](https://unix.stackexchange.com/questions/363376/how-do-i-add-remove-cron-jobs-by-script)
