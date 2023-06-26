<?php
/*
 * clear all .ogg file in this directory
 */

$files = glob('*.ogg');
foreach($files as $file){
    if(is_file($file))
        unlink($file);
}
?>