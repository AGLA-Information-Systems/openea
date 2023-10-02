function get_value_stream_menu_markup(){
    var menu_markup = "<span class='label-1 menu-label'>&nbsp;</span> Capabilité";
    menu_markup += "<span class='label-2 menu-label'>&nbsp;</span> Valeur";
    return menu_markup;
}

function restructure_value_streams(items){
    var vs_roots = [];
    for (const [vs_id, vs_data] of Object.entries(items)){
        if (vs_data['value_stream_trigger_value_stream']){
            if (Object.keys(vs_data['value_stream_trigger_value_stream']['slots']).length === 0){
                vs_roots.push(vs_id);         
            }
            items[vs_id]['triggering'] = [];
            for (const[slot_id, slot] of Object.entries(vs_data['value_stream_trigger_value_stream']['inslots'])){
                items[vs_id]['triggering'].push(slot['subject']);
            }
        }
        items[vs_id]['capabilities'] = 0;
        if (vs_data['capability_enable_value_stream']){
            items[vs_id]['capabilities'] = Object.keys(vs_data['capability_enable_value_stream']['slots']).length;
        }
        items[vs_id]['values'] = 0;
        if (vs_data['value_stream_produce_value']){
            items[vs_id]['values'] = Object.keys(vs_data['value_stream_produce_value']['slots']).length;
        }
    }
    return vs_roots;
}


function get_value_stream_markup(value_streams, vs_id){
    const vs = value_streams[vs_id];
    var vs_markup = `<div class='infobox'  id='${vs.id}'>`;
    vs_markup += `<table class='item-details'>`;
    vs_markup += `<tr>`;
    vs_markup += `<td colspan="2"><a href='/o_instance/detail/${vs.id}'>${vs.name}</a></td>`;
    vs_markup += `</tr><tr>`;
    vs_markup += `<td class='label-1'><span>${vs.capabilities}</span></td>`;
    vs_markup += `<td class='label-2'><span>${vs.values}</span></td>`;
    vs_markup += `</tr>`;
    vs_markup += `</table>`;
    vs_markup += `</div>`;
    
    for (const next_vs_id of vs['triggering']){
        vs_markup = `${get_value_stream_markup(value_streams, next_vs_id)}` + '<span>&#x2192;</span>' + vs_markup;
    }
    return vs_markup;
}

function populate_value_streams(dataPaneId, menuPaneId, value_streams, vs_roots){
    const dataPane = $('#' + dataPaneId);
    const menuPane = $('#' + menuPaneId);
    var root_vs_markup = '';
    for (const root_vs_id of vs_roots){
        root_vs_markup += `${get_value_stream_markup(value_streams, root_vs_id)}`;
    }
    menuPane.html(get_value_stream_menu_markup());
    dataPane.html('<div class="infobox">' + root_vs_markup + '</div>');
}

function value_stream_view(model_id, dataPaneId, menuPaneId){
    var results = {};
    var value_streams = {};
    var predicates = {};
    
    $.ajaxSetup({
        async: false
    });

    var value_stream_concept = null;
    $.getJSON('/api/rest/model/' + model_id + "/concepts/" + configuration['concepts']['value_stream'], (data) => {
        value_stream_concept = data;
    });

    var predicates = {};
    for (const [predicate_key, predicate_id] of Object.entries(configuration['predicates'])){
        if (predicate_key.includes('value_stream')){
            $.getJSON('/api/rest/model/' + model_id + "/predicates/" + predicate_id, (data) => {
                predicates[predicate_key] = data;
    
                predicates[predicate_key]['slots'] = {}
                $.getJSON('/api/rest/model/' + model_id + '/slots?' + 'predicate_id=' + predicate_id, (data2) => {
                    for (const slot of data2['results']){
                        predicates[predicate_key]['slots'][slot.id] = slot;
                    }
                });
            })
            .fail(function() {
                predicates[predicate_key] = null;
            });
        }
    }

    $.getJSON('/api/rest/model/' + model_id + '/instances?concept_id=' + configuration['concepts']['value_stream'], (data) => {
        results = data['results'];
    });
    for (i in results){
        vs = results[i]
        value_streams[vs.id] = vs;
        for (const [predicate_key, predicate_id] of Object.entries(configuration['predicates'])){
            if (predicate_key.includes('value_stream')){
                value_streams[vs.id][predicate_key] = {'slots': {}, 'inslots':{}};
                if (predicates[predicate_key]){
                    for (const [slot_id, slot] of Object.entries(predicates[predicate_key]['slots'])){
                        if (slot.subject == vs.id){
                            value_streams[vs.id][predicate_key]['slots'][slot_id] = slot;
                        }
                        if (slot.object == vs.id){
                            value_streams[vs.id][predicate_key]['inslots'][slot_id] = slot;
                        }
                    }
                }
            }
        }
    }
    var vs_roots = restructure_value_streams(value_streams);
    populate_value_streams(dataPaneId, menuPaneId, value_streams, vs_roots);

    $.ajaxSetup({
        async: true
    });
}