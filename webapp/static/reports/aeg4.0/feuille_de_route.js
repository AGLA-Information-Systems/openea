
function process_report(model){

    var constats = {}
    var ecarts = {}
    var cibles = {}
    var valeurs = {}

    for (const [instance_id, instance] of Object.entries(model.instances)){
        if (instance.concept == 'Constat'){
            constats[instance.id] = instance;
        }
        /*if (instance.concept == 'Écart'){
            ecarts[instance.id] = instance;
        }
        if (instance.concept == 'Cible'){
            cibles[instance.id] = instance;
        }*/
    }

    results = {}
    tags = {}

    for (const [constat_id, constat] of Object.entries(constats)){
        results[constat_id] = {'constat': constat,
                                'ecarts': {},
                                'cibles': {}};
        ecarts = get_object_slot_values(model, constat, 'Écart est associé à Constat', 'Écart');
        for (const ecart of ecarts){
            results[constat_id]['ecarts'][ecart.id] = ecart;
        }
        cibles = get_object_slot_values(model, constat, 'Cible est associé à Constat', 'Cible');
        for (const cible of cibles){
            results[constat_id]['cibles'][cible.id] = cible;
        }
    }

    $("#report").html(build_aeg_fdr(results));
    return true;
}

function get_subject_slot_values(model, instance, slot_predicate, slot_concept){
    slot_values = [];
    for (const [slot_id, slot] of Object.entries(instance['ownslots'])){
        if (slot.predicate == slot_predicate && slot.concept == slot_concept){
            slot_values.push(model.instances[slot.object_id]);
        }
    }
    return slot_values;
}

function get_object_slot_values(model, instance, slot_predicate, slot_concept){
    slot_values = [];
    for (const [slot_id, slot] of Object.entries(instance['inslots'])){
        if (slot.predicate == slot_predicate && slot.concept == slot_concept){
            slot_values.push(model.instances[slot.subject_id]);
        }
    }
    return slot_values;
}

function build_aeg_fdr(results){
    let fdr = `

<style type='text/css'>
* {
    box-sizing: border-box;
}

.transformation-num {
    padding: 0;
    list-style-type: none;
    /*font-family: arial;*/
    /*font-size: 12px;*/
    clear: both;
    line-height: 1em;
    margin: 0 -1px;
    text-align: center;
}

.transformation-num > li {
    float: left;
    padding: 10px 30px 10px 40px;
    background: #333;
    color: #fff;
    position: relative;
    border-top: 1px solid #666;
    border-bottom: 1px solid #666;
    width: 32%;
    margin: 0 1px;
}

.transformation-num  > li:before {
    content: '';
    border-left: 16px solid #fff;
    border-top: 16px solid transparent;
    border-bottom: 16px solid transparent;
    position: absolute;
    top: 0;
    left: 0;
    
}
.transformation-num  > li:after {
    content: '';
    border-left: 16px solid #333;
    border-top: 16px solid transparent;
    border-bottom: 16px solid transparent;
    position: absolute;
    top: 0;
    left: 100%;
    z-index: 20;
}

.transformation-num  > li.transformation {
    background: #555;
}

.transformation-num  > li.transformation:after {
    border-left-color: #555;
}
</style>
`;

   
fdr = fdr +  
`
<div>
<ul class="transformation-num">
    <li>Situation actuelle</li>
    <li class="active">Transformation</li>
    <li>Cible</li>
</ul>`

for (const [constat_id, result] of Object.entries(results)){
    fdr = fdr + 
` <ul class="transformation-num">
  <li>${result['constat'].name}</li>
  <li class="transformation">
    <ol> `
    for (const [ecart_id, ecart] of Object.entries(result['ecarts'])){
        fdr = fdr + `<li>${ecart.name}</li>`
    }
    fdr = fdr + 
`   </ol>
  </li>
  <li>`
    if (Object.keys(result['cibles']).length == 1){
        console.log(result)   
        for (const [cible_id, cible] of Object.entries(result['cibles'])){
            fdr = fdr + cible.name
        }
    }else{
        fdr = fdr + `<ol> `
        for (const [cible_id, cible] of Object.entries(result['cibles'])){
            fdr = fdr + `<li>${cible.name}</li>`
        }
        fdr = fdr + `</ol>`
    }
    fdr = fdr + 
`</li></ul>`
}


fdr = fdr + `
<ul class="transformation-num">
    <li>Situation actuelle</li>
    <li class="active">Transformation</li>
    <li>Cible</li>
</ul></div>`;
    return fdr;
}