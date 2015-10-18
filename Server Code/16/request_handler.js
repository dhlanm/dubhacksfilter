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
	//params.append("info", info);
	params.append("show_blocked", show_blocked);
	params.append("input_hashtag", input_hashtag);
	params.append("blocked_text", blocked_text);

	var request = new XMLHttpRequest();
	request.onload = processImages;
	request.open("POST", "/", true);
	request.send(params);
}

function processImages () {
	var show_blocked = document.getElementById("show_blocked_radio").checked;

	var json = JSON.parse(this.responseText);
	console.log(json);
	document.getElementById("images_left").innerHTML = '';
	document.getElementById("images_right").innerHTML = '';

	if (show_blocked){
		for(var i = 0; i < json.ranked.good.length; i++){
			var image = document.createElement("img");
			image.src = json.ranked.good[i];
			document.getElementById("images_left").appendChild(image);
		}
		for(var i = 0; i < json.ranked.bad.length; i++){
			var image = document.createElement("img");
			image.src = json.ranked.bad[i];
			document.getElementById("images_right").appendChild(image);
		}
	} else {
		for(var i = 0; i < json.ranked.good.length; i++){
			var image = document.createElement("img");
			image.src = json.ranked.good[i];
			if (i % 2 == 0){
				document.getElementById("images_left").appendChild(image);
			} else {
				document.getElementById("images_right").appendChild(image);				
			}
		}
	}
}