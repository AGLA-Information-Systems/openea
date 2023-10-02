
function process_report(model){

    var risques = {}
    var impacts = {}
    var probabilites = {}


    for (const [instance_id, instance] of Object.entries(model.instances)){
        if (instance.concept == 'Risque Organisationnel'){
            risques[instance.id] = instance;
        }
        if (instance.concept == 'Impact de risque'){
            impacts[instance.id] = instance;
        }
        if (instance.concept == 'Probabilité de risque'){
            probabilites[instance.id] = instance;
        }
    }

    var results = {'risques': {}, 'impacts': impacts, 'probabilites': probabilites}
    for (const [probabilite_id, probabilite] of Object.entries(probabilites)){
        for (const [impact_id, impact] of Object.entries(impacts)){
            results['risques'][probabilite_id + ',' + impact_id] = []
        }
    }

    for (const [risque_id, risque] of Object.entries(risques)){
        var impact_id = null
        impacts = get_object_slot_values(model, risque, 'Impact de risque est une propriété de Risque', 'Impact de risque');
        if (impacts.length >= 1){
            impact_id = impacts[0].id
        }
        var probabilite_id = null
        probabilites = get_object_slot_values(model, risque, 'Probabilité de risque est une propriété de Risque', 'Probabilité de risque');
        if (probabilites.length >= 1){
            probabilite_id = probabilites[0].id
        }
        results['risques'][probabilite_id + ',' + impact_id].push(risque)
    }

    $("#report").html(generate_double_entry_table(results));
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


function generate_double_entry_table(results) {
    //console.log(results)
    // creates a <table> element and a <tbody> element
    const tbl = document.createElement("table");
    tbl.className = 'table  table-hover';
    const tblBody = document.createElement("tbody");
  
    const max_i = results['probabilites'].length
    const max_j = results['impacts'].length
    var i = 0
    var j = 0
    // creating all cells
    const header_row = document.createElement("tr");

    const empty_cell = document.createElement("th");
    header_row.appendChild(empty_cell);

    for (const [impact_id, impact] of Object.entries(results['impacts'])) {
        const cell = document.createElement("th");
        const cellText = document.createTextNode(`${impact.name}`);
        cell.appendChild(cellText);
        header_row.appendChild(cell);
    }
    tblBody.appendChild(header_row);

    for (const [probabilite_id, probabilite] of Object.entries(results['probabilites'])) {
    
      // creates a table row
      const row = document.createElement("tr");

        const header_cell = document.createElement("th");
        const cellText = document.createTextNode(`${probabilite.name}`);
        header_cell.appendChild(cellText);
        row.appendChild(header_cell);

  
      for (const [impact_id, impact] of Object.entries(results['impacts'])) {
        // Create a <td> element and a text node, make the text
        // node the contents of the <td>, and put the <td> at
        // the end of the table row      

        const cell = document.createElement("td");
        cell_data = []
        for (risque of results['risques'][probabilite_id + ',' + impact_id]){
            console.log(risque)
            var a = document.createElement('a'); 
            // Create the text node for anchor element.
            var link = document.createTextNode(risque.code);  
            // Append the text node to anchor element.
            a.appendChild(link);
            a.title = risque.name;   
                // Set the href property.
            a.href = risque.url; 
            //cell_data.push(a)
            cell.appendChild(a);
        }
        //const cellText = document.createTextNode(`${cell_data.join(',')}`);
        //cell.appendChild(cellText);
        row.appendChild(cell);
      }
  
      // add the row to the end of the table body
      tblBody.appendChild(row);
    }
  
    // put the <tbody> in the <table>
    tbl.appendChild(tblBody);
    // sets the border attribute of tbl to '2'
    //tbl.setAttribute("border", "2");
    return tbl;
  }