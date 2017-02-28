<?php

require('opencalais.php');
require('parseRtaOpenCalais.php');
require('entitiesToTopics.php');
require('xmltordf.php');

$apikey = "q8e23tj3gvzqx86h8jp882dv";

header('Content-Type: text/html; charset=utf-8');
set_time_limit (0);
$ISO8601 = "Y-m-d\TH:i:sO";
$temp = tempnam(sys_get_temp_dir(), 'evfeed');

$writer = new XMLWriter();
$xmlDoc = new DOMDocument();
//$url = "/Users/JCamilOrt/Documents/Uniandes/2014-II/ProyectoGrado/archivo_feed.rss"
$url = "http://eventos.uniandes.edu.co/controls/cms_v2/components/rss/rss.aspx?sid=1384&gid=26&calcid=8321&page_id=4747"; 
$cache_file = realpath(dirname(__FILE__)) . DIRECTORY_SEPARATOR . 'event_cach3.xml';
$cache_file2 = realpath(dirname(__FILE__)) . DIRECTORY_SEPARATOR . 'producido.xml';



// El servicio de eventos es lentisimo, asi que lo accedemos 1 vez por dia, de resto cache local en tmp.

if (file_exists($cache_file) && (filemtime($cache_file) > (time() - 60 * 60*24 ))) {
$xmlDoc->load($cache_file);
} else {
/*	$ch = curl_init();
$timeout = 0;
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
$data= curl_exec($ch);

file_put_contents($cache_file, $data, LOCK_EX);
curl_close($ch);
*/
//$file = file_get_contents("/Users/JCamilOrt/Documents/Uniandes/2014-II/ProyectoGrado/event_cach3.xml");
//file_put_contents($cache_file, $file, LOCK_EX);
$xmlDoc->load($cache_file);
}


$writer->openURI($cache_file2);   
$writer->startDocument('1.0','UTF-8');   
$writer->setIndent(4);   
$writer->startElement('events');  



