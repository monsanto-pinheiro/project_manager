
/// Add buttons to several itens, where is possible to add remove itens in combo-box
$().ready(function(){
	
	// research
	add_buttons('div_id_research', 'modal_remove_database', 'id_research_remove_modal', 'fa-minus-square', 'Remove client', edit_remove_research_js);
	add_buttons('div_id_research', 'modal_edit_research', 'id_research_edit_modal', 'fa-pencil-square', 'Edit client', edit_remove_research_js);
	add_buttons('div_id_research', 'modal_create_research', 'id_research_add_modal', 'fa-plus-square', 'Add client', true);
	
	// specie
	add_buttons('div_id_specie', 'modal_remove_specie', 'id_specie_remove_modal', 'fa-minus-square', 'Remove specie', edit_remove_specie_js);
	add_buttons('div_id_specie', 'modal_edit_specie', 'id_specie_edit_modal', 'fa-pencil-square', 'Edit specie', edit_remove_specie_js);
	add_buttons('div_id_specie', 'modal_add_specie', 'id_specie_add_modal', 'fa-plus-square', 'Add specie', true);
	
	// project_type
	add_buttons('div_id_project_type', 'modal_remove_project_type', 'id_type_project_remove_modal', 'fa-minus-square', 
			'Remove project type', edit_remove_projects_type_js && possible_to_change_projects_type_js);
	add_buttons('div_id_project_type', 'modal_edit_project_type', 'id_type_project_edit_modal', 'fa-pencil-square', 'Edit project type', 
			edit_remove_projects_type_js && possible_to_change_projects_type_js);
	add_buttons('div_id_project_type', 'modal_add_project_type', 'id_type_project_add_modal', 'fa-plus-square', 'Add project type', 
			possible_to_change_projects_type_js);
	
	// institute
	add_buttons('div_id_institute', 'modal_remove_institute', 'id_institute_remove_modal', 'fa-minus-square', 'Remove institute', edit_remove_institute_js);
	add_buttons('div_id_institute', 'modal_edit_institute', 'id_institute_edit_modal', 'fa-pencil-square', 'Edit institute', edit_remove_institute_js);
	add_buttons('div_id_institute', 'modal_add_institute', 'id_institute_add_modal', 'fa-plus-square', 'Add institute', true);
	
	// return from update, to know the pk
	if (typeof source_pk_js == 'undefined') {
		source_pk_js = '';
	}
	
	// research
	$("#id_research_add_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/create_research/",
        source_pk: source_pk_js			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
        	
    })
    $("#id_research_remove_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/delete_research/",
        id_element: "id_research",
        source_pk: source_pk_js			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
    })
    $("#id_research_edit_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/update_research/",
        id_element: "id_research",
        source_pk: source_pk_js			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
    })
    
    
    // institute
	$("#id_institute_add_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/create_institute/",
        source_pk: source_pk_js			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
    })
    $("#id_institute_remove_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/delete_institute/",
        id_element: "id_institute",
        source_pk: source_pk_js			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
    })
    $("#id_institute_edit_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/update_institute/",
        id_element: "id_institute",
        source_pk: source_pk_js			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
    })
    
    
    // specie
	$("#id_specie_add_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/create_specie/",
        source_pk: source_pk_js			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
    })
    $("#id_specie_remove_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/delete_specie/",
        id_element: "id_specie",
        source_pk: source_pk_js			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
    })
    $("#id_specie_edit_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/update_specie/",
        id_element: "id_specie",
        source_pk: source_pk_js			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
    })
    

    // project type
    $("#id_type_project_add_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/create_project_type/",
        source_pk: source_pk_js			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
    });
    $("#id_type_project_remove_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/delete_project_type/",
        id_element: "id_project_type",
        source_pk: source_pk_js			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
    });
    $("#id_type_project_edit_modal").modalForm({
		modalID: "#modal",
		modalForm: ".modal-content form",
        formURL: "/projects/update_project_type/",
        id_element: "id_project_type",
        source_pk: source_pk_js			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
    });

    // disable dropbox if is in update form and there is events already defined
    // Disabled input will not submit data. Use the readonly attribute.
	// $("#id_project_type").prop("readonly", ! possible_to_change_projects_type_js);
    
	// sort list after because fields are encrypted, and queryset must be a queryset, not list
	sortList('id_research');
	sortList('id_institute');

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
