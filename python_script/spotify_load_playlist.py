################################################################
# POPOLA LA LISTA DELLE PLAYLIST IN BASE AL GENERE SELEZIONATO #
################################################################

inputEntityId = data.get('entity_playlist')
inputGenere = data.get('genre')
if inputGenere is None or inputEntityId is None:
    logger.warning("===== genere e entity id sono richiesti per il popolamento delle playlist.")
    service_data = {'title': 'Spotify Console - spotify_load_playlist','message':'I parametri entity_playlist e genre sono richiesti'}
    hass.services.call('persistent_notification', 'create', service_data, False)        
else:
    playlists = hass.states.get('sensor.spotify_console').attributes['playlists']
    options = ['Seleziona Playlist']
    for playlist in playlists:
        objPlaylist = playlist.split("#")
        if (objPlaylist[0] == inputGenere):
            options.append(objPlaylist[1])
    else:
        service_data = {'entity_id': inputEntityId, 
                        'options': options }
        hass.services.call('input_select', 'set_options', service_data, False)