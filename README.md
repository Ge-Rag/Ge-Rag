If you ever downloaded midi files from the internet then you'll find that
most of them have a cryptical name that does not say much about the file.

Most of the files however have a title embedded. 

I have written python script to mass rename such files based on the embedded
title. The script can be executed interactively or in auto mode.

It is written for linux but can be easily adapted for Windows as well.

I have included a filename checker so that not all kinds of characters end
up in the filename. Linux is very tolerant as to what a filename can contain
however Windows is not.

Basically names are renamed to the title embedded in the file but in the
interactive mode you can change each one as you go along.

Spaces in the filename are converted to underscores, which for me was more
convenient. However if you want to avoid this then you have to tweak the
function get_valid_filename()

Existing files are not overwritten.
