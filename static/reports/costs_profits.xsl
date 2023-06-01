<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                              xmlns:xs="http://www.w3.org/2001/XMLSchema"
                              xmlns:my="my:my">

<xsl:variable name="type_dates"  select="/model/predicates/predicate[object = 'Date' and relation = 'is-a']"/>
<xsl:variable name="type_durees"  select="/model/predicates/predicate[object = 'Durée' and relation = 'is-a']"/>

<xsl:variable name="types_benefices"  select="/model/predicates/predicate[object = 'Bénéfice' and relation = 'is-a']/subject"/>
<xsl:variable name="types_couts"  select="/model/predicates/predicate[object = 'Coût' and relation = 'is-a']/subject"/>

<xsl:variable name="unites_de_temps"  select="/model/instances/instance[concept = 'Unité de temps']"/>
<xsl:variable name="allocations"  select="/model/instances/instance[concept = 'Allocation de Ressource']"/>
<xsl:variable name="valeurs"  select="/model/instances/instance[concept = 'Valeur']"/>

<xsl:variable name="tous_les_montants"  select="/model/instances/instance[concept = 'Montant']"/>


<xsl:template match="/">
<div id="results">
<script id="the_script" type="application/javascript">
  var  unites_de_temps = [<xsl:for-each select="$unites_de_temps"><xsl:text>"</xsl:text><xsl:value-of select="./name"/><xsl:text>"</xsl:text><xsl:if test="not(position() = last())">,</xsl:if></xsl:for-each>];
  var  allocations = {};
  <xsl:for-each select="$allocations">
    <xsl:variable name="allocation_id"  select="./@id"/>
    <xsl:variable name="allocation_durees"  select="/model/instances/instance[concept = 'Durée' and inslots/slot/subject/@id = $allocation_id]"/>
    <xsl:variable name="allocation_montants"  select="/model/instances/instance[concept = 'Montant' and inslots/slot/subject/@id = $allocation_id]"/>
    <xsl:variable name="allocation_date_debut"  select="/model/instances/instance[concept = 'Date de début' and inslots/slot/subject/@id = $allocation_id]"/>
    allocations['<xsl:value-of select="$allocation_id" />'] = {};
    <xsl:for-each select="$unites_de_temps">
      <xsl:variable name="unite_de_temps"  select="."/>
      <xsl:variable name="unite_de_temps_id"  select="$unite_de_temps/@id"/>
      allocations['<xsl:value-of select="$allocation_id" />']['<xsl:value-of select="./name" />'] = {};
      <xsl:variable name="duree_en_unite_de_temps"  select="$allocation_durees[ownslots/slot/object/@id = $unite_de_temps_id]/name"/>
      allocations['<xsl:value-of select="$allocation_id" />']['<xsl:value-of select="./name" />']['duree_en_unite_de_temps'] = [<xsl:for-each select="$duree_en_unite_de_temps"><xsl:text>"</xsl:text><xsl:value-of select="."/><xsl:text>"</xsl:text><xsl:if test="not(position() = last())">,</xsl:if></xsl:for-each>];
      <xsl:variable name="montant_par_unite_de_temps"  select="$allocation_montants[ownslots/slot/object/@id = $unite_de_temps_id]/name"/>
      allocations['<xsl:value-of select="$allocation_id" />']['<xsl:value-of select="./name" />']['montant_par_unite_de_temps'] = [<xsl:for-each select="$montant_par_unite_de_temps"><xsl:text>"</xsl:text><xsl:value-of select="."/><xsl:text>"</xsl:text><xsl:if test="not(position() = last())">,</xsl:if></xsl:for-each>];
    </xsl:for-each>
  </xsl:for-each>

  var  valeurs = {};
  <xsl:for-each select="$valeurs">
    <xsl:variable name="valeur_id"  select="./@id"/>
    <xsl:variable name="valeur_durees"  select="/model/instances/instance[concept = 'Durée' and inslots/slot/subject/@id = $valeur_id]"/>
    <xsl:variable name="valeur_montants"  select="/model/instances/instance[concept = 'Montant' and inslots/slot/subject/@id = $valeur_id]"/>
    valeurs['<xsl:value-of select="$valeur_id" />'] = {};
    <xsl:for-each select="$unites_de_temps">
      <xsl:variable name="unite_de_temps"  select="."/>
      <xsl:variable name="unite_de_temps_id"  select="$unite_de_temps/@id"/>
      valeurs['<xsl:value-of select="$valeur_id" />']['<xsl:value-of select="./name" />'] = {};
      <xsl:variable name="duree_en_unite_de_temps"  select="$valeur_durees[ownslots/slot/object/@id = $unite_de_temps_id]/name"/>
      valeurs['<xsl:value-of select="$valeur_id" />']['<xsl:value-of select="./name" />']['duree_en_unite_de_temps'] = [<xsl:for-each select="$duree_en_unite_de_temps"><xsl:text>"</xsl:text><xsl:value-of select="."/><xsl:text>"</xsl:text><xsl:if test="not(position() = last())">,</xsl:if></xsl:for-each>];
      <xsl:variable name="montant_par_unite_de_temps"  select="$valeur_montants[ownslots/slot/object/@id = $unite_de_temps_id]/name"/>
      valeurs['<xsl:value-of select="$valeur_id" />']['<xsl:value-of select="./name" />']['montant_par_unite_de_temps'] = [<xsl:for-each select="$montant_par_unite_de_temps"><xsl:text>"</xsl:text><xsl:value-of select="."/><xsl:text>"</xsl:text><xsl:if test="not(position() = last())">,</xsl:if></xsl:for-each>];
    </xsl:for-each>
  </xsl:for-each>
  

  function calculer_valeur(){
    var totaux = {
      'benefices': {},
      'couts': {},
    };
    
    for (const [benefice_id, montants_benefices] of Object.entries(valeurs)){
      console.log(montants_benefices);
      totaux['benefices'][benefice_id] = 0
      for (const unite_de_temps of unites_de_temps){

        if (montants_benefices[unite_de_temps]['montant_par_unite_de_temps'][0]){
          if (montants_benefices[unite_de_temps]['duree_en_unite_de_temps'][0] === undefined){
            montants_benefices[unite_de_temps]['duree_en_unite_de_temps'] = [1] 
          }
          console.log(montants_benefices[unite_de_temps]['montant_par_unite_de_temps'][0]);
          console.log(montants_benefices[unite_de_temps]['duree_en_unite_de_temps'][0]);
          montant_calc = parseFloat(montants_benefices[unite_de_temps]['duree_en_unite_de_temps'][0]) * parseFloat(montants_benefices[unite_de_temps]['montant_par_unite_de_temps'][0]).toFixed(2);
          totaux['benefices'][benefice_id] = totaux['benefices'][benefice_id] + montant_calc;
        }
      }
    }


    var total_benefice = 0;
    for (const [id, montant] of Object.entries(totaux['benefices'])){
      total_benefice = total_benefice + montant;
    }

    for (const [cout_id, montants_couts] of Object.entries(allocations)){
      
      totaux['couts'][cout_id] = 0
      for (const unite_de_temps of unites_de_temps){
        
        if (montants_couts[unite_de_temps]['montant_par_unite_de_temps'][0]){
          if (montants_couts[unite_de_temps]['duree_en_unite_de_temps'][0] === undefined){
            montants_couts[unite_de_temps]['duree_en_unite_de_temps'] = [1] 
          }
          console.log(montants_couts[unite_de_temps]['montant_par_unite_de_temps'][0]);
          console.log(montants_couts[unite_de_temps]['duree_en_unite_de_temps'][0]);
          montant_calc = parseFloat(montants_couts[unite_de_temps]['duree_en_unite_de_temps'][0]) * parseFloat(montants_couts[unite_de_temps]['montant_par_unite_de_temps'][0]).toFixed(2);
          totaux['couts'][cout_id] = totaux['couts'][cout_id] + montant_calc;
        }
      }
    }
    var total_cout = 0;
    for (const [id, montant] of Object.entries(totaux['couts'])){
      total_cout = total_cout + montant;
    }

    var valeur_totale = total_benefice - total_cout;
    
    document.getElementById("total_cout").innerHTML = total_cout;
    document.getElementById("total_benefice").innerHTML = total_benefice;
    document.getElementById("valeur_totale").innerHTML = valeur_totale;
    
    console.log(allocations);
    console.log(valeurs);
    console.log(totaux);
  }

