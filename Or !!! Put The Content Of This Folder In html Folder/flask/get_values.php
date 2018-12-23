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

if($_GET["GreenOrRed"] === "1")
{
    if($_GET["LowOrHight"] === "1")
    {
        $sql = "SELECT green_h_low_value, green_s_low_value, green_v_low_value FROM sett;";
        $result = $conn->query($sql);

        if ($result->num_rows > 0)
        {
            // output data of each row
            while($row = $result->fetch_assoc()) {
                echo $row["green_h_low_value"]. "|" . $row["green_s_low_value"]. "|" . $row["green_v_low_value"];
            }
        }
    }
    else if($_GET["LowOrHight"] === "2")
    {
        $sql = "SELECT green_h_hight_value, green_s_hight_value, green_v_hight_value FROM sett;";
        $result = $conn->query($sql);

        if ($result->num_rows > 0)
        {
            // output data of each row
            while($row = $result->fetch_assoc()) {
                echo $row["green_h_hight_value"]. "|" . $row["green_s_hight_value"]. "|" . $row["green_v_hight_value"];
            }
        }
    }
}
else if($_GET["GreenOrRed"] === "2")
{
    if($_GET["LowOrHight"] === "1")
    {
        $sql = "SELECT red_h_low_value, red_s_low_value, red_v_low_value FROM sett;";
        $result = $conn->query($sql);

        if ($result->num_rows > 0)
        {
            // output data of each row
            while($row = $result->fetch_assoc()) {
                echo $row["red_h_low_value"]. "|" . $row["red_s_low_value"]. "|" . $row["red_v_low_value"];
            }
        }
    }
    else if($_GET["LowOrHight"] === "2")
    {
        $sql = "SELECT red_h_hight_value, red_s_hight_value, red_v_hight_value FROM sett;";
        $result = $conn->query($sql);

        if ($result->num_rows > 0)
        {
            // output data of each row
            while($row = $result->fetch_assoc()) {
                echo $row["red_h_hight_value"]. "|" . $row["red_s_hight_value"]. "|" . $row["red_v_hight_value"];
            }
        }
    }
}

//python /var/www/html/flask/test.py

?>