$(document).ready(function () { // Execute Code after page is fully loaded

    // This function is Ajax and calls generator.php
    function send(todo) {
        $.ajax({
            url: 'generator.php',
            type: 'POST',
            async: true,
            cache: false,
            data: {action: todo},
            dataType: "html",
            success: function (response) {
                // do nothing
            },
            error: function (xhr, textStatus, e) {
                alert('Ajax Error');
                return false;
            },
        });
    }

    // To get the current status of a button. Is the button active or not.
    function get_status(element) {
        if (element.hasClass('stop1') || element.hasClass('stop2')) {
            return "stop";
        } else if (element.hasClass('action1') || element.hasClass('action2')) {
            return "action";
        } else if (element.hasClass('reset')) {
            return "reset";
        } else {
            return false;
        }
    }

    // Some function has more than 1 button. I need to know the difference. So I do not reset a button of the same function.
    function get_level(element) {
        if (element.hasClass('stop1') || element.hasClass('action1') || element.hasClass('reset')) {
            return "1";
        } else if (element.hasClass('stop2') || element.hasClass('action2')) {
            return "2";
        } else {
            return false;
        }
    }

    // Reset all buttons except the clicked one
    function reset_buttons(element) {
        // Sniff on every button
        $("button").each(function (index) {
            if (element.attr('id') == $(this).attr('id')) { // If this is the clicked button skip this loop
                return;
            }
            var level = get_level($(this));
            var level_clicked = get_level(element);
            if (level_clicked == "2" && level == "2") { // Do not reset buttons of the same function
                return;
            }
            if ($(this).hasClass('stop' + level)) { // If Button is active make it inactive
                $(this).addClass('action' + level).removeClass('stop' + level);
            }
        });
    }

    // Take care of each button
    $("button").each(function () {
        // Bind click event on button
        $(this).on("click", function () {
            // In case of clicked

            // Reset all Buttons (except the clicked one)
            reset_buttons($(this));
            // Get status and level of clicked button
            var level = get_level($(this));
            var status = get_status($(this));
            switch (status) {
                case "stop":
                    $(this).addClass('action' + level).removeClass('stop' + level); // Remove active state of button
                    var action = $(this).attr('stop'); // Get stop command
                    break;
                case "action":
                    $(this).addClass('stop' + level).removeClass('action' + level); // Set active state for button
                default:
                    var action = $(this).attr('action'); // Get action command (reset command)
                    break;
            }
            send(action); // Start ajax function to call php file to create or delete the control files
        });
    });
});
