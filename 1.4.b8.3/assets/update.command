#!/bin/sh
echo ——————————————————
here="`dirname \"$0\"`"
echo "cd-ing to $here"
cd "$here" || exit 1
echo ——————————————————
version=$(head ../../tempfiles/version.txt)
crossfireversion=$(head ../../tempfiles/crossfireversion.txt)
echo Getting version and Crossfire version from respective files.
echo ——————————————————
cd ../../
git clone https://github.com/bcho04/Crossfire $crossfireversion
echo Cloned git files from https://github.com/bcho04/Crossfire.
cd $crossfireversion
cd ../$crossfireversion
mv $crossfireversion ../tempfiles
cd ../
sudo rm -r $crossfireversion
sudo mv tempfiles/$version .
chmod 777 $crossfireversion/start.command
echo ——————————————————
echo Download of Crossfire $crossfireversion finished! Thank you.