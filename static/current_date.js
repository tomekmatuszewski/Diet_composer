function insert_current_date() {
    let today = new Date();

    let date = `${today.getDate()} / ${today.getMonth() + 1} / ${today.getFullYear()}`

    document.getElementById("current-date").innerText = "Date: " + date;
}

insert_current_date();