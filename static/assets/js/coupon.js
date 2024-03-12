function validateStartDate() {
    var inputDate = new Date(document.getElementById('staring').value);
    var today = new Date();
    today.setDate(today.getDate() - 1);

    if (inputDate < today) {
        document.getElementById('dateError').innerText = "Start date should not be earlier than today.";
        document.getElementById('staring').value = ''; // Clear the input value
    } else {
        document.getElementById('dateError').innerText = "";
    }
}

function validateEndDate() {
    var inputDate = new Date(document.getElementById('ending').value);
    var tomorrow = new Date();
    // tomorrow.setDate(tomorrow.getDate() + 1); // Get tomorrow's date

    if (inputDate < tomorrow) {
        document.getElementById('endDateError').innerText = "End date should not be later than tomorrow.";
        document.getElementById('ending').value = ''; // Clear the input value
    } else {
        document.getElementById('endDateError').innerText = "";
    }
}