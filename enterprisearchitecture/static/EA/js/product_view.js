function get_product_menu_markup(){
    var menu_markup = "<span class='label-1 menu-label'>&nbsp;</span> Capabilité";
    menu_markup += "<span class='label-2 menu-label'>&nbsp;</span> Contrat";
    return menu_markup;
}

function restructure_products(items){
    var prod_roots = [];
    for (const [prod_id, prod_data] of Object.entries(items)){
        if (prod_data['product_partof_product']){
            if (Object.keys(prod_data['product_partof_product']['slots']).length === 0){
                prod_roots.push(prod_id);         
            }
            items[prod_id]['children'] = [];
            for (const[slot_id, slot] of Object.entries(prod_data['product_partof_product']['inslots'])){
                items[prod_id]['children'].push(slot['subject']);
            }
        }
        items[prod_id]['services'] = 0;
        if (prod_data['service_partof_product']){
            items[prod_id]['services'] = Object.keys(prod_data['service_partof_product']['slots']).length;
        }
        items[prod_id]['contracts'] = 0;
        if (prod_data['contract_partof_product']){
            items[prod_id]['contracts'] = Object.keys(prod_data['contract_partof_product']['slots']).length;
        }
    }
    return prod_roots;
}


function get_product_markup(products, prod_id){
    const prod = products[prod_id];
    var prod_markup = `<div id='${prod.id}'>`;
    prod_markup += `<table class='item-details'>`;
    prod_markup += `<tr>`;
    prod_markup += `<td colspan="2"><a href='/o_instance/detail/${prod.id}'>${prod.name}</a></td>`;
    prod_markup += `</tr><tr>`;
    prod_markup += `<td class='label-1'><span>${prod.services}</span></td>`;
    prod_markup += `<td class='label-2'><span>${prod.contracts}</span></td>`;
    prod_markup += `</tr>`;
    prod_markup += `</table>`;
    prod_markup += `</div>`;
    
    for (const next_prod_id of prod['children']){
        prod_markup += `<div>${get_product_markup(products, next_prod_id)}</div>`;
    }
    return `<div class='infobox'>${prod_markup}</div>`;
}


function populate_products(dataPaneId, menuPaneId, products, prod_roots){
    const dataPane = $('#' + dataPaneId);
    const menuPane = $('#' + menuPaneId);
    var root_prod_markup = '';
    for (const root_prod_id of prod_roots){
        root_prod_markup += `${get_product_markup(products, root_prod_id)}`;
    }
    menuPane.html(get_product_menu_markup());
    dataPane.html('<div class="infobox">' + root_prod_markup + '</div>');
}

function product_view(model_id, dataPaneId, menuPaneId){
    var results = {};
    var products = {};
    var predicates = {};
    
    $.ajaxSetup({
        async: false
    });

    var product_concept = null;
    $.getJSON('/api/rest/model/' + model_id + "/concepts/" + configuration['concepts']['product'], (data) => {
        product_concept = data;
    });

    var predicates = {};
    var slots = {};
    for (const [predicate_key, predicate_id] of Object.entries(configuration['predicates'])){
        if (predicate_key.includes('product')){
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

    $.getJSON('/api/rest/model/' + model_id + '/instances?concept_id=' + configuration['concepts']['product'], (data) => {
        results = data['results'];
    });
    for (i in results){
        prod = results[i]
        products[prod.id] = prod;
        for (const [predicate_key, predicate_id] of Object.entries(configuration['predicates'])){
            if (predicate_key.includes('product')){
                products[prod.id][predicate_key] = {'slots': {}, 'inslots':{}};
                if (predicates[predicate_key]){
                    for (const [slot_id, slot] of Object.entries(predicates[predicate_key]['slots'])){
                        if (slot.subject == prod.id){
                            products[prod.id][predicate_key]['slots'][slot_id] = slot;
                        }
                        if (slot.object == prod.id){
                            products[prod.id][predicate_key]['inslots'][slot_id] = slot;
                        }
                    }
                }
            }
        }
    }
    var prod_roots = restructure_products(products);
    populate_products(dataPaneId, menuPaneId, products, prod_roots);

    $.ajaxSetup({
        async: true
    });
}