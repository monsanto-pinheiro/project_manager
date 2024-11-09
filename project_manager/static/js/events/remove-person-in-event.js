

///
$(document).on("click", "a", function(e){
	var attr = $(this).attr('id');
	
	// For some browsers, `attr` is undefined; for others `attr` is false.  Check for both.
	if (attr === 'id_remove_person_in_event'){
		var ref_name = $(this).attr('ref_name');
		var hours_of_work = $(this).attr('hours_of_work');
		var tr_to_remove = e.target.parentNode.parentNode.parentNode.parentNode.id;
		
		$('#id-label-remove-person-in_event').text('Do you want to remove this person \'' + ref_name + '\'' + hours_of_work + ' of work, in this event?');
		$('#id-modal-body-remove-person-in_event').attr('pk', $(this).attr('pk'));
		$('#id-modal-body-remove-person-in_event').attr('ref_name', ref_name);
		$('#id-modal-body-remove-person-in_event').attr('tr_to_remove', tr_to_remove);
	}
});


$('#id-remove-person-button').on('click', function(){

	$.ajax({
        url: $('#id-modal-body-remove-person-in_event').attr("remove-single-value-url"),
        data : { 
        	man_power_id : $('#id-modal-body-remove-person-in_event').attr('pk'),
    		csrfmiddlewaretoken: '{{ csrf_token }}'
        }, // data sent with the post request
        		
        success: function (data) {
          if (data['is_ok']) {
        	  
        	  /// remove line
        	  document.getElementById($('#id-modal-body-remove-person-in_event').attr('tr_to_remove')).remove();
        	  
        	  /// add message with information
        	  $('#id_messages_remove').append('<div class="alert alert-dismissible alert-success">' +
        		'The person \'' + $('#id-modal-body-remove-person-in_event').attr('ref_name') + '\' in event was successfully removed.' +
				'<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
				'</div>');
          }
          else{
        	/// add message with informaton
        	  $('#id_messages_remove').append('<div class="alert alert-dismissible alert-warning">' +
        		'The person \'' + $('#id-modal-body-remove-person-in_event').attr('ref_name') + '\' in event was not removed.' +
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