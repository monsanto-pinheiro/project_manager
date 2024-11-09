

///
$(document).on("click", "a", function(e){
	var attr = $(this).attr('id');
	var ref_name = $(this).attr('ref_name');
	var tr_to_remove = e.target.parentNode.parentNode.parentNode.parentNode.id;
	
	// For some browsers, `attr` is undefined; for others `attr` is false.  Check for both.
	if (attr === 'id_remove_event'){
		$('#id-label-remove').text('Do you want to remove \'' + ref_name + '\'?');
		$('#id-modal-body-remove-event').attr('pk', $(this).attr('pk'));
		$('#id-modal-body-remove-event').attr('ref_name', ref_name);
		$('#id-modal-body-remove-event').attr('tr_to_remove', tr_to_remove);
	}
});


$('#id-remove-button').on('click', function(){

	$.ajax({
        url: $('#id-modal-body-remove-event').attr("remove-single-value-url"),
        data : { 
        	event_id : $('#id-modal-body-remove-event').attr('pk'),
    		csrfmiddlewaretoken: '{{ csrf_token }}'
        }, // data sent with the post request
        		
        success: function (data) {
          if (data['is_ok']) {
        	  
        	  /// remove line
        	  document.getElementById($('#id-modal-body-remove-event').attr('tr_to_remove')).remove();
        	  
        	  /// add message with informaton
        	  $('#id_messages_remove').append('<div class="alert alert-dismissible alert-success">' +
        		'The event \'' + $('#id-modal-body-remove-event').attr('ref_name') + '\' was successfully removed.' +
				'<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
				'</div>');
          }
          else{
        	/// add message with informaton
        	  $('#id_messages_remove').append('<div class="alert alert-dismissible alert-warning">' +
        		'The event \'' + $('#id-modal-body-remove-event').attr('ref_name') + '\' was not removed.' +
				'<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
				'</div>');
          }
        },
        
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            alert(errmsg);
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
	});
});