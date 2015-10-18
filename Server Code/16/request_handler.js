/*
{
	hashtag: "Shit", 
	bad_words: ['weed', 'drugs', 'heroin', 'meth', 'porn']
}
*/

var interval;

window.onload = function (){
	document.getElementById("submit_button").onclick = start_interval;
}

function start_interval () {
	interval = setInterval(get_images, 60000);
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

	document.getElementById("images_left").innerHTML = '';
	document.getElementById("images_right").innerHTML = '';

	if (show_blocked){
		for(var i = 0; i < json.ranked.good.length; i++){
			var image = document.createElement("img");
			image.src = json.ranked.good[i]['path'];
			document.getElementById("images_left").appendChild(image);
			var text = document.createElement("p");
			p.innerHTML = '<span class="username">' + json.ranked.good[i]['username'] + '</span>: ' + json.ranked.good[i]['text']
			document.getElementById("images_left").appendChild(text);
		}
		for(var i = 0; i < json.ranked.bad.length; i++){
			var image = document.createElement("img");
			image.src = json.ranked.bad[i]['path'];
			document.getElementById("images_right").appendChild(image);
			var text = document.createElement("p");
			p.innerHTML = '<span class="username">@' + json.ranked.bad[i]['username'] + '</span>: ' + json.ranked.bad[i]['text']
			document.getElementById("images_right").appendChild(text);

		}
	} else {
		for(var i = 0; i < json.ranked.good.length; i++){
			var image = document.createElement("img");
			image.src = json.ranked.good[i]['path'];
			if (i % 2 == 0){
				var image = document.createElement("img");
				image.src = json.ranked.good[i]['path'];
				document.getElementById("images_left").appendChild(image);
				var text = document.createElement("p");
				p.innerHTML = '<span class="username">@' + json.ranked.good[i]['username'] + '</span>: ' + json.ranked.good[i]['text']
				document.getElementById("images_left").appendChild(text);
			} else {
				var image = document.createElement("img");
				image.src = json.ranked.good[i]['path'];
				document.getElementById("images_right").appendChild(image);
				var text = document.createElement("p");
				p.innerHTML = '<span class="username">@' + json.ranked.good[i]['username'] + '</span>: ' + json.ranked.good[i]['text']
				document.getElementById("images_right").appendChild(text);			
			}
		}
	}
}