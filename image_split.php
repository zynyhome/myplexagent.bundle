<?php
$mode = 'right';
$imageurl = $_GET['url'];
$mode = $_GET['mode'];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $imageurl); 
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_BINARYTRANSFER, 1);
$data = curl_exec($ch);
curl_close($ch);

$source = imagecreatefromstring($data);

header('Content-Type: image/jpeg');
//imagejpeg($source);

$width = 320;
$height = 180;
$newheight = $height;
if ( $mode == 'right') {
	$x = 170;
	$newwidth = $width - $x;
} else {
	$x = 0;
	$newwidth = 150;
}

$thumb = imagecreatetruecolor($newwidth, $newheight);
$source = imagecreatefromstring($data);
if ( $mode == 'right') {
	imagecopyresized($thumb, $source, 0, 0, $x, 0, $newwidth, $newheight, $width-$x, $height);
} else {
	imagecopyresized($thumb, $source, 0, 0, 0, 0, $newwidth, $newheight, 150, $height);
}
imagejpeg($thumb);
//bool imagecopyresized ( resource $dst_image , resource $src_image , int $dst_x , int $dst_y , int $src_x , int $src_y , int $dst_w , int $dst_h , int $src_w , int $src_h )
?>

