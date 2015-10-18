/*
{
	hashtag: "Shit", 
	bad_words: ['weed', 'drugs', 'heroin', 'meth', 'porn']
}
*/


window.onload = function (){
	document.getElementById("submit_button").onclick = get_images;
}

function get_images (){
	var show_blocked = document.getElementById("show_blocked_radio").checked;
	var input_hashtag = document.getElementById("hashtag").value;
	var blocked_text = document.getElementById("blocked_words_textbox").value;

	var blocked_words = blocked_text.split(',');
	for (var i = 0; i < blocked_words.length; i++){
		blocked_words[i] = blocked_words[i].trim();
	}
	
	var info = {hashtag:input_hashtag, bad_words:blocked_words};
	console.log(info);

	var params = new FormData();
	params.append("info", info);

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