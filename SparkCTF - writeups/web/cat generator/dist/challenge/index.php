<?php 

function clean_pic($pic){
     $blacklist = ['filter','resource','php','base64','flag','flag.txt'];
     
     foreach ($blacklist as $x){
          if (str_contains($pic, $x)) { 
               $pic = preg_replace('/'.$x.'/i','',$pic);
         }
     }
     return $pic;
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>cat gallery (ꏿ ᆺ ꏿ) </title>
</head>
<body>
<center>
     <p  style="font-family:Arial;font-size:50px"> Cat Generator  (ꏿ ᆺ ꏿ) </p>
     <p  style="font-family:Arial;font-size:25px">Refresh to get a new picture :3</p><br>
<p>🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈</p>

<?php
 if (isset($_GET['pic']) ) {  

     $p = $_GET['pic']; 
     $clean = clean_pic($p);
     if (str_starts_with(file_get_contents($clean),'SparkCTF{')){
          echo "<p> HAX! </p>"  ;
          exit();
          die();
     }
echo "<img width='600' height='600' src='data:image/png;base64," .base64_encode(file_get_contents($clean)) ."' >"; 
}else{
echo  "<img width='600' height='600' src='data:image/png;base64," . base64_encode(file_get_contents('./cats/cat'.rand(1,10).'.jpg')) ."' >"; 
}

 ?> 
 <p>🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈🐈</p>
</center>
</body>
</html>