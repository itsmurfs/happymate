
/*
* Javascript module to handle all the ajax capability
* This requires jquery and jquery-ui
 */


/**
 * Add autodiscover ajax capability to a component with class="autodiscover"
 * This func send a GET to the server and use the json returned to make the
 * autocomplete runs. The autocomplete capability is provided by the
 * jquery-ui plug-in
 * @param app_name
 */
function discover_autocomplete(app_name){

    $('.autocomplete').each(function(){
        var model_name = this.id.substring(3);
        var elem = this;
        model_name = model_name.charAt(0).toUpperCase() + model_name.slice(1);
        $.getJSON('/commons/autocomplete/'+app_name+'/'+model_name,
            function(data){
                $(elem).autocomplete({
                source: data
            });

            });

    })

}

/**
 * An ajax observer is an html tag, often a div, that can be reloaded
 * by an ajax request. The tag must be linked to a server-side view that
 * returns the html that will be substituted to the element itself.
 * @param selector_id a # prefixed id
 * @param url the url that render the element
 * @constructor
 */
var AjaxObserver = function(selector_id, url){
    this.selector_id = selector_id;
    this.url = url;

    this.reload = function(){

        $(this.selector_id).load(this.url);

    }
};

/***
 * If window.ajax_observer contains ajaxObs (equals by selector_id) returns the index
 * else returns -1
 * @param ajaxObs
 * @returns {number}
 */
function findAjaxObserver(ajaxObs){
    for (var i = 0; i< window.ajax_observers.length; i++){
       if(ajaxObs.selector_id === window.ajax_observers[i].selector_id){
           return i;
       }
    }
    return -1;
}


/***
 * This is the register method of the observer pattern,
 * It takes a selector_id (# included) and the url which load
 * the contents of the element selected by the selector_id,
 * Construct an AjaxObserver and stores it inside the observers collection.
 * If an AjaxObserver with id equals to selector_id already exists inside the collection
 * it will be overwritten
 * @param selector_id a # prefixed id
 * @param url
 */
function registerAjaxObserver(selector_id, url){
    var ajaxObs = new AjaxObserver(selector_id, url)

    if (window.ajax_observers === undefined)
    {
        window.ajax_observers = [];
    }

    var index = findAjaxObserver(ajaxObs);
    if (index > -1) {
        window.ajax_observers[index] = ajaxObs;

    }else{
        window.ajax_observers.push(ajaxObs);
    }

}

/***
 * This is the notifyAll() method of the observer pattern.
 * When it is invoked will be called the reload method of each AjaxObserver
 * inside the observers collection.
 */
function reloadAllAjaxObserver(){

    for (var i = 0; i< window.ajax_observers.length; i++)
        window.ajax_observers[i].reload();

}

/**
 * This is an helper method that you can use to register all the html
 * element that have a class_selector equals to 'ajax'.
 * In order to make the reload function work automatically you MUST specify
 * the url inside the element attribute data-ajax.
 * es: <div id='test-ajax-id' data-ajax='/ajax/test'> ...</div>
 */
function registerAll(){

    class_selector = '.ajax';
    $(class_selector).each(function(){
        registerAjaxObserver("#"+this.id, $(this).data('ajax'));
    });

}

/**
 * This function executes a ajax submit of the elem's form.
 * The form is found using closest('form').
 * If the submit was successful it replace the closest('.ajax')
 * element with the data returned by the POST AND reload all the
 * ajax observer (except the one in which the form is
 * You can specify also a callback function that will be called after
 * the replace.
 * This function uses malsup ajaxSubmit
 * REM: the closest div (the first parent) with class="ajax" that contains
 * the form will be replaced entirely with the html returned by the response.
 * @param elem
 * @param options it is a map whose keys can be input and callback.
 * The input_param option should be a map of additional parameters that will be sent
 * with the POST request to the server
 * The callback_func option is a function called after the POST has returned a successful state
 * and after the reload of all the AjaxObserver. This function take as first argument the
 * submitted form
 */
function ajaxSubmitForm(elem, form_options){

    var form = $(elem).closest('form');

    options = {};

    options.success = function(data, status){

        if (status === 'success'){

            $(form).closest('.ajax').replaceWith(data);
            reloadAllAjaxObserver();
            if(form_options !== undefined){
            if (options.callback_func !== undefined)
                options.callback_func.call(form);
        }
        }


    };

    if(form_options !== undefined){
    if (form_options.input_param !== undefined){
        options.data = form_options.input_param;
    }
    }

    form.ajaxSubmit(options);

}
/**
 * This is the ajax navigator. This should be used when you need to reload an element
 * via ajax. It uses jQuery.load and it take at least the reloaded element id and
 * the url to send the request. When it ends all the ajax observer will be registered again
 *
 * It accepts a callback function that will be called after the ajax obs registration.
 * @param id_selector
 * @param url
 * @param callback_func
 */
function  ajaxNavigator(id_selector, url,  callback_func){
    $(id_selector).load(url, function(){
        registerAll();
        if (callback_func !== undefined)
                callback_func.call( $(id_selector));
    });
}