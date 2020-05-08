<?php
if (isset($_POST['submit'])){
    $state = array();
    $state['request'] = "getState";
    $state['state'] = $_POST['State'];
    $state_json = json_encode($state);
    echo $state;
}


//$ch = curl_init();
//curl_setopt($ch, CURLOPT_URL, "172.26.131.203:8000");
//curl_setopt($ch, CURLOPT_POSTFIELDS, $state_json);
//curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
//echo "package over, send soon";
//$data = curl_exec($ch);
//curl_close($ch);


$http = new HttpRequest("172.26.131.203:8000/test", HttpRequest::METH_POST);
$http->setContentType('application/json');
$http->addPostFields($state);
$response = $http->send();
echo $response->getBody();

