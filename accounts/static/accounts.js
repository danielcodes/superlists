//small chain here, superlists gets called from the test,
//it then calls account and it's initialize function
//whatever object is passed, we take the id key and call request
//request sets the requestcalled var to true

var initialize = function(navigator, user, token, urls) {
    $('#id_login').on('click', function() {
		navigator.id.request();
	});

	//3 step tdd cycle, create function, do an ajax call, 
	//get the login url, and pass assertion
	navigator.id.watch({
		loggedInUser: user,
		//what the heck is this browserid assertion
		onlogin: function(assertion) {
			$.post(
				urls.login,
				{assertion: assertion, csrfmiddlewaretoken: token}
			)
				.done(function () { window.location.reload(); })
                .fail(function () { navigator.id.logout(); });
		},
		onlogout: function() {}	
	});
};

//Superlists is a global object
window.Superlists = {
	Accounts: {
		initialize: initialize 
	}
};



