var cbbc= doc("consololidado_bbc.xml");

var cwired = doc("consololidado_wired.xml");

function prueba1(){
	for $x in doc("consololidado_wired.xml")/item
		where $x/title[contains(.,'Cape')]
		order by $x/title
		return $x/title
}

resultP = prueba1;