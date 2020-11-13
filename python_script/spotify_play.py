#############################################################
# AVVIA LA RIPRODUZIONE DELLA PLAYLIST SELEZIONATA O RANDOM #
#############################################################

media_player = 'media_player.spotify'
source = data.get('source')
genre = data.get('genre')
playlist = data.get('playlist')
random_option = data.get('random')

playlists = hass.states.get('sensor.spotify_console').attributes['playlists']
sources = hass.states.get('sensor.spotify_console').attributes['sources']

if source is None or random_option is None:
    logger.warning("===== I parametri source e random sono richiesti.")
    service_data = {'title': 'Spotify Console - spotify_play','message':'I parametri source e random sono richiesti per la riproduzione'}
    hass.services.call('persistent_notification', 'create', service_data, False)    
else:
    for a_source in sources:
        objSource = a_source.split("#")
        if (objSource[0] == source):
            source_device = objSource[1]
            break
            
    if random_option == "no":
        if playlist is None:
            logger.warning("===== Il parametro playlist è richiesto.")
            service_data = {'title': 'Spotify Console - spotify_play','message':'Il parametro playlist è richiesto'}
            hass.services.call('persistent_notification', 'create', service_data, False)    
            valid = 'false'
        else:
            for a_playlist in playlists:
                objPlaylist = a_playlist.split("#")
                if (objPlaylist[1] == playlist):
                    uri = objPlaylist[2]
                    break
            valid = 'true'
    elif random_option == "genre":
        if genre is None:
            logger.warning("===== Il parametro genre è richiesto.")
            service_data = {'title': 'Spotify Console - spotify_play','message':'Il parametro genre è richiesto'}
            hass.services.call('persistent_notification', 'create', service_data, False)    
            valid = 'false'
        else:
            array_uri = []
            for a_playlist in playlists:
                objPlaylist = a_playlist.split("#")
                if (objPlaylist[0] == genre):
                    array_uri.append(objPlaylist[2])
            else:
                uri = random.choice(array_uri) 
                valid = 'true'
    elif random_option == "all":
        array_uri = []
        for a_playlist in playlists:
            objPlaylist = a_playlist.split("#")
            array_uri.append(objPlaylist[2])
        else:
            uri = random.choice(array_uri)
            valid = 'true'
    else:
        logger.warning("===== Valore del parametro random non valido. Valori ammessi: no | genre | all")
        service_data = {'title': 'Spotify Console - spotify_play','message':'Valore del parametro random non valido. Valori ammessi: no | genre | all'}
        hass.services.call('persistent_notification', 'create', service_data, False)    
        valid = 'false'

    if valid == 'true':    
        # SELECT SOURCE DEVICE
        service_data = {'entity_id': media_player, 
                        'source': source_device }
        hass.services.call('media_player', 'select_source', service_data, True)

        # PLAY PLAYLIST
        
        service_data = {'media_content_id': uri, 'media_content_type' : 'playlist', 'entity_id' : media_player}
        hass.services.call('media_player', 'play_media', service_data, True)
