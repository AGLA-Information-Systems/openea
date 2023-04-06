var couts_benefices_def = {'cout': 'Coûts', 'benefice': 'Bénéfices'}

var unit_to_seconds = {
    'Heure': 60*60,
    'Jour': 24*60*60,
    'Jour ouvrable': 7*60*60,
    'Semaine': 7*24*60*60,
    'Semaine ouvrable': 5*7*60*60,
    'Mois': 30.5*24*60*60,
    'Mois ouvrable': 20*7*60*60,
    'Année': 365*24*60*60
}

var years = {}
today = new Date()
for(var i = 0; i < 10; i++){
    years[''+i] = {'debut': null,'fin': null}
    years[''+i]['debut'] = new Date(today.getTime() + i*unit_to_seconds['Année']*1000);
    years[''+i]['fin'] = new Date(today.getTime() + (i+1)*unit_to_seconds['Année']*1000);
}

function process_report(model){
    
    var type_benefices = ['Coût']
    var type_couts = ['Bénéfice']
    for (const [predicate_id, predicate] of Object.entries(model.predicates)){
        if (predicate.relation == 'is-a' && predicate.object == 'Coût'){
            type_couts.push(predicate.subject);
        }
        if (predicate.relation == 'is-a' && predicate.object == 'Bénéfice'){
            type_benefices.push(predicate.subject);
        }
    }

    var toutes_les_unite_de_temps = {}
    var tous_les_montants = []
    var allocations = {}
    var valeurs = {}
    var durees_en_unite_de_temps = {}
    for (const [instance_id, instance] of Object.entries(model.instances)){
        if (instance.concept == 'Unité de temps'){
            toutes_les_unite_de_temps[instance.id] = instance;
        }
        if (instance.concept == 'Montant'){
            tous_les_montants.push(instance);
        }
        if (instance.concept == 'Allocation de Ressource'){
            allocations[instance.id] = instance;
        }
        if (instance.concept == 'Valeur'){
            valeurs[instance.id] = instance;
        }
        if (instance.concept == 'Durée'){
            durees_en_unite_de_temps[instance.id] = instance;
        }
    }

    //Total
    var totaux = {
        'benefices': {},
        'couts': {},
    };

    for (const [benefice_id, benefice] of Object.entries(valeurs)){
        totaux['benefices'][benefice_id] = {'date_debut': new Date(),
                                            'duree': {},
                                            'montant': {},
                                            'nom': benefice.name};
        durees = {};
        durees_par_unite_de_temps = {};
        montants = {};
        montants_par_unite_de_temps =  {};
        dates_de_debut = get_slot_values(model, benefice, 'Date de Début');
        if (dates_de_debut.length > 0){
            totaux['benefices'][benefice_id]['date_debut'] = new Date(dates_de_debut[0].name);
        }
            
        durees = get_slot_values(model, benefice, 'Durée');
        unites_de_temps = get_slot_values(model, durees[0], 'Unité de temps');
        totaux['benefices'][benefice_id]['duree_en_s'] = parseFloat(durees[0].name)*unit_to_seconds[unites_de_temps[0].name];
        totaux['benefices'][benefice_id]['duree'] = durees[0].name +' '+ unites_de_temps[0].name;

        montants = get_slot_values(model, benefice, 'Montant');
        unites_de_temps = get_slot_values(model, montants[0], 'Unité de temps');
        totaux['benefices'][benefice_id]['montant_per_s'] = parseFloat(montants[0].name) / unit_to_seconds[unites_de_temps[0].name];
        totaux['benefices'][benefice_id]['montant'] = montants[0].name+' par '+ unites_de_temps[0].name;
        totaux['benefices'][benefice_id]['montant_total'] = parseFloat(totaux['benefices'][benefice_id]['montant_per_s']) * parseFloat(totaux['benefices'][benefice_id]['duree_en_s'])
        valuate_by_year(totaux['benefices'][benefice_id]);
    }

    for (const [cout_id, cout] of Object.entries(allocations)){
        totaux['couts'][cout_id] = {'date_debut': new Date(),
                                    'duree': {},
                                    'montant': {},
                                    'nom': cout.name};
        durees = {};
        durees_par_unite_de_temps = {};
        montants = {};
        montants_par_unite_de_temps =  {};
        
        dates_de_debut = get_slot_values(model, cout, 'Date de Début');
        if (dates_de_debut.length > 0){
            totaux['couts'][cout_id]['date_debut'] = new Date(dates_de_debut[0].name);
        }

        durees = get_slot_values(model, cout, 'Durée');
        unites_de_temps = get_slot_values(model, durees[0], 'Unité de temps');
        totaux['couts'][cout_id]['duree_en_s'] = parseFloat(durees[0].name)*unit_to_seconds[unites_de_temps[0].name];
        totaux['couts'][cout_id]['duree'] = durees[0].name +' '+ unites_de_temps[0].name;

        montants = get_slot_values(model, cout, 'Montant');
        unites_de_temps = get_slot_values(model, montants[0], 'Unité de temps');
        totaux['couts'][cout_id]['montant_per_s'] = parseFloat(montants[0].name) / unit_to_seconds[unites_de_temps[0].name];
        totaux['couts'][cout_id]['montant'] = montants[0].name+' par '+ unites_de_temps[0].name;
        totaux['couts'][cout_id]['montant_total'] = parseFloat(totaux['couts'][cout_id]['montant_per_s']) * parseFloat(totaux['couts'][cout_id]['duree_en_s'])
        valuate_by_year(totaux['couts'][cout_id]);
    }

    var totaux_par_an = {}
    for (const [year_index, year] of Object.entries(years)){
        totaux_par_an[year_index] = {
            'couts': 0,
            'benefices': 0
        }
        for (const [x_id, x] of Object.entries(totaux['couts'])){
            totaux_par_an[year_index]['couts'] = parseFloat(totaux_par_an[year_index]['couts']) + parseFloat(x['years'][year_index])
        }
        for (const [x_id, x] of Object.entries(totaux['benefices'])){
            totaux_par_an[year_index]['benefices'] = parseFloat(totaux_par_an[year_index]['benefices']) + parseFloat(x['years'][year_index])
        }
    }
    

    $("#report").html(build_report_table(totaux_par_an) + '<br>' + build_list_table(totaux));
    return true;
}

