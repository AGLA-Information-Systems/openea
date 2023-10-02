var locations = {};
var loc_roots = [];
var legend = {};

//======
function location_toggle_stickers(){
    legend = {'label-1': 'Objectifs', 'label-2': 'Flux de valeur', 'label-3': 'Produits'};
    set_location_legend_markup();

    $('.sticker').toggle();
}

function location_heatmap_criticality(){
    legend = {};
    collect(locations, loc_roots, max_all, 'children', 'criticality');

    $('.gradient-1').removeClass();
    for (const [loc_id, loc_data] of Object.entries(locations)){
        $('#'+loc_data.id).addClass('gradient-1');
        $('#'+loc_data.id).addClass('gradient-1-' + loc_data.criticality);

        legend['gradient-1-' + loc_data.criticality] = loc_data.criticality;
    }

    set_location_legend_markup();
}
//======
function set_location_legend_markup(){
    var legend_markup = ``;
    for (const [legend_color, legend_item] of Object.entries(legend)){
        legend_markup += `<span class='legend-label ${legend_color}'>&nbsp;</span> ${legend_item}`;
    }
    return $('#' + panes['legend']).html(`${legend_markup}`);
}

function set_location_menu_markup(){
    var menu_markup = `<a class='menu-item' id='location-heatmap-maturity'>Maturité</a>`;
    menu_markup += `<a class='menu-item' id='location-heatmap-effectiveness'>Efficacité</a>`;
    menu_markup += `<a class='menu-item' id='location-heatmap-performance'>Performance</a>`;
    menu_markup += `<a class='menu-item' id='location-heatmap-value'>Valeur</a>`;
    menu_markup += `<a class='menu-item' id='location-heatmap-usage'>Utilisation</a>`;
    menu_markup += `<a class='menu-item' id='location-heatmap-cost-distribution'>Districution des coûts</a>`;
    menu_markup += `<a class='menu-item' id='location-heatmap-criticality'>Criticité</a>`;
    menu_markup += `<a class='menu-item' id='location-toggle-stickers'>Étiquettes</a>`;


    legend = {'label-1': 'Objectifs', 'label-2': 'Flux de valeur', 'label-3': 'Produits'};
    set_location_legend_markup();

    return $('#' + panes['menu']).html(`<div class='submenu'>${menu_markup}</div>`);
}


function restructure_locations(items){
    var loc_roots = [];
    for (const [loc_id, loc_data] of Object.entries(items)){
        if (loc_data['location_partof_location']){
            if (Object.keys(loc_data['location_partof_location']['slots']).length === 0){
                loc_roots.push(loc_id);         
            }
            items[loc_id]['children'] = [];
            for (const[slot_id, slot] of Object.entries(loc_data['location_partof_location']['inslots'])){
                items[loc_id]['children'].push(slot['subject']);
            }
        }
        items[loc_id]['applications'] = 0;
        if (loc_data['application_in_location']){
            items[loc_id]['applications'] = Object.keys(loc_data['application_in_location']['slots']).length;
        }
    }
    return loc_roots;
}


function get_location_markup(locations, loc_id){
    const loc = locations[loc_id];
    var loc_markup = `<div id='${loc.id}'>`;
    loc_markup += `<table class='item-details'>`;
    loc_markup += `<tr>`;
    loc_markup += `<td ><a href='/o_instance/detail/${loc.id}'>${loc.name}</a></td>`;
    loc_markup += `</tr><tr class="sticker">`;
    loc_markup += `<td class='label-1'><span>${loc.applications}</span></td>`;
    loc_markup += `</tr>`;
    loc_markup += `</table>`;
    loc_markup += `</div>`;
    
    for (const child_loc_id of loc['children']){
        loc_markup += `<div >${get_location_markup(locations, child_loc_id)}</div>`;
    }
    return `<div class='infobox'>${loc_markup}</div>`;
}


function populate_locations(panes, locations, loc_roots){
    const dataPane = $('#' + panes['data']);
    var root_loc_markup = '';
    for (const root_loc_id of loc_roots){
        root_loc_markup += `${get_location_markup(locations, root_loc_id)}`;
    }
    set_location_menu_markup();
    dataPane.html('<div class="infobox">' + root_loc_markup + '</div>');
}

function create_location_subview(submenu_id){
    const create_heatmap = submenu_id.replaceAll('-', '_');
    window[create_heatmap]();
}

function location_view(model_id, panes){
    var results = {};
    var predicates = {};
    
    $.ajaxSetup({
        async: false
    });

    var location_concept = null;
    $.getJSON('/api/rest/model/' + model_id + "/concepts/" + configuration['concepts']['location'], (data) => {
        location_concept = data;
    });

    var predicates = {};
    var slots = {};
    for (const [predicate_key, predicate_id] of Object.entries(configuration['predicates'])){
        if (predicate_key.includes('location')){
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


    $.getJSON('/api/rest/model/' + model_id + '/instances?concept_id=' + configuration['concepts']['location'], (data) => {
        results = data['results'];
    });
    for (i in results){
        loc = results[i]
        locations[loc.id] = loc;
        for (const [predicate_key, predicate_id] of Object.entries(configuration['predicates'])){
            if (predicate_key.includes('location')){
                locations[loc.id][predicate_key] = {'slots': {}, 'inslots':{}};
                if (predicates[predicate_key]){
                    for (const [slot_id, slot] of Object.entries(predicates[predicate_key]['slots'])){
                        if (slot.subject == loc.id){
                            locations[loc.id][predicate_key]['slots'][slot_id] = slot;
                        }
                        if (slot.object == loc.id){
                            locations[loc.id][predicate_key]['inslots'][slot_id] = slot;
                        }
                    }
                }
            }
        }
    }
    loc_roots = restructure_locations(locations);
    populate_locations(panes, locations, loc_roots);

    $('.menu-item').click(function() {
        var submenu_id  = this.id;
        create_location_subview(submenu_id);
    });

    $.ajaxSetup({
        async: true
    });
}
