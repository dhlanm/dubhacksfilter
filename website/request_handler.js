window.onload = function (){
	document.getElementById("submit_button").onclick = get_images;
}

function get_images (){
	var show_blocked = document.getElementById("show_blocked_radio").checked;
	var hashtag = document.getElementById("hashtag").value;
	var blocked_words = document.getElementById("blocked_words_textbox").value;

	var params = new FormData();
	params.append("hashtag", hashtag);
	params.append("blocked_words", blocked_words);
	params.append("show_blocked", show_blocked);

	var request = new XMLHttpRequest();
	request.onload = processImages;
	request.open("POST", "url", true);
	request.send(params);
}

function processImages () {
	var json = JSON.parse(this.responseText);
	for(var i = 0; i < json.images.good.length; i++){
		var image = document.createElement("img");
		image.src = json.images.good[i].link;
		document.getElementById("good_images").appendChild(image);
	}
}