</script>
<div id="results_table">
  

  <table class="table table-fluid"  id='cb_table'>
    <thead>
        <tr>
            <th>Cout Total</th>
            <th>Bénéfice Total</th>
            <th>Valeur</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td id='total_cout'></td>
            <td id='total_benefice'></td>
            <td id='valeur_totale'></td>
        </tr>
    </tbody>
  </table>
  <hr/>
  <table class="table table-fluid"  id='cb_detail_table_3'>
    <thead>
        <tr>
            <th>Benefice</th>
            <th>Cout</th>
            <th>Montant</th>
            <th>Unité de temps</th>
        </tr>
    </thead>
    <tbody>
      <xsl:for-each select="$tous_les_montants">
        <xsl:variable name="montant_id"  select="./@id"/>
        <xsl:variable name="montant_name"  select="./name"/>
        <xsl:variable name="unité_de_temps"  select="/model/instances/instance[concept = 'Unité de temps' and inslots/slot/subject/@id = $montant_id]"/>
        <xsl:variable name="cout"  select="/model/instances/instance[contains($types_couts, concept) and ownslots/slot/object/@id = $montant_id]"/>
        <xsl:variable name="benefice"  select="/model/instances/instance[contains($types_benefices, concept) and ownslots/slot/object/@id = $montant_id]"/>
        <tr>
            <td>
              <xsl:element name="a">
                <xsl:attribute name="href">
                  <xsl:value-of select="$benefice/id"/>
                </xsl:attribute>
                <xsl:value-of select="$benefice/name"/>
              </xsl:element>
            </td>
            <td>
              <xsl:element name="a">
                <xsl:attribute name="href">
                  <xsl:value-of select="$cout/id"/>
                </xsl:attribute>
                <xsl:value-of select="$cout/name"/>
              </xsl:element>
            </td>
            <td>
              <xsl:element name="a">
                <xsl:attribute name="href">
                  <xsl:value-of select="$montant_id"/>
                </xsl:attribute>
                <xsl:value-of select="$montant_name"/>
              </xsl:element>
            </td>
            <td>
              <xsl:element name="a">
                <xsl:attribute name="href">
                  <xsl:value-of select="$unité_de_temps/id"/>
                </xsl:attribute>
                <xsl:value-of select="$unité_de_temps/name"/>
              </xsl:element>
            </td>
        </tr>
      </xsl:for-each>
    </tbody>
  </table>
</div>
</div>
</xsl:template>

<xsl:variable name="vDate1" select="my:dateFromUsDate('04/06/2011')"/>
<xsl:variable name="vDate2" select="my:dateFromUsDate('04/06/2022')"/>
<xsl:sequence select="($vDate1 - $vDate2) div xs:dayTimeDuration('P1D')"/>

<xsl:function name="my:dateFromUsDate" as="xs:date">
  <xsl:param name="pUsDate" as="xs:string"/>
  <xsl:sequence select="xs:date(concat(substring($pUsDate,7,4),
                  '-',
                  substring($pUsDate,1,2),
                  '-',
                  substring($pUsDate,4,2)
                 )
          )"/>
</xsl:function>

</xsl:stylesheet>
