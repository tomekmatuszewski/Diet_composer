function highlightSearch() {

    let searched = document.getElementById("searchItem").value;
    if (searched !== "") {
        let tag = document.getElementsByTagName("p")
        for (i = 0; i < tag.length; i++) {
            let text = tag[i].innerHTML;
            let re = new RegExp(searched, "g"); // search for all instances
            let newText = text.replace(re, `<mark>${searched}</mark>`);
            tag[i].innerHTML = newText;
        }
    }
}
