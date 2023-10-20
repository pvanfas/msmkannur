$(document).on('submit', 'form.ajax', function(e) {
    e.preventDefault();
    var $this = $(this);
    var data = new FormData(this);
    var action_url = $this.attr('action');
    var reset = $this.hasClass('reset');
    var reload = $this.hasClass('reload');
    var redirect = $this.hasClass('redirect');
    var redirect_url = $this.attr('data-redirect');

    $.ajax({
        url: action_url,
        type: 'POST',
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        dataType: "json",

        success: function(data) {

            var status = data.status;
            var title = data.title;
            var message = data.message;
            var pk = data.pk;

            if (status == "true") {
                if (title) {
                    title = title;
                } else {
                    title = "Success";
                }

                Swal.fire({
                    title: title,
                    html: message,
                    icon: 'success',
                }).then(function() {
                    if (redirect) {
                        window.location.href = redirect_url;
                    }
                    if (reload) {
                        window.location.reload();
                    }
                    if (reset) {
                        window.location.reset();
                    }
                });

            } else {
                if (title) {
                    title = title;
                } else {
                    title = "An Error Occurred";
                }
                Swal.fire({
                    title: title,
                    html: message,
                    icon: "error"
                });

            }
        },
        error: function(data) {
            var title = "An error occurred";
            var message = "something went wrong";
            Swal.fire({
                title: title,
                html: message,
                icon: "error"
            });
        }
    });
});

$(document).on('click', '.instant-action-button', function(e) {
    e.preventDefault();
    $this = $(this);
    var text = $this.attr('data-text');
    var type = "success";
    var key = $this.attr('data-key');
    var url = $this.attr('data-url');
    var reload = $this.hasClass('reload');
    var reset = $this.hasClass('reset');
	var redirect = $this.hasClass('redirect');
    var title = $this.attr('data-title');
    var redirect_url = $this.attr('data-redirect');

    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        data: { pk: key },

        success: function(data) {
            var status = data.status;
            var message = data.message;

            if (status == "true") {
                title?title=title:title="Success";

                Swal.fire({title:title,text:message,icon:"success"}).then(function() {
                    redirect&&(window.location.href=redirect_url),
                    reload&&window.location.reload(),
                    reset&&window.location.reset();
                });

            } else {
                title?title=title:title="An Error Occurred";
                Swal.fire({title:title,text:message,icon:"error"});

            }
        },
        error: function(data) {
            var title = "An error occurred";
            var message = "An error occurred. Please try again later.";
            Swal.fire({title:title,text:message,icon:"error"});
        }
    });
});


$(".coming").on('click',function(){
    alert("Coming Soon")
});
