var capabilities = {};
var cap_roots = [];
var legend = {};

//======
function capability_toggle_stickers(){
    legend = {'label-1': 'Objectifs', 'label-2': 'Flux de valeur', 'label-3': 'Produits'};
    set_capability_legend_markup();

    $('.sticker').toggle();
}

function capability_heatmap_criticality(){
    legend = {};
    collect(capabilities, cap_roots, max_all, 'children', 'criticality');

    $('.gradient-1').removeClass();
    for (const [cap_id, cap_data] of Object.entries(capabilities)){
        $('#'+cap_data.id).addClass('gradient-1');
        $('#'+cap_data.id).addClass('gradient-1-' + cap_data.criticality);

        legend['gradient-1-' + cap_data.criticality] = cap_data.criticality;
    }

    set_capability_legend_markup();
}
//======
function set_capability_legend_markup(){
    var legend_markup = ``;
    for (const [legend_color, legend_item] of Object.entries(legend)){
        legend_markup += `<span class='legend-label ${legend_color}'>&nbsp;</span> ${legend_item}`;
    }
    return $('#' + panes['legend']).html(`${legend_markup}`);
}

function set_capability_menu_markup(){
    var menu_markup = `<a class='menu-item' id='capability-heatmap-maturity'>Maturité</a>`;
    menu_markup += `<a class='menu-item' id='capability-heatmap-effectiveness'>Efficacité</a>`;
    menu_markup += `<a class='menu-item' id='capability-heatmap-performance'>Performance</a>`;
    menu_markup += `<a class='menu-item' id='capability-heatmap-value'>Valeur</a>`;
    menu_markup += `<a class='menu-item' id='capability-heatmap-usage'>Utilisation</a>`;
    menu_markup += `<a class='menu-item' id='capability-heatmap-cost-distribution'>Districution des coûts</a>`;
    menu_markup += `<a class='menu-item' id='capability-heatmap-criticality'>Criticité</a>`;
    menu_markup += `<a class='menu-item' id='capability-toggle-stickers'>Étiquettes</a>`;


    legend = {'label-1': 'Objectifs', 'label-2': 'Flux de valeur', 'label-3': 'Produits'};
    set_capability_legend_markup();

    return $('#' + panes['menu']).html(`<div class='submenu'>${menu_markup}</div>`);
}


function restructure_capabilities(items){
    var cap_roots = [];
    for (const [cap_id, cap_data] of Object.entries(items)){
        if (cap_data['capability_support_capability']){
            if (Object.keys(cap_data['capability_support_capability']['slots']).length === 0){
                cap_roots.push(cap_id);         
            }
            items[cap_id]['children'] = [];
            for (const[slot_id, slot] of Object.entries(cap_data['capability_support_capability']['inslots'])){
                items[cap_id]['children'].push(slot['subject']);
            }
        }
        items[cap_id]['objectives'] = 0;
        if (cap_data['capability_realize_objective']){
            items[cap_id]['objectives'] = Object.keys(cap_data['capability_realize_objective']['slots']).length;
        }
        items[cap_id]['value_streams'] = 0;
        if (cap_data['capability_enable_value_stream']){
            items[cap_id]['value_streams'] = Object.keys(cap_data['capability_enable_value_stream']['slots']).length;
        }
        items[cap_id]['products'] = 0;
        if (cap_data['product_support_capability']){
            items[cap_id]['products'] = Object.keys(cap_data['product_support_capability']['slots']).length;
        }
    }
    return cap_roots;
}


function get_capability_markup(capabilities, cap_id){
    const cap = capabilities[cap_id];
    var cap_markup = `<div id='${cap.id}'>`;
    cap_markup += `<table class='item-details'>`;
    cap_markup += `<tr>`;
    cap_markup += `<td colspan = "3"><a href='/o_instance/detail/${cap.id}'>${cap.name}</a></td>`;
    cap_markup += `</tr><tr class="sticker">`;
    cap_markup += `<td class='label-1'><span>${cap.objectives}</span></td>`;
    cap_markup += `<td class='label-2'><span>${cap.value_streams}</span></td>`;
    cap_markup += `<td class='label-3'><span>${cap.products}</span></td>`;
    cap_markup += `</tr>`;
    cap_markup += `</table>`;
    cap_markup += `</div>`;
    
    for (const child_cap_id of cap['children']){
        cap_markup += `<div >${get_capability_markup(capabilities, child_cap_id)}</div>`;
    }
    return `<div class='infobox'>${cap_markup}</div>`;
}


function populate_capabilities(panes, capabilities, cap_roots){
    const dataPane = $('#' + panes['data']);
    var root_cap_markup = '';
    for (const root_cap_id of cap_roots){
        root_cap_markup += `${get_capability_markup(capabilities, root_cap_id)}`;
    }
    set_capability_menu_markup();
    dataPane.html('<div class="infobox">' + root_cap_markup + '</div>');
}

function create_capability_subview(submenu_id){
    const create_heatmap = submenu_id.replaceAll('-', '_');
    window[create_heatmap]();
}

function capability_view(model_id, panes){
    var results = {};
    var predicates = {};
    
    $.ajaxSetup({
        async: false
    });

    var capability_concept = null;
    $.getJSON('/api/rest/model/' + model_id + "/concepts/" + configuration['concepts']['capability'], (data) => {
        capability_concept = data;
    });

    var predicates = {};
    var slots = {};
    for (const [predicate_key, predicate_id] of Object.entries(configuration['predicates'])){
        if (predicate_key.includes('capability')){
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

    // var process_concept = null;
    // $.getJSON('/api/rest/model/' + model_id + "/concepts?name=" + configuration['process'], (data) => {
    //     console.log(JSON.stringify(data, undefined, 2));
    //     process_concept = data['results'][0];
    // });

    $.getJSON('/api/rest/model/' + model_id + '/instances?concept_id=' + configuration['concepts']['capability'], (data) => {
        results = data['results'];
    });
    for (i in results){
        cap = results[i]
        capabilities[cap.id] = cap;
        for (const [predicate_key, predicate_id] of Object.entries(configuration['predicates'])){
            if (predicate_key.includes('capability')){
                capabilities[cap.id][predicate_key] = {'slots': {}, 'inslots':{}};
                if (predicates[predicate_key]){
                    for (const [slot_id, slot] of Object.entries(predicates[predicate_key]['slots'])){
                        if (slot.subject == cap.id){
                            capabilities[cap.id][predicate_key]['slots'][slot_id] = slot;
                        }
                        if (slot.object == cap.id){
                            capabilities[cap.id][predicate_key]['inslots'][slot_id] = slot;
                        }
                    }
                }
            }
        }
    }
    cap_roots = restructure_capabilities(capabilities);
    populate_capabilities(panes, capabilities, cap_roots);

    $('.menu-item').click(function() {
        var submenu_id  = this.id;
        create_capability_subview(submenu_id);
    });

    $.ajaxSetup({
        async: true
    });
}