$items = $xmlDoc->getElementsByTagName( "item" );
foreach( $items as $item )
{
/*$EventDates = $item->getElementsByTagName( "EventDate" );
$EventDate = $EventDates->item(0)->nodeValue;
$EventDate = str_replace('/', '-', $EventDate);

if(strtotime($EventDate)>strtotime('-30 days')) {
 */ 
	$writer->startElement('event');  


	$Names = $item->getElementsByTagName( "title" );
	$Name = $Names->item(0)->nodeValue;
	if (empty($Name)){
		$Name = "Event";
	}
	$writer->writeElement('title', html_entity_decode($Name,ENT_QUOTES, "utf-8"));
	
  /*$EventDates = $item->getElementsByTagName( "EventDate" );
  $EventDate = $EventDates->item(0)->nodeValue;
  $EventDate = str_replace('/', '-', $EventDate);
  $writer->writeElement('start_date', gmdate($ISO8601, strtotime($EventDate)));

  $EndEventDates = $item->getElementsByTagName( "EndEventDate" );
  $EndEventDate = $EndEventDates->item(0)->nodeValue;
  $EndEventDate = str_replace('/', '-', $EventDate);
  $writer->writeElement('end_date', gmdate($ISO8601, strtotime($EndEventDate)));
	 
  
  $EventDate_Dates = $item->getElementsByTagName( "EventDate_Date" );
  $EventDate_Date = $EventDate_Dates->item(0)->nodeValue;
  
  
  $EventDate_Times = $item->getElementsByTagName( "EventDate_Time" );
  $EventDate_Time = $EventDate_Times->item(0)->nodeValue;*/
  
  $Descriptions = $item->getElementsByTagName( "description" );
  $Description = $Descriptions->item(0)->nodeValue;
  $Description = trim(preg_replace('/\s+/', ' ', $Description));
  $Description = strip_tags($Description);
  $Description = eregi_replace("\.{2,}", "\.", $Description);  
  $writer->writeElement('description', html_entity_decode($Description,ENT_QUOTES, "utf-8"));
 //$writer->writeElement('description', $Description); 

  try{
		  //OBTENGO LOS TEMAS DEL EVENTO DE OPEN CALAIS-->
  	$oc = new OpenCalais($apikey);
  	$entities = $oc->getEntities($Description);
  	$parser = new EntitiesToTopics();
  	$temas = array();
  	$temas = $parser->getTopicsFromEntities($entities);
  	foreach ($temas as $tema ) {
  		$writer->writeElement('isAbout', $tema);
  	}

  }
  catch(Exception $e){
  	echo 'Excepción capturada: ',  $e->getMessage(), "\n";
  }

  //-->LISTO LOS TEMAS	

  /*$Groups = $item->getElementsByTagName( "Group" );
  $Group = $Groups->item(0)->nodeValue;
  
  $Links = $item->getElementsByTagName( "Link" );
  $Link = $Links->item(0)->nodeValue;
  $writer->writeElement('event_url', $Link);
  
  $ThumbnailUrls = $item->getElementsByTagName( "ThumbnailUrl" );
  $ThumbnailUrl = $ThumbnailUrls->item(0)->nodeValue;
  
  */
  if (strpos($Description,'Lugar:') !== false) {
  	$locationArray = array();
  	preg_match_all("/Lugar: (([A-Za-z]*(([ ]+)[A-Za-z0-9]+){1,2})|(((salón|Salón)? *([a-zA-Z]+)[- _][0-9]+)))/", $Description, $locationArray);
  	$Location = $locationArray[0];
  	$locVar = $Location[0];
  	$locVar = str_replace("Lugar: ", "", $locVar);
  	$locVar = sprintf('%s',$locVar);
  	echo "Locacion:________________________________________________________".$locVar;
  	$writer->writeElement('location', $locVar);
  }
  $dateArray = array();

  //TODO llenar con el codigo qe Andres tiene
  preg_match_all("/[0-9]{2}[\/][0-9]{2}[\/][0-9]{4} ([0-9]+:[0-9]{2} [A|P]M)?/", $Description, $dateArray);
  $bothDates = $dateArray[0];
  $startDate = $dateArray[0][0];
  $writer->writeElement('startDate', $startDate);
  $endDate = 'no_end_date';
  if(count($bothDates)>1){
  	$endDate = $dateArray[0][1];
  	$writer->writeElement('endDate', $endDate);
  }
  echo "Start Date: ".$startDate." ---- End Date: ".$endDate;

  /*
   
  $Location_Names = $item->getElementsByTagName( "Location_Name" );
  $Location_Name = $Location_Names->item(0)->nodeValue;
  
  $Location_Directionss = $item->getElementsByTagName( "Location_Directions" );
  $Location_Directions = $Location_Directionss->item(0)->nodeValue;
  
  $Location_Directionss = $item->getElementsByTagName( "Location_Directions" );
  $Location_Directions = $Location_Directionss->item(0)->nodeValue;
	
  $Contact1_Emails = $item->getElementsByTagName( "Contact1_Email" );
  $Contact1_Email = $Contact1_Emails->item(0)->nodeValue;
  if (strpos($Contact1_Email,'[Contact1 Email]') === false) {
	$writer->writeElement('contact_email', $Contact1_Email);
	}
  
  
  $Contact1_First_Names = $item->getElementsByTagName( "Contact1_First_Name" );
  $Contact1_First_Name = $Contact1_First_Names->item(0)->nodeValue;
  if (strpos($Contact1_First_Name,'[Contact1 First Name]') === false) {
	$writer->writeElement('contact_person', $Contact1_First_Name);
	}
  */
	$IDs = $item->getElementsByTagName( "guid" );
	$ID = $IDs->item(0)->nodeValue;
	$ID2 = crc32($ID.$Name.$EventDate.$Description);
	$ID2 = sprintf('%u',$ID2);
	$writer->writeElement('id', $ID);


  //if (strtotime($EventDate) > time() ){ 
	print("SIEGE:" .$ID . ' rdfs:label "' . $Name . '"' . " . \n");  
	print("SIEGE:" .$ID . " rdfs:type SIEGE:Event . \n");  
	print("SIEGE:" .$ID . ' rdfs:comment "' . html_entity_decode($Description,ENT_QUOTES, "utf-8") . '"' . " . \n");  
  //print("SIEGE:" .$ID . " SIEGE:startDateTime " . strtotime($EventDate) . " . \n");  
  //print("SIEGE:" .$ID . " SIEGE:endDateTime " . strtotime($EndEventDate) . " . \n");

  //Registro de temas por OpenCalais
	foreach($temas as $tema)
	{
		print("SIEGE:" .$ID . " SIEGE: isAbout " . $tema . " . \n");
	}  
	print("\n");
	print("\n");
  print("\n"); 	 // } 
  
  $writer->endElement();   
}
//}
$writer->endElement();   
$writer->endDocument();   
//$writer->flush(); 

//XML to RDF Parse
$rdfParser = new XMLtoRDF();
$rdfParser ->parserRDF(realpath(dirname(__FILE__)) . DIRECTORY_SEPARATOR . 'producido.xml');
?>	
