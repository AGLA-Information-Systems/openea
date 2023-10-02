
function process_report(model){
    $("#report").html(build_aeg_tb());
    return true;
}

function build_aeg_tb(){
    let tb = `

<style type='text/css'>
.block-1 {margin:5px; padding:5px; text-align:center}
</style>

<div class=' bg-light border block-1' id='vision_et_orientations'>Vision et Orientations<br>
    <div class='row border block-1' >
    <div class='col bg-light border block-1' id='vision'>Vision</div>
    <div class='col bg-light border block-1' id='principe'>Principe</div>
    <div class='col bg-light border block-1' id='orientation'>Orientation</div>
    <div class='col bg-light border block-1' id='plan_strategique'>Plan stratégique</div>
    </div>
</div>

<div class='row' >

    <div class='col bg-light border block-1' id='segment_interoperabilite'>Segment d'interopérabilité<br>
        <div class='dnot bg-light border block-1' id='interoperabilite'>Interopérabilité
            <div class='dnot bg-light border block-1' id='interoperabilite_affaires'>Interopérabilité d'affaires</div>
            <div class='dnot bg-light border block-1' id='interoperabilite_information'>Interopérabilité de l'information</div>
            <div class='dnot bg-light border block-1' id='interoperabilite_applicative_technologique'>Interopérabilité applicative et technologique</div>
        </div>
    </div>

    <div class='col-8 bg-light border block-1' >
        <div class='dnot bg-light border block-1' id='volet_affaires'>Volet Affaires<br>

            <div class='row bg-light border block-1' >
                <div class='col bg-light border block-1' id='contexte_affaires'>Contexte d'affaires
                    <div class='dnot bg-light border block-1' id='cadre_legal_réglementaire'>Cadre légal et réglementaire</div>
                    <div class='dnot bg-light border block-1' id='programme'>Programme</div>
                    <div class='dnot bg-light border block-1' id='objectif'>Objectif</div>
                    <div class='dnot bg-light border block-1' id='indicateur_performance'>Indicateur de performance</div>
                </div>
                <div class='col bg-light border block-1' id='organisation'>Organisation<br>
                    <div class='dnot bg-light border block-1' id='clientele'>Clientele</div>
                    <div class='dnot bg-light border block-1' id='mission'>Mission</div>
                    <div class='dnot bg-light border block-1' id='unite_administrative'>Unité administrative</div>
                    <div class='dnot bg-light border block-1' id='organisme_public'>Organisme public</div>
                    <div class='dnot bg-light border block-1' id='role'>Rôle</div>
                    <div class='dnot bg-light border block-1' id='responsabilité'>Responsabilité</div>
                </div>
                <div class='col bg-light border block-1' id='prestation_service'>Prestation de service<br>
                    <div class='dnot bg-light border block-1' id='service'>Service
                        <div class='dnot bg-light border block-1' id='service_affaires'>Service d'affaires</div>
                    </div>
                    <div class='dnot bg-light border block-1' id='acteur'>Acteur</div>
                    <div class='dnot bg-light border block-1' id='processus'>Processus</div>
                    <div class='dnot bg-light border block-1' id='besoin'>Besoin</div>
                    <div class='dnot bg-light border block-1' id='resultat'>Résultat</div>
                </div>
            </div>
        </div>
        
        <div class='dnot bg-light border block-1' id='volet_information'>Volet Information<br>

            <div class='row bg-light border block-1' >
                <div class='col bg-light border block-1' id='balise_gestion_information'>Balise de gestion l'information
                    <div class='dnot bg-light border block-1' id='classification_information'>Classification de l'information</div>
                    <div class='dnot bg-light border block-1' id='droits_restrictions_acces'>Droits - Restrictions d'acces</div>
                    <div class='dnot bg-light border block-1' id='portee_information'>Portée de l'information</div>
                    <div class='dnot bg-light border block-1' id='calendrier_conservation'>Calendrier de conservation</div>
                    <div class='dnot bg-light border block-1' id='plan_diffusion_proactive'>Plan de diffusion proactive</div>
                    <div class='dnot bg-light border block-1' id='valeur_juridique_information'>Valeur juridique de l'information</div>
                </div>
                <div class='col bg-light border block-1' id='objet_information'>Objet d'information<br>
                    <div class='dnot bg-light border block-1' id='domaine_information'>Domaine d'information</div>
                    <div class='dnot bg-light border block-1' id='sujet_donnee'>Sujet de données</div>
                </div>
                <div class='col bg-light border block-1' id='dossier'>Dossier<br>
                    <div class='dnot bg-light border block-1' id='Document'>Document</div>
                </div>
            </div>
        </div>
        <div class='dnot bg-light border block-1' id='volet_application'>Volet Application<br>
            <div class='row bg-light border block-1' >
                <div class='col bg-light border block-1' id='catalogue_services'>Catalogue de services
                    <div class='dnot bg-light border block-1' id='service_'>Service
                        <div class='dnot bg-light border block-1' id='service_applicatif'>Service applicatif</div>
                    </div>
                    <div class='dnot bg-light border block-1' id='contrat_service'>Contrat de service</div>
                </div>
                <div class='col bg-light border block-1' id='actif_informatique'>Actif informatique<br>
                    <div class='row bg-light border block-1' >
                        <div class='col bg-light border block-1' id='composante_technologique'>Composante technologique
                            <div class='dnot bg-light border block-1' id='logiciel'>Logiciel
                                <div class='dnot bg-light border block-1' id='logiciel_applicatif'>Logiciel applicatif</div>
                                <div class='dnot bg-light border block-1' id='composant_logiciel'>Composant logiciel</div>
                            </div>
                        </div>
                        <div class='col bg-light border block-1' id='systeme_informatique'>Système informatique<br>
                            <div class='dnot bg-light border block-1' id='systeme_mission'>Système de mission</div>
                            <div class='dnot bg-light border block-1' id='systeme_soutien'>Système de soutien</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class='dnot bg-light border block-1' id='volet_infrastructure'>Volet Infrastructure<br>

            <div class='dnot bg-light border block-1' id='t_actif_informatique'>Actif informatique<br>
                <div class='row bg-light border block-1' >
                    <div class='col bg-light border block-1' id='t_composante_technologique'>Composante technologique
                        <div class='dnot bg-light border block-1' id='t_logiciel'>Logiciel
                            <div class='dnot bg-light border block-1' id='t_logiciel_infrastructure'>Logiciel d'infrastructure</div>
                        </div>
                        <div class='dnot bg-light border block-1' id='composante_virtuelle'>Composante virtuelle</div>
                        <div class='dnot bg-light border block-1' id='materiel_informatique'>Matériel informatique</div>
                    </div>
                    <div class='col bg-light border block-1' id='t_service_'>Service<br>
                        <div class='dnot bg-light border block-1' id='service_infrastructure'>Service d'infrastructure</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class='col bg-light border block-1' id='segment_securite'>Segment sécurité
        <div class='dnot bg-light border block-1' id='risque'>Risque</div>
        <div class='dnot bg-light border block-1' id='incidents'>Incidents</div>
        <div class='dnot bg-light border block-1' id='controle'>Contrôle</div>
        <div class='dnot bg-light border block-1' id='reponse'>Réponse</div>
        <div class='dnot bg-light border block-1' id='categorisation_information'>Catégorisation de l'information</div>
    </div>

</div>
  `;

    return tb;
}