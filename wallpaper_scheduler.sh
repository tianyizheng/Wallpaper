crontab -l > tempcron
echo "*/20 * * * * `which python` `pwd`/wallpaper.py > /dev/null" >> tempcron
crontab tempcron
rm tempcron
