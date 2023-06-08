<?php
/**
 * Setup theme functions for Consulting.
 *
 * @package ThinkUpThemes
 */

// function that runs when shortcode is called
function wpb_demo_shortcode() { 
  
// Things that you want to do.
$message = 'Hello world!<br>'; 
  
// Output needs to be return
return $message;
}
// register shortcode
add_shortcode('greeting', 'wpb_demo_shortcode');

function wpb_kgwg_list($attrs) {
  $num = $attrs['num'];
  $delta = $attrs['delta'];
  $message = '<h1>List content</h1>';
  $message .= '<ol>';
  for ($x=0; $x <= $num; $x += $delta) {
    $message .= '<li>Number is '.$x.'</li>';
  }
  $message .= '</ol>';
  return $message;
}
add_shortcode('mklist', 'wpb_kgwg_list');

function wpb_kgwg_publications($attrs) {
  $file_name = './publications/kgwg_publications_'.$attrs['year'].'_ol.html';
  $myfile = fopen($file_name, "r");
  if (!$myfile) {
    $message = "Unable to open file [".$file_name."]!";
    return $message;
  }
  $content = fread($myfile,filesize($file_name));
  fclose($myfile);
  //$num = 6;
  //$delta = 2;
  $message = '<h1>Full Author Publications</h1>';
  $message .= $content;
  //$message .= '<ol>';
  //$message .= $file_name;
  //for ($x=0; $x <= $num; $x += $delta) {
  //  $message .= '<li><a href="https://ui.adsabs.harvard.edu/#abs/2018mgm..conf.3170O/abstract" target="_blank">Development of KAGRA Algorithmic Library (KAGALI)</a></li>';
  //}
  //$message .= '</ol>';
  return $message;
}
add_shortcode('publications', 'wpb_kgwg_publications');
