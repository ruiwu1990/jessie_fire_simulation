$(document).ready(function(){
	
	$('#confirmButtonID').on('click',function(){
		var selectedItem = $('#existingSelectBoxID').find(":selected").text();
		window.location.replace("/fire_vis/"+selectedItem);
	});

});

