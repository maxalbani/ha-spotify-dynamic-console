# ha-spotify-dynamic-console
Una console di Spotify su Home Assistant con playlist dinamiche.
Media player e playlist sono archiviate in un sensore custom e possono essere aggiunte/modificate senza la necessità di riavviare Home Assistant.

![console_image](console.png)

## Requisiti

  - Avere un abbonamento a Spotify Premium
  - Creare prima una [Spotify Application](https://www.home-assistant.io/integrations/spotify/)
  - Configurare il componente [python_script](https://www.home-assistant.io/components/python_script/)
  - Abilitare la gestione dei [packages](https://www.home-assistant.io/docs/configuration/packages/)
  
## Nota sui Media Player

Questo progetto necessita di dispositivi che siano SEMPRE disponibili su Spotify per la riproduzione.
Gli Amazon Echo ad esempio lo sono. I Google Home (con l'integrazione Google Cast) no purtroppo, hanno bisogno di essere prima attivati dall'app di Spotify.

Per risolvere il problema si può usare il custom component [Spotcast](https://github.com/fondberg/spotcast/), ma in questo progetto non è descritto il suo funzionamento.

## Installazione

  - Copiare gli script python nella propria directory **/config/python_scripts**
  - Copiare il package **spotify.yaml** nella propria directory **/config/packages**
  - Nel proprio file **secret.yaml** configurare le entry **spotify_client_id** e **spotify_client_secret**

## Configurazione

Le playlist Spotify e i propri dispositivi media player sono configurati come attributi in un sensore custom.
Questo consente agli script python di popolare dinamicamente le input select nella UI di lovelace e di aggiornare il proprio archivio di playlist senza la necessità di riavviare Home Assistant ogni volta.
Per applicare le modifiche alla configurazione è sufficiente lanciare lo script python_script.spotify_init indicando nei parametri i nomi delle proprie input select.

![init_image](spotify_init.png)

### Configurazione delle playlist

Aprire il file **spotify_init.py** nella directory **python_script** e modificare l'attributo **playlists** secondo il seguente tracciato:

```
genere#Nome Playlist#Spotify URI
```

Per trovare lo **Spotify URI** della playlist seguire [queste indicazioni](https://support.spotify.com/us/article/sharing-music/).

### Configurazione dei media player

Aprire il file **spotify_init.py** nella directory **python_script** e modificare l'attributo **sources** secondo il seguente tracciato:

```
Stanza#Nome dispositivo visualizzato su Spotify
```

Il nome del dispositivo Spotify deve essere **esattamente quello mostrato nell'app Spotify tra i dispositivi disponibili**, rispettando minuscole e maiuscole

## Utilizzo degli Script Python

Il progetto è composto da 3 script python:

### spotify_init 

Inizializza la console e viene eseguito allo start di Home Assistant (automazione nel package) o dopo aver modificato la configurazione.

Parametri:

  - **entity_source**: entity_id della input select dei dispositivi media player
  - **entity_genre**: entity_id della input select dei generi musicali
  
### spotify_load_playlist

Popola dinamicamente la lista delle playlist in base al genere selezionato dalla UI (automazione nel package)

Parametri:

  - **entity_playlist**: entity_id della input select delle playlist
  
### spotify_play

E' lo script che si occupa di far partire la riproduzione.

Parametri:

  - **source**: Stanza dove riprodurre la playlist (Obbligatorio)
  - **random**: Tipologia di riproduzione (Obbligatorio). Accetta 3 valori:
    - **no**: Avvia la playlist specificata nel parametro **playlist**
    - **genre**: Avvia la riproduzione di una playlist casuale in base al genere specificato nel parametro **genre**
    - **all**: Avvia la riproduzione di una playlist casuale tra tutte quelle configurate
  - **genre**: Obbligatorio nel caso di **random=genre**
  - **playlist**: Obbligatorio nel caso di **random=no**
