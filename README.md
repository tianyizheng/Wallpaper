# Wallpaper
I've long wanted a lightweight tool to change my wallpaper automatically without taking up much space. This is a collection of python scripts that can be added to the crontab to download them locally or save them on your cloud drive.

Inspired by the Mojave system's dynamic wallpaper, these scripts will have the added functionality to select wallpaper based on your local time.

# Use With Cloud Storage
Execute the scripts below sequentially.

`brightness.py` analyzes the perceived brightness of all images from SimpleDesktops and saves the score to a local sqlite database.

`batchJob.py` is a script that uses `futures` to upload collections of images from [SimpleDesktops](http://simpledesktops.com/) to your NextCloud drive.

`nextcloud.py` grabs a image suitable for your local time from the database and downloads it to your local machine from your cloud hosting.

# Use Locally
The only difference would be that now you wouldn't be having a collection and relies on SimpleDesktop's hosting to be up.

`brightness.py` analyzes the perceived brightness of all images from SimpleDesktops and saves the score to a local sqlite database.

`applyWallpaper.py` grabs a image suitable for your local time from the database and downloads it to your local machine from SimpleDesktop.

# Additional Usage
`sh wallpaper_scheduler add goes.py` or `sh wallpaper_scheduler add applyWallpaper.py`

`simpleDesktop.py` grabs a random image from [SimpleDesktops](http://simpledesktops.com/) and saves to a local buffer. It will override the same image everytime.

`goes.py` grabs the current image of the GOES-16 satellite from [NOAA.gov](noaa.gov), crops it to 16:9 and centers around the atlantic coast.

## Next Steps
- [x] Pre-calcualte brightness of all images, stores to sqlite and analyze
- [x] Update wallpaper from NextCloud
- [x] Upload in batches to NextCloud
- [x] Calcualte the brightness of one image
- [x] Near real time image of the earth
- [x] Update wallpaper based on perceived brightness
- [x] Store original url in sqlite
- [ ] Deploy serverless function to return an image based on time of request
- [ ] Add unsplash support

## Ackowledgement
Spencer Woo's [original script](https://github.com/spencerwoo98/spencer-simple-desktop-api) for his blog.

[CronScheduler](https://unix.stackexchange.com/questions/363376/how-do-i-add-remove-cron-jobs-by-script)
