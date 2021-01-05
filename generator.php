<?php ob_start(); // Suppress possible output. Ajax would fail with output.

// Control class
class car_control
{
    protected $dircontrol;
    protected $fileprefix;
    protected $mods;
    protected $cars;

    public function __construct()
    {
        $this->dircontrol = realpath(__DIR__) . "/ledcontrol/";
        $this->fileprefix = ".rex";
        $this->mods = ["rnd", "alt"];
        $this->cars = [1, 2];
    }

    public function start($number)
    {
        $this->modstop();
        @touch($this->dircontrol . $number . $this->fileprefix); // generate control file
        // The @ suppresses any output and error, warning and notice messages. Be sure the directory is writeable.
    }

    public function stop($number = "")
    {
        if (!empty($number))
            @unlink($this->dircontrol . $number . $this->fileprefix); // delete control file
        else {
            foreach ($this->cars as $car)
                $this->stop($car);
        }
    }

    public function modstart($mod)
    {
        $this->stop();
        $this->modstop();
        @touch($this->dircontrol . $mod . $this->fileprefix);
    }

    public function modstop()
    {
        foreach ($this->mods as $known_mod) {
            @unlink($this->dircontrol . $known_mod . $this->fileprefix);
        }
    }

    public function reset()
    {
        $this->stop();
        $this->modstop();
    }

}

$car_control = new car_control();
$action = $_POST['action']; // Get the info about your job

// Execute job
switch ($action) {
    case "car1start":
        $car_control->start(1);
        break;
    case "car2start":
        $car_control->start(2);
        break;
    case "car1stop":
        $car_control->stop(1);
        break;
    case "car2stop":
        $car_control->stop(2);
        break;
    case "carsaltstart":
        $car_control->modstart("alt");
        break;
    case "carsrndstart":
        $car_control->modstart("rnd");
        break;
    case "carsaltstop":
    case "carsrndstop":
        $car_control->modstop();
        break;
    case "reset":
        $car_control->reset();
        break;
    default:
        // none
        break;
}
return true;