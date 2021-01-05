<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="reset.css">
    <link rel="stylesheet" href="style.css">
    <title>Race control</title>
    <link rel="shortcut icon" type="image/x-icon" href="favicon.ico">
    <script src="jquery-3.5.1.min.js"></script>
    <script src="generator.js"></script>
</head>
<body>
<div class="container">
    <legend class="clear">
        <button id="car1start" action="car1start" stop="car1stop" class="left action2">Car 1</button>
        <span class="spacer"></span>
        <button id="car2start" action="car2start" stop="car2stop" class="right action2">Car 2</button>
    </legend>
    <legend>
        <button id="carsalternately" action="carsaltstart" stop="carsaltstop" class="full action1">Alternately</button>
    </legend>
    <legend>
        <button id="carsrandom" action="carsrndstart" stop="carsrndstop" class="full action1">Random</button>
    </legend>
    <legend>
        <button id="reset" action="reset" stop="reset" class="full reset">Reset</button>
    </legend>
</div>
</body>
</html>
