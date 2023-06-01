function debounce(fn, delay) {
    var timeout;

    return function () {
        var context = this, args = arguments;

        clearTimeout(timeout);
        timeout = setTimeout(function () {
            fn.apply(context, args);
        }, delay || 250);
    };
}

const sortHandler = (a, b) => $(a).text() < $(b).text() ? -1 : $(a).text() > $(b).text() ? 1 : 0;

function toggle_checkbox(select_id, checkbox_id){
    if ($("#"+checkbox_id).is(':checked')){
      $('#' + select_id +' option').prop('selected', true);
    } else{
      $('#' + select_id +' option').prop('selected', false);
    }
    $('#' + select_id).change();
}

function uncheck_all_checkbox(select_id, checkbox_id) {
    var allSelected = $("#"+select_id+" option:not(:selected)").length == 0;
    if (! allSelected) {
      $("#"+checkbox_id).prop( "checked", false );
    }
}

function saveSvg(svgEl, name) {
    svgEl.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    var svgData = svgEl.outerHTML;
    var preface = '<?xml version="1.0" standalone="no"?>\r\n';
    var svgBlob = new Blob([preface, svgData], {type:"image/svg+xml;charset=utf-8"});
    var svgUrl = URL.createObjectURL(svgBlob);
    var downloadLink = document.createElement("a");
    downloadLink.href = svgUrl;
    downloadLink.download = name;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

async function filter_model_data(filter_data, success_function, success_function_params) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    try {
        const result_data = await $.ajax({
            url: '/o_model/filter/'+modelId+'/json',
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            contentType : 'application/json',
            success: function (result) {
              success_function(result, success_function_params);
            },
            data: JSON.stringify(filter_data)
        });
        return result_data;
    } catch (error) {
        console.error("Error: ", error);
    }
}

function create_link_node(item, name_key, uri_key){
    var a = document.createElement('a');
    a.title = ''
    if (item[name_key]){
        a.title = item[name_key];
        var link = document.createTextNode(item[name_key]);
        a.appendChild(link);   
    }
    a.href = ''
    if (item[uri_key]){
        a.href = item[uri_key];
    }
    a.classList.add("link-dark");
    return a;
}