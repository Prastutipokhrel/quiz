class Remote{
    static call_api(url, type, data, success_callback, failure_callback, notify=false ){
        $.ajax({
            type: type,
            url: url,
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            headers: {
             'X-CSRF-TOKEN': Cookies.get('csrf_access_token')
            }
        }).done(function (response) {
            $("#progress_bar").css("display","none");
            if( response.status == 401){
                alert('Unauthorized: You are not allowed to do this task.')
            }
            if(notify) {
                if( response.status == 200){
                    alert(response.msg);
                    // $.notify(response.msg, "info");
                }
                else{
                    alert(response.msg + response.err);
                    // $.notify(response.msg + response.err, "error");

                }
            }
            success_callback(response);
        }).fail(function (jqXHR, textStatus )  { 
            $("#progress_bar").css("display","none");
            if(jqXHR.status==400){
                alert("BAD ! "+ jqXHR.responseJSON.msg);
            }
            if(jqXHR.status == 401){
                alert('Unauthorized: You are not allowed to do this task.')            }
            failure_callback(jqXHR.status);
        });
    }

    static send_formdata(url,data, success_callback, failure_callback, notify=false ){
        $.ajax({
            type: "POST",
            url: url,
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            headers: {
             'X-CSRF-TOKEN': Cookies.get('csrf_access_token')
            }
        }).done(function (response) {
            // console.log(response)
            if(notify) {
                if( response.status == 200){
                    $.notify(response.msg, "info");
                }
                else{
                    $.notify(response.msg + response.err, "error");

                }
            }
            success_callback(response);
        }).fail(function (jqXHR, textStatus )  {
            if(jqXHR.status==400){
                $.notify("BAD ! "+ jqXHR.responseJSON.msg,"error");
            }
            failure_callback(jqXHR.status);
        });
    }

    static get_form(url, data, success_callback, failure_callback, notify=false ){
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            contentType: "text/html; charset=utf-8",
            headers: {
             'X-CSRF-TOKEN': Cookies.get('csrf_access_token')
            }
        }).done(function (response) {
            if(notify) $.notify("Data Loaded successfully", "info");
            success_callback(response);
        }).fail(function (jqXHR, textStatus )  {
            if(jqXHR.status==400){
                $.notify("BAD ! "+ jqXHR.responseJSON.msg,"error");
            }
            failure_callback(jqXHR.status);
        });
    }
}