function get_slot_values(model, subjet, slot_concept){
    slot_values = [];
    for (const [slot_id, slot] of Object.entries(subjet['ownslots'])){
        if (slot.concept == slot_concept){
            slot_values.push(model.instances[slot.object_id]);
        }
    }
    return slot_values;
}

function build_report_table(totaux_par_an){
    //set header of table
let table = `
<table class="table table-fluid" id = "myTable">
  <thead>
    <tr>
      <th scope="col">Année" %}</th>
      <th scope="col">Coûts" %}</th>
      <th scope="col">Bénéfices" %}</th>
      <th scope="col">Valeur" %}</th>
    </tr>
  </thead>
  <tbody>
  `;
  //create//append rows
for (const [year_index, year] of Object.entries(years)){
    table = table +
    `<tr>
      <th scope="row">${year_index}" %}</th>
      <td>${totaux_par_an[year_index]['couts'].toFixed(0)}</td>
      <td>${totaux_par_an[year_index]['benefices'].toFixed(0)}</td>
      <td>${totaux_par_an[year_index]['benefices'].toFixed(0) - totaux_par_an[year_index]['couts'].toFixed(0)}</td>
    </tr>`
}
//close off table
table = table +
  `</tbody>
  </table>`
  ;

  return table;
}

function build_list_table(totaux){
    //set header of table
let table = `
<table class="table table-fluid" id = "myTable">
  <thead>
    <tr>
      <th scope="col">type" %}</th>
      <th scope="col">Nom" %}</th>
      <th scope="col">Montant" %}</th>
      <th scope="col">Durée" %}</th>
      <th scope="col">Total" %}</th>
    </tr>
  </thead>
  <tbody>
  `;
  //create//append rows
  for ( const[type_code, type_display] of Object.entries(couts_benefices_def)){
    total = 0.0
    for (const [element_id, element] of Object.entries(totaux[type_code+'s'])){
        montant_total = element['montant_total']
        total = parseFloat(total) + parseFloat(montant_total)
         
        table = table +
        `<tr>
          <td>${type_display}</td>
          <td>${element['nom']}</td>
          <td>${element['montant']}</td>
          <td>${element['duree']}</td>
          <td>${montant_total.toFixed(0)}</td>
        </tr>`
    }
    table = table +
        `<tr>
          <td><strong>${type_display}</strong></td>
          <td></td>
          <td></td>
          <td></td>
          <td><strong>${total.toFixed(0)}</strong></td>
        </tr>`
  }

//close off table
table = table +
  `</tbody>
  </table>`
  ;

  return table;
}

  
function valuate_by_year(item) {
    item['years'] = {};
    //split by year
    for (const [year_index, year] of Object.entries(years)){
        var date_debut = item['date_debut'];
        var date_fin = new Date(date_debut);
        date_fin.setSeconds(date_fin.getSeconds() + item['duree_en_s']);

        //console.log(date_debut);
        //console.log(date_fin);

        if (item['date_debut'] < year['debut']){
            date_debut = year['debut'];
        }
        if (date_fin > year['fin']){
            date_fin = year['fin'];
        }
        //console.log(date_debut);
        //console.log(date_fin);
        seconds_in_current_year = (date_fin.getTime() - date_debut.getTime()) / 1000;
        item['years'][year_index] = 0
        if (seconds_in_current_year >= 0){
            item['years'][year_index] = parseFloat(item['montant_per_s'])*seconds_in_current_year;
        }
    }
}