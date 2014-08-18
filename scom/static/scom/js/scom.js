$(document).ready(function() {
	$(".toggle_aktion").click(function() {
		$(this).parent().parent().next().removeClass("hidden");
	});
});
