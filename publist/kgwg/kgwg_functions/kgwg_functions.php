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
  //$file_name = './publications/kgwg_publications_'.$attrs['year'].'_ol.html';
  //$pub_year = $attrs['year'];
  $no_short = True;
  $pub_year = wpb_kgwg_pub_year();
  $file_name = './publications/kgwg_publications_'.$pub_year.'_full.html';
  $myfile = fopen($file_name, "r");
  if (!$myfile) {
    $message = "<h1>Not available collaboration publication list for Year ".$pub_year.".</h1><hr> Unable to open file [".$file_name."]!<br>";
    if ($no_short) {
      $message .= "You may need to run /publications/mk_pub_list.sh script.";
      return $message;
    }
  }
  else {
    $content = fread($myfile,filesize($file_name));
    fclose($myfile);
    $message = '<h1>Collaboration Papers</h1>';
    $message .= $content;
    //$message .= "<div class=\"wp-block-file\"><a href=\"https://www.kgwg.org/publications/kgwg_publications_".$pub_year."_full.bib\" class=\"wp-block-file__button wp-element-button\" download>Downlaod bib</a></div>";
    $message .= "<div class=\"wp-block-file\"><a href=\"".home_url( $wp->request )."/publications/kgwg_publications_".$pub_year."_full.bib\" class=\"wp-block-file__button wp-element-button\" download>Downlaod bib</a><a href=\"".home_url( $wp->request )."/publications/kgwg_publications_".$pub_year."_full.pdf\" class=\"wp-block-file__button wp-element-button\" download>Downlaod pdf</a></div>";
    if ($no_short) {
      return $message;
    }
  }

  // set the following variable to be True, if you want to separated short author paper list
  $separated = False;
  if (! $separated) {
  // list in the same page
    $file_name = './publications/kgwg_publications_'.$pub_year.'_short.html';
    $myfile = fopen($file_name, "r");
    if (!$myfile) {
      $message .= "Unable to open file [".$file_name."]!<br>";
      $message .= "You may need to run /publications/mk_pub_list.sh script.";
      return $message;
    }
    $content = fread($myfile,filesize($file_name));
    fclose($myfile);
    $message .= '<h1>GW Short-authored Papers</h1>';
    $message .= $content;
  }
  else {
  // using separate short author pages
    $message .= '<h1><a href="'.home_url( $wp->request ).'/gw-short-authored-papers/?pub_year='.$pub_year.'">GW Short-authored Paper List</a></h1>';
  }

  return $message;
}
add_shortcode('publications', 'wpb_kgwg_publications');

function wpb_kgwg_get_query() {
  //$queries = array();
  //parse_str($_SERVER['QUERY_STRING'], $queries);
  //$size = sizeof($queries);
  //$message = "query size : ".$size;
  //for ($n=0; $n < $size; $n++) {
  //  $message .= queries[$n];
  //}
  $message = "";
  $year = "";
  if ( isset( $_GET['pub'] )) {
    $year .= $_GET['pub'];
    $message .= "Year = ".$year;
  }
  return $message;
}
add_shortcode('get_query', 'wpb_kgwg_get_query');

function wpb_kgwg_list_years($attrs) {
  $s_year = $attrs['start'];
  $e_year = $attrs['end'];
  $c_year = date("Y");
  if ((int)$c_year > (int)$e_year) {
    $e_year = $c_year;
  }
  // simple <ul>
  //$message = "<ul>";
  //for ($y=(int)$s_year; $y <= (int)$e_year; $y++) {
  //  $message .= "<li><a href=\"/list-of-publications-for-kgwg-in-year-2018/?pub_year=".$y."\">Year ".$y."</a></li>";
  //}
  //$message .= "</ul>";
  // using table
  $columns = 8;
  //$message = "<table class='pub_years'> <tbody>";
  $message = "<table id='customers'> <tbody>";
  $count = 0;
  for ($y=(int)$s_year; $y <= (int)$e_year; $y++) {
    if ($count==0) {
      //$message .= "<tr class='pub_years pub_tr'>";
      $message .= "<tr>";
    }
    else if ($count%$columns == 0 and $y < (int)$e_year) {
      //$message .= "</tr><tr class='pub_years pub_tr'>";
      $message .= "</tr><tr>";
    }
    else if ($count%$columns == 0) {
      $message .= "</tr>";
    }
    $message .= "<td><a href=\"/list-of-publications-for-kgwg-in-year-2018/?pub_year=".$y."\">Year ".$y."</a></td>";
    $count++;
  }
  if ($count%$columns != 0) {
      $message .= "</tr>";
  }
  $message .= "</tbody></table>";
  return $message;
}
add_shortcode('list_years', 'wpb_kgwg_list_years');

function wpb_kgwg_pub_year() {
  $year = "";
  if ( isset( $_GET['pub_year'] )) {
    $year .= $_GET['pub_year'];
  }
  return $year;
}
add_shortcode('pub_year', 'wpb_kgwg_pub_year');

function wpb_kgwg_change_title_short() {
  $year = wpb_kgwg_pub_year();
  if ($year == "") {
    $year = date("Y");
  }
  $message = '<script>document.getElementById("intro-core-wrap").innerHTML="<h1 class=\"page-title\">List of GW Short-authored Papers for KGWG in year '.$year.'</h1>";</script>';
  return $message;
}
add_shortcode('change_title_short', 'wpb_kgwg_change_title_short');

function wpb_kgwg_change_title() {
  $year = wpb_kgwg_pub_year();
  if ($year == "") {
    $year = date("Y");
  }
  $message = '<script>document.getElementById("intro-core-wrap").innerHTML="<h1 class=\"page-title\">List of Collaboration Papers for KGWG in year '.$year.'</h1>";</script>';
  return $message;
}
add_shortcode('change_title', 'wpb_kgwg_change_title');

function wpb_kgwg_redirect_current() {
  $year = date("Y");
  $message = '<script>window.location.href = "https://www.kgwg.org/list-of-publications-for-kgwg-in-year-2018/?pub_year='.$year.'"</script>';
  return $message;
}
add_shortcode('redirect_current', 'wpb_kgwg_redirect_current');

function wpb_kgwg_add_bootstrap() {
  // Register style & scripts
  //wp_register_style('kgwg-bootstrap-style', 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css');
  //wp_register_script('kgwg-bootstarp-script', 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js', array(), '0.1', true);
  //wp_register_style('kgwg-bootstrap-style', '/wp-content/kgwg/kgwg_css/bootstrap.min.css');
  //wp_register_script('kgwg-bootstarp-script', '/wp-content/kgwg/kgwg_js/bootstrap.bundle.min.js', array(), '0.1', true);
  wp_register_style('kgwg-bootstrap-style', '/wp-content/kgwg/kgwg_css/kgwg_styles.css');

  // Enqueue kgwg styles & scripts
  wp_enqueue_style('kgwg-bootstrap-style');
  //wp_enqueue_script('kgwg-bootstrap-script');
}
add_action('wp_enqueue_scripts', 'wpb_kgwg_add_bootstrap');
