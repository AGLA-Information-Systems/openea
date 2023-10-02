function sum_all(arr){
    return arr.reduce((a, b) => a + b, 0);
}
function max_all(arr){
    return arr.reduce((a, b) => Math.max(a, b), 0);
}
function min_all(arr){
    return arr.reduce((a, b) => Math.min(a, b), 0);
}

function collect_recurs(items, item_id, res_fn, children_key, res_key){
    const item = items[item_id];
    var res = [];
    for (const child_item_id of item[children_key]){
        res.push(collect_recurs(items, child_item_id, res_fn, children_key, res_key));
    }
    const compiled_res = res_fn(res);
    items[item_id][res_key] = compiled_res;
    return compiled_res;
}

function collect(items, item_roots, res_fn, children_key, res_key){
    var res = 0;
    for (const root_item_id of item_roots){
        res = collect_recurs(items, root_item_id, res_fn, children_key, res_key);
        items[root_item_id][res_key] = res;
    }
}