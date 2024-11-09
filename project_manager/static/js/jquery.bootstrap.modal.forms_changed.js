/*
django-bootstrap-modal-forms
version : 1.5.0
Copyright (c) 2019 Uros Trstenjak
https://github.com/trco/django-bootstrap-modal-forms

These itens were added by me

id_element: "",
source_pk: "",			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
reverse: ""   			url name of reverse of result        
*/


(function ($) {

    // Open modal & load the form at formURL to the modalContent element
    var newForm = function (modalID, modalContent, modalForm, formURL, errorClass, submitBtn, id_element,
    		source_pk, reverse) {
    	//
    	// id_element element is necessary to pass the ID of update and remove item,
    	// in the original code the link is hard coded in button, when created
    	// this case is dynamic, it only works for combo box, in this case
    	if (id_element.length){
    		var selelected = document.getElementById(id_element);
    		formURL = formURL + selelected.options[selelected.selectedIndex].value
    	}
    	
        $(modalID).find(modalContent).load(formURL, function () {
            $(modalID).modal("show");
            $(modalForm).attr("action", formURL);
            
            /// source_pk to get pk in reverse_lazy in update 
            $(modalForm).append('<input type="hidden" name="source_pk" value=' + source_pk + '>')
            /// reverse to get reverse in reverse_lazy link
            $(modalForm).append('<input type="hidden" name="reverse" value=' + reverse + '>')
            
            // Add click listener to the submitBtn
            addListeners(modalID, modalContent, modalForm, formURL, errorClass, submitBtn, id_element,
            		source_pk, reverse);
        });
    };

    // Submit form callback function
    var submitForm = function(modalForm) {
      $(modalForm).submit();
    };
    
    var addListeners = function (modalID, modalContent, modalForm, formURL, errorClass, submitBtn, id_element,
    			source_pk, reverse) {
        // submitBtn click listener
        $(submitBtn).on("click", function (event) {
            isFormValid(modalID, modalContent, modalForm, formURL, errorClass, submitBtn, submitForm, id_element,
            	source_pk, reverse);
        });
        // modal close listener
        $(modalID).on('hidden.bs.modal', function (event) {
            $(modalForm).remove();
        });
    };

    // Check if form.is_valid() & either show errors or submit it
    var isFormValid = function (modalID, modalContent, modalForm, formURL, errorClass, submitBtn, callback, id_element,
    		source_pk, reverse) {
    	
    	if (id_element.length){
    		var selelected = document.getElementById(id_element);
    		formURL = formURL + selelected.options[selelected.selectedIndex].value
    	}
        $.ajax({
            type: $(modalForm).attr("method"),
            url: $(modalForm).attr("action"),
            // Serialize form data
            data: $(modalForm).serialize(),
            beforeSend: function() {
                $(submitBtn).prop("disabled", true);
            },
            success: function (response) {
                if ($(response).find(errorClass).length > 0) {
                    // Form is not valid, update it with errors
                    $(modalID).find(modalContent).html(response);
                    $(modalForm).attr("action", formURL);
                    
                    /// source_pk to get pk in reverse_lazy in update 
                    $(modalForm).append('<input type="hidden" name="source_pk" value=' + source_pk + '>')
                    /// reverse to get reverse in reverse_lazy link
                    $(modalForm).append('<input type="hidden" name="reverse" value=' + reverse + '>')
                    
                    // Reinstantiate listeners
                    addListeners(modalID, modalContent, modalForm, formURL, errorClass, submitBtn, id_element,
                    		source_pk, reverse);
                } else {
                    // Form is valid, submit it
                    callback(modalForm);
                }
            }
        });
    };

    $.fn.modalForm = function (options) {
        // Default settings
        var defaults = {
            modalID: "#modal",
            modalContent: ".modal-content",
            modalForm: ".modal-content form",
            formURL: null,
            errorClass: ".invalid",
            submitBtn: ".submit-btn",
            id_element: "",			// in the original code the link is hard coded in button, when created
            source_pk: "",			// with this, is possible to pass the pk_project, to include in rever_lazy in django-update-forms
            reverse: ""				// url name of reverse of result
        };

        // Extend default settings with provided options
        var settings = $.extend(defaults, options);

        return this.each(function () {
            // Add click listener to the element with attached modalForm
            $(this).click(function (event) {
                // Instantiate new modalForm in modal
                newForm(settings.modalID,
                    settings.modalContent,
                    settings.modalForm,
                    settings.formURL,
                    settings.errorClass,
                    settings.submitBtn,
                    settings.id_element,
                    settings.source_pk,
                    settings.reverse);
            });
        });
    };

}(jQuery));
