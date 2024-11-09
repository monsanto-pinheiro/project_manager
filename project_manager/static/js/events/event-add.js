
/// Add buttons to several itens, where is possible to add remove itens in combo-box
$().ready(function(){
	
	// event_type
	add_buttons('div_id_event_type', 'modal_remove_event_type', 'id_type_event_remove_modal', 'fa-minus-square', 'Remove event type', true);
	add_buttons('div_id_event_type', 'modal_edit_event_type', 'id_type_event_edit_modal', 'fa-pencil-square', 'Edit event type', edit_remove_events_type_js);
	add_buttons('div_id_event_type', 'modal_add_event_type', 'id_type_event_add_modal', 'fa-plus-square', 'Add event type', edit_remove_events_type_js);

	// return from update, to know the pk
	if (typeof source_pk_js == 'undefined') {
		source_pk_js = '';
	}

    // event type
    $("#id_type_event_add_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/create_event_type/",
        source_pk: source_pk_js			// with this, is possible to pass the pk_event, to include in rever_lazy in django-update-forms
    });
    $("#id_type_event_remove_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/delete_event_type/",
        id_element: "id_event_type",
        source_pk: source_pk_js			// with this, is possible to pass the pk_event, to include in rever_lazy in django-update-forms
    });
    $("#id_type_event_edit_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/update_event_type/",
        id_element: "id_event_type",
        source_pk: source_pk_js			// with this, is possible to pass the pk_event, to include in rever_lazy in django-update-forms
    });
    
});

$(function () {
	  $('[data-toggle="tooltip"]').tooltip()
})
	
function add_buttons(div_id, modal_id, link_id, icon_, text_tooltip, possible_edit_remove) {
	if (possible_edit_remove){
		$('#' + div_id).append('<a href="javascript:;" id="' + link_id + '" data-toggle="tooltip" title="' + text_tooltip + '"> <span> <i class="fa ' +
				icon_ + ' fa-2x padding-button-add-remove"></i></span> </a>' );
	}
	else{
		$('#' + div_id).append('<a href="javascript:;" id="' + link_id + '" data-toggle="tooltip" title="Operation not possible"' + 
				'" onclick="return false;" class="disabled"> <span> <i class="fa ' +
				icon_ + ' fa-2x padding-button-add-remove" style="color:#C0C0C0;"></i></span> </a>' );
	}
	
	$('#' + link_id).prependTo('#' + div_id);
}
