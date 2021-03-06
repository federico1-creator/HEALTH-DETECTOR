# Progetto IoT & 3D: HEALTH DETECTOR
## Exam project of Internet of Things and 3D Intelligent Systems
### Sistema di monitoraggio a distanza della salute dei pazienti con riferimento ai principali parametri vitali utilizzati per controllare e predire la pandemia COVID-19.


![](/images/oggetto.jpg)


Il progetto ha come obiettivo quello di creare un prototipo funzionante grazie al quale si possa monitorare a distanza la salute del paziente durante un periodo di tempo prolungato. 
Raccogliendo e analizzando i suoi principali dati medici come: temperatura corporea, saturazione dell’ossigeno nel sangue, battito cardiaco e geolocalizzazione si può predire/controllare la malattia COVID-19.
I dati sono raccolti attraverso sensori collegati ad ARDUINO presenti all’interno di ogni dispositivo consegnato ad ogni paziente.


![](/images/hw%20connections.jpg)

 
I dati rilevati sono destinati al paziente, ma anche al suo medico curante che può analizzarli ed agire (prescrizione cure, coinvolgimento USCA, ricovero in ospedale). I dati sono a disposizione anche della AUSL di riferimento che li utilizza per una gestione della malattia a livello territoriale. 
Questo servizio può essere esteso in modo scalabile, consegnando i dispositivi alla cittadinanza costruendo così la rete di pazienti monitorati. 
Attraverso l’utilizzo di un server, il sistema rende possibile anche l’elaborazione e la visualizzazione dei dati con un’interfaccia web a disposizione sia del paziente sia del medico. 


![](/images/architettura.jpg)


Il medico individua ed assegna lo stato di salute ai vari pazienti. Conoscendo tale stato il sistema crea un database annotato dei vari pazienti e partendo dal database si possono creare statistiche, grafici e reportistiche. 


![](/images/DB%20relazionale%20struttura.jpg)


Una volta acquisiti i vari dati dai pazienti è stata implementata la possibilità di allenare algoritmi di machine learning al fine di prevedere lo stato di salute nei giorni successivi a quelli dell’ultima rilevazione. Questo è l’ambito più innovativo trattato e può portare ad individuare precocemente l’insorgere della malattia sulla base dei dati rilevati e richiamare l’attenzione del medico curante che poi potrà scegliere il miglior trattamento per il suo paziente, alzando così il livello di cure	possibili da somministrare all’assistito.
La presenza di un sistema che raccoglie lo storico dei dati di salute dei pazienti può essere resa disponibile anche ad altri medici presenti nel sistema sanitario che debbano in qualche modo dover curare il paziente. Rendendo di fatto accessibile la storia clinica del paziente.
Il sistema progettato permette anche di evitare possibili contagi dovuti dalle visite in presenza. Il paziente e il medico possono comunicare a distanza attraverso una comunicazione a due vie che permette il dialogo tra le parti in tempo reale. 
 
## Aspetti innovativi del progetto: 
In questo periodo di emergenza sanitaria la medicina sul territorio è di centrale importanza e un dispositivo che renda disponibile in remoto al medico i dati di tutti i suoi pazienti è sicuramente uno strumento utile per sorvegliare lo stato di salute degli assistiti e in caso di contagio per anticipare il più presto la diagnosi e le cure riducendo il rischio di raggiungere livelli gravi della malattia. 
L’utilizzo su larga scala del dispositivo sanitario progettato permette il monitoraggio della salute della popolazione di un territorio e l’attivazione di predizioni che permettono di migliorare le azioni di tracciamento e di indirizzare i comportamenti delle persone per ridurre la diffusione del virus. 
Aumentando i parametri vitali da monitorare, aggiungendo sensori adeguati al dispositivo, si potranno monitorare a distanza anche altre patologie e se la rilevazione verrà fatta con lo stesso dispositivo si potrà giungere a valutare la salute dell’assistito in modo personalizzato e integrato.


## Parte 3D
Si è creato un prototipo del contenitore di tutta la componentistica (cavi, sensori, ECU) e tramite una serie di immagini si è ricostruita una nuvola di punti dell'oggetto e quindi la sua struttura in 3D. Oltre a ciò è stato possibile tramite sw come 3DF Zephyr di creare il modello in un formato itilizzabile da stampanti 3D.
Quindi tramite stampa si possono realizzare i case che poi conterranno il sistema 'HEALTH DETECTOR' implementato.


![](/images/nuvola%20di%20punti.jpg)


---
Progetto realizzato da:
- Cocchi Federico
- Agazzotti Riccardo
