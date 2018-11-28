from lxml import etree
import pandas as pd
import datetime
import sys
import os
import re


def converter(path_args: list):
    search_pattern_1 = re.compile(r'[/\\]\w*\.csv')

    try:
        archive = os.path.normpath(path_args[0])
        last_slash = re.search(search_pattern_1, path_args[0])
        if last_slash is not None:
            name = '{}{}'.format(path_args[0][last_slash.span()[0] + 1:last_slash.span()[1] - 4], '.xml')
            destination = os.path.join(path_args[1], name)

            with open(destination, 'wb') as f:
                f.write(b'')

            if os.path.exists(archive):
                csv = pd.read_csv(archive, sep=';', header=0,
                                  names=['Cognome Lavoratore', 'Nome Lavoratore', 'Sesso Lavoratore',
                                         'Data Nascita Lavoratore',
                                         'Codice Comune Nascita Lavoratore', 'Codice Fiscale Lavoratore',
                                         'Codice Cittadinanza Lavoratore', 'Codice Comune domicilio Lavoratore',
                                         'Indirizzo Lavoratore (domicilio)', 'Cap domicilio Lavoratore',
                                         'codice Livello Istruzione Lavoratore', 'Codice Fiscale Datore di Lavoro',
                                         'Denominazione Datore di Lavoro', 'Settore Datore di Lavoro',
                                         'Pubblica Amministrazione',
                                         'Codice Comune Sede Legale', 'Cap Sede Legale', 'Indirizzo Sede Legale',
                                         'e-mail Sede Legale', 'Telefono Sede Legale', 'Fax Sede Legale',
                                         'Codice Comune Sede Lavoro', 'Cap Sede Lavoro', 'Indirizzo Sede Lavoro',
                                         'e-mail Sede Lavoro', 'Telefono Sede Lavoro', 'Fax Sede Lavoro',
                                         'Data Inizio rapporto di lavoro', 'Data Fine rapporto di lavoro',
                                         'Data Fine periodo formativo', 'Ente Previdenziale',
                                         'Codice Ente Previdenziale',
                                         'Pat INAIL', 'Codice agevolazione', 'Tipologia Contrattuale',
                                         'Socio Lavoratore',
                                         'Lavoratore in mobilita', 'Lavoro stagionale', 'Codice tipo Orario',
                                         'ore Settimanali Medie (solo se Part Time)', 'Qualifica Professionale ISTAT',
                                         'Assunzione obbligatoria', 'Categoria Lavoratore per Assunzione Obbligatoria',
                                         'Contratto collettivo applicato', 'Livello di Inquadramento',
                                         'Retribuzione / Compenso',
                                         'Lavoro in agricoltura', 'Giornate lavorative previste', 'Tipo lavorazione',
                                         'Codice categoria del Delegato (se diverso dal datore di lavoro)',
                                         'Codice Fiscale del Delegato (se diverso dal datore di lavoro)',
                                         'E-mail del soggetto che effettua la comunicazione', 'Tipo Comunicazione',
                                         'Assunzione per cause di forza maggiore', 'descrizione causa forza maggiore',
                                         'Codice comunicazione precedente', 'Titolo di soggiorno Lavoratore',
                                         'Numero titolo di soggiorno Lavoratore',
                                         'Motivo titolo di soggiorno Lavoratore',
                                         'Scadenza titolo di soggiorno Lavoratore',
                                         'Questura che ha rilasciato il titolo di soggiorno Lavoratore',
                                         'Sussistenza sistemazione alloggiativa (Modello Q) Lavoratore',
                                         'Impegno datore lavoro al pagamento spese rimpatrio  (Modello  Q) Lavoratore',
                                         'Tipologia soggetto promotore tirocinio',
                                         'Codice Fiscale soggetto promotore tirocinio',
                                         'Denominazione soggetto promotore tirocinio', 'Categoria tirocinante',
                                         'Tipologia tirocinio', 'Cognome Datore di Lavoro', 'Nome Datore di Lavoro',
                                         'Sesso Datore di Lavoro', 'Data di nascita Datore di Lavoro',
                                         'Codice Comune (o Stato estero) Nascita Datore di Lavoro',
                                         'Cittadinanza Datore di Lavoro',
                                         'Datore di Lavoro Soggiornante in Italia',
                                         'Titolo di soggiorno Datore di Lavoro',
                                         'Numero titolo di soggiorno Datore di Lavoro',
                                         'Motivo titolo di soggiorno Datore di Lavoro',
                                         'Scadenza titolo di soggiorno Datore di Lavoro',
                                         'Questura che ha rilasciato titolo soggiorno Datore di Lavoro',
                                         'Cognome Lavoratore Coobbligato', 'Nome Lavoratore Coobbligato',
                                         'Codice Fiscale Lavoratore Coobbligato', 'Sesso Lavoratore Coobbligato',
                                         'Data Nascita Lavoratore Coobbligato',
                                         'Codice Comune (o Stato estero) Nascita Lavoratore Coobbligato',
                                         'Codice Cittadinanza Lavoratore Coobbligato',
                                         'Codice Comune domicilio Lavoratore Coobbligato',
                                         'Indirizzo Lavoratore Coobbligato (domicilio)',
                                         'Cap domicilio Lavoratore Coobbligato',
                                         'codice Livello Istruzione Lavoratore Coobbligato',
                                         'Titolo di soggiorno Lavoratore Coobbligato',
                                         'Numero titolo di soggiorno Lavoratore Coobbligato',
                                         'Motivo titolo di soggiorno Lavoratore Coobbligato',
                                         'Scadenza titolo di soggiorno Lavoratore Coobbligato',
                                         'Questura che ha rilasciato il titolo soggiorno Lav Coobbligato',
                                         'Sussistenza sistemazione alloggiativa (ModelloQ) Lav Coobbligato',
                                         'Impegno datore lavoro spese rimpatrio (ModelloQ) Lav Coobbligato',
                                         'CheckCF_NoImport'], index_col=False, dtype=str)
                data = pd.DataFrame(csv)
                data.dropna(axis=0, how='all')

                flag = True

                for i in range(0, len(data)):
                    tree = etree.Element('UniLav', xmlns='http://servizi.lavoro.gov.it/unilav',
                                         codiceComunicazione='0000000000000000',
                                         dataInvio='{}'.format(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')),
                                         assunzioneForzaMaggiore='NO', versione='CO160201R1')

                    t_1 = etree.SubElement(tree, 'DatoreLavoro', codiceFiscale="02877740213",
                                           denominazione="DS XXXVI ITALY SRL")

                    t_1_1 = etree.SubElement(t_1, 'SedeLegale')
                    t_1_1_1 = etree.SubElement(t_1_1, 'Comune')
                    t_1_1_2 = etree.SubElement(t_1_1, 'cap')
                    t_1_1_3 = etree.SubElement(t_1_1, 'Indirizzo')

                    t_1_2 = etree.SubElement(t_1, 'SedeLavoro')
                    t_1_2_1 = etree.SubElement(t_1_2, 'Comune')
                    t_1_2_2 = etree.SubElement(t_1_2, 'cap')
                    t_1_2_3 = etree.SubElement(t_1_2, 'Indirizzo')
                    t_1_2_4 = etree.SubElement(t_1_2, 'e-mail')

                    t_1_3 = etree.SubElement(t_1, 'Settore')

                    t_1_4 = etree.SubElement(t_1, 'PubblicaAmministrazione')

                    t_2 = etree.SubElement(tree, 'Lavoratore')

                    t_2_1 = etree.SubElement(t_2, 'AnagraficaCompleta')
                    t_2_1_1 = etree.SubElement(t_2_1, 'cognome')
                    if not pd.isnull(data.loc[i, 'Cognome Lavoratore']):
                        t_2_1_1.text = data.loc[i, 'Cognome Lavoratore']
                    t_2_1_2 = etree.SubElement(t_2_1, 'nome')
                    if not pd.isnull(data.loc[i, 'Cognome Lavoratore']):
                        t_2_1_2.text = data.loc[i, 'Nome Lavoratore']
                    t_2_1_3 = etree.SubElement(t_2_1, 'codice-fiscale')
                    t_2_1_4 = etree.SubElement(t_2_1, 'cittadinanza')
                    t_2_1_5 = etree.SubElement(t_2_1, 'sesso')
                    t_2_1_6 = etree.SubElement(t_2_1, 'nascita')
                    t_2_1_6_1 = etree.SubElement(t_2_1_6, 'comune')
                    t_2_1_6_2 = etree.SubElement(t_2_1_6, 'data')

                    t_2_2 = etree.SubElement(t_2, 'IndirizzoLavoratore')
                    t_2_2_1 = etree.SubElement(t_2_2, 'Comune')
                    t_2_2_2 = etree.SubElement(t_2_2, 'cap')
                    t_2_2_3 = etree.SubElement(t_2_2, 'Indirizzo')

                    t_2_3 = etree.SubElement(t_2, 'LivelloIstruzione')

                    t_3 = etree.SubElement(tree, 'InizioRapporto', lavInMobilita='NO', lavoroStagionale='NO',
                                           socioLavoratore='NO', entePrevidenziale='01', lavoroInAgricoltura='NO',
                                           assunzioneObbligatoria='NO', dataInizio="2017-10-16")

                    t_3_1 = etree.SubElement(t_3, 'ccnl')
                    t_3_2 = etree.SubElement(t_3, 'livelloInquadramento')
                    t_3_3 = etree.SubElement(t_3, 'tipoOrario', codice='F')
                    t_3_4 = etree.SubElement(t_3, 'qualificaProfessionale')
                    t_3_5 = etree.SubElement(t_3, 'RetribuzioneCompenso')
                    t_3_6 = etree.SubElement(t_3, 'PatINAIL')
                    t_3_7 = etree.SubElement(t_3, 'Agevolazioni')

                    t_4 = etree.SubElement(tree, 'TipoComunicazione')

                    w = etree.tostring(tree, xml_declaration=flag, encoding='UTF-8', pretty_print=True)
                    with open(destination, 'ab') as f:
                        f.write(w)
                        f.write(b'\n')

                    flag = False

        elif last_slash is None:
            raise Exception('Incorrect path or file extension: {}'.format(archive))

    except IndexError:
        raise Exception("Fill script arguments!!!")


if __name__ == '__main__':
    converter(sys.argv[1:])
