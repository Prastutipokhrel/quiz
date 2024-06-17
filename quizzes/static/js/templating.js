class Template{ 
    static render_template(template_name, data, template_placeholder) {
        // var source   = $("#"+template_name).html();
        // var template = Handlebars.compile(source);
        // var context = {title: "My New Post", body: "This is my first post!"};
        $("#"+template_placeholder).html( Template.get_template(template_name, data) );
    }
    static get_template(template_name, data) {
        Handlebars.registerHelper('ifCond', function(v1, v2, options) {
                    if(v1 === v2) {
                        return options.fn(this);
                    }
                    return options.inverse(this);
        });
        var source   = $("#"+template_name).html();
        // console.log("source",source);
        var template = Handlebars.compile(source);
        // var template = Handlebars.compile($("#list-active-template").html());
        
        //var context = {title: "My New Post", body: "This is my first post!"};
        return template(data=data);
    }

    static show_dialog(template_name, title, data,btn=""){ 
        var default_btn = '<button type="button" class="btn btn-sm btn-danger" data-dismiss="modal">Close</button>';       
        $("#global-modal-dialog-title").html(title);
        $("#global-modal-dialog-body").html( Template.get_template(template_name, data) );
        $("#global-modal-dialog-footer").html(default_btn+btn);
        $("#global-modal-dialog").modal('show');
    }
    
}

//TODO remove log func by tracking it
function log(msg) {
    // console.log(msg);
}