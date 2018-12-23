<?php

$servername = "localhost";
$username = "mondir";
$password = "035896";
$dbname = "robot";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error)
{
    die("Connection failed: " . $conn->connect_error);
}

if($_POST["operation"] === "changeReturn")
{
    $sql = "UPDATE sett SET what=" . $_POST["value"];
    if ($conn->query($sql) === TRUE) {
        echo "Record updated successfully";
    } else {
        echo "Error updating record: " . $conn->error;
    }
}
elseif($_POST["operation"] === "setHSV")
{
    $sql = "";
    if($_POST["GreenOrRed"] == "1")
    {
        if($_POST["LowOrHight"] == "1")
        {
            $sql = "UPDATE sett SET green_h_low_value=" . $_POST["h"] . ", green_s_low_value = " . $_POST["s"] . ", green_v_low_value = " . $_POST["v"];         
        }
        else if($_POST["LowOrHight"] == "2")
        {
            $sql = "UPDATE sett SET green_h_hight_value=" . $_POST["h"] . ", green_s_hight_value = " . $_POST["s"] . ", green_v_hight_value = " . $_POST["v"];         
        }
    }
    else if($_POST["GreenOrRed"] == "2")
    {
        if($_POST["LowOrHight"] == "1")
        {
            $sql = "UPDATE sett SET red_h_low_value=" . $_POST["h"] . ", red_s_low_value = " . $_POST["s"] . ", red_v_low_value = " . $_POST["v"];         
        }
        else if($_POST["LowOrHight"] == "2")
        {
            $sql = "UPDATE sett SET red_h_hight_value=" . $_POST["h"] . ", red_s_hight_value = " . $_POST["s"] . ", red_v_hight_value = " . $_POST["v"];         
        }
    }
    if ($conn->query($sql) === TRUE) {
        echo "Record updated successfully";
    } else {
        echo "Error updating record: " . $conn->error;
    }
}

//python /var/www/html/flask/test.py

?>